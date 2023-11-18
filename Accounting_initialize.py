from Accounting import Account
from PyQt5 import QtWidgets
import sys


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = Account()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
