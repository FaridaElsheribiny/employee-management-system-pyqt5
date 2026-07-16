"""
Main application window.
===========================
The app shell: a dark sidebar for navigation, a top bar with the page
title and a live clock, and a QStackedWidget that swaps between pages.

Hard rule followed throughout: THE GUI NEVER CONTAINS BUSINESS LOGIC
AND NEVER EXECUTES SQL. MainWindow only wires pages together and owns
the QMainWindow chrome (menu bar, status bar); all data access still
goes through EmployeeManager.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtWidgets import (
    QFrame, QHBoxLayout, QLabel, QMainWindow, QMessageBox, QStackedWidget,
    QVBoxLayout, QWidget,
)

from config import Config
from database.database_manager import DatabaseConnectionError
from services.employee_manager import EmployeeManager
from ui.pages.dashboard_page import DashboardPage
from ui.pages.employees_page import EmployeesPage
from ui.theme import STYLESHEET
from ui.widgets.sidebar import Sidebar

NAV_ITEMS = [
    ("dashboard", "\u2302", "Dashboard"),
    ("employees", "\u2630", "Employees"),
]

PAGE_TITLES = {
    "dashboard": ("Dashboard", "Live overview of your workforce"),
    "employees": ("Employees", "Add, search, update, and manage your team"),
}


class MainWindow(QMainWindow):

    def __init__(self, employee_manager: Optional[EmployeeManager] = None) -> None:
        super().__init__()

        try:
            self.manager = employee_manager or EmployeeManager()
        except DatabaseConnectionError as error:
            QMessageBox.critical(self, "Database Connection Error", str(error))
            raise

        self.setWindowTitle(Config.APP_NAME)
        self.resize(1280, 760)
        self.setMinimumSize(1040, 640)
        self.setStyleSheet(STYLESHEET)

        self._build_menu_bar()
        self._build_ui()
        self._start_clock()

        self.setStatusBar(self.statusBar())
        self.statusBar().showMessage("Ready")

    # ------------------------------------------------------------
    # Menu bar
    # ------------------------------------------------------------
    def _build_menu_bar(self) -> None:
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction("Refresh", self._refresh_current_page)
        file_menu.addSeparator()
        file_menu.addAction("Exit", self.close)

        edit_menu = menu_bar.addMenu("&Edit")
        edit_menu.addAction("Add Employee", lambda: self.employees_page.add_employee())
        edit_menu.addAction("Update Employee", lambda: self.employees_page.update_employee())
        edit_menu.addAction("Delete Employee", lambda: self.employees_page.delete_employee())
        edit_menu.addAction("Clear Form", lambda: self.employees_page.clear_form())

        help_menu = menu_bar.addMenu("&Help")
        help_menu.addAction("About", self._show_about_dialog)

    def _show_about_dialog(self) -> None:
        QMessageBox.information(
            self, "About",
            f"{Config.APP_NAME}\nVersion {Config.APP_VERSION}\n\n"
            "Built with PyQt5 and Microsoft SQL Server.",
        )

    # ------------------------------------------------------------
    # Shell construction: sidebar + top bar + stacked pages
    # ------------------------------------------------------------
    def _build_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.sidebar = Sidebar(NAV_ITEMS)
        self.sidebar.page_changed.connect(self._on_nav_changed)
        root.addWidget(self.sidebar)

        right_col = QVBoxLayout()
        right_col.setContentsMargins(0, 0, 0, 0)
        right_col.setSpacing(0)

        right_col.addWidget(self._build_top_bar())

        self.stack = QStackedWidget()
        self.stack.setContentsMargins(0, 0, 0, 0)

        content_wrapper = QWidget()
        content_layout = QVBoxLayout(content_wrapper)
        content_layout.setContentsMargins(20, 16, 20, 16)
        content_layout.addWidget(self.stack)

        self.dashboard_page = DashboardPage(
            self.manager,
            on_status=lambda msg, timeout: self.statusBar().showMessage(msg, timeout),
            on_navigate_to_employees=self._go_to_employees_to_add,
        )
        self.employees_page = EmployeesPage(
            self.manager,
            on_status=lambda msg, timeout: self.statusBar().showMessage(msg, timeout),
            on_data_changed=self.dashboard_page.refresh,
        )
        self.stack.addWidget(self.dashboard_page)   # index 0 -> "dashboard"
        self.stack.addWidget(self.employees_page)   # index 1 -> "employees"
        self._page_index = {"dashboard": 0, "employees": 1}

        right_col.addWidget(content_wrapper, stretch=1)

        right_wrapper = QWidget()
        right_wrapper.setLayout(right_col)
        root.addWidget(right_wrapper, stretch=1)

    def _build_top_bar(self) -> QWidget:
        bar = QFrame()
        bar.setObjectName("TopBar")
        bar.setFixedHeight(54)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(20, 0, 20, 0)

        title_col = QVBoxLayout()
        title_col.setSpacing(0)
        self.page_title_label = QLabel()
        self.page_title_label.setObjectName("PageTitle")
        self.page_subtitle_label = QLabel()
        self.page_subtitle_label.setObjectName("PageSubtitle")
        title_col.addWidget(self.page_title_label)
        title_col.addWidget(self.page_subtitle_label)
        layout.addLayout(title_col)
        layout.addStretch(1)

        clock_col = QVBoxLayout()
        clock_col.setSpacing(0)
        clock_col.setAlignment(Qt.AlignRight)
        self.clock_label = QLabel()
        self.clock_label.setObjectName("ClockLabel")
        self.clock_label.setAlignment(Qt.AlignRight)
        self.date_label = QLabel()
        self.date_label.setObjectName("DateLabel")
        self.date_label.setAlignment(Qt.AlignRight)
        clock_col.addWidget(self.clock_label)
        clock_col.addWidget(self.date_label)
        layout.addLayout(clock_col)

        self._set_page_header("dashboard")
        return bar

    # ------------------------------------------------------------
    # Navigation
    # ------------------------------------------------------------
    def _on_nav_changed(self, key: str) -> None:
        self.stack.setCurrentIndex(self._page_index[key])
        self._set_page_header(key)
        if key == "dashboard":
            self.dashboard_page.refresh()

    def _set_page_header(self, key: str) -> None:
        title, subtitle = PAGE_TITLES[key]
        self.page_title_label.setText(title)
        self.page_subtitle_label.setText(subtitle)

    def _refresh_current_page(self) -> None:
        self.dashboard_page.refresh()
        self.employees_page.refresh_table()

    def _go_to_employees_to_add(self) -> None:
        """Wired to the Dashboard's "Add Employee" quick action: switch
        to the Employees page (keeping the sidebar's active state in
        sync, since this bypasses an actual sidebar click) and make
        sure the form is empty and focused for a new entry."""
        self.sidebar.set_active("employees")
        self._on_nav_changed("employees")
        self.employees_page.clear_form()
        self.employees_page.name_input.setFocus()

    # ------------------------------------------------------------
    # Live clock (updates the top bar every second)
    # ------------------------------------------------------------
    def _start_clock(self) -> None:
        self._tick_clock()
        timer = QTimer(self)
        timer.timeout.connect(self._tick_clock)
        timer.start(1000)
        self._clock_timer = timer  # keep a reference so it isn't garbage-collected

    def _tick_clock(self) -> None:
        now = datetime.now()
        self.clock_label.setText(now.strftime("%I:%M:%S %p"))
        self.date_label.setText(now.strftime("%A, %B %d, %Y"))
