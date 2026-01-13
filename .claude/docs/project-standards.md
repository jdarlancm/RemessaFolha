# Normativas do Projeto RemessaFolha

## Visão Geral

RemessaFolha é um sistema de automação de folha de pagamento construído com **arquitetura em camadas** seguindo princípios de **Domain-Driven Design (DDD)**. Este documento define os padrões e práticas obrigatórias para desenvolvimento.

---

## 1. Arquitetura em Camadas

### Estrutura Obrigatória

```
src/
├── domain/          # Modelos de negócio (entidades)
├── repositories/    # Acesso a dados (PDFs, Excel, CSV)
├── services/        # Lógica de negócio e orquestração
├── helpers/         # Funções auxiliares específicas do domínio
├── utils/           # Utilitários genéricos reutilizáveis
├── config/          # Configurações centralizadas
└── ui/              # Interface de usuário (CLI/GUI)
```

### Responsabilidades das Camadas

#### Domain Layer (`src/domain/`)
- **Responsabilidade:** Modelos de dados do negócio
- **Padrão:** Usar `@dataclass` para todas as entidades
- **Imutabilidade:** Preferir objetos imutáveis quando possível
- **Sem lógica:** Apenas estrutura de dados, sem regras de negócio complexas

```python
from dataclasses import dataclass

@dataclass
class Employee:
    """Representa um funcionário no sistema de folha."""
    registration: str  # Formato: "001", "042" (3 dígitos)
    name: str
    email: str
    bank: str
    agency: str
    account: str
```

#### Repository Layer (`src/repositories/`)
- **Responsabilidade:** Acesso e persistência de dados
- **Isolamento:** Abstrair fonte de dados (PDF, Excel, CSV, API)
- **Sem lógica de negócio:** Apenas CRUD e queries
- **Nomenclatura:** `*Repository` (ex: `PayrollRepository`)

```python
class PayrollRepository:
    """Abstrai acesso aos dados de folha de pagamento."""

    def get_employees_from_spreadsheet(self, month: int, year: int) -> list[Employee]:
        """Lê funcionários da planilha Excel."""
        pass

    def save_paycheck_pdf(self, paycheck: Paycheck, output_path: Path) -> None:
        """Salva contra-cheque individual em PDF."""
        pass
```

#### Service Layer (`src/services/`)
- **Responsabilidade:** Lógica de negócio e orquestração
- **Coordenação:** Usa repositories e outros services
- **Transações:** Gerencia operações complexas multi-step
- **Nomenclatura:** `*Service` (ex: `PayrollService`, `NotificationService`)
- **Dependency Injection:** Recebe dependências via construtor

```python
class PayrollService:
    """Orquestra operações de folha de pagamento."""

    def __init__(self, repository: PayrollRepository, spreadsheet_service: SpreadsheetService):
        self._repository = repository
        self._spreadsheet_service = spreadsheet_service

    def process_payroll(self, month: int, year: int) -> tuple[int, int]:
        """Processa folha completa: extração, validação, geração de remessa."""
        pass
```

#### Helper Layer (`src/helpers/`)
- **Responsabilidade:** Funções auxiliares específicas do domínio
- **Escopo:** Lógica especializada que não cabe em services
- **Exemplos:** Extração de dados de PDFs, parsing de valores, formatações específicas
- **Nomenclatura:** `*_helper.py` (ex: `paycheck_helper.py`)

```python
def extract_net_value_from_paycheck(pdf_path: Path) -> float:
    """Extrai valor líquido de um PDF de contra-cheque.

    Args:
        pdf_path: Caminho para o arquivo PDF

    Returns:
        Valor líquido como float

    Raises:
        ValueError: Se valor não puder ser extraído
    """
    pass
```

#### Utils Layer (`src/utils/`)
- **Responsabilidade:** Utilitários genéricos reutilizáveis
- **Escopo:** Funções que podem ser usadas em qualquer projeto
- **Exemplos:** Validação de e-mail, formatação de datas, operações de string
- **Nomenclatura:** `*_utils.py` (ex: `email_utils.py`, `date_utils.py`)

```python
def validate_email(email: str) -> bool:
    """Valida formato básico de e-mail."""
    return "@" in email and "." in email.split("@")[1]
```

---

## 2. Padrões de Nomenclatura

### Regras Obrigatórias

| Elemento | Padrão | Exemplo |
|----------|--------|---------|
| Arquivos | `snake_case` | `payroll_service.py` |
| Classes | `PascalCase` | `PayrollService` |
| Funções | `snake_case` | `process_payroll()` |
| Variáveis | `snake_case` | `total_amount` |
| Constantes | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT` |
| Privados | `_prefixo` | `_internal_method()` |

### Convenções Específicas do Domínio

#### Matrícula de Funcionário
- **Formato:** String com 3 dígitos, zero-padding à esquerda
- **Exemplos:** `"001"`, `"042"`, `"123"`
- **Conversão:** Use `str.zfill(3)`

```python
# BOM
registration = "42".zfill(3)  # "042"

# RUIM
registration = "42"  # Faltando zero-padding
registration = 42    # Tipo errado (int ao invés de str)
```

#### Nomes de Arquivos PDF
- **Contra-cheque:** `{MATRICULA}-{NOME}-Contra-Cheque.pdf`
- **Comprovante:** `{MATRICULA}-{NOME}-pagamento.pdf`
- **Nome:** Nome completo do funcionário, sem normalização

```python
# Exemplo correto
"042-João da Silva-Contra-Cheque.pdf"
"042-João da Silva-pagamento.pdf"
```

#### Estrutura de Diretórios
```
{PATH_FOLHA}/
└── {ANO}/
    └── {MES:02d}-{nome_mes}/
        ├── Contra-Cheque.pdf      # PDF unificado original
        ├── comprovantes/          # PDFs processados
        │   ├── 001-Nome-Contra-Cheque.pdf
        │   └── 001-Nome-pagamento.pdf
        └── temp/                  # Temporários para renomeação
```

---

## 3. Type Hints e Docstrings

### Type Hints Obrigatórios
- **SEMPRE** use type hints em funções públicas
- Use tipos do módulo `typing` quando necessário
- Especifique tipo de retorno, incluindo `None`

```python
from typing import Optional
from pathlib import Path

def find_employee(registration: str) -> Optional[Employee]:
    """Busca funcionário por matrícula."""
    pass

def process_files(files: list[Path]) -> dict[str, int]:
    """Processa múltiplos arquivos."""
    pass
```

### Docstrings Obrigatórias
- **Funções/métodos públicos:** Docstring completa em INGLÊS
- **Classes públicas:** Docstring descrevendo propósito
- **Módulos:** Docstring no topo do arquivo
- **Formato:** Google Style ou NumPy Style

```python
def extract_net_value_from_pdf(pdf_path: Path) -> float:
    """Extract the net payment value from a paycheck PDF.

    Uses pdfplumber to extract text and regex to find the net value
    pattern in Brazilian currency format (R$ X.XXX,XX).

    Args:
        pdf_path: Path to the PDF file to process

    Returns:
        Net payment value as float

    Raises:
        ValueError: If net value pattern is not found in PDF
        FileNotFoundError: If PDF file does not exist
    """
    pass
```

### Comentários em Português
- **Lógica de negócio complexa:** Comentários inline em PORTUGUÊS
- **Explicações de domínio:** PORTUGUÊS
- **Razão para código não-óbvio:** PORTUGUÊS

```python
def validate_bank_data(agency: str, account: str) -> bool:
    """Validate bank agency and account format."""
    # Agência deve ter 4 dígitos, com ou sem dígito verificador
    if not re.match(r'^\d{4}-?\d?$', agency):
        return False

    # Conta deve ter entre 5-12 dígitos, com dígito verificador
    if not re.match(r'^\d{5,12}-\d$', account):
        return False

    return True
```

---

## 4. Tratamento de Erros e Logging

### Logging Obrigatório
- Use logger configurado em `src/config/logging_config.py`
- **INFO:** Operações importantes completadas
- **WARNING:** Situações anormais não críticas
- **ERROR:** Erros que impedem operação específica
- **CRITICAL:** Erros que impedem sistema de funcionar

```python
import logging

logger = logging.getLogger(__name__)

def process_employee_paycheck(employee: Employee) -> bool:
    logger.info(f"Processing paycheck for {employee.registration} - {employee.name}")

    try:
        # processamento
        logger.info(f"Paycheck processed successfully for {employee.registration}")
        return True
    except ValueError as e:
        logger.error(f"Failed to process paycheck for {employee.registration}: {e}")
        return False
```

### Exceções Específicas
- **NUNCA** use `except:` (bare except)
- **EVITE** `except Exception:` (muito genérico)
- Use exceções específicas do tipo de erro
- Sempre faça log antes de re-raise

```python
# BOM - Específico
try:
    value = float(text.replace('.', '').replace(',', '.'))
except ValueError as e:
    logger.error(f"Invalid number format: {text}")
    raise ValueError(f"Cannot convert to float: {text}") from e

# RUIM - Genérico demais
try:
    value = float(text.replace('.', '').replace(',', '.'))
except Exception:
    pass  # Silenciar erros é perigoso
```

---

## 5. Validações e Segurança

### Validação nos Limites do Sistema
- Valide entrada do usuário (CLI, GUI)
- Valide dados externos (arquivos, APIs)
- **NÃO** valide excessivamente código interno

```python
# BOM - Valida entrada externa
def process_month(month: int, year: int) -> None:
    if not (1 <= month <= 12):
        raise ValueError(f"Invalid month: {month}. Must be 1-12")
    if not (2020 <= year <= 2100):
        raise ValueError(f"Invalid year: {year}")
    # processa...

# DESNECESSÁRIO - Código interno confiável
def _internal_helper(value: float) -> float:
    if value is None:  # Chamador sempre passa valor válido
        raise ValueError("Value cannot be None")
    return value * 2
```

### Segurança de Caminhos
- **SEMPRE** use `pathlib.Path`
- Valide existência antes de processar
- Não concatene strings para caminhos

```python
from pathlib import Path

# BOM
base_path = Path(os.getenv("PATH_FOLHA"))
file_path = base_path / str(year) / f"{month:02d}-{month_name}" / "Contra-Cheque.pdf"

if not file_path.exists():
    raise FileNotFoundError(f"File not found: {file_path}")

# RUIM - Concatenação de strings
file_path = os.getenv("PATH_FOLHA") + "/" + year + "/" + month + "/Contra-Cheque.pdf"
```

### Validação de E-mail
- Use função `email_utils.validate_email()` antes de enviar
- Normalize e-mails (lowercase, trim)

```python
from src.utils.email_utils import validate_email, normalize_email

email = normalize_email(employee.email)
if not validate_email(email):
    logger.warning(f"Invalid email for {employee.name}: {email}")
    continue
```

---

## 6. Testes

### Estrutura de Testes
- Usar **pytest** como framework
- Testes em `test/` com estrutura espelhando `src/`
- Nome de arquivo: `test_*.py`
- Nome de função: `test_*`

### Padrões de Teste
```python
import pytest
from src.utils.email_utils import validate_email

class TestEmailValidation:
    """Testes para validação de e-mail."""

    @pytest.mark.parametrize("email,expected", [
        ("user@example.com", True),
        ("invalid.email", False),
        ("no@domain", False),
    ])
    def test_validate_email(self, email: str, expected: bool):
        assert validate_email(email) == expected

    def test_validate_email_with_none(self):
        with pytest.raises(TypeError):
            validate_email(None)
```

### Fixtures para Setup
```python
@pytest.fixture
def sample_employee():
    return Employee(
        registration="001",
        name="João Silva",
        email="joao@example.com",
        bank="001",
        agency="1234",
        account="12345-6"
    )
```

---

## 7. Imports e Organização

### Ordem de Imports
1. **Biblioteca padrão** (stdlib)
2. **Third-party** (bibliotecas externas)
3. **Imports locais** (src.*)
4. Linha em branco entre grupos

```python
# 1. Stdlib
import logging
import os
from pathlib import Path
from typing import Optional

# 2. Third-party
import pandas as pd
from google.oauth2.credentials import Credentials

# 3. Locais
from src.domain.payroll import Employee, Paycheck
from src.repositories.payroll_repository import PayrollRepository
from src.utils.email_utils import validate_email
```

### Imports Absolutos
- Prefira imports absolutos a relativos
- Use `from src.module import Class` ao invés de `from ..module import Class`

---

## 8. Dependency Injection

### Services Devem Receber Dependências
- **NÃO** instancie dependências dentro de services
- Receba via construtor (`__init__`)
- Facilita testes e reutilização

```python
# BOM - Dependency Injection
class NotificationService:
    def __init__(self, gmail_service: GmailService, repository: PayrollRepository):
        self._gmail_service = gmail_service
        self._repository = repository

    def notify_employees(self, month: int, year: int) -> tuple[int, int]:
        employees = self._repository.get_employees(month, year)
        # usa gmail_service...

# RUIM - Instanciação interna
class NotificationService:
    def __init__(self):
        self._gmail_service = GmailService()  # Acoplamento forte
        self._repository = PayrollRepository()

    def notify_employees(self, month: int, year: int) -> tuple[int, int]:
        # ...
```

---

## 9. Evitar Over-engineering

### Princípios
1. **Não crie abstrações prematuras:** 3 linhas similares são OK
2. **Não adicione features não solicitadas:** Foque no requisito atual
3. **Não refatore código não relacionado:** Apenas o necessário
4. **Delete código não usado:** Não comente, delete

```python
# BOM - Simples e direto
def calculate_total(values: list[float]) -> float:
    return sum(values)

# OVER-ENGINEERING - Abstração desnecessária
class CalculationStrategy:
    def calculate(self, values):
        raise NotImplementedError

class SumStrategy(CalculationStrategy):
    def calculate(self, values):
        return sum(values)

class Calculator:
    def __init__(self, strategy: CalculationStrategy):
        self.strategy = strategy

    def calculate_total(self, values):
        return self.strategy.calculate(values)
```

### Código Não Usado
```python
# BOM - Deletar completamente
def active_function():
    pass

# RUIM - Código comentado
# def old_function():
#     pass
```

---

## 10. Checklist de Desenvolvimento

### Antes de Criar/Editar Código

- [ ] Li os arquivos relacionados primeiro
- [ ] Entendi a arquitetura em camadas
- [ ] Identifiquei a camada correta para meu código
- [ ] Verifiquei se já existe função similar

### Durante Desenvolvimento

- [ ] Usei `@dataclass` para modelos de domínio
- [ ] Adicionei type hints em funções públicas
- [ ] Adicionei docstrings em inglês
- [ ] Usei logger para operações importantes
- [ ] Validei entradas externas
- [ ] Usei `pathlib.Path` para caminhos
- [ ] Tratei exceções específicas
- [ ] Segui nomenclatura do projeto (matrícula, arquivos, pastas)

### Antes de Finalizar

- [ ] Rodei testes relacionados (`pytest`)
- [ ] Verifiquei logs gerados
- [ ] Removi código não usado
- [ ] Verifiquei PEP 8 básico (indentação, espaços, linha)
- [ ] Testei manualmente se aplicável

---

## Resumo dos Padrões Principais

1. **Arquitetura em camadas:** Domain → Repository → Service → Helper → Utils
2. **Nomenclatura:** `snake_case` arquivos/funções, `PascalCase` classes
3. **Type hints:** Obrigatórios em funções públicas
4. **Docstrings:** Inglês para APIs públicas, português para lógica de negócio
5. **Logging:** Use logger configurado, níveis apropriados
6. **Exceções:** Específicas, sempre com log
7. **Validação:** Nos limites do sistema, não internamente
8. **Dependency Injection:** Services recebem dependências
9. **Testes:** pytest, parametrize, fixtures
10. **Simplicidade:** Evite over-engineering, delete código não usado