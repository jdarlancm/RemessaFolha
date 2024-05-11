import pandas
import csv

from helpers import paths_helper
from utils import date_utils


def generate(month, year):
    employees = _get_employees_info(year)
    employees = _get_salary(month, year, employees)
    _create_file(month, year, employees)


def _get_employees_info(year):
    employees = []
    payroll_filename = paths_helper.get_payroll_year_complete_filename(year)
    spreadsheet_tab = "funcionarios"

    df = pandas.read_excel(payroll_filename, sheet_name=spreadsheet_tab, header=1)

    for index, row in df.iterrows():
        if row["status"] == "Inativo":
            continue

        employee = {
            "matricula": row["codigo"],
            "nome": row["nome"],
            "cpf": str(row["cpf"]),
            "agencia": str(row["agencia"]),
            "conta": str(row["conta"]),
        }

        employees.append(employee)

    return employees


def _get_salary(month, year, employees):
    payroll_filename = paths_helper.get_payroll_year_complete_filename(year)
    spreadsheet_tab = "folha"
    col_name_reference_month = f"{date_utils.nome_mes(month)}-fol"

    df = pandas.read_excel(payroll_filename, sheet_name=spreadsheet_tab, header=1)

    for employee in employees:
        idx = df.index[df["matricula"] == int(employee["matricula"])].tolist()
        if idx:
            employee["salario"] = df.loc[idx[0], col_name_reference_month]

    return employees


def _create_file(month, year, payroll_data):
    folha_path = paths_helper.get_payroll_month_folder(month, year)
    path_filename = f"{folha_path}\\remessa_folha.csv"
    header = payroll_data[0].keys()

    filtered_payroll_data = [
        funcionario
        for funcionario in payroll_data
        if funcionario["salario"] != 0.0
        and funcionario["agencia"] != "nan"
        and funcionario["conta"] != "nan"
        and funcionario["cpf"] != "nan"
    ]

    temp = [
        funcionario
        for funcionario in payroll_data
        if funcionario["salario"] == 0.0
        or funcionario["agencia"] == "nan"
        or funcionario["conta"] == "nan"
        or funcionario["cpf"] == "nan"
    ]

    with open(path_filename, mode="w", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=header, delimiter=";")
        writer.writeheader()
        writer.writerows(filtered_payroll_data)
