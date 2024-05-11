import os
import pandas as pd

from helpers import paths_helper
from utils import string_utils
from payment_return import gmail_service


class NotifyEmployees:
    def __init__(self, month, year):
        self.month = month
        self.year = year

    def execute(self):
        all_employees = self._get_list_employee()
        filtred_employees = self._filter_exist_paycheck_receipt(all_employees)
        self._notify(filtred_employees)

    def _get_list_employee(self):
        employees = []

        payroll_filename = paths_helper.get_payroll_year_complete_filename(self.year)
        spreadsheet_tab = "funcionarios"
        df = pd.read_excel(payroll_filename, sheet_name=spreadsheet_tab, header=1)
        for index, row in df.iterrows():
            if row["status"] == "Inativo":
                continue

            employee = {}
            employee["matricula"] = str(row["codigo"]).zfill(3)
            employee["nome"] = string_utils.remove_accents_and_special_characters(
                row["nome"]
            )
            employee["email"] = row["email"] if not pd.isna(row["email"]) else ""
            employees.append(employee)

        return employees

    def _filter_exist_paycheck_receipt(self, list_all_employee):
        employees_exists_receipts = self._get_employees_from_receipts_folder()
        # filtered_employees = [item for item in list_all_employee if item["matricula"] in employees_exists_receipts ]
        filtered_employees = []
        for employee in list_all_employee:
            matricula = employee["matricula"]
            if matricula not in employees_exists_receipts:
                continue

            employee["contra_cheque"] = employees_exists_receipts[matricula][
                "contra_cheque"
            ]
            employee["recibo"] = employees_exists_receipts[matricula]["recibo"]
            filtered_employees.append(employee)

        return filtered_employees

    def _get_employees_from_receipts_folder(self):
        receipts_path = paths_helper.get_payroll_receipts_folder(self.month, self.year)
        lista_arquivos = os.listdir(receipts_path)
        lista_final = {}

        for arquivo in lista_arquivos:
            if arquivo.endswith(".pdf"):
                nome_arquivo = os.path.splitext(arquivo)[0]  # Remove a extensão .pdf
                partes_nome = nome_arquivo.split("-")

                matricula = partes_nome[0]
                nome = partes_nome[1]
                tipo = partes_nome[-1]

                if matricula not in lista_final:
                    lista_final[matricula] = {
                        "nome": nome,
                        "recibo": arquivo if tipo == "pagamento" else "",
                        "contra_cheque": arquivo if tipo == "Contra Cheque" else "",
                    }
                else:
                    if tipo == "pagamento":
                        lista_final[matricula]["recibo"] = arquivo
                    if tipo == "Contra Cheque":
                        lista_final[matricula]["contra_cheque"] = arquivo

        return lista_final

    def _notify(self, employees):
        for employee in employees:
            email = employee["email"]
            if not email:
                continue
            self._send_mail(employee)

    def _send_mail(self, employee):
        print(employee["email"])
        if not employee["email"] or (
            not employee["contra_cheque"] and not employee["recibo"]
        ):
            return ""  # nao tem email, nem arquivo a ser enviado

        employee["email"] = employee["email"]
        gmail_service.send_mail(self.month, self.year, employee)
