# Remessa Folha
<small><font color="#999999">[Versão em Português](README.md)</font></small>

Welcome to the Remessa Folha project!

This project aims to automate manual tasks in the payroll payment process, which previously required approximately 8 hours of manual work. With the implementation of this project, the entire process can be completed in a matter of minutes.

Below are the steps of this process, highlighting the activities that have been automated (in bold):

1. Receive payroll files
2. Validate payroll data
3. **Separate paycheck files.**: Paychecks come in a single file and are separated into individual files for each employee to be sent later, using the naming convention "MAT-FIRST_NAME LAST_NAME-Paycheck.pdf".
4. **Update spreadsheet** for payroll control and verification for the year
5. **Generate remittance file (.csv)** to import into the bank's payroll system
6. Download payment receipts from the bank and place them in the temporary folder.
7. **Rename receipts** to the standard "MAT-FIRST_NAME LAST_NAME-payment.pdf". Automation was performed for the BB receipt model.
8. **Move files** to individual paycheck folder
9. **Send email** to employees with paycheck and payment receipt

### Challenges

During this process, several tasks were identified as repetitive, tedious, and time-consuming for employees. Below, we list the problems that have been resolved:

1. Single-File Pay Stubs: Pay stubs were received in a single PDF file, requiring them to be separated for individual distribution.
   - Risk of Data Leakage: Separating pay stubs using free online services exposed employee data to potential leaks.
   - Manual Renaming: After separation, each file needed to be opened to determine the corresponding employee and renamed to the standard format, leading to time waste.
   
2. Updating Payroll Control Spreadsheet: The company maintains a current year payroll control file containing employee information, monthly net salaries, as well as vacation and termination details. It was necessary to open the payroll and obtain each employee's net salary and enter it into the spreadsheet, requiring time and prone to errors.
   
3. CSV File Generation: Information was manually copied from the control spreadsheet to another spreadsheet and then saved as a CSV file. It was a time-consuming process with risks of errors in copying the information since each necessary column for the CSV was copied separately and pasted.
   
4. Renaming Bank Files: Another laborious process was renaming bank receipts to the standard format. The bank's file naming convention did not include any employee identifiers, requiring each receipt to be opened to identify the name, search for the employee's ID, close the file, and then rename it.
   
5. Email Sending: Finally, the last and slowest task was sending emails to employees with their pay stubs and receipts. It was necessary to send them one by one, clicking on compose, typing the email, subject, and body, attaching the files, and sending them. This occasionally led to sending the pay stub to the wrong employee.

Automating these processes resulted in reduced errors, data leakage risks, and time wasted on trivial tasks, providing cost savings for the company.

## Features

The automation consists of two stages: the first is the preparation of the payroll for submission to the bank, and the second is the receipt of the payroll payment return.

### Stage 1: Prepare Remittance for the Bank

- **Pay Stub Splitting**: Splits the PDF file containing all pay stubs, separating and renaming them by employee.

- **Salary Updates**: Employee net salaries are updated in an Excel spreadsheet containing month-to-month payroll information.

- **CSV File Generation**: Generates a CSV file with the information required by the bank to be imported into the bank's payroll program.

### Stage 2: Payroll Payment Return

- **Receipt Renaming**: Receipts are downloaded from the bank in separate PDF files (for each payment) and saved in a temporary folder. The files in this folder are read, renamed to the standard format, and then moved alongside the pay stubs.

- **Email Sending**: Finally, the system sends an email to each employee containing their pay stub and payment receipt, using the Google API.

## Usage

1. **Development Environment**:
   - Ensure you have Python and pipenv installed on your system.
   - Clone the GitHub repository.
   - Inside the project directory, run the command `pipenv install` to install dependencies.
   - Configure the environment variables in the `.env` file, check the necessary variables in the [/examples/.env_example](/examples/.env_example) file.

2. **Running the Project**:
   - Activate the virtual environment using the command `pipenv shell`.
   - To run the project: `python ./src/main.py`.

3. **Generating Executable**:
   - To generate a single executable, use the command:
     ```
     pyinstaller --onefile --name remessafolha --version-file version.txt .\src\main.py
     ```
   - The generated executable will be in the `dist` folder.

4. **Configuring Gmail Account on Google Cloud**:
   - Access the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project or select an existing one.
   - Enable the Gmail API for the project.
   - Create OAuth 2.0 credentials and download the `client_secret.json` file.
   - Place the `client_secret.json` file in the `src/payment_return/` folder of your project.

## Contribuição

Contributions are welcome! Feel free to open issues or submit pull requests.

## Licença

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).