import os
import re
import pdfplumber
from datetime import date
from pathlib import Path
from helpers.paycheck_helper import extract_matricula, extract_net_salary

def main():
    paychecks_file = r"G:\.shortcut-targets-by-id\0B09afXUG5DVWfkpDZW40b3NHZTlORk5oOURPRjNGdUNfZWpSRnFMSmRjZV9PVnk1TkJrYTg\cjmc\02.00. administrativo\02.03. rh\folha de pagamento\2025\08-ago\Contra-Cheque.pdf"
    with pdfplumber.open(paychecks_file) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_content = page.extract_text()
                #print(page_content)
                matricula = extract_matricula(page_content)
                print(f"Matrícula: {matricula}")

                net_salary = extract_net_salary(page_content)
                print(f"Salário Líquido: {net_salary}")
                   
                raise Exception("Stop")
            
    # Primeiro vamos listar os arquivos para ter certeza do caminho correto
    base_path = Path("G:/")
    
    # Procurar o arquivo de contracheque
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file == "Contra-Cheque.pdf":
                paycheck_file = os.path.join(root, file)
                print(f"Arquivo encontrado: {paycheck_file}")
                
                try:
                    # Extrair dados de todas as páginas
                    paychecks = extract_paycheck_data(paycheck_file)
                    
                    print(f"\nContracheques encontrados: {len(paychecks)}")
                    for paycheck in paychecks:
                        print(f"\nPágina {paycheck['page']}:")
                        print(f"Matrícula: {paycheck['registration']}")
                        print(f"Nome: {paycheck['name']}")
                        print(f"Salário Líquido: {paycheck['net_salary']}")
                    
                except Exception as e:
                    print(f"Erro ao processar arquivo: {e}")
                
                # Sair após encontrar o primeiro arquivo
                return

    print("Arquivo não encontrado!")

if __name__ == "__main__":
    main()