from payroll_remittance import (
    remittance_file,
    split_paychecks,
    update_control_sheet,
)


def execute(month, year, paycheck_file_unified):
    if paycheck_file_unified:
        split_paychecks.extract(month, year)

    update_control_sheet.update(month, year)
    remittance_file.generate(month, year)
