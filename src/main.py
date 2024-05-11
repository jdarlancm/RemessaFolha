from dotenv import load_dotenv

from helpers import paths_helper
from payment_return import payment_return
from payroll_remittance import payroll_remittance

"""
.env colocado no lugar do exe
extDataDir = os.getcwd()
if getattr(sys, 'frozen', False):
    extDataDir = sys._MEIPASS
load_dotenv(dotenv_path=os.path.join(extDataDir, '.env'))
"""

load_dotenv()


def prompt_mes():
    while True:
        mes = input("Digite o mês da folha (1-12): ")
        if not mes.isdigit() or int(mes) < 1 or int(mes) > 12:
            print("Mês inválido. Por favor, digite um número entre 1 e 12.")
            exit()
        else:
            return int(mes)


def prompt_ano():
    ano = input("Digite o ano da folha: ")
    if not ano.isdigit():
        print("O ano deve ser numérico.")
        exit()
    return int(ano)


def prompt_selecao_etapa():
    opcao = input(
        "Etapa 1) Preparar Arquivo de Remessa\nEtapa 2) Tratar comprovantes e notificar funcionários.\nQual etapa deseja processar: "
    )
    if not opcao.isdigit() or int(opcao) not in [1, 2]:
        print("Etapa indexistente")
        exit()
    return int(opcao)


def prompt_contra_cheques_unificados():
    opcao = input("Os contra-cheques estão em um único arquivo? (s/n): ")
    return opcao.lower() == "s"


def main():
    mes = prompt_mes()
    ano = prompt_ano()
    etapa = prompt_selecao_etapa()

    paths_helper.check_payroll_paths(mes, ano)

    if etapa == 1:
        arquivo_contracheque_unificado = prompt_contra_cheques_unificados()
        payroll_remittance.execute(mes, ano, arquivo_contracheque_unificado)

    elif etapa == 2:
        payment_return.execute(mes, ano)

    else:
        print("Etapa indexistente.")


if __name__ == "__main__":
    main()
