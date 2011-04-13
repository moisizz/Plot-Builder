# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'form.ui'
#
# Created: Wed Apr 13 22:00:43 2011
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(803, 574)
        self.centralWidget = QtGui.QWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralWidget.sizePolicy().hasHeightForWidth())
        self.centralWidget.setSizePolicy(sizePolicy)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.verticalLayoutWidget = QtGui.QWidget(self.centralWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(0, 0, 801, 541))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.plotArea = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.plotArea.setSizeConstraint(QtGui.QLayout.SetMaximumSize)
        self.plotArea.setMargin(0)
        self.plotArea.setObjectName(_fromUtf8("plotArea"))
        MainWindow.setCentralWidget(self.centralWidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 803, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.editMenu = QtGui.QMenu(self.menubar)
        self.editMenu.setObjectName(_fromUtf8("editMenu"))
        MainWindow.setMenuBar(self.menubar)
        self.exitAction = QtGui.QAction(MainWindow)
        self.exitAction.setObjectName(_fromUtf8("exitAction"))
        self.constEditAction = QtGui.QAction(MainWindow)
        self.constEditAction.setObjectName(_fromUtf8("constEditAction"))
        self.calculateAction = QtGui.QAction(MainWindow)
        self.calculateAction.setObjectName(_fromUtf8("calculateAction"))
        self.saveImageAction = QtGui.QAction(MainWindow)
        self.saveImageAction.setObjectName(_fromUtf8("saveImageAction"))
        self.editMenu.addAction(self.calculateAction)
        self.editMenu.addAction(self.saveImageAction)
        self.editMenu.addAction(self.constEditAction)
        self.menubar.addAction(self.editMenu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.exitAction, QtCore.SIGNAL(_fromUtf8("activated()")), MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Осциллятор", None, QtGui.QApplication.UnicodeUTF8))
        self.editMenu.setTitle(QtGui.QApplication.translate("MainWindow", "Правка", None, QtGui.QApplication.UnicodeUTF8))
        self.exitAction.setText(QtGui.QApplication.translate("MainWindow", "Выход", None, QtGui.QApplication.UnicodeUTF8))
        self.constEditAction.setText(QtGui.QApplication.translate("MainWindow", "Константы...", None, QtGui.QApplication.UnicodeUTF8))
        self.calculateAction.setText(QtGui.QApplication.translate("MainWindow", "Просчитать и отобразить", None, QtGui.QApplication.UnicodeUTF8))
        self.saveImageAction.setText(QtGui.QApplication.translate("MainWindow", "Сохранить изображение...", None, QtGui.QApplication.UnicodeUTF8))

