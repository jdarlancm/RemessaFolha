# Remessa Folha
<small><font color="#999999">[Versão em Português](README.md)</font></small>

Welcome to the Remessa Folha project!

This project aims to automate manual tasks in the payroll payment process, which previously required approximately 8 hours of manual work. With the implementation of this project, the entire process can be completed in a matter of minutes.

## Process Overview

The payroll process consists of three main stages:

1. **Remittance Preparation**
   - Individual paycheck separation
   - Control spreadsheet update
   - Bank remittance file generation

2. **Receipt Processing**
   - Bank receipt renaming
   - File organization in correct folders

3. **Employee Notification**
   - Email sending with paychecks and receipts
   - Sending confirmation

## System Architecture

The project follows a clean architecture with clear separation of concerns:

```
src/
├── domain/           # Domain models (Employee, Paycheck, etc.)
├── repositories/     # Data access layer
├── services/        # Business logic
│   ├── config/     # System configurations
│   └── ...
├── helpers/         # Specific helper functions
└── utils/          # Generic utilities
```

## Features

### 1. Remittance Preparation

- **Paycheck Splitting**: 
  - Automatic PDF split of all paychecks
  - Renaming following the pattern: `ID-NAME_SURNAME-Paycheck.pdf`
  - Employee data validation

- **Spreadsheet Update**: 
  - Automatic net salary extraction
  - Annual control spreadsheet update
  - Value validation

- **Remittance Generation**: 
  - Bank CSV file creation
  - Formatting according to bank specifications
  - Security validations

### 2. Receipt Processing

- **File Management**:
  - Automatic receipt renaming
  - Organization in month/year folders
  - Integrity validation

### 3. Notification

- **Email System**:
  - Automatic sending via Gmail API
  - Paycheck and receipt attachments
  - Sending confirmation
  - Error handling

## Installation

1. **Prerequisites**:
   ```bash
   # Install Python 3.8+ and pipenv
   pip install pipenv
   ```

2. **Environment Setup**:
   ```bash
   # Clone repository
   git clone [repository-url]
   cd RemessaFolha
   
   # Install dependencies
   pipenv install
   
   # Create .env file (use examples/.env_example as base)
   cp examples/.env_example .env
   ```

3. **Google Cloud Setup**:
   - Access [Google Cloud Console](https://console.cloud.google.com/)
   - Create a project and enable Gmail API
   - Configure OAuth 2.0 credentials
   - Save `client_secret.json` in `src/services/config/`

## Usage

1. **Development**:
   ```bash
   # Activate virtual environment
   pipenv shell
   
   # Run application
   python src/main.py
   ```

2. **Production**:
   ```bash
   # Generate executable
   pyinstaller --onefile --name remessafolha --version-file version.txt .\src\main.py
   ```

3. **Execution**:
   - The program will request:
     1. Reference month (1-12)
     2. Reference year
     3. Stage to process (1-3)

## File Structure

```
[YEAR]/
├── [MONTH]-[MONTH_NAME]/
│   ├── Paycheck.pdf          # Original PDF with all paychecks
│   ├── receipts/             # Individual paychecks and receipts
│   └── temp/                 # Temporary files
└── payroll.xlsx             # Annual control spreadsheet
```

## Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Support

For support or questions, open an issue on GitHub or contact the development team.