import sys
import os
from PyQt5 import uic
from PyQt5.QtWidgets import QLabel, QLineEdit, QSpinBox, QDoubleSpinBox
import json

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
path = os.path.dirname(os.path.abspath(__file__))
MainWindowUI, MainWindowBase = uic.loadUiType(
    os.path.join(path, 'gui/main_page.ui'))

AddNewPaymentUI, AddNewPaymentBase = uic.loadUiType(
    os.path.join(path, 'gui/new_payment.ui'))

AddNewUserUI, AddNewUserBase = uic.loadUiType(
    os.path.join(path, 'gui/new_user.ui'))

AddNewCostUI, AddNewCostBase = uic.loadUiType(
    os.path.join(path, 'gui/new_cost.ui'))

AddNewSalaryUI, AddNewSalaryBase = uic.loadUiType(
    os.path.join(path, 'gui/input_salary.ui'))

AddNewInstallmentUI, AddNewInstallmentBase = uic.loadUiType(
    os.path.join(path, 'gui/new_installment.ui'))

AddNewSaveMoneyUI, AddNewSaveMoneyBase = uic.loadUiType(
    os.path.join(path, 'gui/new_save_money.ui'))

AddNewStaticUI, AddNewStaticBase = uic.loadUiType(
    os.path.join(path, 'gui/static_cost.ui'))


class MainPageDialog(MainWindowBase, MainWindowUI):
    def __init__(self, parent=None):
        """Constructor."""
        MainWindowBase.__init__(self, parent)
        self.setupUi(self)


class AddNewPaymentDialog(AddNewPaymentUI, AddNewPaymentBase):
    def __init__(self, parent=None):
        """Constructor."""
        AddNewPaymentBase.__init__(self, parent)
        

class AddNewUserDialog(AddNewUserUI, AddNewUserBase):
    def __init__(self, parent=None):
        """Constructor."""
        AddNewUserBase.__init__(self, parent)


class AddNewCostDialog(AddNewCostUI, AddNewCostBase):
    def __init__(self, parent=None):
        """Constructor."""
        AddNewCostBase.__init__(self, parent)


class AddNewSalaryDialog(AddNewSalaryUI, AddNewSalaryBase):
    def __init__(self, parent=None):
        """Constructor."""
        AddNewSalaryBase.__init__(self, parent)


class AddNewInstallmentDialog(AddNewInstallmentUI, AddNewInstallmentBase):
    def __init__(self, parent=None):
        """Constructor."""
        AddNewInstallmentBase.__init__(self, parent)


class AddNewSaveMoneyDialog(AddNewSaveMoneyUI, AddNewSaveMoneyBase):
    def __init__(self, parent=None):
        """Constructor."""
        AddNewSaveMoneyBase.__init__(self, parent)


class AddNewStaticDialog(AddNewStaticUI, AddNewStaticBase):
    def __init__(self, parent=None):
        """Constructor."""
        AddNewStaticBase.__init__(self, parent)

