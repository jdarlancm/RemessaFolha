# Remessa Folha
<small><font color="#999999">[English Version](README-en.md)</font></small>

Bem vindo ao projeto Remessa Folha!

Este projeto visa automatizar tarefas manuais no processo de pagamento da folha de pagamento, que anteriormente demandava aproximadamente 8 horas de trabalho manual. Com a implementação deste projeto, todo o processo pode ser concluído em questão de minutos.

Abaixo estão as etapas deste processo, destacando as atividades que foram automatizadas (em negrito):
1. Receber arquivos da folha de pagamento
2. Validar dados da folha de pagamento
3. **Separar arquivos de contra-cheques. Os contra-cheques vem em um único arquivo e são separados em um arquivo por funcionario para depois serem enviados, usando a nomenclatura "MAT-PRIMEIRO_NOME ULTIMO_NOME-Contra cheque.pdf".**
4. **Preencher planilha excel de controle e conferência da folha de pagamento do ano**
5. **Gerar arquivo de remessa (.csv) para impotar no sistema de folha de pagamento do banco**
6. Baixar comprovantes de pagamento do banco e colocar na pasta temporária. 
7. **Renomear os comprovantes para o padrão "MAT-PRIMEIRO_NOME ULTIMO_NOME-pagamento.pdf". Foi realizada auomtação para o modelo de comprovante do BB.**
8. **Mover arquivos para a pasta dos contra-cheques individuais**
9. **Enviar e-mail para os funcionários com o contra-cheque e o comprovante de pagamento**

### Problemáticas
Neste processo foram solucionadas algumas tarefas que eram repetitivas, tediosas e que consumiam muito tempo do funcionário. Abaixo, listamos os problemas que foram resolvidos:

1. Contra-Cheques em arquivo único: Os contra-cheques eram recebidos em um único arquivo PDF, tornando necessário separá-los para envio individual.
   - Risco de vazamento de dados: A separação dos contra-cheques era feita utilizando serviços online gratuitos, expondo os dados dos funcionários a possíveis vazamentos.
   - Renomeação manual: Após a separação era necessário entrar arquivo a arquvi para verificar a qual funcionário pertencia e renomear para o padrão utilizado (facilitar a organização).
   - Desperdício de tempo

2. Atualizar planilha de controle da folha: A empresa mantém um arquivo de controle da folha do ano corrente. Nela contem as informações dos funcionários, valores pagos (salário líquido) mês a mês, assim como férias e rescições. Era necessário abrir a folha e obter o salário liquído de cada funcionário e digitar na planilha, demandando tempo e propenso a erros.
   
3. Geração do arquivo CSV: As informações eram copiadas manualmente da planilha de controle para outra planilha e depois salvando em csv. Era um processo demorado e corria riscos de erros na copia das informações, já que cada coluna necessária para o csv era copiada separadamente e colada.
   
4. Renomar arquivos bancários: Outro processo trabalhoso era renomear os comprovatens do banco para o formato utilizado. Na nomenclatura do arquivo do banco não vem nenhum identificador do funcionário (óbvio). Era necessário abrir o comprovante, obter o nome, buscar a matrícula do funcionario, fechar o arquivo e depois renomear.
   
5. Por fim, o último e a mais lenta das tarefas era o envio dos e-mail para os funcionários com o contra-cheque e comprovante. Era necessário enviar um a um, clicando em escrever, digitar e-mail, digitar assunto e corpo, anexar os arquivos e enviar. Ocasionando eventualmente, o envio do contra-cheque para o funcionário errado.

A automação desses processos resultou em redução de erros, riscos de vazamento de dados e tempo desperdiçado em tarefas triviais, proporcionando uma redução de custos para a empresa.

## Funcionalidades

A automação consiste em duas etapas, a primeira e a preparação da folha para emitir ao banco. A segunda é o recebimento do retorno do pagamento da folha.

### Etapa 1: Preparar remessa para o banco

- **Divisão de Contra-Cheques**: Realiza o split do arquivo pdf contendo todos os contra-cheques, separando e renomenado por funcionário.

- **Atualização de Salários**: Os salários líquidos dos funcionários são atualizados em uma planilha Excel que contém as informações da folha mês a mês.

- **Geração de Arquivo CSV**: É gerado um arquivo CSV com as informações exigidas pelo banco para ser importado no programa da folha de pagamento do banco.

### Etapa 2: Retorno do pagamento da folha

- **Renomeação dos comprovantes**: Os comprovantes são baixados do banco em arquivos pdf separados (para cada pagamento) e salvos em uma pasta temporária. Os arquivos dessa pasta são lidos e renomeados para o padrão utilizado e em seguida movidos para junto dos contra-cehques.

- **Envio de E-mails**: Por fim, o sistema envia um e-mail para cada funcionário contendo o contra-cheque e o comprovante de pagamento, utilizando a API do Google.

## Uso

1. **Ambiente de Desenvolvimento**:
   - Certifique-se de ter o Python e o pipenv instalados no seu sistema.
   - Clone o repositório do GitHub.
   - Dentro do diretório do projeto, execute o comando `pipenv install` para instalar as dependências.
   - Configure as variáveis de ambiente no arquivo `.env`, verifique as variáveis necessárias no arquivo [/examples/.env_example](/examples/.env_example).

2. **Executar o Projeto**:
   - Execute o ambiente virtual usando o comando `pipenv shell`.
   - Para executar o projeto: `python ./src/main.py`.

3. **Gerar Executável**:
   - Para gerar um executável único, utilize o comando:
     ```
     pyinstaller --onefile --name remessafolha --version-file version.txt .\src\main.py
     ```
   - O executável gerado estará na pasta `dist`.

4. **Configuração da Conta do Gmail no Google Cloud**:
   - Acesse o [Google Cloud Console](https://console.cloud.google.com/).
   - Crie um novo projeto ou selecione um existente.
   - Ative a API do Gmail para o projeto.
   - Crie as credenciais OAuth 2.0 e baixe o arquivo `client_secret.json`.
   - Coloque o arquivo `client_secret.json` na pasta `src/payment_return/` do seu projeto.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir problemas ou enviar solicitações de recebimento.

## Licença

Este projeto é licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT).