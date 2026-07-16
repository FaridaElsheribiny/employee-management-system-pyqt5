"""
Domain models.
================
    - Encapsulation : every attribute is private and reachable only
                      through a validated property.
    - Abstraction   : Person is an abstract base class; callers only
                      need to know "a Person can display_info() and
                      calculate_salary()", not how each subclass does it.
    - Inheritance   : Person -> Employee -> Manager.
    - Polymorphism  : calculate_salary(), display_info() and role_name()
                      behave differently per class with no type checks
                      required by the caller.

Logic is unchanged from the original single-file version -- only the
location moved, plus the relative import of Config.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional

from config import Config


class Person(ABC):
    """Abstract base class representing any person in the system."""

    def __init__(self, name: str, age: int) -> None:
        # Assigning through the properties (not the private variables
        # directly) means validation runs the instant the object is
        # created, not only when a value is edited later.
        self.name = name
        self.age = age

    # ---------------------------------------------------------------- name
    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if not value or not str(value).strip():
            raise ValueError("Name cannot be empty.")
        self.__name = str(value).strip()

    # ----------------------------------------------------------------- age
    @property
    def age(self) -> int:
        return self.__age

    @age.setter
    def age(self, value: Any) -> None:
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValueError("Age must be a whole number.")
        if value < Config.MIN_AGE or value > Config.MAX_AGE:
            raise ValueError(f"Age must be between {Config.MIN_AGE} and {Config.MAX_AGE}.")
        self.__age = value

    @abstractmethod
    def display_info(self) -> str:
        """Human-readable summary of this person (Abstraction)."""
        raise NotImplementedError

    @abstractmethod
    def calculate_salary(self) -> float:
        """Salary calculation -- meaning differs by role (Polymorphism)."""
        raise NotImplementedError


class Employee(Person):
    """A regular employee. Inherits identity/validation from Person."""

    def __init__(
        self,
        name: str,
        age: int,
        department: str,
        base_salary: float,
        emp_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        super().__init__(name, age)
        self.department = department
        self.base_salary = base_salary

        # emp_id / created_at / updated_at are system-generated metadata
        # (assigned by SQL Server), not user input -- nothing to validate,
        # so they are stored directly rather than through a setter.
        self.__emp_id = int(emp_id) if emp_id is not None else None
        self.__created_at = created_at
        self.__updated_at = updated_at

    # ------------------------------------------------------- emp_id (read-only)
    @property
    def emp_id(self) -> Optional[int]:
        return self.__emp_id

    def _assign_id(self, new_id: int) -> None:
        """Internal hook used ONLY by EmployeeManager right after an
        INSERT, when SQL Server generates the real EmployeeID. Not part
        of the public API."""
        self.__emp_id = int(new_id)

    @property
    def created_at(self) -> Optional[datetime]:
        return self.__created_at

    @property
    def updated_at(self) -> Optional[datetime]:
        return self.__updated_at

    # ------------------------------------------------------------ department
    @property
    def department(self) -> str:
        return self.__department

    @department.setter
    def department(self, value: str) -> None:
        if not value or not str(value).strip():
            raise ValueError("Department cannot be empty.")
        self.__department = str(value).strip()

    # ------------------------------------------------------------ base_salary
    @property
    def base_salary(self) -> float:
        return self.__base_salary

    @base_salary.setter
    def base_salary(self, value: Any) -> None:
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("Salary must be a number.")
        if value < 0:
            raise ValueError("Salary cannot be negative.")
        self.__base_salary = value

    def role_name(self) -> str:
        """Human-readable role label. Overridden by Manager (Polymorphism)."""
        return "Employee"

    # ---- Polymorphism: same method name, different behaviour in Manager ----
    def calculate_salary(self) -> float:
        return self.base_salary

    def display_info(self) -> str:
        return (
            f"#{self.emp_id} | {self.name} ({self.role_name()}) | "
            f"Dept: {self.department} | Age: {self.age} | "
            f"Salary: {self.calculate_salary():,.2f}"
        )

    def to_dict(self) -> dict:
        """Plain dict representation for the database layer / debugging."""
        return {
            "emp_id": self.emp_id,
            "name": self.name,
            "age": self.age,
            "department": self.department,
            "role": self.role_name(),
            "base_salary": self.base_salary,
            "bonus": 0.0,
            "team_size": 0,
            "total_salary": self.calculate_salary(),
        }


class Manager(Employee):
    """
    A manager: everything an Employee has, plus a team and a bonus.
    Overrides calculate_salary(), display_info() and role_name() to
    demonstrate Polymorphism.
    """

    def __init__(
        self,
        name: str,
        age: int,
        department: str,
        base_salary: float,
        team_size: int = 0,
        bonus: float = 0.0,
        emp_id: Optional[int] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ) -> None:
        super().__init__(name, age, department, base_salary, emp_id, created_at, updated_at)
        self.team_size = team_size
        self.bonus = bonus

    # -------------------------------------------------------------- team_size
    @property
    def team_size(self) -> int:
        return self.__team_size

    @team_size.setter
    def team_size(self, value: Any) -> None:
        try:
            value = int(value)
        except (TypeError, ValueError):
            raise ValueError("Team size must be a whole number.")
        if value < 0:
            raise ValueError("Team size cannot be negative.")
        self.__team_size = value

    # ------------------------------------------------------------------ bonus
    @property
    def bonus(self) -> float:
        return self.__bonus

    @bonus.setter
    def bonus(self, value: Any) -> None:
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("Bonus must be a number.")
        if value < 0:
            raise ValueError("Bonus cannot be negative.")
        self.__bonus = value

    def role_name(self) -> str:
        return "Manager"

    def calculate_salary(self) -> float:
        return self.base_salary + self.bonus + (self.team_size * 50)

    def display_info(self) -> str:
        base = super().display_info()
        return base + f" | Team: {self.team_size} | Bonus: {self.bonus:,.2f}"

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            "role": self.role_name(),
            "bonus": self.bonus,
            "team_size": self.team_size,
            "total_salary": self.calculate_salary(),
        })
        return data
