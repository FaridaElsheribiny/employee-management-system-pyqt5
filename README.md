<div align="center">

# 👥 Employee Management System

### A modern desktop Employee Management System built with Python & PyQt5

*Clean architecture • Reusable UI components • Beautiful, responsive interface*

<br/>

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PyQt5](https://img.shields.io/badge/PyQt5-GUI-41CD52?style=for-the-badge&logo=qt&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Database-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

</div>

<br/>

## 📚 Table of Contents

- [✨ Features](#-features)
- [🛠️ Technologies Used](#️-technologies-used)
- [📁 Project Structure](#-project-structure)
- [⚙️ Installation](#️-installation)
- [📦 Requirements](#-requirements)
- [🚀 How to Run](#-how-to-run)
- [📸 Screenshots](#-screenshots)
- [🔮 Future Improvements](#-future-improvements)
- [👤 Author](#-author)
- [📄 License](#-license)

<br/>

## ✨ Features

<table>
<tr>
<td width="50%">

### 📊 Dashboard with KPIs
Get a real-time overview of your workforce with key performance indicators at a glance.

</td>
<td width="50%">

### 🧑‍💼 Employee Management (CRUD)
Add, view, update, and delete employee records with a smooth, intuitive workflow.

</td>
</tr>
<tr>
<td width="50%">

### 🏢 Department Management
Organize employees into departments and manage department data with ease.

</td>
<td width="50%">

### 🔍 Search Employees
Quickly find any employee using fast, responsive search and filtering.

</td>
</tr>
<tr>
<td width="50%">

### 📈 Analytics & Charts
Visualize workforce data with interactive charts powered by Matplotlib.

</td>
<td width="50%">

### 📤 CSV Export
Export employee and department data to CSV for reporting and analysis.

</td>
</tr>
<tr>
<td width="50%">

### 🗄️ SQLite Database
Lightweight, file-based database with zero external setup required.

</td>
<td width="50%">

### 🧭 Modern Sidebar Navigation
Clean, icon-driven sidebar for effortless navigation between modules.

</td>
</tr>
<tr>
<td width="50%" colspan="2">

### 📱 Responsive UI
A polished, adaptive interface that stays consistent across different window sizes.

</td>
</tr>
</table>

<br/>

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| 🐍 **Python** | Core application logic |
| 🎨 **PyQt5** | Desktop GUI framework |
| 🗄️ **SQLite** | Local relational database |
| 📊 **Matplotlib** | Data visualization & charts |
| ⭐ **QtAwesome** | Icon library for the modern UI |

<br/>

## 📁 Project Structure

```
Employee-Management-System/
│
├── main.py                        # Application entry point
├── config.py                      # Application configuration
│
├── database/
│   ├── database_manager.py        # Database connection & operations
│   └── models.py                  # Data models / schema definitions
│
├── ui/
│   ├── main_window.py             # Main application window
│   ├── dashboard.py                # Dashboard with KPIs
│   ├── employees_view.py          # Employee CRUD interface
│   ├── departments_view.py        # Department management interface
│   ├── analytics_view.py          # Charts & analytics
│   └── components/                # Reusable UI components (cards, sidebar, tables)
│
├── assets/
│   ├── icons/                     # Application icons
│   └── screenshots/                # README screenshots
│
├── utils/
│   └── csv_exporter.py            # CSV export helper
│
├── requirements.txt                # Project dependencies
└── README.md                       # Project documentation
```

<br/>

## ⚙️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/employee-management-system.git
   cd employee-management-system
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate      # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

<br/>

## 📦 Requirements

- Python 3.9+
- PyQt5
- SQLite3 (bundled with Python)
- Matplotlib
- QtAwesome

```
pip install PyQt5 matplotlib qtawesome
```

<br/>

## 🚀 How to Run

```bash
python main.py
```

The SQLite database is created automatically on first launch — no manual setup required.

<br/>

## 📸 Screenshots

### Dashboard
![Dashboard](assets/dashboard.png)

### Employees
![Employees](assets/employees.png)

<br/>

## 🔮 Future Improvements

- [ ] 🌙 Dark mode support
- [ ] 🔐 Role-based authentication (Admin / HR / Employee)
- [ ] ☁️ Cloud database sync option
- [ ] 🌐 Multi-language support (English / Arabic)
- [ ] 📄 PDF report generation
- [ ] 🔔 Notifications & reminders for HR tasks

<br/>

## 👤 Author

**Farida Elsheribiny**

- GitHub: [@FaridaElsheribiny](https://github.com/FaridaElsheribiny)

<br/>

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.

<br/>

<div align="center">

⭐ If you found this project useful, consider giving it a star!

</div>
