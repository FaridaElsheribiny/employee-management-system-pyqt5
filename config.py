"""
Application configuration.
============================
Every SQL Server setting lives here -- nowhere else in the codebase
hardcodes a server name, database name, or driver string.

Unchanged from the original single-file version except for its new
location in the package.
"""


class Config:
    """Centralized application configuration."""

    # Edit these to match the SQL Server instance you log into via SSMS.
    SERVER: str = r"localhost\SQLEXPRESS01"
    DATABASE: str = "EmployeeManagementDB"
    DRIVER: str = "{ODBC Driver 18 for SQL Server}"

    # True  -> Windows Authentication (same login you use in SSMS).
    # False -> SQL Server Authentication (fill in USERNAME / PASSWORD).
    TRUSTED_CONNECTION: bool = True
    USERNAME: str = "sa"
    PASSWORD: str = "YourPassword"

    # ODBC Driver 18 encrypts connections by default and rejects
    # self-signed certificates (common on local/dev SQL Server
    # instances) unless told to trust them explicitly.
    TRUST_SERVER_CERTIFICATE: bool = True

    CONNECTION_TIMEOUT: int = 5

    APP_NAME: str = "Employee Management System"
    APP_VERSION: str = "3.1.0"
    ORG_NAME: str = "Nova HR Solutions"

    # Business rules kept alongside the config that mirrors them in SQL
    # (see the CHECK constraints in DatabaseManager.ensure_database_and_table).
    MIN_AGE: int = 18
    MAX_AGE: int = 65
