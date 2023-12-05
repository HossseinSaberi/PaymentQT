from PyQt5.QtGui import QColor


class TableItemStylingMixin:
    def item_color_styles(self, qtablewidget_obj, color):
        color = self.set_color_by_money_value(qtablewidget_obj, color)
        qtablewidget_obj.setForeground(color)
        return qtablewidget_obj

    @staticmethod
    def set_color_by_money_value(item, color):
        item_value = item.text()
        if ',' in item_value:
            color = QColor(color)
        else:
            color = QColor('BLACK')
        return color


class TabStylingMixin:
    @staticmethod
    def apply_qtab_styles(qtabwidget_obj):
        qtabwidget_obj.setStyleSheet("QTabWidget { background-color: lightblue; }")


class ComboBoxStylingMixin:
    @staticmethod
    def apply_qcombobox_styles(combobox_obj):
        combobox_obj.setStyleSheet("QComboBox { background-color: lightgreen; }")


class ButtonStylingMixin:
    @staticmethod
    def apply_qbutton_styles(button_obj):
        button_obj.setStyleSheet("QPushButton { background-color: lightcoral; }")


class TotalStyleMixin(TableItemStylingMixin, TabStylingMixin, ComboBoxStylingMixin, ButtonStylingMixin):
    pass


class RemainderUtilsMixin:

    @staticmethod
    def get_payment_spin_box_value(total_obj, paied_obj):
        total = total_obj.value()
        paied = paied_obj.value()
        return total, paied

    @staticmethod
    def calculate_remainder(total_obj, paied_obj):
        total, paied = RemainderUtilsMixin.get_payment_spin_box_value(total_obj, paied_obj)
        if paied:
            total = total - paied
        return total

