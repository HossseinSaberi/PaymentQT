from datetime import datetime
from AccountingDialog import MainPageDialog
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt
from DataAccess import Queries, ConnectToDB
from MixinsClass import TotalStyleMixin
from Utils import JDateUtils , CustomItemDelegate
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
        self.create_page_trigger()
        self.dlg.account_tab.currentChanged.connect(self.tab_active)
        self.salary_tab_trigger()

    def create_page_trigger(self):
        self.dlg.new_user.triggered.connect(functools.partial(self.create_page, UserTabDetail))
        self.dlg.new_input.triggered.connect(functools.partial(self.create_page, SalaryTabDetail))
        self.dlg.new_output.triggered.connect(functools.partial(self.create_page, CostTabDetail))
        self.dlg.new_static_output.triggered.connect(functools.partial(self.create_page, StaticCostTabDetail))
        self.dlg.new_installment.triggered.connect(functools.partial(self.create_page, InstallmentTabDetail))
        self.dlg.new_saving.triggered.connect(functools.partial(self.create_page, SaveTabDetail))
        self.dlg.new_debt_credit.triggered.connect(functools.partial(self.create_page, PaymentTabDetail))

    def salary_tab_trigger(self):
        self.dlg.all_input_list.selectionModel().selectionChanged.connect(self.update_salary_tree_filters)

    def update_salary_tree_filters(self, selected, deselected):
        sender_obj = self.dlg.sender()
        indexes = sender_obj.selectedRows()
        if indexes:
            self.update_source_filter_tree(self.dlg.all_input_list, 1, self.dlg.source_filter, indexes)
            self.update_date_filter_tree(self.dlg.all_input_list, 3, self.dlg.date_filter, indexes)


    def update_date_filter_tree(self, qtw_dlg_object, date_column, qtree_dlg_obj, indexes):
        self.set_style_for_qtree_widget(qtree_dlg_obj)
        date_value = qtw_dlg_object.item(indexes[0].row(), date_column)
        georgian_date_value = JDateUtils.convert_to_gregorian(date_value.text())
        filter_result = self.query_handler.filter_salary_with_date(georgian_date_value.year, georgian_date_value.month)
        tree_item = QtWidgets.QTreeWidgetItem(qtree_dlg_obj)
        total_money = 0
        month_name = JDateUtils.get_jmonth_name(date_value.text())
        tree_item.setText(0, month_name)
        for i in filter_result:
            child_item = QtWidgets.QTreeWidgetItem(tree_item)
            jdate = JDateUtils.convert_to_jalali(i[0])
            child_item.setText(0, str(jdate))
            child_item.setText(1, str(i[1]))
            total_money += i[1]

        self.add_q_tree_total_item(qtree_dlg_obj, total_money, 'Green')

    def update_source_filter_tree(self, qtw_dlg_object, date_column, qtree_dlg_obj, indexes):
        self.set_style_for_qtree_widget(qtree_dlg_obj)
        office_name = qtw_dlg_object.item(indexes[0].row(), date_column).text()
        filter_result = self.query_handler.filter_salary_with_source(office_name)
        tree_item = QtWidgets.QTreeWidgetItem(qtree_dlg_obj)
        tree_item.setText(0, office_name)
        total_money = 0

        for i in filter_result:
            child_item = QtWidgets.QTreeWidgetItem(tree_item)
            jdate = JDateUtils.convert_to_jalali(i[0])
            child_item.setText(0, str(jdate))
            child_item.setText(1, str(i[1]))
            total_money += i[1]
        self.add_q_tree_total_item(qtree_dlg_obj, total_money, 'Green')

    def add_q_tree_total_item(self, qtree_obj, total_money, color):
        line_item = QtWidgets.QTreeWidgetItem()
        line_item.setFirstColumnSpanned(True)
        qtree_obj.addTopLevelItem(line_item)
        sum_item = QtWidgets.QTreeWidgetItem(['جمع کل', str(total_money)])
        # self.item_color_styles(sum_item, color)
        qtree_obj.addTopLevelItem(sum_item)

    def set_style_for_qtree_widget(self, qtree_obj):
        delegate = CustomItemDelegate()
        qtree_obj.setItemDelegate(delegate)
        current_style = qtree_obj.styleSheet()
        qtree_obj.clear()
        qtree_obj.setStyleSheet(current_style)
        qtree_obj.header().setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)

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
        self.add_data_to_qtablewidget(self.dlg.all_debtor_list, debtor_list, 'GREEN')

    def update_creditor_tab(self):
        creditor_list = self.query_handler.get_debtor_creditor_list('قرض گرفته شده')
        self.add_data_to_qtablewidget(self.dlg.all_creditor_list, creditor_list, 'RED')

    def update_salary_tab(self):
        salary_list = self.query_handler.get_salary_list()
        self.add_data_to_qtablewidget(self.dlg.all_input_list, salary_list, 'GREEN')

    def update_installment_tab(self):
        installment_list = self.query_handler.get_installment_list()
        self.add_data_to_qtablewidget(self.dlg.all_installment, installment_list, 'RED')

    def update_static_cost_tab(self):
        static_cost_list = self.query_handler.get_static_cost_list()
        self.add_data_to_qtablewidget(self.dlg.all_static_output_list, static_cost_list, 'RED')

    def add_data_to_qtablewidget(self, object_name, data_list, color):
        self.clear_qtable_widget(object_name)
        for each_result in data_list:
            details = self.clear_data_to_insert_qtable_widget(each_result)
            self.add_new_row_to_main_list(object_name, details, color)
        object_name.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        object_name.resizeColumnsToContents()
        object_name.horizontalHeader().setSectionResizeMode(object_name.columnCount() - 1, QtWidgets.QHeaderView.Stretch)

    def add_new_row_to_main_list(self, obj_name, data, color):
        row_position = obj_name.rowCount()
        obj_name.insertRow(row_position)
        for index, each_item in enumerate(data.items(), start=0):
            item = QtWidgets.QTableWidgetItem(str(each_item[1]))
            self.item_color_styles(item, color)
            item.setTextAlignment(Qt.AlignCenter)
            obj_name.setItem(row_position, index, item)

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