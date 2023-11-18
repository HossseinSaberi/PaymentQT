from PyQt5.QtGui import QColor

class TableItemStylingMixin:
    def debtor_creditor_color_styles(self, qtablewidget_obj):
        color = self.set_color_by_money_value(qtablewidget_obj)
        color = QColor(color)
        qtablewidget_obj.setForeground(color)
        return qtablewidget_obj

    @staticmethod
    def set_color_by_money_value(item):
        item_value = item.text()
        if ',' in item_value:
            money_value = int(item_value.replace(',', ''))
            color = 'RED' if money_value < 0 else 'GREEN'
            return color
        return 'BLACK'


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
