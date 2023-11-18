from datetime import datetime
from AccountingDialog import MainPageDialog, AddNewPaymentDialog, AddNewUserDialog, AddNewInstallmentDialog
from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from DataAccess import Queries, ConnectToDB
from StyleMixins import TotalStyleMixin
from Utils import JDateUtils


class InitialVar:
    def __init__(self):
        self.dlg = self.anp = self.anu = self.asm = self.ani = self.ais = self.asc = self.anc = None
        self.add_payment_win = self.add_user_win = self.add_cost_win = self.add_salary_win = None
        self.add_installment_win = self.add_save_money_win = self.add_static_cost_win = None


class Account(InitialVar, TotalStyleMixin):
    def __init__(self):
        super().__init__()
        self.cdb = ConnectToDB()
        self.query_handler = Queries(db_connection=self.cdb.get_conn())
        self.init_gui()

    def init_gui(self):
        self.create_ui()
        self.check_trigger()
        self.dlg.show()
        self.update_main_window()

    def check_trigger(self):
        self.check_dlg_trigger()
        self.check_anu_trigger()
        self.check_anp_trigger()
        self.check_asm_trigger()
        self.check_ani_trigger()
        self.check_ais_trigger()
        self.check_asc_trigger()
        self.check_anc_trigger()

    def check_dlg_trigger(self):
        self.dlg.new_debt_credit.triggered.connect(self.show_new_pay_page)
        self.dlg.new_user.triggered.connect(self.show_new_user_page)
        self.dlg.new_installment.triggered.connect(self.show_new_installment_page)

    def check_anu_trigger(self):
        if self.anu:
            self.anu.add_new_user_submit.clicked.connect(self.create_new_user)

    def check_asm_trigger(self):
        if self.asm:
            pass

    def check_ani_trigger(self):
        if self.ani:
            self.ani.add_new_installment_QB.clicked.connect(self.create_new_installment)

    def check_ais_trigger(self):
        if self.ais:
            pass

    def check_asc_trigger(self):
        if self.asc:
            pass

    def check_anc_trigger(self):
        if self.anc:
            pass

    def check_anp_trigger(self):
        if self.anp:
            self.anp.add_new_payment_submit.clicked.connect(self.create_new_payment)
            self.anp.total_money_QSB.valueChanged.connect(self.calculate_first_remainder)
            self.anp.paied_money_QSB.valueChanged.connect(self.calculate_payment_remainder)

    def create_ui(self):
        self.create_main_page_dialog()
        self.create_add_new_payment_dialog()
        self.create_add_new_user_dialog()
        self.create_add_new_installment_dialog()

    def create_main_page_dialog(self):
        self.dlg = MainPageDialog()

    def create_add_new_payment_dialog(self):
        self.anp = AddNewPaymentDialog()
        self.add_payment_win = QtWidgets.QDialog()
        self.anp.setupUi(self.add_payment_win)

    def create_add_new_user_dialog(self):
        self.anu = AddNewUserDialog()
        self.add_user_win = QtWidgets.QDialog()
        self.anu.setupUi(self.add_user_win)

    def create_add_new_installment_dialog(self):
        self.ani = AddNewInstallmentDialog()
        self.add_installment_win = QtWidgets.QDialog()
        self.ani.setupUi(self.add_installment_win)

    def create_new_payment(self):
        new_payment_details = self.read_data_from_new_payment_form()
        self.query_handler.insert_new_payment(new_payment_details)
        self.add_payment_win.close()
        self.update_main_window()

    def create_new_installment(self):
        new_installment_details = self.read_data_from_new_installment_form()
        self.query_handler.insert_new_isntallment(new_installment_details)
        self.add_installment_win.close()
        self.update_main_window()


    def create_new_user(self):
        new_user_details = self.read_data_from_new_user_form()
        self.query_handler.insert_new_user(new_user_details)
        self.add_user_win.close()

    def read_data_from_new_user_form(self):
        new_user_details = dict()
        new_user_details['name'] = self.anu.name_LE.text()
        new_user_details['phone_number'] = self.anu.phone_num_LE.text()
        new_user_details['type'] = self.anu.user_type.currentText()
        new_user_details['description'] = self.anu.description_TE.toPlainText()
        new_user_details['address'] = self.anu.address_TE.toPlainText()
        return new_user_details

    def read_data_from_new_installment_form(self):
        new_installment_details = dict()
        new_installment_details['office_id'] = self.ani.office_name_list_CB.currentData()
        new_installment_details['total_money'] = self.ani.total_money_QSB.value()
        new_installment_details['installment'] = self.ani.each_installment_QSB.value()
        new_installment_details['description'] = self.ani.description_TE.toPlainText()
        new_installment_details['start_date'] = self.ani.start_date_LE.text()
        return new_installment_details

    def read_data_from_new_payment_form(self):
        new_payment_details = dict()
        new_payment_details['user_id'] = self.anp.user_name_list_CB.currentData()
        new_payment_details['total_money'] = self.anp.total_money_QSB.value()
        new_payment_details['status'] = self.anp.status_CB.currentText()
        new_payment_details['paied_money'] = self.anp.paied_money_QSB.value()
        new_payment_details['remainder'] = self.anp.remainder_QSB.value()
        new_payment_details['description'] = self.anp.description_TE.toPlainText()
        return new_payment_details

    def show_new_user_page(self):
        self.add_user_win.show()

    def show_new_installment_page(self):
        self.add_installment_win.show()
        user_list = self.query_handler.get_user_list('موسسه')
        self.add_users_to_users_list_cmb(user_list, self.ani.office_name_list_CB)

    def show_new_pay_page(self):
        self.add_payment_win.show()
        user_list = self.query_handler.get_user_list('شخص')
        self.add_users_to_users_list_cmb(user_list, self.anp.user_name_list_CB)

    @staticmethod
    def add_users_to_users_list_cmb(users_list, qb_object):
        qb_object.clear()
        for each_user in users_list:
            qb_object.addItem(each_user[1], each_user[0])

    def add_users_to_users_list_cmb1(self, users_list):
        self.ani.office_name_list_CB.clear()
        for each_user in users_list:
            self.ani.office_name_list_CB.addItem(each_user[1], each_user[0])

    def get_payment_spin_box_value(self):
        total = self.anp.total_money_QSB.value()
        paied = self.anp.paied_money_QSB.value()
        return total, paied

    def calculate_payment_remainder(self):
        total, paied = self.get_payment_spin_box_value()
        remainder_value = total - paied
        self.anp.remainder_QSB.setValue(remainder_value)

    def calculate_first_remainder(self):
        total, paied = self.get_payment_spin_box_value()
        if paied:
            total = total - paied
        self.anp.remainder_QSB.setValue(total)

    def update_main_window(self):
        self.update_debtor_list()
        self.update_creditor_list()
        self.update_installment_list()
        # unchange each tab , that tab update ,

    def update_debtor_list(self):
        result = self.query_handler.get_debtor_creditor_list('قرض داده شده')
        for each_result in result:
            payment_details = self.clear_data_to_insert_qtable_widget(each_result)
            self.add_new_row_to_main_list(self.dlg.all_debtor_list, payment_details, 'GREEN')

    def update_creditor_list(self):
        result = self.query_handler.get_debtor_creditor_list('قرض گرفته شده')
        for each_result in result:
            payment_details = self.clear_data_to_insert_qtable_widget(each_result)
            self.add_new_row_to_main_list(self.dlg.all_creditor_list, payment_details, 'RED')

    def update_installment_list(self):
        result = self.query_handler.get_installment_list()
        for each_result in result:
            installment_details = self.clear_data_to_insert_qtable_widget(each_result)
            self.add_new_row_to_main_list(self.dlg.all_installment, installment_details, 'RED')

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
