"""
Employee Management System -- entry point.
=============================================
Setup:
    pip install PyQt5 pyodbc
    Edit config.py to match your SQL Server instance, then run:
        python main.py

The database and table are created automatically on first run.
"""
from __future__ import annotations

import sys

from PyQt5.QtWidgets import QApplication

from config import Config
from database.database_manager import DatabaseConnectionError
from ui.main_window import MainWindow


def main() -> None:
    app = QApplication(sys.argv)
    app.setApplicationName(Config.APP_NAME)

    try:
        window = MainWindow()
    except DatabaseConnectionError:
        # The error dialog was already shown inside MainWindow.__init__;
        # here we just exit cleanly instead of raising a raw traceback.
        sys.exit(1)

    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
