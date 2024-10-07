from payment_return.rename_receipts import RenameReceipts
from payment_return.notify_employees import NotifyEmployees


def execute(month, year):
    RenameReceipts(month, year).execute()
    #NotifyEmployees(month, year).execute()
