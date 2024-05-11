# Remessa Folha

Este projeto visa facilitar o processo de preparação de remessas bancárias e o tratamento de comprovantes de pagamento para funcionários de uma empresa.

## Funcionalidades

### Etapa 1: Preparar remessa para o banco

- **Divisão de Contra-Cheques**: O projeto pode receber um arquivo PDF contendo todos os contra-cheques e dividir em vários contra-cheques individuais para cada funcionário.

- **Atualização de Salários**: Os salários líquidos dos funcionários são atualizados em uma planilha Excel que contém as informações da folha mês a mês.

- **Geração de Arquivo CSV**: Após a preparação dos contra-cheques, é gerado um arquivo CSV que pode ser importado no programa da folha de pagamento do banco.

### Etapa 2: Tratar comprovantes e notificar funcionários

- **Salvamento de Comprovantes**: Os comprovantes de pagamento do banco são salvos em uma pasta temporária, um arquivo para cada comprovante. Esta operação é realizada manualmente, geralmente no dia seguinte ao processamento da remessa.

- **Renomeação de Arquivos**: Os arquivos de comprovantes de pagamento são lidos e renomeados com a matrícula do funcionário e colocados na mesma pasta onde estão os contra-cheques. Os comprovantes terão o nome "-pagamento" e os contra-cheques "contra cheque".

- **Envio de E-mails**: Por fim, o sistema envia um e-mail para cada funcionário contendo o contra-cheque e o comprovante de pagamento, utilizando a API do Google.

## Uso

1. **Ambiente de Desenvolvimento**:
   - Certifique-se de ter o Python e o pipenv instalados no seu sistema.
   - Clone o repositório do GitHub.
   - Dentro do diretório do projeto, execute o comando `pipenv install` para instalar as dependências.
   - Configure as variáveis de ambiente no arquivo `.env` conforme necessário.

2. **Executar o Projeto**:
   - Execute o ambiente virtual usando o comando `pipenv shell`.
   - Para executar o projeto: `python ./src/main.py`.

3. **Gerar Executável**:
   - Para gerar um executável único, utilize o comando:
     ```
     pyinstaller --onefile --name remessafolha .\src\main.py
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