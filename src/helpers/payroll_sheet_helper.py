import pandas

from helpers import paths_helper
from utils import string_utils


def get_first_last_name_employee(year, matricula):
    employee_info = get_employee_info(year, matricula)

    if not employee_info:
        return None

    name_parts = (
        string_utils.remove_accents_and_special_characters(employee_info["nome"])
        .upper()
        .split(" ")
    )

    return name_parts[0] + " " + name_parts[-1]


def get_employee_info(year, matricula):
    payroll_filename = paths_helper.get_payroll_year_complete_filename(year)
    df = pandas.read_excel(payroll_filename, sheet_name="funcionarios", header=1)

    employee_row = df.loc[df["codigo"] == matricula]
    if employee_row.empty:
        return {}

    return employee_row.to_dict(orient="records")[0]
