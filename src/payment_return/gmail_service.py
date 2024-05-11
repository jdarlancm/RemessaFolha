import os.path
import base64
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from utils import date_utils
from helpers import paths_helper

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def login():
    token_json = "src/payment_return/token.json"
    creds = None
    if os.path.exists(token_json):
        creds = Credentials.from_authorized_user_file(token_json, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "src/payment_return/client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_json, "w") as token:
            token.write(creds.to_json())

    return creds


def attach_file(attachment_filename):
    filename = os.path.basename(attachment_filename)
    with open(attachment_filename, "rb") as fp:
        attachment_data = MIMEApplication(fp.read(), Name=filename)
    return attachment_data


def send_mail(month, year, employee):
    reference_month = f"{date_utils.nome_mes(month)}/{year}"
    receipts_path = paths_helper.get_payroll_receipts_folder(month, year)
    creds = login()

    try:
        service = build("gmail", "v1", credentials=creds)
        message = MIMEMultipart()

        message["To"] = employee["email"]
        message["From"] = "'Administrativo CJMC' <admin@colegiojosemoreira.com.br>"
        message["Subject"] = f"Contra-Cheque - {reference_month}"
        html_body = f"""
            Olá {employee['nome']}
            <p>Gostaríamos de informar que o pagamento do seu salário referente ao mês de {reference_month} já foi efetuado.</p>
            <p>Em anexo, você encontrará o contra-cheque e o comprovante de pagamento para conferência.<p>
            <p>Se surgir alguma dúvida ou se precisar de mais alguma informação, por favor, não hesite em entrar em contato.</p>
            <br><br>
            Atenciosamente,
            <div style="font-size:small">
              ______________________________<wbr>________________<br>
              <div style="font-size:2;color:#e69138;font-weight:bold;">
                  Colégio José Moreira da Costa
              </div>
              <div style="color:#0b5394;font-size:x-small">
                (84) 3318-2124<br>
                Rua Ozieme Rosado, 1670- Abolição - 59614-280 - Mossoró/RN
              </div>
            </div>
        """
        message.attach(MIMEText(html_body, "html"))

        if employee["contra_cheque"]:
            attachment_filename = f"{receipts_path}\\{employee["contra_cheque"]}"
            message.attach(attach_file(attachment_filename))

        if employee["recibo"]:
            attachment_filename = f"{receipts_path}\\{employee["recibo"]}"
            message.attach(attach_file(attachment_filename))

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )

        print(f'Message id: {send_message["id"]}')
    except HttpError as error:
        print(f"An error occurred: {error}")
