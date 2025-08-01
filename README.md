# Remessa Folha
<small><font color="#999999">[English Version](README-en.md)</font></small>

Bem vindo ao projeto Remessa Folha!

Este projeto visa automatizar tarefas manuais no processo de pagamento da folha de pagamento, que anteriormente demandava aproximadamente 8 horas de trabalho manual. Com a implementação deste projeto, todo o processo pode ser concluído em questão de minutos.

## Visão Geral do Processo

O processo de folha de pagamento consiste em três etapas principais:

1. **Preparação da Remessa**
   - Separação dos contra-cheques individuais
   - Atualização da planilha de controle
   - Geração do arquivo de remessa para o banco

2. **Processamento dos Comprovantes**
   - Renomeação dos comprovantes bancários
   - Organização dos arquivos nas pastas corretas

3. **Notificação dos Funcionários**
   - Envio de e-mails com contra-cheques e comprovantes
   - Confirmação de envio

## Arquitetura do Sistema

O projeto segue uma arquitetura limpa com separação clara de responsabilidades:

```
src/
├── domain/           # Modelos de domínio (Employee, Paycheck, etc.)
├── repositories/     # Camada de acesso a dados
├── services/        # Lógica de negócios
│   ├── config/     # Configurações do sistema
│   └── ...
├── helpers/         # Funções auxiliares específicas
└── utils/          # Utilitários genéricos
```

## Funcionalidades

### 1. Preparação da Remessa

- **Divisão de Contra-Cheques**: 
  - Split automático do PDF com todos os contra-cheques
  - Renomeação seguindo o padrão: `MAT-NOME_SOBRENOME-Contra-Cheque.pdf`
  - Validação de dados dos funcionários

- **Atualização de Planilha**: 
  - Extração automática dos salários líquidos
  - Atualização da planilha de controle anual
  - Validação dos valores

- **Geração de Remessa**: 
  - Criação do arquivo CSV para o banco
  - Formatação conforme especificações bancárias
  - Validações de segurança

### 2. Processamento de Comprovantes

- **Gestão de Arquivos**:
  - Renomeação automática dos comprovantes
  - Organização em pastas por mês/ano
  - Validação de integridade

### 3. Notificação

- **Sistema de E-mail**:
  - Envio automático via API do Gmail
  - Anexos de contra-cheque e comprovante
  - Confirmação de envio
  - Tratamento de erros

## Instalação

1. **Pré-requisitos**:
   ```bash
   # Instalar Python 3.8+ e pipenv
   pip install pipenv
   ```

2. **Configuração do Ambiente**:
   ```bash
   # Clonar o repositório
   git clone [url-do-repositorio]
   cd RemessaFolha
   
   # Instalar dependências
   pipenv install
   
   # Criar arquivo .env (use examples/.env_example como base)
   cp examples/.env_example .env
   ```

3. **Configuração do Google Cloud**:
   - Acesse o [Google Cloud Console](https://console.cloud.google.com/)
   - Crie um projeto e ative a API do Gmail
   - Configure as credenciais OAuth 2.0
   - Salve o `client_secret.json` em `src/services/config/`

## Uso

1. **Desenvolvimento**:
   ```bash
   # Ativar ambiente virtual
   pipenv shell
   
   # Executar aplicação
   python src/main.py
   ```

2. **Produção**:
   ```bash
   # Gerar executável
   pyinstaller --onefile --name remessafolha --version-file version.txt .\src\main.py
   ```

3. **Execução**:
   - O programa solicitará:
     1. Mês de referência (1-12)
     2. Ano de referência
     3. Etapa a processar (1-3)

## Estrutura de Arquivos

```
[ANO]/
├── [MES]-[NOME_MES]/
│   ├── Contra-Cheque.pdf     # PDF original com todos os contra-cheques
│   ├── comprovantes/         # Contra-cheques e comprovantes individuais
│   └── temp/                 # Arquivos temporários
└── folha.xlsx               # Planilha de controle anual
```

## Contribuição

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## Licença

Este projeto é licenciado sob a [Licença MIT](https://opensource.org/licenses/MIT).

## Suporte

Para suporte ou dúvidas, abra uma issue no GitHub ou entre em contato com a equipe de desenvolvimento.