"""
Pages package
"""

from .base_page import BasePage
from .login_page import LoginPage
from .dashboard_page import DashboardPage
from .schemes_page import SchemesPage
from .users_page import UsersPage
from .admins_page import AdminsPage

__all__ = [
    'BasePage',
    'LoginPage',
    'DashboardPage',
    'SchemesPage',
    'UsersPage',
    'AdminsPage'
]
