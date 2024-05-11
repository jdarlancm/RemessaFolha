import os
import pandas as pd

from pypdf import PdfReader

from helpers import paths_helper
from utils import os_utils, string_utils


class RenameReceipts:
    def __init__(self, month, year):
        self.month = month
        self.year = year
        self.temp_receipts_folder = paths_helper.get_payroll_temp_folder(
            self.month, self.year
        )

    def execute(self):
        receipts_filename = self._get_receipts_list()

        if not receipts_filename:
            raise FileNotFoundError("Nenhum comprovante encontrado.")

        for receipt_filename in receipts_filename:
            employee = self._get_employee_data(receipt_filename)
            new_name = f"{employee["matricula"]}-{employee["nome"]}-pagamento.pdf"
            self._rename_receipt(receipt_filename, new_name)

        # TODO mover arquivos para pasta de comprovante

    def _get_receipts_list(self):
        return os_utils.list_files(self.temp_receipts_folder, ".pdf")

    def _get_employee_data(self, receipt_filename):
        payee_first_name, payee_last_name = self._get_payee_fom_receipt(
            receipt_filename
        )

        employee = {"matricula": "###", "nome": "NAO LOCALIZADO"}

        if payee_first_name and payee_last_name:
            employee = self._found_employee_info(payee_first_name, payee_last_name)

        return employee

    def _get_payee_fom_receipt(self, receipt_filename):
        FIRST_PAGE = 0

        reader = PdfReader(f"{self.temp_receipts_folder}\\{receipt_filename}")
        page_text = reader.pages[FIRST_PAGE].extract_text()
        lines = page_text.split("\n")
        first_name = ""
        last_name = ""

        for line in lines:
            x = line.split(":")
            if x and x[0] == "FAVORECIDO":
                payee_name = x[1].strip().split(" ")
                first_name = payee_name[0].strip().upper()
                last_name = payee_name[-1].strip().upper()
                break

        return first_name, last_name

    def _found_employee_info(self, payee_first_name, payee_last_name):
        employee = {
            "matricula": "###",
            "nome": payee_first_name + " " + payee_last_name,
        }

        payroll_filename = paths_helper.get_payroll_year_complete_filename(self.year)
        spreadsheet_tab = "funcionarios"
        df = pd.read_excel(payroll_filename, sheet_name=spreadsheet_tab, header=1)
        for index, row in df.iterrows():
            if row["status"] == "Inativo":
                continue
            full_name = string_utils.remove_accents_and_special_characters(row["nome"])
            name_parts = full_name.split()
            first_name = name_parts[0].strip().upper()
            last_name = name_parts[-1].strip().upper()
            if (
                first_name == payee_first_name
                and last_name[: len(payee_last_name)] == payee_last_name
            ):
                employee["matricula"] = str(row["codigo"]).zfill(3)
                employee["nome"] = first_name + " " + last_name

        return employee

    def _rename_receipt(self, actual_name, new_name):
        os.rename(
            f"{self.temp_receipts_folder}\\{actual_name}",
            f"{self.temp_receipts_folder}\\{new_name}",
        )
