# Formato da Linha:
# 0                -3          -2  -1
# NOME COMPLETO DO FUNCIONARIO COD DATA_ADMISSAO
def extract_matricula(page_content):
    ROW_EMPLOYEE_DATA = 2
    COL_MATRICULA = -2
    lines = page_content.split("\n")
    matricula = lines[ROW_EMPLOYEE_DATA].strip().split(" ")[COL_MATRICULA]
    return int(matricula) if matricula else 0


def extract_net_salary(page_content):
    lines = page_content.split("\n")
    salario_liquido = None

    for line in lines:
        if line.__contains__("LÍQUIDO"):
            # Dependendo das rubricas a posicao ao quebrar com \n pode variar
            if line.startswith("VALOR LÍQUIDO"):
                salario_liquido = line.split(" ")[2].replace(".", "")
            elif line.startswith(" ____ /"):
                temp = line.split("LÍQUIDO")[1]
                salario_liquido = temp.strip().split(" ")[0].replace(".", "")

            break

    return salario_liquido
