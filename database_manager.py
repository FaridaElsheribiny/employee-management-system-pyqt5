"""
Database access layer.
=========================
The ONLY module in this codebase allowed to import pyodbc or write SQL.

Logic is unchanged from the original single-file version -- only the
location moved, plus the relative import of Config.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

import pyodbc

from config import Config


class DatabaseConnectionError(Exception):
    """Raised when the application cannot connect to SQL Server."""


class DatabaseQueryError(Exception):
    """Raised when a query fails to execute (constraint violation, etc.)."""


class DatabaseManager:
    """
    Every public method here opens exactly one connection, always
    closes its cursor and connection in a `finally` block (even if an
    exception is raised), and rolls back on failure -- so a failed
    write never leaves a half-committed transaction behind.
    """

    TABLE = "Employees"

    def __init__(self) -> None:
        self.ensure_database_and_table()

    # ------------------------------------------------------------
    # Connection handling
    # ------------------------------------------------------------
    @staticmethod
    def _connection_string(database: str) -> str:
        trust_cert = "yes" if Config.TRUST_SERVER_CERTIFICATE else "no"
        if Config.TRUSTED_CONNECTION:
            return (
                f"DRIVER={Config.DRIVER};SERVER={Config.SERVER};"
                f"DATABASE={database};Trusted_Connection=yes;"
                f"Encrypt=yes;TrustServerCertificate={trust_cert};"
            )
        return (
            f"DRIVER={Config.DRIVER};SERVER={Config.SERVER};"
            f"DATABASE={database};UID={Config.USERNAME};PWD={Config.PASSWORD};"
            f"Encrypt=yes;TrustServerCertificate={trust_cert};"
        )

    def _connect(self, database: Optional[str] = None) -> pyodbc.Connection:
        """Open a single new connection. Never reuses or caches a
        connection across calls -- this avoids the classic bug of a
        stale/duplicate connection being used after the server closes
        an idle session."""
        target_db = database or Config.DATABASE
        try:
            return pyodbc.connect(
                self._connection_string(target_db),
                timeout=Config.CONNECTION_TIMEOUT,
            )
        except pyodbc.Error as error:
            raise DatabaseConnectionError(
                f"Could not connect to SQL Server '{Config.SERVER}'.\n"
                f"Please check that the server name in Config is correct "
                f"and that SQL Server is running.\n\nDetails: {error}"
            ) from error

    def _execute(
        self,
        sql: str,
        params: tuple = (),
        database: Optional[str] = None,
        fetch: Optional[str] = None,
    ) -> Any:
        """
        Single helper that every CRUD method below delegates to, so the
        connect / cursor / execute / commit / close / rollback cycle is
        written in exactly ONE place instead of being repeated in every
        method.
        """
        connection = None
        cursor = None
        try:
            connection = self._connect(database)
            cursor = connection.cursor()
            cursor.execute(sql, params)

            if fetch == "one":
                result = cursor.fetchone()
            elif fetch == "all":
                result = cursor.fetchall()
            else:
                result = cursor.rowcount

            connection.commit()
            return result
        except pyodbc.Error as error:
            if connection is not None:
                connection.rollback()
            raise DatabaseQueryError(f"Database operation failed: {error}") from error
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()

    # ------------------------------------------------------------
    # Setup (idempotent -- safe to call every time the app starts)
    # ------------------------------------------------------------
    def ensure_database_and_table(self) -> None:
        """Create EmployeeManagementDB and the Employees table if they
        don't already exist, including CHECK constraints that mirror
        the validation rules enforced in Python (defense in depth)."""
        try:
            connection = self._connect(database="master")
            connection.autocommit = True
            connection.cursor().execute(
                f"IF DB_ID('{Config.DATABASE}') IS NULL "
                f"CREATE DATABASE [{Config.DATABASE}]"
            )
            connection.close()

            connection = self._connect()
            connection.autocommit = True
            connection.cursor().execute(f"""
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name = '{self.TABLE}' AND xtype = 'U')
                CREATE TABLE {self.TABLE}
                (
                    EmployeeID   INT IDENTITY(1000,1) PRIMARY KEY,
                    Name         NVARCHAR(100)   NOT NULL,
                    Age          INT             NOT NULL
                                 CHECK (Age BETWEEN {Config.MIN_AGE} AND {Config.MAX_AGE}),
                    Department   NVARCHAR(100)   NOT NULL,
                    Role         NVARCHAR(20)    NOT NULL,
                    BaseSalary   DECIMAL(12, 2)  NOT NULL CHECK (BaseSalary >= 0),
                    Bonus        DECIMAL(12, 2)  NOT NULL DEFAULT 0 CHECK (Bonus >= 0),
                    TeamSize     INT             NOT NULL DEFAULT 0 CHECK (TeamSize >= 0),
                    TotalSalary  DECIMAL(12, 2)  NOT NULL,
                    CreatedAt    DATETIME        NOT NULL DEFAULT GETDATE(),
                    UpdatedAt    DATETIME        NOT NULL DEFAULT GETDATE()
                )
            """)
            connection.close()
        except pyodbc.Error as error:
            raise DatabaseConnectionError(
                f"Could not initialize the database/table: {error}"
            ) from error

    # ------------------------------------------------------------
    # CRUD -- every query is parameterized; nothing is ever built by
    # concatenating user input into a SQL string.
    # ------------------------------------------------------------
    def insert_employee(self, data: Dict[str, Any]) -> int:
        """Insert a new row and return the generated EmployeeID."""
        sql = f"""
            INSERT INTO {self.TABLE}
                (Name, Age, Department, Role, BaseSalary, Bonus, TeamSize, TotalSalary)
            OUTPUT INSERTED.EmployeeID
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            data["name"], data["age"], data["department"], data["role"],
            data["base_salary"], data["bonus"], data["team_size"], data["total_salary"],
        )
        row = self._execute(sql, params, fetch="one")
        return int(row[0])

    def update_employee(self, emp_id: int, data: Dict[str, Any]) -> bool:
        """
        Update every column for an existing employee. Also used when the
        role changes (Employee <-> Manager): since every column already
        exists on every row, switching roles is just a normal UPDATE --
        no row deletion or re-insertion, and EmployeeID never changes.
        """
        sql = f"""
            UPDATE {self.TABLE}
            SET Name = ?, Age = ?, Department = ?, Role = ?,
                BaseSalary = ?, Bonus = ?, TeamSize = ?, TotalSalary = ?,
                UpdatedAt = GETDATE()
            WHERE EmployeeID = ?
        """
        params = (
            data["name"], data["age"], data["department"], data["role"],
            data["base_salary"], data["bonus"], data["team_size"],
            data["total_salary"], emp_id,
        )
        rows_affected = self._execute(sql, params)
        return rows_affected > 0

    def delete_employee(self, emp_id: int) -> bool:
        """Delete an employee. Returns True if a row was actually removed."""
        rows_affected = self._execute(
            f"DELETE FROM {self.TABLE} WHERE EmployeeID = ?", (emp_id,)
        )
        return rows_affected > 0

    def fetch_employee(self, emp_id: int) -> Optional[Dict[str, Any]]:
        rows = self._fetch_as_dicts(
            f"SELECT * FROM {self.TABLE} WHERE EmployeeID = ?", (emp_id,)
        )
        return rows[0] if rows else None

    def fetch_all_employees(self) -> List[Dict[str, Any]]:
        return self._fetch_as_dicts(f"SELECT * FROM {self.TABLE} ORDER BY EmployeeID")

    def search_employees(self, keyword: str) -> List[Dict[str, Any]]:
        like = f"%{keyword}%"
        sql = f"""
            SELECT * FROM {self.TABLE}
            WHERE Name LIKE ? OR Department LIKE ? OR Role LIKE ?
               OR CAST(EmployeeID AS NVARCHAR) LIKE ?
            ORDER BY EmployeeID
        """
        return self._fetch_as_dicts(sql, (like, like, like, like))

    def _fetch_as_dicts(self, sql: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """Run a SELECT and convert rows into plain dicts keyed by column
        name, so callers never depend on positional column order."""
        connection = None
        cursor = None
        try:
            connection = self._connect()
            cursor = connection.cursor()
            cursor.execute(sql, params)
            columns = [col[0] for col in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
        except pyodbc.Error as error:
            raise DatabaseQueryError(f"Query failed: {error}") from error
        finally:
            if cursor is not None:
                cursor.close()
            if connection is not None:
                connection.close()
