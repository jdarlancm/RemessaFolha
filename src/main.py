from datetime import date
from dotenv import load_dotenv

from repositories.payroll_repository import PayrollRepository
from services.notification_service import NotificationService
from services.spreadsheet_service import SpreadsheetService
from services.payroll_service import PayrollService

VERSION = "1.0.0"
"""
.env colocado no lugar do exe
extDataDir = os.getcwd()
if getattr(sys, 'frozen', False):
    extDataDir = sys._MEIPASS
load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))
"""

load_dotenv()


def prompt_mes() -> int:
    """Prompt for month input."""
    while True:
        mes = input("Digite o mês da folha (1-12): ")
        if not mes.isdigit() or int(mes) < 1 or int(mes) > 12:
            print("Mês inválido. Por favor, digite um número entre 1 e 12.")
            exit()
        return int(mes)


def prompt_ano() -> int:
    """Prompt for year input."""
    ano = input("Digite o ano da folha: ")
    if not ano.isdigit():
        print("O ano deve ser numérico.")
        exit()
    return int(ano)


def prompt_selecao_etapa() -> int:
    """Prompt for process step selection."""
    opcao = input(
        "Etapa 1) Preparar Arquivo de Remessa\n"
        "Etapa 2) Processar Comprovantes\n"
        "Etapa 3) Notificar Funcionários\n"
        "Qual etapa deseja processar: "
    )
    if not opcao.isdigit() or int(opcao) not in [1, 2, 3]:
        print("Etapa inexistente")
        exit()
    return int(opcao)


def prompt_contra_cheques_unificados() -> bool:
    """Prompt for unified paycheck option."""
    opcao = input("Os contra-cheques estão em um único arquivo? (s/n): ")
    return opcao.lower() == "s"


def main():
    # Get user input
    mes = prompt_mes()
    ano = prompt_ano()
    etapa = prompt_selecao_etapa()
    
    # Create service instances
    repository = PayrollRepository()
    notification_service = NotificationService()
    spreadsheet_service = SpreadsheetService()
    payroll_service = PayrollService(
        repository,
        notification_service,
        spreadsheet_service
    )
    
    # Process based on selected step
    reference_date = date(ano, mes, 1)
    
    try:
        if etapa == 1:
            unified_paycheck = prompt_contra_cheques_unificados()
            payroll_service.create_remittance(reference_date, unified_paycheck)
            print("Arquivo de remessa criado com sucesso!")
            
        elif etapa == 2:
            payroll_service.process_payment_receipts(reference_date)
            print("Comprovantes processados com sucesso!")
            
        elif etapa == 3:
            notified = payroll_service.notify_employees(reference_date)
            print(f"Notificação concluída! {len(notified)} funcionários notificados.")
            
        else:
            print("Etapa inexistente.")
            
    except Exception as e:
        print(f"Erro durante o processamento: {str(e)}")
        exit(1)


if __name__ == "__main__":
    main()
