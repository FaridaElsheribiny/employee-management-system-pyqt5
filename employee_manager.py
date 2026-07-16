"""
Business-logic facade sitting between the GUI and the database.

This is the only class the GUI is allowed to call. It builds and
validates Employee/Manager objects (validation happens inside the
model layer's property setters), converts them to/from the plain
dicts DatabaseManager understands, and never executes SQL itself.

Logic is unchanged from the original single-file version -- only the
location moved, plus the relative imports.
"""
from __future__ import annotations

import csv
from typing import Any, List, Optional

from database.database_manager import DatabaseManager
from models.person import Employee, Manager


class EmployeeManager:

    def __init__(self, database_manager: Optional[DatabaseManager] = None) -> None:
        # Dependency injection: a DatabaseManager can be supplied (handy
        # for testing); otherwise a real one is created here.
        self.db = database_manager or DatabaseManager()

    # ------------------------------------------------------------
    # Conversions between model objects and DB rows
    # ------------------------------------------------------------
    @staticmethod
    def _row_to_object(row: dict) -> Employee:
        """Build the correct object (Employee or Manager) from a DB row.
        Centralized here so the "which class do I build" decision exists
        in exactly one place."""
        common = dict(
            name=row["Name"],
            age=row["Age"],
            department=row["Department"],
            base_salary=float(row["BaseSalary"]),
            emp_id=row["EmployeeID"],
            created_at=row.get("CreatedAt"),
            updated_at=row.get("UpdatedAt"),
        )
        if row["Role"] == "Manager":
            return Manager(
                **common,
                team_size=row.get("TeamSize", 0),
                bonus=float(row.get("Bonus", 0.0)),
            )
        return Employee(**common)

    @staticmethod
    def _object_to_data(employee: Employee) -> dict:
        """Flatten an Employee/Manager object into the plain dict shape
        DatabaseManager expects, computing TotalSalary along the way."""
        is_manager = isinstance(employee, Manager)
        return {
            "name": employee.name,
            "age": employee.age,
            "department": employee.department,
            "role": employee.role_name(),
            "base_salary": employee.base_salary,
            "bonus": employee.bonus if is_manager else 0.0,
            "team_size": employee.team_size if is_manager else 0,
            "total_salary": employee.calculate_salary(),
        }

    @staticmethod
    def _build_employee(
        name: str, age: Any, department: str, role: str,
        base_salary: Any, team_size: Any = 0, bonus: Any = 0.0,
        emp_id: Optional[int] = None,
    ) -> Employee:
        """Construct an Employee or Manager from raw form values. All
        validation happens inside the constructors themselves -- this
        method only decides WHICH class to build."""
        if role == "Manager":
            return Manager(name, age, department, base_salary, team_size, bonus, emp_id=emp_id)
        return Employee(name, age, department, base_salary, emp_id=emp_id)

    # ------------------------------------------------------------
    # CRUD -- the only methods the GUI is allowed to call.
    # ------------------------------------------------------------
    def add_employee(
        self, name: str, age: Any, department: str, role: str,
        base_salary: Any, team_size: Any = 0, bonus: Any = 0.0,
    ) -> Employee:
        """Validate, insert, and return the new object (with its real
        database-generated ID attached)."""
        employee = self._build_employee(name, age, department, role, base_salary, team_size, bonus)
        new_id = self.db.insert_employee(self._object_to_data(employee))
        employee._assign_id(new_id)
        return employee

    def update_employee(
        self, emp_id: int, name: str, age: Any, department: str, role: str,
        base_salary: Any, team_size: Any = 0, bonus: Any = 0.0,
    ) -> bool:
        """
        Validate and update an employee's data. Also handles a role
        change (Employee <-> Manager): since every column exists on
        every row in SQL Server, switching roles is just an UPDATE --
        no delete/re-insert, and the EmployeeID never changes.
        """
        employee = self._build_employee(
            name, age, department, role, base_salary, team_size, bonus, emp_id=emp_id
        )
        return self.db.update_employee(emp_id, self._object_to_data(employee))

    def delete_employee(self, emp_id: int) -> bool:
        """Returns True if an employee was found and removed, else False."""
        return self.db.delete_employee(emp_id)

    def get_employee(self, emp_id: int) -> Optional[Employee]:
        row = self.db.fetch_employee(emp_id)
        return self._row_to_object(row) if row else None

    def load_employees(self) -> List[Employee]:
        """Return every employee in the system."""
        return [self._row_to_object(row) for row in self.db.fetch_all_employees()]

    def search_employees(self, keyword: str) -> List[Employee]:
        """Search by ID, name, department, or role. An empty keyword
        returns everyone (equivalent to load_employees())."""
        keyword = keyword.strip()
        if not keyword:
            return self.load_employees()
        return [self._row_to_object(row) for row in self.db.search_employees(keyword)]

    def export_to_csv(self, path: str) -> int:
        """Write every employee to a CSV file at `path`. Returns the
        number of rows written. Raises whatever DatabaseQueryError
        load_employees() raises, or OSError if the file can't be
        written -- the GUI is responsible for catching and reporting
        both."""
        employees = self.load_employees()
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                "EmployeeID", "Name", "Role", "Department", "Age",
                "BaseSalary", "Bonus", "TeamSize", "TotalSalary",
            ])
            for employee in employees:
                is_manager = isinstance(employee, Manager)
                writer.writerow([
                    employee.emp_id, employee.name, employee.role_name(),
                    employee.department, employee.age,
                    f"{employee.base_salary:.2f}",
                    f"{employee.bonus:.2f}" if is_manager else "",
                    employee.team_size if is_manager else "",
                    f"{employee.calculate_salary():.2f}",
                ])
        return len(employees)
