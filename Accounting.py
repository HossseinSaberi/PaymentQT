from datetime import datetime
from AccountingDialog import MainPageDialog
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from DataAccess import Queries, ConnectToDB
from MixinsClass import TotalStyleMixin
from Utils import JDateUtils
import functools
from TabClasses import CostTabDetail, SaveTabDetail, PaymentTabDetail, InstallmentTabDetail, StaticCostTabDetail, SalaryTabDetail, UserTabDetail


class Account(TotalStyleMixin):

    function_with_tab_index = {}

    def __init__(self):
        super().__init__()
        self.dlg = None
        # self.cost_dialog = self.save_dialog = QtWidgets.QDialog()
        self.dialog_object = QtWidgets.QDialog()
        self.cdb = ConnectToDB()
        self.query_handler = Queries(db_connection=self.cdb.get_conn())
        self.initial_tab_index_function()
        self.init_gui()

    def initial_tab_index_function(self):
        self.function_with_tab_index = {
            0: self.update_salary_tab,
            1: self.update_cost_tab,
            2: self.update_static_cost_tab,
            3: self.update_installment_tab,
            4: self.update_save_tab,
            5: self.update_debtor_tab,
            6: self.update_creditor_tab
        }

    def init_gui(self):
        self.create_ui()
        self.check_trigger()
        self.update_salary_tab()
        self.dlg.show()

    def create_ui(self):
        self.create_main_page_dialog()

    def check_trigger(self):
        self.check_dlg_trigger()

    def tab_active(self, index):
        func_instance = functools.partial(self.function_with_tab_index[index])
        func_instance()

    def check_dlg_trigger(self):
        self.dlg.new_user.triggered.connect(functools.partial(self.create_page, UserTabDetail))
        self.dlg.new_input.triggered.connect(functools.partial(self.create_page, SalaryTabDetail))
        self.dlg.new_output.triggered.connect(functools.partial(self.create_page, CostTabDetail))
        self.dlg.new_static_output.triggered.connect(functools.partial(self.create_page, StaticCostTabDetail))
        self.dlg.new_installment.triggered.connect(functools.partial(self.create_page, InstallmentTabDetail))
        self.dlg.new_saving.triggered.connect(functools.partial(self.create_page, SaveTabDetail))
        self.dlg.new_debt_credit.triggered.connect(functools.partial(self.create_page, PaymentTabDetail))
        self.dlg.account_tab.currentChanged.connect(self.tab_active)

    def create_page(self, class_object):
        self.create_dialog()
        class_object(self.dlg, self.dialog_object, self.query_handler)

    def create_main_page_dialog(self):
        self.dlg = MainPageDialog()

    def create_dialog(self):
        self.dialog_object.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.dialog_object = QtWidgets.QDialog()

    def update_cost_tab(self):
        cost_list = self.query_handler.get_cost_list()
        self.add_data_to_qtablewidget(self.dlg.all_output_list, cost_list, 'RED')

    def update_save_tab(self):
        save_money_list = self.query_handler.get_save_money_list()
        self.add_data_to_qtablewidget(self.dlg.all_saving_list, save_money_list, 'GREEN')

    def update_debtor_tab(self):
        debtor_list = self.query_handler.get_debtor_creditor_list('قرض داده شده')
        self.clear_qtable_widget(self.dlg.all_debtor_list)
        self.add_data_to_qtablewidget(self.dlg.all_debtor_list, debtor_list, 'GREEN')

    def update_creditor_tab(self):
        creditor_list = self.query_handler.get_debtor_creditor_list('قرض گرفته شده')
        self.clear_qtable_widget(self.dlg.all_creditor_list)
        self.add_data_to_qtablewidget(self.dlg.all_creditor_list, creditor_list, 'RED')

    def update_salary_tab(self):
        salary_list = self.query_handler.get_salary_list()
        self.clear_qtable_widget(self.dlg.all_input_list)
        self.add_data_to_qtablewidget(self.dlg.all_input_list, salary_list, 'GREEN')

    def update_installment_tab(self):
        installment_list = self.query_handler.get_installment_list()
        self.clear_qtable_widget(self.dlg.all_installment)
        self.add_data_to_qtablewidget(self.dlg.all_installment, installment_list, 'RED')

    def update_static_cost_tab(self):
        static_cost_list = self.query_handler.get_static_cost_list()
        self.clear_qtable_widget(self.dlg.all_debtor_list)
        self.add_data_to_qtablewidget(self.dlg.all_static_output_list, static_cost_list, 'RED')

    def add_data_to_qtablewidget(self, object_name, data_list, color):
        self.clear_qtable_widget(object_name)
        for each_result in data_list:
            cost_details = self.clear_data_to_insert_qtable_widget(each_result)
            self.add_new_row_to_main_list(object_name, cost_details, color)

    def add_new_row_to_main_list(self, obj_name, data, color):
        row_position = obj_name.rowCount()
        obj_name.insertRow(row_position)
        for index, each_item in enumerate(data.items(), start=0):
            item = QtWidgets.QTableWidgetItem(str(each_item[1]))
            self.item_color_styles(item, color)
            item.setTextAlignment(Qt.AlignCenter)
            obj_name.setItem(row_position, index, item)
        obj_name.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        obj_name.resizeColumnsToContents()
        obj_name.horizontalHeader().setStretchLastSection(True)

    @staticmethod
    def clear_data_to_insert_qtable_widget(data: dict):

        details = dict()
        for key, value in data.items():
            details[key] = value
            if isinstance(value, datetime):
                details[key] = JDateUtils.convert_to_jalali(data[key].date()) if data[key] else '-'
            elif isinstance(value, int):
                details[key] = f"{data[key]:,}"
            else:
                details[key] = value if value else '-'

        return details

    @staticmethod
    def clear_qtable_widget(obj_name):
        obj_name.setRowCount(0)
