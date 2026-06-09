"""Configurações para o serviço Gmail API."""


class GmailConfig:
    """Constantes de configuração do Gmail API."""

    # Timeouts (em segundos)
    DEFAULT_TIMEOUT = 30        # Chamadas de API gerais
    TOKEN_REFRESH_TIMEOUT = 45  # Renovação do token OAuth
    CONNECT_TIMEOUT = 10        # Timeout de conexão TCP
    READ_TIMEOUT = 30           # Timeout de leitura de resposta

    # Configurações de retry
    MAX_RETRIES = 3             # Número máximo de tentativas
    RETRY_BACKOFF_FACTOR = 2    # Fator exponencial: 1s, 2s, 4s
    RETRY_MIN_WAIT = 1          # Espera mínima entre retries
    RETRY_MAX_WAIT = 10         # Espera máxima entre retries

    # Exceções que devem acionar retry
    RETRIABLE_EXCEPTIONS = (
        ConnectionError,
        TimeoutError,
        OSError,  # WinError 10060 é subclasse de OSError
    )
