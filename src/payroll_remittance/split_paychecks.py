from pypdf import PdfReader
from pypdf import PdfWriter

from helpers import paths_helper, payroll_sheet_helper


def extract(month, year):
    paychecks_file = paths_helper.get_payckeck_complete_filename(month, year)
    paychecks_dest = paths_helper.get_payroll_receipts_folder_and_create_if_not_exists(
        month, year
    )

    reader = PdfReader(paychecks_file)

    for page_idx in range(len(reader.pages)):
        page = reader.pages[page_idx]
        page_content = page.extract_text()

        if not _is_paycheck_file(page_content):
            continue

        paycheck_filename = _create_paycheck_filename(year, page_content)
        output_file = f"{paychecks_dest}\\{paycheck_filename}"

        _create_pdf_file(page, output_file)


def _is_paycheck_file(page_content):
    text_identifies_paycheck_file = "RECIBO DE PAGAMENTO DE SALÁRIO"
    return text_identifies_paycheck_file in page_content


def _create_paycheck_filename(year, page_content):
    matricula = _extract_matricula_paycheck(page_content)
    employee_name = payroll_sheet_helper.get_first_last_name_employee(year, matricula)

    if not employee_name or matricula == 0:
        raise ValueError(
            f"Não foi possível obter informaçoes do funcionário no contra-cheque ({matricula=}, {employee_name=})"
        )

    return paths_helper.get_employee_payckeck_filename(matricula, employee_name)


# Formato da Linha:
# 0                -3          -2  -1
# NOME COMPLETO DO FUNCIONARIO COD DATA_ADMISSAO
def _extract_matricula_paycheck(page_content):
    ROW_EMPLOYEE_DATA = 2
    COL_MATRICULA = -2
    lines = page_content.split("\n")
    matricula = lines[ROW_EMPLOYEE_DATA].strip().split(" ")[COL_MATRICULA]
    return int(matricula) if matricula else 0


def _create_pdf_file(page, filename):
    writer = PdfWriter()
    writer.add_page(page)

    with open(filename, "wb") as out:
        writer.write(out)

    writer.close()
