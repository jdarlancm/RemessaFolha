# PEP 8 - Guia de Estilo para Código Python

## 1. Indentação e Formatação

### Indentação
- Use **4 espaços** por nível de indentação (nunca tabs)
- Linha de continuação deve alinhar elementos verticalmente ou usar indentação adicional

```python
# BOM - Alinhamento vertical
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# BOM - Indentação adicional
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)

# RUIM - Sem alinhamento
foo = long_function_name(var_one, var_two,
    var_three, var_four)
```

### Tamanho de Linha
- **Máximo 79 caracteres** por linha para código
- **Máximo 72 caracteres** para docstrings e comentários
- Use parênteses para quebra implícita de linha (preferível a `\`)

```python
# BOM
with open('/path/to/some/file/you/want/to/read') as file_1, \
     open('/path/to/some/file/being/written', 'w') as file_2:
    file_2.write(file_1.read())

# MELHOR
with (open('/path/to/some/file/you/want/to/read') as file_1,
      open('/path/to/some/file/being/written', 'w') as file_2):
    file_2.write(file_1.read())
```

### Linhas em Branco
- **2 linhas em branco** antes de definições de classes e funções top-level
- **1 linha em branco** entre métodos de uma classe
- Use linhas em branco com parcimônia dentro de funções para separar seções lógicas

```python
import os
import sys


def top_level_function():
    pass


class MyClass:
    def method_one(self):
        pass

    def method_two(self):
        pass
```

## 2. Imports

### Organização
- Sempre no topo do arquivo, após docstrings do módulo
- Imports separados em grupos (ordem):
  1. Biblioteca padrão
  2. Bibliotecas third-party
  3. Imports locais
- Linha em branco entre cada grupo

```python
"""Module docstring."""

import os
import sys
from typing import List, Optional

import pandas as pd
import requests

from mypackage.module import MyClass
from mypackage import helpers
```

### Formato
- Cada import em linha separada (exceto `from ... import`)
- Imports absolutos preferíveis a relativos
- Evite wildcard imports (`from module import *`)

```python
# BOM
import os
import sys
from typing import List, Dict

# RUIM
import os, sys

# EVITE
from module import *
```

## 3. Espaçamento

### Espaços em Branco
- **NÃO** adicione espaços:
  - Imediatamente dentro de parênteses, colchetes ou chaves
  - Antes de vírgula, ponto e vírgula ou dois pontos
  - Antes do parêntese que inicia lista de argumentos

```python
# BOM
spam(ham[1], {eggs: 2})
if x == 4: print(x, y); x, y = y, x

# RUIM
spam( ham[ 1 ], { eggs: 2 } )
if x == 4 : print(x , y) ; x , y = y , x
```

- **ADICIONE** espaços:
  - Ao redor de operadores de atribuição (`=`, `+=`, etc.)
  - Ao redor de comparações (`==`, `<`, `>`, `!=`, `<=`, `>=`, `in`, `not in`, `is`, `is not`)
  - Ao redor de operadores booleanos (`and`, `or`, `not`)
  - Ao redor de operadores aritméticos (com prioridade mais baixa)

```python
# BOM
i = i + 1
submitted += 1
x = x*2 - 1
hypot2 = x*x + y*y
c = (a+b) * (a-b)

# RUIM
i=i+1
submitted +=1
x = x * 2 - 1
hypot2 = x * x + y * y
c = (a + b) * (a - b)
```

## 4. Nomenclatura

### Convenções Gerais
- **nunca** use caracteres `l` (L minúsculo), `O` (o maiúsculo), ou `I` (i maiúsculo) sozinhos
- Use nomes descritivos, evite abreviações obscuras

### Padrões por Tipo

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| Módulos/Pacotes | `lowercase`, `lower_with_under` | `mymodule`, `my_package` |
| Classes | `CapWords` (PascalCase) | `MyClass`, `PayrollService` |
| Funções | `lowercase_with_underscores` | `my_function`, `get_employee` |
| Variáveis | `lowercase_with_underscores` | `my_variable`, `total_count` |
| Constantes | `UPPERCASE_WITH_UNDERSCORES` | `MAX_SIZE`, `API_KEY` |
| Métodos | `lowercase_with_underscores` | `class_method`, `instance_method` |

### Nomes Especiais
- `_single_leading_underscore`: uso interno fraco
- `single_trailing_underscore_`: evitar conflito com palavras-chave Python
- `__double_leading_underscore`: name mangling em classes
- `__double_leading_and_trailing__`: objetos "mágicos" (não crie, apenas use)

```python
class MyClass:
    def __init__(self):
        self.public = 1
        self._internal_use = 2
        self.__private = 3

    def public_method(self):
        pass

    def _internal_method(self):
        pass
```

## 5. Comentários e Docstrings

### Comentários de Linha
- Devem ser frases completas
- Primeira palavra maiúscula (exceto identificadores)
- Use `#` seguido de espaço

```python
# BOM - Comentário claro e completo
x = x + 1  # Compensate for border

# EVITE - Comentário óbvio
x = x + 1  # Increment x
```

### Docstrings
- Use `"""triple double quotes"""`
- Para one-liner: `"""Tudo na mesma linha."""`
- Para multi-line: linha de resumo, linha em branco, detalhes

```python
def simple_function():
    """Do something simple."""
    pass


def complex_function(arg1: str, arg2: int) -> bool:
    """Summarize the function in one line.

    More detailed explanation of what the function does,
    including any important details about the arguments
    and return value.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When arg2 is negative
    """
    pass
```

## 6. Type Hints (PEP 484)

### Anotações de Tipo
- Use type hints para parâmetros de função e retornos
- Imports de tipos do módulo `typing`

```python
from typing import List, Dict, Optional, Union, Tuple

def greeting(name: str) -> str:
    return f'Hello {name}'

def process_items(items: List[str]) -> Dict[str, int]:
    return {item: len(item) for item in items}

def find_user(user_id: int) -> Optional[User]:
    # Retorna User ou None
    pass

def get_config() -> Dict[str, Union[str, int, bool]]:
    return {'debug': True, 'timeout': 30}
```

## 7. Boas Práticas

### Comparações
```python
# BOM
if greeting:  # Verifica se string não vazia
if not sequence:  # Verifica se lista vazia
if x is None:  # Compara com None
if x is not None:

# RUIM
if greeting == True:
if len(sequence) == 0:
if x == None:
```

### Estruturas de Controle
```python
# BOM - Pythonic
for item in sequence:
    process(item)

# BOM - Com índice quando necessário
for i, item in enumerate(sequence):
    print(f'{i}: {item}')

# RUIM - Estilo C
for i in range(len(sequence)):
    process(sequence[i])
```

### Context Managers
```python
# BOM - Sempre use context managers para arquivos
with open('file.txt') as f:
    data = f.read()

# RUIM - Pode vazar recursos
f = open('file.txt')
data = f.read()
f.close()
```

### List Comprehensions
```python
# BOM - Simples e legível
squares = [x**2 for x in range(10)]
evens = [x for x in range(10) if x % 2 == 0]

# RUIM - Muito complexo, use loop normal
result = [(x, y) for x in range(10) if x % 2 == 0
          for y in range(10) if y % 3 == 0 if x + y > 5]
```

### Retorno de Valores
```python
# BOM - Consistente
def foo(x):
    if x >= 0:
        return math.sqrt(x)
    else:
        return None

# BOM - Mais pythonic
def foo(x):
    if x < 0:
        return None
    return math.sqrt(x)

# RUIM - Inconsistente
def foo(x):
    if x >= 0:
        return math.sqrt(x)
    # Retorno implícito None
```

## 8. Exceções

### Tratamento
- Seja específico nas exceções capturadas
- Use `try-except-else-finally` apropriadamente
- Sempre use logging para erros

```python
# BOM
try:
    value = collection[key]
except KeyError:
    return default_value
else:
    return handle_value(value)
finally:
    cleanup()

# RUIM - Muito genérico
try:
    value = collection[key]
except:  # Nunca use bare except
    pass

# RUIM - Muito amplo
try:
    value = collection[key]
except Exception:  # Muito genérico
    pass
```

### Levantamento de Exceções
```python
# BOM - Exceção específica com mensagem clara
raise ValueError(f'Invalid value: {value}')

# BOM - Re-raise preservando stack trace
try:
    risky_operation()
except SomeError as e:
    logger.error(f'Operation failed: {e}')
    raise

# RUIM - Exceção genérica
raise Exception('Something went wrong')
```

## 9. Principais Regras Resumidas

1. **Indentação:** 4 espaços, nunca tabs
2. **Linha:** Máximo 79 caracteres
3. **Imports:** Agrupados (stdlib, third-party, local) no topo
4. **Espaços:** Ao redor de operadores, não dentro de parênteses
5. **Nomenclatura:** `snake_case` para funções/variáveis, `PascalCase` para classes
6. **Docstrings:** Sempre para funções/classes públicas
7. **Type Hints:** Use em todas as funções públicas
8. **Comparações:** Use `is` para None, evite `== True`
9. **Context Managers:** Sempre para recursos (arquivos, conexões)
10. **Exceções:** Específicas, nunca bare `except`

## 10. Ferramentas de Verificação

### Linters e Formatadores
- **Black:** Formatador automático (opinionated)
- **Flake8:** Verificador de estilo PEP 8
- **pylint:** Análise estática de código
- **mypy:** Verificador de type hints
- **isort:** Organiza imports automaticamente

```bash
# Instalar ferramentas
pip install black flake8 pylint mypy isort

# Usar
black .
flake8 src/
pylint src/
mypy src/
isort src/
```

---

**Referência Completa:** [PEP 8 – Style Guide for Python Code](https://peps.python.org/pep-0008/)