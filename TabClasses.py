from AccountingDialog import AddNewPaymentDialog, AddNewInstallmentDialog, \
    AddNewSalaryDialog, AddNewStaticDialog, AddNewCostDialog, AddNewSaveMoneyDialog, AddNewUserDialog
from MixinsClass import TotalStyleMixin , RemainderUtilsMixin


class TabDetails(TotalStyleMixin):
    window_instance = _win_inst = None

    def __init__(self, main_page_instance, dialog_instance, query_handler):
        self._dlg_inst = dialog_instance
        self.query_handler = query_handler
        self.main_page_instance = main_page_instance
        self.create_ui()

    def create_ui(self):
        self._win_inst = self.window_instance()
        self._win_inst.setupUi(self._dlg_inst)

    def show_dialog(self):
        self._dlg_inst.exec_()

    @property
    def dlg_inst(self):
        return self._dlg_inst

    @property
    def win_inst(self):
        return self._win_inst

    def check_trigger(self):
        pass

    def initial_form_objects(self, object_name, object_value):
        pass

    def read_form_data(self):
        pass

    @staticmethod
    def add_users_to_users_list_cmb(users_list, qb_object):
        qb_object.clear()
        for each_user in users_list:
            qb_object.addItem(each_user[1], each_user[0])

    def close_dialog(self):
        self._dlg_inst.close()


class SaveTabDetail(TabDetails):
    window_instance = AddNewSaveMoneyDialog

    def __init__(self, main_page_instance, dialog_instance, query_handler):
        super().__init__(main_page_instance, dialog_instance, query_handler)
        self.check_trigger()
        self.show_dialog()

    def check_trigger(self):
        self.win_inst.add_new_save_QB.clicked.connect(self.create_new_save_money)

    def create_new_save_money(self):
        new_save_details = self.read_form_data()
        self.query_handler.insert_new_save(new_save_details)
        self.dlg_inst.close()

    def read_form_data(self):
        new_save_money_details = dict()
        new_save_money_details['save_place'] = self.win_inst.save_place_LE.text()
        new_save_money_details['total_money'] = self.win_inst.total_money_QSB.value()
        new_save_money_details['save_date'] = self.win_inst.date_LE.text()
        new_save_money_details['description'] = self.win_inst.description_TE.toPlainText()
        return new_save_money_details


class CostTabDetail(TabDetails):
    window_instance = AddNewCostDialog

    def __init__(self, main_page_instance, dialog_instance, query_handler):
        super().__init__(main_page_instance, dialog_instance, query_handler)
        self.check_trigger()
        self.show_dialog()

    def check_trigger(self):
        self.win_inst.add_new_cost_QB.clicked.connect(self.create_new_cost)

    def create_new_cost(self):
        new_cost_details = self.read_form_data()
        self.query_handler.insert_new_cost(new_cost_details)
        self.dlg_inst.close()

    def read_form_data(self):
        new_cost_details = dict()
        new_cost_details['subject'] = self.win_inst.cost_subject_LE.text()
        new_cost_details['total_money'] = self.win_inst.total_money_QSB.value()
        new_cost_details['pay_date'] = self.win_inst.date_LE.text()
        new_cost_details['description'] = self.win_inst.description_TE.toPlainText()
        return new_cost_details


class PaymentTabDetail(RemainderUtilsMixin, TabDetails):
    window_instance = AddNewPaymentDialog

    def __init__(self, main_page_instance, dialog_instance, query_handler):
        super().__init__(main_page_instance, dialog_instance, query_handler)
        self.check_trigger()
        self.show_dialog()

    def check_trigger(self):
        self.win_inst.add_new_payment_submit.clicked.connect(self.create_new_payment)

    def create_new_payment(self):
        new_payment_details = self.read_form_data()
        self.query_handler.insert_new_payment(new_payment_details)
        self.dlg_inst.close()

    def show_dialog(self):
        user_list = self.query_handler.get_user_list('شخص')
        self.add_users_to_users_list_cmb(user_list, self.win_inst.user_name_list_CB)
        super().show_dialog()

    def read_form_data(self):
        new_payment_details = dict()
        new_payment_details['user_id'] = self.win_inst.user_name_list_CB.currentData()
        new_payment_details['total_money'] = self.win_inst.total_money_QSB.value()
        new_payment_details['status'] = self.win_inst.status_CB.currentText()
        new_payment_details['paied_money'] = self.win_inst.paied_money_QSB.value()
        new_payment_details['remainder'] = self.calculate_remainder(self.win_inst.total_money_QSB, self.win_inst.paied_money_QSB)
        new_payment_details['description'] = self.win_inst.description_TE.toPlainText()
        return new_payment_details


class InstallmentTabDetail(TabDetails):
    window_instance = AddNewInstallmentDialog

    def __init__(self, main_page_instance, dialog_instance, query_handler):
        super().__init__(main_page_instance, dialog_instance, query_handler)
        self.check_trigger()
        self.show_dialog()

    def check_trigger(self):
        self.win_inst.add_new_installment_QB.clicked.connect(self.create_new_installment)

    def create_new_installment(self):
        new_installment_details = self.read_form_data()
        self.query_handler.insert_new_isntallment(new_installment_details)
        self.dlg_inst.close()

    def show_dialog(self):
        user_list = self.query_handler.get_user_list('موسسه')
        self.add_users_to_users_list_cmb(user_list, self.win_inst.office_name_list_CB)
        self.dlg_inst.exec_()

    def read_form_data(self):
        new_installment_details = dict()
        new_installment_details['office_id'] = self.win_inst.office_name_list_CB.currentData()
        new_installment_details['total_money'] = self.win_inst.total_money_QSB.value()
        new_installment_details['installment'] = self.win_inst.each_installment_QSB.value()
        new_installment_details['description'] = self.win_inst.description_TE.toPlainText()
        new_installment_details['start_date'] = self.win_inst.start_date_LE.text()
        return new_installment_details


class StaticCostTabDetail(TabDetails):
    window_instance = AddNewStaticDialog

    def __init__(self, main_page_instance, dialog_instance, query_handler):
        super().__init__(main_page_instance, dialog_instance, query_handler)
        self.check_trigger()
        self.show_dialog()

    def check_trigger(self):
        self.win_inst.add_new_stastic_cost_QB.clicked.connect(self.create_new_static_cost)

    def create_new_static_cost(self):
        new_static_cost_details = self.read_form_data()
        self.query_handler.insert_new_static_cost(new_static_cost_details)
        self.dlg_inst.close()

    def show_dialog(self):
        user_list = self.query_handler.get_user_list('ثابت')
        self.add_users_to_users_list_cmb(user_list, self.win_inst.user_name_list_CB)
        self.dlg_inst.exec_()

    def read_form_data(self):
        new_static_details = dict()
        new_static_details['subject'] = self.win_inst.cost_subject_LE.text()
        new_static_details['static_user_id'] = self.win_inst.user_name_list_CB.currentData()
        new_static_details['total_money'] = self.win_inst.total_money_QSB.value()
        new_static_details['description'] = self.win_inst.description_TE.toPlainText()
        return new_static_details


class SalaryTabDetail(TabDetails):
    window_instance = AddNewSalaryDialog

    def __init__(self, main_page_instance, dialog_instance, query_handler):
        super().__init__(main_page_instance, dialog_instance, query_handler)
        self.check_trigger()
        self.show_dialog()

    def check_trigger(self):
        self.win_inst.add_new_salary_QB.clicked.connect(self.create_new_salary)

    def create_new_salary(self):
        new_salary_details = self.read_form_data()
        self.query_handler.insert_new_static_cost(new_salary_details)
        self.dlg_inst.close()

    def show_dialog(self):
        user_list = self.query_handler.get_user_list('موسسه')
        self.add_users_to_users_list_cmb(user_list, self.win_inst.office_list_CB)
        self.dlg_inst.exec_()

    def read_form_data(self):
        new_salary_details = dict()
        new_salary_details['office_id'] = self.win_inst.office_list_CB.currentData()
        new_salary_details['total_money'] = self.win_inst.total_money_QSB.value()
        new_salary_details['description'] = self.win_inst.description_TE.toPlainText()
        return new_salary_details


class UserTabDetail(TabDetails):
    window_instance = AddNewUserDialog

    def __init__(self, main_page_instance, dialog_instance, query_handler):
        super().__init__(main_page_instance, dialog_instance, query_handler)
        self.check_trigger()
        self.show_dialog()

    def check_trigger(self):
        self.win_inst.add_new_user_submit.clicked.connect(self.create_new_user)

    def create_new_user(self):
        new_user_details = self.read_form_data()
        self.query_handler.insert_new_user(new_user_details)
        self.dlg_inst.close()

    def read_form_data(self):
        new_user_details = dict()
        new_user_details['name'] = self.win_inst.name_LE.text()
        new_user_details['phone_number'] = self.win_inst.phone_num_LE.text()
        new_user_details['type'] = self.win_inst.user_type.currentText()
        new_user_details['description'] = self.win_inst.description_TE.toPlainText()
        new_user_details['address'] = self.win_inst.address_TE.toPlainText()
        return new_user_details
