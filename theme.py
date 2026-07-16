"""
Design system.
================
Single source of truth for color, spacing, and the global QSS
stylesheet. Every widget in the app should pull colors from `Palette`
rather than hardcoding hex values, so a future theme (dark mode, etc.)
only has to change this one file.
"""
from __future__ import annotations

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect


class Palette:
    """Enterprise color tokens -- a dark navy sidebar with an indigo
    accent, on a light neutral canvas. Chosen to read as "enterprise
    SaaS" (Linear / Notion / Stripe Dashboard family) rather than the
    stock light-blue Qt look."""

    # Brand / accent
    PRIMARY = "#4F46E5"        # indigo-600
    PRIMARY_HOVER = "#4338CA"  # indigo-700
    PRIMARY_PRESSED = "#3730A3"
    PRIMARY_SOFT = "#EEF2FF"   # indigo-50, used for soft backgrounds

    # Sidebar (dark)
    SIDEBAR_BG = "#111827"        # gray-900
    SIDEBAR_BG_ALT = "#0B0F19"
    SIDEBAR_HOVER = "#1F2937"     # gray-800
    SIDEBAR_ACTIVE = "#4F46E5"
    SIDEBAR_TEXT = "#E5E7EB"
    SIDEBAR_TEXT_MUTED = "#9CA3AF"
    SIDEBAR_BORDER = "#1F2937"

    # Canvas / surfaces
    BG = "#F3F4F6"             # gray-100 app background
    SURFACE = "#FFFFFF"        # cards
    BORDER = "#E5E7EB"         # gray-200
    BORDER_STRONG = "#D1D5DB"

    # Text
    TEXT_PRIMARY = "#111827"
    TEXT_SECONDARY = "#6B7280"
    TEXT_MUTED = "#9CA3AF"

    # Semantic
    SUCCESS = "#10B981"
    SUCCESS_SOFT = "#ECFDF5"
    DANGER = "#EF4444"
    DANGER_SOFT = "#FEF2F2"
    WARNING = "#F59E0B"
    WARNING_SOFT = "#FFFBEB"
    INFO = "#3B82F6"
    INFO_SOFT = "#EFF6FF"
    VIOLET = "#8B5CF6"
    VIOLET_SOFT = "#F5F3FF"

    FONT_FAMILY = '"Segoe UI", "Inter", "Cairo", Arial, sans-serif'


def card_shadow(blur: int = 24, y_offset: int = 6, alpha: int = 28) -> QGraphicsDropShadowEffect:
    """Soft drop shadow applied in Python to card widgets -- QSS alone
    can't render shadows."""
    effect = QGraphicsDropShadowEffect()
    effect.setBlurRadius(blur)
    effect.setOffset(0, y_offset)
    effect.setColor(QColor(17, 24, 39, alpha))
    return effect


STYLESHEET = f"""
QWidget {{
    background-color: {Palette.BG};
    font-family: {Palette.FONT_FAMILY};
    font-size: 11px;
    color: {Palette.TEXT_PRIMARY};
}}

/* ---------------- Sidebar ---------------- */
QFrame#Sidebar {{
    background-color: {Palette.SIDEBAR_BG};
    border: none;
}}
QLabel#BrandTitle {{
    color: #020617;
    font-size: 17px;
    font-weight: 700;
}}
QLabel#BrandSubtitle {{
    color: {Palette.SIDEBAR_TEXT_MUTED};
    font-size: 8.5px;
    font-weight: 500;
    letter-spacing: 0.4px;
}}
QPushButton#NavButton {{
    background-color: transparent;
    color: {Palette.SIDEBAR_TEXT};
    text-align: left;
    padding: 8px 13px;
    border-radius: 7px;
    font-weight: 500;
    font-size: 11px;
    border: none;
}}
QPushButton#NavButton:hover {{
    background-color: {Palette.SIDEBAR_HOVER};
    color: #FFFFFF;
}}
QPushButton#NavButton:checked {{
    background-color: {Palette.SIDEBAR_ACTIVE};
    color:  #374151;
    font-weight: 600;
}}
QLabel#NavSectionLabel {{
    color: {Palette.SIDEBAR_TEXT_MUTED};
    font-size: 9px;
    font-weight: 700;
    letter-spacing: 0.8px;
    padding: 5px 13px 2px 13px;
}}
QFrame#SidebarDivider {{
    background-color: {Palette.SIDEBAR_BORDER};
    max-height: 1px;
    min-height: 1px;
}}
QLabel#SidebarFooter {{
    color: {Palette.SIDEBAR_TEXT_MUTED};
    font-size: 9px;
}}

/* ---------------- Top bar ---------------- */
QFrame#TopBar {{
    background-color: {Palette.SURFACE};
    border-bottom: 1px solid {Palette.BORDER};
}}
QLabel#PageTitle {{
    font-size: 17px;
    font-weight: 700;
    color: {Palette.TEXT_PRIMARY};
}}
QLabel#PageSubtitle {{
    font-size: 11px;
    color: {Palette.TEXT_SECONDARY};
}}
QLabel#ClockLabel {{
    font-size: 13px;
    font-weight: 600;
    color: {Palette.TEXT_PRIMARY};
}}
QLabel#DateLabel {{
    font-size: 11px;
    color: {Palette.TEXT_SECONDARY};
}}

/* ---------------- Cards ---------------- */
QFrame#Card {{
    background-color: {Palette.SURFACE};
    border: 1px solid {Palette.BORDER};
    border-radius: 12px;
}}
QLabel#SectionTitle {{
    font-size: 12px;
    font-weight: 700;
    color: {Palette.TEXT_PRIMARY};
}}
QLabel#SectionCaption {{
    font-size: 11px;
    color: {Palette.TEXT_SECONDARY};
}}

/* ---------------- Stat cards ---------------- */
QFrame#StatCard {{
    background-color: {Palette.SURFACE};
    border: 1px solid {Palette.BORDER};
    border-radius: 12px;
}}
QLabel#StatIcon {{
    border-radius: 9px;
    font-size: 13px;
    font-weight: 700;
    qproperty-alignment: AlignCenter;
}}
QLabel#StatValue {{
    font-size: 19px;
    font-weight: 700;
    color: {Palette.TEXT_PRIMARY};
}}
QLabel#StatLabel {{
    font-size: 10px;
    font-weight: 600;
    color: {Palette.TEXT_SECONDARY};
    letter-spacing: 0.3px;
}}

/* ---------------- Inputs ---------------- */
QLineEdit, QSpinBox, QDoubleSpinBox, QComboBox {{
    background-color: #FFFFFF;
    border: 1px solid {Palette.BORDER_STRONG};
    border-radius: 7px;
    padding: 6px 8px;
    min-height: 22px;
    selection-background-color: {Palette.PRIMARY_SOFT};
}}
QLineEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus, QComboBox:focus {{
    border: 1.5px solid {Palette.PRIMARY};
}}
QLineEdit:disabled, QSpinBox:disabled, QDoubleSpinBox:disabled, QComboBox:disabled {{
    background-color: #F1F5F9;
    color: {Palette.TEXT_MUTED};
}}
QComboBox::drop-down {{ border: none; width: 20px; }}
QComboBox QAbstractItemView {{
    background-color: #FFFFFF;
    border: 1px solid {Palette.BORDER_STRONG};
    selection-background-color: {Palette.PRIMARY_SOFT};
    selection-color: {Palette.PRIMARY};
    outline: none;
}}
QLabel#FieldLabel {{
    font-size: 10px;
    font-weight: 600;
    color: {Palette.TEXT_SECONDARY};
}}

/* ---------------- Buttons ---------------- */
QPushButton {{
    border-radius: 7px;
    padding: 7px 14px;
    font-weight: 600;
    color: #FFFFFF;
    background-color: {Palette.PRIMARY};
    border: none;
}}
QPushButton:hover {{ background-color: {Palette.PRIMARY_HOVER}; }}
QPushButton:pressed {{ background-color: {Palette.PRIMARY_PRESSED}; }}
QPushButton:disabled {{ background-color: #CBD5E1; color: #6B7280; }}

QPushButton#AddButton {{ background-color: {Palette.SUCCESS}; }}
QPushButton#AddButton:hover {{ background-color: #059669; }}
QPushButton#UpdateButton {{ background-color: {Palette.PRIMARY}; }}
QPushButton#DeleteButton {{ background-color: {Palette.DANGER}; }}
QPushButton#DeleteButton:hover {{ background-color: #DC2626; }}
QPushButton#ClearButton {{ background-color: #6B7280; }}
QPushButton#ClearButton:hover {{ background-color: #4B5563; }}
QPushButton#GhostButton {{
    background-color: transparent;
    color: {Palette.TEXT_SECONDARY};
    border: 1px solid {Palette.BORDER_STRONG};
}}
QPushButton#GhostButton:hover {{
    background-color: {Palette.BG};
    color: {Palette.TEXT_PRIMARY};
}}

/* ---------------- Table ---------------- */
QTableWidget {{
    background-color: {Palette.SURFACE};
    border: none;
    gridline-color: #F1F5F9;
    selection-background-color: {Palette.PRIMARY_SOFT};
    selection-color: {Palette.PRIMARY};
    alternate-background-color: #FAFBFC;
}}
QTableWidget::item {{ padding: 6px; border-bottom: 1px solid #F1F5F9; }}
QHeaderView::section {{
    background-color: #FAFBFC;
    color: {Palette.TEXT_SECONDARY};
    font-weight: 700;
    font-size: 9.5px;
    letter-spacing: 0.3px;
    padding: 8px 6px;
    border: none;
    border-bottom: 1px solid {Palette.BORDER};
}}

/* ---------------- Menus / toolbars / status bar ---------------- */
QMenuBar {{ background-color: {Palette.SURFACE}; border-bottom: 1px solid {Palette.BORDER}; padding: 2px; }}
QMenuBar::item {{ padding: 5px 10px; background: transparent; border-radius: 5px; }}
QMenuBar::item:selected {{ background-color: {Palette.PRIMARY_SOFT}; color: {Palette.PRIMARY}; }}
QMenu {{ background-color: #FFFFFF; border: 1px solid {Palette.BORDER}; border-radius: 7px; padding: 4px; }}
QMenu::item {{ padding: 5px 16px; border-radius: 5px; }}
QMenu::item:selected {{ background-color: {Palette.PRIMARY_SOFT}; color: {Palette.PRIMARY}; }}
QStatusBar {{
    background-color: {Palette.SURFACE};
    color: {Palette.TEXT_SECONDARY};
    font-weight: 500;
    border-top: 1px solid {Palette.BORDER};
}}
QMessageBox {{ background-color: #FFFFFF; }}
QMessageBox QLabel {{ color: {Palette.TEXT_PRIMARY}; }}
QMessageBox QPushButton {{ min-width: 70px; }}

QScrollBar:vertical {{
    background: transparent; width: 9px; margin: 0;
}}
QScrollBar::handle:vertical {{
    background: {Palette.BORDER_STRONG}; border-radius: 4px; min-height: 26px;
}}
QScrollBar::handle:vertical:hover {{ background: {Palette.TEXT_MUTED}; }}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
"""
