# Gmail API Diagnostics Script

## Propósito
Testar e diagnosticar problemas de conectividade da Gmail API, autenticação OAuth, e capacidades de envio de email.

## Requisitos
- Python 3.12+
- Dependências do Pipfile instaladas
- `client_secret.json` válido em `src/services/config/`
- Conectividade de rede para googleapis.com

## Uso

### Diagnóstico Básico (Sem Autenticação)
```bash
cd c:\arquivos\dev\projects\cjmc\RemessaFolha
python scripts/test_gmail_service.py --check-only
```

### Teste Completo (Com Autenticação)
```bash
python scripts/test_gmail_service.py
```

### Enviar Email de Teste
```bash
python scripts/test_gmail_service.py --send-test-email seu@email.com
```

## O Que É Testado

### 1. Conectividade de Rede
- Resolução DNS para oauth2.googleapis.com, www.googleapis.com
- Conexão TCP na porta 443
- Mede latência

### 2. Bibliotecas HTTP
- Funcionalidade da biblioteca `requests`
- Funcionalidade da biblioteca `httplib2`

### 3. Configuração OAuth
- Presença e formato de `client_secret.json`
- Presença e validade de `token.json`
- Status de expiração do token
- Disponibilidade do refresh token

### 4. Autenticação
- Inicialização do GmailService
- Capacidade de renovar token
- Mede tempo de autenticação

### 5. Funcionalidade de Email
- Teste de envio de email real (opcional)
- Mede tempo de envio

## Interpretando os Resultados

### ✓ Verde (Sucesso)
Tudo funcionando corretamente.

### ⚠ Amarelo (Aviso)
Pode ainda funcionar mas precisa de atenção:
- Token expirado (pode ser renovado)
- Resposta de rede lenta

### ✗ Vermelho (Falha)
Necessita correção:
- Problemas de conectividade de rede
- Arquivos de configuração ausentes ou inválidos
- Falhas de autenticação
- Refresh token ausente

## Troubleshooting

### WinError 10060 - Connection Timeout
- Verifique os testes de conectividade de rede
- Confirme que não há firewall bloqueando googleapis.com
- Verifique se os valores de timeout precisam de ajuste

### Token Expirado
- O script tentará renovação automática
- Se a renovação falhar, delete `token.json` e re-autentique

### Refresh Token Ausente
- Delete `token.json`
- Execute novamente o fluxo de autenticação
- Certifique-se de aprovar todos os escopos solicitados

### Problemas de Rede Intermitentes
- Execute o script múltiplas vezes para identificar padrões
- Verifique logs detalhados para informações específicas de timing
- Considere ajustar valores de timeout em `src/config/gmail_config.py`

## Arquivos de Log
Logs detalhados são salvos em: `logs/gmail_diagnostics_YYYYMMDD_HHMMSS.log`

Cada execução cria um novo arquivo de log com timestamp para facilitar o rastreamento histórico de problemas.

## Códigos de Saída
- `0`: Todos os testes passaram
- `1`: Um ou mais testes falharam (útil para CI/CD)

## Melhorias Implementadas

Este script faz parte de uma melhoria maior no serviço Gmail API que inclui:

1. **Timeouts Configuráveis**: Todas as requisições HTTP agora têm timeouts definidos
2. **Retry com Exponential Backoff**: Falhas de rede são automaticamente retentadas (3x)
3. **Melhor Tratamento de Erros**: Mensagens de erro mais claras e específicas
4. **Logging Detalhado**: Facilita debug de problemas de produção

## Suporte

Se você encontrar problemas:
1. Execute o script com `--check-only` primeiro para diagnóstico básico
2. Revise os logs detalhados em `logs/`
3. Verifique a configuração de rede e firewall
4. Confirme que `client_secret.json` está correto
