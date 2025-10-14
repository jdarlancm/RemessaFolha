import pdfplumber
import os
import pandas
import csv
import shutil

from datetime import date
from typing import List, Optional
from pypdf import PdfReader, PdfWriter

from domain.payroll import Employee, Paycheck, PayrollRemittance
from helpers.paths_helper import (
  get_payroll_year_complete_filename,
  get_payckeck_complete_filename,
  get_payroll_receipts_folder_and_create_if_not_exists,
  get_payroll_temp_folder,
  get_employee_payckeck_filename,
  get_payroll_month_folder
)
from helpers.paycheck_helper import extract_matricula, extract_net_salary
from helpers.payroll_sheet_helper import get_first_last_name_employee
from services.spreadsheet_service import SpreadsheetService
from utils.date_utils import nome_mes
from utils import os_utils, string_utils

class PayrollRepository:
    """Repository for payroll data access."""

    def __init__(self):
        self.spreadsheet_service = SpreadsheetService()

    def get_employees(self, reference_date: date) -> List[Employee]:
        """Get employees from the control sheet for the given date."""
        employees = []
        payroll_filename = get_payroll_year_complete_filename(reference_date.year)
        spreadsheet_tab = "funcionarios"

        print(f"Lendo planilha: {payroll_filename}")
        df = pandas.read_excel(payroll_filename, sheet_name=spreadsheet_tab, header=1)

        for _, row in df.iterrows():
            if row["status"] == "Inativo":
                continue

            # Tratar dados bancários
            conta = str(row["conta"]).strip()
            agencia = str(row["agencia"]).strip()
            
            # Se dados bancários forem inválidos, usar None
            if conta == "nan":
                conta = None
            if agencia == "nan":
                agencia = None

            print(f"Dados bancários - {row['nome']}: conta={conta}, agencia={agencia}")
            # Get email from the row
            email = str(row.get("email", "")).strip()
            if email == "nan" or not email:
                email = None

            employee = Employee(
                name=row["nome"],
                email=email,
                registration=str(row["codigo"]).zfill(3),  # Ensure 3 digits
                cpf=str(row["cpf"]),
                bank_account=conta,
                bank_branch=agencia
            )

            employees.append(employee)

        return employees

    def get_paychecks(
        self,
        reference_date: date,
        unified_paycheck: bool
    ) -> List[Paycheck]:
        """Get paychecks from files for the given date."""
        if not unified_paycheck:
            return self._get_paychecks_from_separate_files(reference_date)
        
        return self._get_paychecks_from_unified_file(reference_date)

    def _get_paychecks_from_separate_files(self, reference_date: date) -> List[Paycheck]:
        """Get paychecks from individual files."""
        paychecks = []
        paychecks_dest = get_payroll_receipts_folder_and_create_if_not_exists(
            reference_date.month,
            reference_date.year
        )
        
        # Listar arquivos de contracheque
        paycheck_files = os_utils.list_files(paychecks_dest, ".pdf")
        if not paycheck_files:
            raise FileNotFoundError(
                f"Nenhum contra-cheque encontrado em {paychecks_dest}"
            )
            
        # Processar cada arquivo
        for paycheck_file in paycheck_files:
            if not paycheck_file.endswith("Contra-Cheque.pdf"):
                continue
                
            file_path = f"{paychecks_dest}\\{paycheck_file}"
            
            # Ler conteúdo do arquivo
            reader = PdfReader(file_path)
            page_content = reader.pages[0].extract_text()
            
            if not self._is_paycheck_page(page_content):
                continue
                
            # Extrair dados do funcionário
            registration = self._extract_registration_from_paycheck(page_content)
            employee_name = get_first_last_name_employee(
                reference_date.year,
                registration
            )
            print(f"AQUI: {employee_name}")
            if not employee_name or registration == 0:
                raise ValueError(
                    f"Não foi possível obter informações do funcionário no contra-cheque "
                    f"({registration=}, {employee_name=})"
                )
                
            # Extrair valor
            amount_str = self._extract_net_salary(page_content)
            if not amount_str:
                raise ValueError(
                    f"Não foi possível extrair o valor líquido do contra-cheque "
                    f"do funcionário {employee_name} (matrícula {registration})"
                )
            amount = float(amount_str.replace(",", "."))
            
            # Criar objetos
            employee = Employee(
                name=employee_name,
                email=None,
                registration=str(registration)
            )
            
            paycheck = Paycheck(
                employee=employee,
                amount=amount,
                reference_date=reference_date,
                file_path=file_path
            )
            
            paychecks.append(paycheck)
            
        return paychecks

    def _get_paychecks_from_unified_file(self, reference_date: date) -> List[Paycheck]:
        """Extract paychecks from unified PDF file."""
        paychecks = []
        paychecks_file = get_payckeck_complete_filename(
            reference_date.month,
            reference_date.year
        )
        paychecks_dest = get_payroll_receipts_folder_and_create_if_not_exists(
            reference_date.month,
            reference_date.year
        )

        # Carregar lista de funcionários com dados bancários
        employees_dict = {}
        for employee in self.get_employees(reference_date):
            employees_dict[employee.registration] = employee

        with pdfplumber.open(paychecks_file) as pdf:
            reader = PdfReader(paychecks_file)

            for page_num, page in enumerate(pdf.pages):
                page_content = page.extract_text()
                print(f"Processando página {page_num}...")

                if not self._is_paycheck_page(page_content):
                    continue

                registration = self._extract_registration_from_paycheck(page_content)

                employee_name = get_first_last_name_employee(
                    reference_date.year,
                    registration
                )

                if not employee_name or registration == 0:
                    raise ValueError(
                        f"Não foi possível obter informações do funcionário no contra-cheque "
                        f"({registration=}, {employee_name=})"
                    )

                filename = get_employee_payckeck_filename(registration, employee_name)
                output_file = f"{paychecks_dest}\\{filename}"

                print(f"Nome: {employee_name}")
                self._save_paycheck_page(reader.pages[page_num], output_file)

                amount_str = self._extract_net_salary(page_content)
                if not amount_str:
                    raise ValueError(
                        f"Não foi possível extrair o valor líquido do contra-cheque "
                        f"do funcionário {employee_name} (matrícula {registration})"
                    )

                amount = float(amount_str.replace(",", "."))

                # Tentar encontrar funcionário na planilha
                registration_str = str(registration).zfill(3)
                employee = employees_dict.get(registration_str)
                if not employee:
                    print(f"Aviso: Funcionário {employee_name} (matrícula {registration_str}) não encontrado na planilha")
                    print("       Dados bancários não serão incluídos na remessa")

                paycheck = Paycheck(
                    employee=employee,
                    amount=amount,
                    reference_date=reference_date,
                    file_path=output_file
                )

                paychecks.append(paycheck)
            
        return paychecks

    def _is_paycheck_page(self, page_content: str) -> bool:
        """Check if page is a paycheck."""
        return "RECIBO DE PAGAMENTO DE SALÁRIO" in page_content

    def _extract_registration_from_paycheck(self, page_content: str) -> int:
        """Extract employee registration from paycheck content."""
        return extract_matricula(page_content)

    def _save_paycheck_page(self, page, filename: str) -> None:
        """Save a single paycheck page to PDF file."""
        writer = PdfWriter()
        writer.add_page(page)
        
        with open(filename, "wb") as out:
            writer.write(out)

        writer.close()

    def _extract_net_salary(self, page_content: str) -> Optional[str]:
        """Extract net salary from paycheck content."""
        return extract_net_salary(page_content)
    
    def save_remittance(self, remittance: PayrollRemittance) -> PayrollRemittance:
        """Save the remittance batch and update control sheet."""
        # Criar arquivo de remessa no diretório do mês
        month_folder = get_payroll_month_folder(
            remittance.reference_date.month,
            remittance.reference_date.year
        )
        path_filename = os.path.join(month_folder, "remessa_folha.csv")
        print(f"Tentando salvar arquivo em: {path_filename}")
        
        # Converter para formato do arquivo
        remittance_data = []
        for paycheck in remittance.paychecks:
            print(f"Verificando dados para remessa - {paycheck.employee.name}:")
            print(f"  Valor: {paycheck.amount}")
            print(f"  Conta: {paycheck.employee.bank_account}")
            print(f"  Agência: {paycheck.employee.bank_branch}")
            
            # Verificar cada condição separadamente
            if paycheck.amount <= 0:
                print(f"  -> NÃO incluído na remessa: valor zerado ou negativo")
            elif not paycheck.employee.bank_account:
                print(f"  -> NÃO incluído na remessa: conta bancária não informada")
            elif not paycheck.employee.bank_branch:
                print(f"  -> NÃO incluído na remessa: agência bancária não informada")
            else:
                print(f"  -> Incluído na remessa")
                remittance_data.append({
                    "matricula": paycheck.employee.registration,
                    "nome": paycheck.employee.name,
                    "cpf": paycheck.employee.cpf or "",
                    "agencia": paycheck.employee.bank_branch,
                    "conta": paycheck.employee.bank_account,
                    "salario": paycheck.amount
                })

        # Salvar arquivo CSV
        print(f"Dados para remessa: {len(remittance_data)} funcionários")
        if remittance_data:
            header = remittance_data[0].keys()
            with open(path_filename, mode="w", newline="") as csv_file:
                writer = csv.DictWriter(csv_file, fieldnames=header, delimiter=";")
                writer.writeheader()
                writer.writerows(remittance_data)
                print(f"Arquivo CSV criado em: {path_filename}")
        else:
            print("Nenhum dado para gerar arquivo de remessa!")

        # Atualizar planilha de controle
        self.spreadsheet_service.update_control_sheet(remittance)
        
        return remittance

    def get_remittance(
        self,
        reference_date: date
    ) -> Optional[PayrollRemittance]:
        """Get an existing remittance batch for the given date."""
        month_folder = get_payroll_month_folder(
            reference_date.month,
            reference_date.year
        )
        remittance_file = os.path.join(month_folder, "remessa_folha.csv")
        
        if not os.path.exists(remittance_file):
            return None
        
        # Ler arquivo de remessa
        remittance_data = []
        with open(remittance_file, mode="r") as csv_file:
            reader = csv.DictReader(csv_file, delimiter=";")
            remittance_data = list(reader)
        
        if not remittance_data:
            return None
        
        # Primeiro vamos carregar todos os funcionários da planilha para ter os emails
        all_employees = {
            emp.registration: emp 
            for emp in self.get_employees(reference_date)
        }
        
        employees = []
        paychecks = []
        total = 0.0
        
        # Obter lista de contracheques
        receipts_path = get_payroll_receipts_folder_and_create_if_not_exists(
            reference_date.month,
            reference_date.year
        )
        paycheck_files = os_utils.list_files(receipts_path, ".pdf")
        
        for row in remittance_data:
            registration = str(row["matricula"]).zfill(3)
            
            if registration in all_employees:
                employee = all_employees[registration]
            else:
                print(f"Aviso: Funcionário {row['nome']} (matrícula {registration}) não encontrado na planilha")
                employee = Employee(
                    name=row["nome"],
                    email=row["email"],
                    registration=registration,
                    bank_account=row["conta"],
                    bank_branch=row["agencia"]
                )
            
            employees.append(employee)
            amount = float(row["salario"])
            total += amount
            
            # Buscar arquivo do contracheque
            file_path = ""
            expected_pattern = f"{employee.registration}-{employee.name}"
            
            for paycheck_file in paycheck_files:
                if (paycheck_file.startswith(expected_pattern) and
                    paycheck_file.endswith("Contra-Cheque.pdf")):
                    file_path = f"{receipts_path}\\{paycheck_file}"
                    break
            
            if not file_path:
                # Busca alternativa - procurar por matrícula apenas
                for paycheck_file in paycheck_files:
                    if (paycheck_file.startswith(f"{employee.registration}-") and
                        paycheck_file.endswith("Contra-Cheque.pdf")):
                        file_path = f"{receipts_path}\\{paycheck_file}"
                        break
            
            paycheck = Paycheck(
                employee=employee,
                amount=amount,
                reference_date=reference_date,
                file_path=file_path
            )
            paychecks.append(paycheck)
        
        return PayrollRemittance(
            reference_date=reference_date,
            employees=employees,
            paychecks=paychecks,
            total_amount=total
        )

    def process_payment_receipts(self, remittance: PayrollRemittance) -> None:
        """Process payment receipts for the given remittance."""
        # Obter caminhos das pastas
        temp_folder = get_payroll_temp_folder(
            remittance.reference_month,
            remittance.reference_year
        )
        receipts_folder = get_payroll_receipts_folder_and_create_if_not_exists(
            remittance.reference_month,
            remittance.reference_year
        )
        
        # Listar comprovantes na pasta temp
        receipt_files = os_utils.list_files(temp_folder, ".pdf")
        if not receipt_files:
            raise FileNotFoundError(f"Nenhum comprovante encontrado em {temp_folder}")
            
        print(f"Processando {len(receipt_files)} comprovantes...")
        
        # Processar cada comprovante
        for receipt_file in receipt_files:
            print(f"Processando arquivo: {receipt_file}")
            
            # Extrair dados do favorecido
            payee_data = self._extract_payee_from_receipt(temp_folder, receipt_file)
            if not payee_data:
                print(f"  -> Não foi possível extrair dados do favorecido")
                continue
                
            print(f"  -> Favorecido: {payee_data['first_name']} {payee_data['last_name']}")
                
            # Buscar funcionário correspondente
            employee = self._find_employee_by_name(
                remittance.reference_year,
                payee_data["first_name"],
                payee_data["last_name"]
            )
            
            print(f"  -> Funcionário encontrado: {employee.name} (matrícula {employee.registration})")
            
            # Criar novo nome do arquivo
            new_name = f"{employee.registration}-{employee.name}-pagamento.pdf"
            
            # Verificar se arquivo já existe no destino
            source_path = os.path.join(temp_folder, receipt_file)
            dest_path = os.path.join(receipts_folder, new_name)
            
            if os.path.exists(dest_path):
                print(f"  -> ERRO: Arquivo já existe no destino: {dest_path}")
                continue
                
            # Mover arquivo da pasta temp para a pasta de comprovantes
            shutil.move(source_path, dest_path)
            print(f"  -> Arquivo movido para: {receipts_folder}\\{new_name}")
            
        print("Processamento de comprovantes concluído.")
            
    def _extract_payee_from_receipt(
        self,
        folder: str,
        filename: str
    ) -> Optional[dict]:
        """Extract payee information from receipt PDF."""
        FIRST_PAGE = 0
        
        reader = PdfReader(f"{folder}\\{filename}")
        page_text = reader.pages[FIRST_PAGE].extract_text()
        lines = page_text.split("\n")
        
        for line in lines:
            parts = line.split(":")
            if parts and parts[0] == "FAVORECIDO":
                payee_name = parts[1].strip().split(" ")
                return {
                    "first_name": payee_name[0].strip().upper(),
                    "last_name": payee_name[-1].strip().upper()
                }
                
        return None
        
    def _find_employee_by_name(
        self,
        year: int,
        first_name: str,
        last_name: str
    ) -> Employee:
        """Find employee by first and last name."""
        payroll_filename = get_payroll_year_complete_filename(year)
        spreadsheet_tab = "funcionarios"
        
        df = pandas.read_excel(payroll_filename, sheet_name=spreadsheet_tab, header=1)
        
        for _, row in df.iterrows():
            if row["status"] == "Inativo":
                continue
                
            full_name = string_utils.normalize_text(row["nome"])
            name_parts = full_name.split()
            emp_first = name_parts[0].strip().upper()
            emp_last = name_parts[-1].strip().upper()
            
            if (emp_first == first_name and 
                emp_last[:len(last_name)] == last_name):
                return Employee(
                    name=f"{emp_first} {emp_last}",
                    email=None,
                    registration=str(row["codigo"]).zfill(3),
                    cpf=str(row["cpf"]),
                    bank_account=str(row["conta"]),
                    bank_branch=str(row["agencia"])
                )
                
        # Se não encontrar, retorna um funcionário não localizado
        return Employee(
            name=f"{first_name} {last_name}",
            email=None,
            registration="###",
            cpf=None,
            bank_account=None,
            bank_branch=None
        )
        
    def _rename_receipt(self, folder: str, old_name: str, new_name: str) -> bool:
        """
        Rename a receipt file.
        
        Returns:
            bool: True if rename was successful, False if destination file already exists
        """
        source_path = os.path.join(folder, old_name)
        dest_path = os.path.join(folder, new_name)
        
        if os.path.exists(dest_path):
            print(f"  -> ERRO: Arquivo já existe no destino: {dest_path}")
            return False
            
        shutil.move(source_path, dest_path)
        return True 