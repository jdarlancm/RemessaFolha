"""Gmail service for sending emails."""
import os.path
import base64
import logging
import time
import socket
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google_auth_httplib2 import AuthorizedHttp
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import httplib2
import requests

from helpers import paths_helper
from config.gmail_config import GmailConfig

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Configuration files
CONFIG_DIR = os.path.join(os.path.dirname(__file__), "config")
TOKEN_FILE = os.path.join(CONFIG_DIR, "token.json")
CLIENT_SECRET_FILE = os.path.join(CONFIG_DIR, "client_secret.json")


def retry_with_backoff(max_retries=GmailConfig.MAX_RETRIES):
  """Decorator para retry com exponential backoff."""
  def decorator(func):
    def wrapper(*args, **kwargs):
      logger = logging.getLogger(__name__)
      last_exception = None

      for attempt in range(max_retries):
        try:
          return func(*args, **kwargs)
        except GmailConfig.RETRIABLE_EXCEPTIONS as e:
          last_exception = e
          if attempt < max_retries - 1:
            wait_time = min(
              GmailConfig.RETRY_BACKOFF_FACTOR ** attempt,
              GmailConfig.RETRY_MAX_WAIT
            )
            logger.warning(
              f"Tentativa {attempt + 1}/{max_retries} falhou: {e}. "
              f"Tentando novamente em {wait_time}s..."
            )
            time.sleep(wait_time)
          else:
            logger.error(
              f"Todas as {max_retries} tentativas falharam. "
              f"Último erro: {e}"
            )

      raise last_exception
    return wrapper
  return decorator


class GmailService:
  """Service for sending emails using Gmail API."""
  
  def __init__(self):
    self.creds = None
    self.logger = logging.getLogger(__name__)
    self._authenticate()
    
  @retry_with_backoff()
  def _authenticate(self):
    """Autentica com Gmail API com timeout e retry."""
    # Carrega credenciais existentes
    if os.path.exists(TOKEN_FILE):
      self.creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # Renova ou cria credenciais
    if not self.creds or not self.creds.valid:
      if self.creds and self.creds.expired and self.creds.refresh_token:
        # Cria session com timeout configurado
        session = requests.Session()
        session.timeout = (
          GmailConfig.CONNECT_TIMEOUT,
          GmailConfig.READ_TIMEOUT
        )

        request = Request(session=session)

        self.logger.info("Renovando token OAuth...")
        try:
          self.creds.refresh(request)
          self.logger.info("Token renovado com sucesso")
        except Exception as e:
          self.logger.error(f"Falha ao renovar token: {e}")
          raise
      else:
        # Novo fluxo de autenticação
        self.logger.info("Iniciando novo fluxo OAuth...")
        flow = InstalledAppFlow.from_client_secrets_file(
          CLIENT_SECRET_FILE,
          SCOPES
        )
        self.creds = flow.run_local_server(
          port=0,
          timeout_seconds=120
        )
        self.logger.info("Autenticação bem-sucedida")

      # Salva credenciais
      os.makedirs(CONFIG_DIR, exist_ok=True)
      with open(TOKEN_FILE, "w") as token:
        token.write(self.creds.to_json())
        
  @retry_with_backoff()
  def send_email(
    self,
    to: str,
    subject: str,
    body: str,
    attachments: list[str] = None
  ) -> None:
    """
    Envia email usando Gmail API com timeout e retry.

    Args:
        to: Endereço de email do destinatário
        subject: Assunto do email
        body: Corpo do email
        attachments: Lista de caminhos de arquivos para anexar

    Raises:
        PermissionError: Acesso negado à API do Gmail
        ValueError: Requisição de email inválida
        RuntimeError: Erro da API do Gmail
        ConnectionError: Problemas de conectividade de rede
    """
    try:
      # Cria service com timeout configurado
      http = httplib2.Http(timeout=GmailConfig.DEFAULT_TIMEOUT)
      authed_http = AuthorizedHttp(self.creds, http=http)
      service = build("gmail", "v1", http=authed_http)

      # Cria mensagem
      message = MIMEMultipart()
      message["To"] = to
      message["Subject"] = subject
      message.attach(MIMEText(body))

      # Adiciona anexos
      if attachments:
        for attachment in attachments:
          with open(attachment, "rb") as f:
            part = MIMEApplication(
              f.read(),
              Name=os.path.basename(attachment)
            )
            part["Content-Disposition"] = (
              f'attachment; filename="{os.path.basename(attachment)}"'
            )
            message.attach(part)

      # Codifica e envia
      raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode("utf-8")
      service.users().messages().send(
        userId="me",
        body={"raw": raw_message}
      ).execute()

      self.logger.info(f"Email enviado com sucesso para {to}")

    except socket.timeout as error:
      self.logger.error(f"Timeout ao enviar email para {to}: {error}")
      raise ConnectionError(f"Timeout de rede: {error}")
    except HttpError as error:
      self.logger.error(f"Erro da API Gmail ao enviar email para {to}: {error}")
      if error.resp.status == 403:
        raise PermissionError(
          f"Acesso negado à API do Gmail. Verifique permissões e autenticação."
        )
      elif error.resp.status == 400:
        raise ValueError(f"Requisição de email inválida: {error}")
      else:
        raise RuntimeError(f"Erro da API Gmail: {error}")
    except Exception as error:
      self.logger.error(f"Erro inesperado ao enviar email para {to}: {error}")
      raise 