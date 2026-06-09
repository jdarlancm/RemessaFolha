#!/usr/bin/env python3
"""
Comprehensive Gmail API Service Test & Diagnostic Script

This script tests Gmail API connectivity, authentication, and email sending
capabilities with detailed diagnostics for troubleshooting.

Usage:
    python scripts/test_gmail_service.py
    python scripts/test_gmail_service.py --send-test-email your@email.com
    python scripts/test_gmail_service.py --check-only
"""

import sys
import os
import json
import socket
import time
from datetime import datetime, timezone
from pathlib import Path
import argparse
import logging

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

# Test configuration
TEST_CONFIG = {
    'google_oauth_hosts': [
        'oauth2.googleapis.com',
        'www.googleapis.com',
        'accounts.google.com'
    ],
    'timeout': 10,
    'token_file': 'src/services/config/token.json',
    'client_secret_file': 'src/services/config/client_secret.json'
}

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    END = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print formatted header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text:^70}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'=' * 70}{Colors.END}\n")


def print_success(text):
    """Print success message."""
    try:
        print(f"{Colors.GREEN}✓ {text}{Colors.END}")
    except UnicodeEncodeError:
        print(f"{Colors.GREEN}[OK] {text}{Colors.END}")


def print_warning(text):
    """Print warning message."""
    try:
        print(f"{Colors.YELLOW}⚠ {text}{Colors.END}")
    except UnicodeEncodeError:
        print(f"{Colors.YELLOW}[WARN] {text}{Colors.END}")


def print_error(text):
    """Print error message."""
    try:
        print(f"{Colors.RED}✗ {text}{Colors.END}")
    except UnicodeEncodeError:
        print(f"{Colors.RED}[FAIL] {text}{Colors.END}")


def print_info(text):
    """Print info message."""
    try:
        print(f"{Colors.BLUE}ℹ {text}{Colors.END}")
    except UnicodeEncodeError:
        print(f"{Colors.BLUE}[INFO] {text}{Colors.END}")


class GmailDiagnostics:
    """Gmail API diagnostic tests."""

    def __init__(self):
        self.results = {}
        self.logger = self._setup_logger()

    def _setup_logger(self):
        """Setup logging for diagnostics."""
        logger = logging.getLogger('gmail_diagnostics')
        logger.setLevel(logging.DEBUG)

        # Create logs directory
        log_dir = Path(__file__).parent.parent / 'logs'
        log_dir.mkdir(exist_ok=True)

        # File handler
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = log_dir / f"gmail_diagnostics_{timestamp}.log"
        fh = logging.FileHandler(log_file, encoding='utf-8')
        fh.setLevel(logging.DEBUG)

        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        logger.addHandler(fh)
        logger.addHandler(ch)

        print_info(f"Detailed logs: {log_file}")
        return logger

    def test_network_connectivity(self):
        """Test basic network connectivity to Google servers."""
        print_header("Network Connectivity Tests")

        for host in TEST_CONFIG['google_oauth_hosts']:
            try:
                self.logger.info(f"Testing connectivity to {host}...")

                # DNS resolution
                start_time = time.time()
                ip_address = socket.gethostbyname(host)
                dns_time = (time.time() - start_time) * 1000

                print_success(f"{host} resolves to {ip_address} ({dns_time:.2f}ms)")

                # TCP connection test (HTTPS port 443)
                start_time = time.time()
                sock = socket.create_connection(
                    (host, 443),
                    timeout=TEST_CONFIG['timeout']
                )
                connect_time = (time.time() - start_time) * 1000
                sock.close()

                print_success(f"  TCP connection successful ({connect_time:.2f}ms)")
                self.results[f'connectivity_{host}'] = True

            except socket.gaierror as e:
                print_error(f"{host} - DNS resolution failed: {e}")
                self.results[f'connectivity_{host}'] = False
            except socket.timeout as e:
                print_error(f"{host} - Connection timeout: {e}")
                self.results[f'connectivity_{host}'] = False
            except Exception as e:
                print_error(f"{host} - Connection failed: {e}")
                self.results[f'connectivity_{host}'] = False

    def test_http_libraries(self):
        """Test HTTP library functionality."""
        print_header("HTTP Library Tests")

        # Test requests library
        try:
            import requests
            response = requests.get(
                'https://www.googleapis.com',
                timeout=TEST_CONFIG['timeout']
            )
            print_success(f"requests library working (status: {response.status_code})")
            self.results['requests_lib'] = True
        except Exception as e:
            print_error(f"requests library failed: {e}")
            self.results['requests_lib'] = False

        # Test httplib2
        try:
            import httplib2
            http = httplib2.Http(timeout=TEST_CONFIG['timeout'])
            resp, content = http.request('https://www.googleapis.com')
            print_success(f"httplib2 working (status: {resp.status})")
            self.results['httplib2'] = True
        except Exception as e:
            print_error(f"httplib2 failed: {e}")
            self.results['httplib2'] = False

    def test_token_status(self):
        """Test OAuth token file and status."""
        print_header("OAuth Token Status")

        token_path = Path(__file__).parent.parent / TEST_CONFIG['token_file']

        if not token_path.exists():
            print_error(f"Token file not found: {token_path}")
            self.results['token_exists'] = False
            return

        print_success(f"Token file found: {token_path}")
        self.results['token_exists'] = True

        try:
            with open(token_path, 'r') as f:
                token_data = json.load(f)

            # Check required fields
            required_fields = ['token', 'refresh_token', 'expiry', 'client_id']
            for field in required_fields:
                if field in token_data:
                    print_success(f"  {field}: present")
                else:
                    print_error(f"  {field}: MISSING")

            # Check expiry
            if 'expiry' in token_data:
                expiry = datetime.fromisoformat(
                    token_data['expiry'].replace('Z', '+00:00')
                )
                now = datetime.now(timezone.utc)

                if expiry > now:
                    remaining = expiry - now
                    print_success(
                        f"  Token valid for {remaining.total_seconds() / 3600:.1f} hours"
                    )
                    self.results['token_valid'] = True
                else:
                    print_warning(
                        f"  Token expired {(now - expiry).total_seconds() / 3600:.1f} "
                        f"hours ago (will be refreshed)"
                    )
                    self.results['token_valid'] = False

            # Check refresh token
            if 'refresh_token' in token_data and token_data['refresh_token']:
                print_success("  Refresh token available")
                self.results['has_refresh_token'] = True
            else:
                print_error("  Refresh token MISSING - re-authentication required")
                self.results['has_refresh_token'] = False

        except Exception as e:
            print_error(f"Error reading token file: {e}")
            self.results['token_readable'] = False

    def test_client_secret(self):
        """Test client secret file."""
        print_header("Client Secret Configuration")

        secret_path = Path(__file__).parent.parent / TEST_CONFIG['client_secret_file']

        if not secret_path.exists():
            print_error(f"Client secret file not found: {secret_path}")
            self.results['client_secret_exists'] = False
            return

        print_success(f"Client secret file found: {secret_path}")
        self.results['client_secret_exists'] = True

        try:
            with open(secret_path, 'r') as f:
                secret_data = json.load(f)

            if 'installed' in secret_data:
                print_success("  Format: installed application")
                installed = secret_data['installed']

                for field in ['client_id', 'client_secret', 'auth_uri', 'token_uri']:
                    if field in installed:
                        print_success(f"    {field}: present")
                    else:
                        print_error(f"    {field}: MISSING")

                self.results['client_secret_valid'] = True
            else:
                print_error("  Invalid format: 'installed' key not found")
                self.results['client_secret_valid'] = False

        except Exception as e:
            print_error(f"Error reading client secret: {e}")
            self.results['client_secret_readable'] = False

    def test_gmail_service_import(self):
        """Test importing Gmail service."""
        print_header("Gmail Service Import Test")

        try:
            from services.gmail_service import GmailService
            print_success("GmailService imported successfully")
            self.results['import_service'] = True
            return GmailService
        except Exception as e:
            print_error(f"Failed to import GmailService: {e}")
            self.logger.exception("Import error details:")
            self.results['import_service'] = False
            return None

    def test_gmail_authentication(self, GmailService):
        """Test Gmail service authentication."""
        print_header("Gmail Authentication Test")

        if not GmailService:
            print_error("Skipping - GmailService not available")
            return None

        try:
            print_info("Initializing Gmail service (this may take 30-45 seconds)...")
            start_time = time.time()

            service = GmailService()

            elapsed = time.time() - start_time
            print_success(f"Authentication successful ({elapsed:.2f}s)")
            self.results['authentication'] = True
            return service

        except Exception as e:
            elapsed = time.time() - start_time
            print_error(f"Authentication failed after {elapsed:.2f}s: {e}")
            self.logger.exception("Authentication error details:")
            self.results['authentication'] = False
            return None

    def test_send_email(self, service, recipient):
        """Test sending an email."""
        print_header("Email Send Test")

        if not service:
            print_error("Skipping - Gmail service not initialized")
            return

        if not recipient:
            print_warning("Skipping - no recipient specified (use --send-test-email)")
            return

        try:
            print_info(f"Sending test email to {recipient}...")
            start_time = time.time()

            subject = f"Gmail API Test - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            body = """
Este é um email de teste do script de diagnóstico da Gmail API.

Se você recebeu este email, o serviço Gmail API está funcionando corretamente.

Detalhes do teste:
- Serviço: Gmail API v1
- Autenticação: OAuth 2.0
- Script: test_gmail_service.py
            """

            service.send_email(
                to=recipient,
                subject=subject,
                body=body
            )

            elapsed = time.time() - start_time
            print_success(f"Email sent successfully ({elapsed:.2f}s)")
            self.results['send_email'] = True

        except Exception as e:
            elapsed = time.time() - start_time
            print_error(f"Email send failed after {elapsed:.2f}s: {e}")
            self.logger.exception("Email send error details:")
            self.results['send_email'] = False

    def print_summary(self):
        """Print test summary."""
        print_header("Test Summary")

        total_tests = len(self.results)
        passed_tests = sum(1 for v in self.results.values() if v is True)

        print(f"\nTotal tests: {total_tests}")
        print(f"Passed: {Colors.GREEN}{passed_tests}{Colors.END}")
        print(f"Failed: {Colors.RED}{total_tests - passed_tests}{Colors.END}")

        if passed_tests == total_tests:
            print(f"\n{Colors.GREEN}{Colors.BOLD}All tests passed!{Colors.END}\n")
        else:
            print(f"\n{Colors.YELLOW}Some tests failed. Check details above.{Colors.END}\n")

        # Detailed results
        print("\nDetailed Results:")
        for test, result in self.results.items():
            status = f"{Colors.GREEN}PASS{Colors.END}" if result else f"{Colors.RED}FAIL{Colors.END}"
            print(f"  {test}: {status}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Gmail API Service Test & Diagnostic Tool'
    )
    parser.add_argument(
        '--send-test-email',
        metavar='EMAIL',
        help='Send a test email to specified address'
    )
    parser.add_argument(
        '--check-only',
        action='store_true',
        help='Only run checks, skip authentication and email tests'
    )

    args = parser.parse_args()

    print_header("Gmail API Service Diagnostics")
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    diagnostics = GmailDiagnostics()

    # Run tests
    diagnostics.test_network_connectivity()
    diagnostics.test_http_libraries()
    diagnostics.test_client_secret()
    diagnostics.test_token_status()

    if not args.check_only:
        GmailService = diagnostics.test_gmail_service_import()
        service = diagnostics.test_gmail_authentication(GmailService)

        if args.send_test_email:
            diagnostics.test_send_email(service, args.send_test_email)

    # Print summary
    diagnostics.print_summary()

    # Exit code based on results
    if all(diagnostics.results.values()):
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
