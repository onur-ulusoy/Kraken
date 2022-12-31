import interface
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sqlite3
import os
import requests
from bs4 import BeautifulSoup
import uiClasses
from uiFunctions import *

if __name__ == "__main__":

    if not is_file_exist("database"):
        os.mkdir("database")

    os.chdir("database")
    app = QtWidgets.QApplication(sys.argv)
    error = False
    if not is_file_exist("MainLectures.db") or not is_file_exist("SecondaryLectures.db"):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText("Program files might be damaged. Please run repair module.")
        msgBox.setWindowTitle("İTÜ Kraken")
        msgBox.setWindowIcon(QtGui.QIcon(":/terminal/windowicon.png"))
        msgBox.show()
        error = True
    elif os.stat("MainLectures.db").st_size < 10000 or os.stat("SecondaryLectures.db").st_size < 10000:
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText("Program files might be damaged. Please run repair module.")
        msgBox.setWindowTitle("İTÜ Kraken")
        msgBox.setWindowIcon(QtGui.QIcon(":/terminal/windowicon.png"))
        msgBox.show()
        error = True

    if not is_file_exist("Preferences.db"):
        create_preferences()

    if not is_file_exist("Gpa.db"):
        create_gpa()

    ui = interface.MainWindow()

    ui.show()

    if not error:
        update_dep_codes(ui)
        update_cap_codes(ui)
        name, name_capitals, department, Gpa, TCredit, Secondary = get_info_from_db()

        index = ui.depCode.findText(department, QtCore.Qt.MatchFixedString)
        if index >= 0:
            ui.depCode.setCurrentIndex(index)
        render_my_lectures(update_my_lectures(ui))
        index = ui.capCode.findText(Secondary.replace("_", "-"), QtCore.Qt.MatchFixedString)
        if index >= 0:
            ui.capCode.setCurrentIndex(index)
        update_my_secondary_lectures(ui)

        ui.name_lineEdit.setText(name)
        ui.name_lineEdit.setMaximumSize(QtCore.QSize(len(name) * 20, 16777215))
        ui.user_icon_label.setText(name_capitals)
        ui.AgButton.setText(name_capitals)
    else:
        ui.depCode.setEnabled(False)
        ui.capCode.setEnabled(False)
        ui.editButton.setEnabled(False)
        ui.okButton.setEnabled(False)
        ui.cancelButton.setEnabled(False)

    ui.depCode.currentIndexChanged.connect(lambda: render_my_lectures(update_my_lectures(ui)))
    ui.capCode.currentIndexChanged.connect(lambda: update_my_secondary_lectures(ui))
    ui.editButton.clicked.connect(lambda: edit_name(ui))
    ui.okButton.clicked.connect(lambda: ok_edit(ui))
    ui.cancelButton.clicked.connect(lambda: cancel_edit(ui))

    ui.user_icon_label.clicked.connect(lambda: open_profile(ui))
    ui.main_menu_button.clicked.connect(lambda: open_main_menu(ui))
    ui.theme1.clicked.connect(lambda: change_theme("1", ui))
    ui.theme2.clicked.connect(lambda: change_theme("2", ui))
    ui.theme3.clicked.connect(lambda: change_theme("3", ui))
    ui.theme4.clicked.connect(lambda: change_theme("4", ui))

    ui.yearComboBox.currentIndexChanged.connect(lambda: fill_secondComboBox(ui))
    ui.listComboBox.currentIndexChanged.connect(lambda: get_calendar(ui))
    ui.comboBox1254.currentIndexChanged.connect(lambda: set_archivedCourseList(ui))
    ui.comboBox1255.currentIndexChanged.connect(lambda: set_archivedCourseList(ui))
    ui.pushButton_2189.clicked.connect(lambda: change_courses_database(ui))
    ui.Color_Button.clicked.connect(lambda: repair(ui))
    ui.label_11.stateChanged.connect(ui.setToolTipStatus)

    ui.TRButton.clicked.connect(lambda: change_language("TR", ui))
    ui.UKButton.clicked.connect(lambda: change_language("EN", ui))
    ui.DEButton.clicked.connect(lambda: change_language("DE", ui))
    for tabButton in ui.tabButtons:
        if tabButton.character == "Profile":
            tabButton.clicked.connect(lambda: open_profile(ui))
        elif tabButton.character == "Home":
            tabButton.clicked.connect(lambda: open_main_menu(ui))
        elif tabButton.character == "LectProgram":
            tabButton.clicked.connect(lambda: open_lecture_program(ui))
        elif tabButton.character == "Calendar":
            tabButton.clicked.connect(lambda: open_calendar(ui))
        elif tabButton.character == "Cafeteria":
            tabButton.clicked.connect(lambda: open_cafeteria(ui))
        elif tabButton.character == "AboutUs":
            tabButton.clicked.connect(lambda: open_aboutus(ui))
        elif tabButton.character == "archive":
            tabButton.clicked.connect(lambda: open_archive(ui))

    ui.op_shortcut = Open()
    for i in ui.shortcutButtons:
        for j in i:
            if j.character == "Profile":
                j.clicked.connect(lambda: open_profile(ui))
            elif j.character == "LectProgram":
                j.clicked.connect(lambda: open_lecture_program(ui))
            elif j.character == "Shortcut":
                j.clicked.connect(lambda: new_shortcut(ui.op_shortcut, ui))
            elif j.character == "Calendar":
                j.clicked.connect(lambda: open_calendar(ui))
            elif j.character == "Cafeteria":
                j.clicked.connect(lambda: open_cafeteria(ui))
            elif j.character == "AboutUs":
                j.clicked.connect(lambda: open_aboutus(ui))
            elif j.character == "archive":
                j.clicked.connect(lambda: open_archive(ui))

    op = Open()
    ui.plusButton.clicked.connect(lambda: open_more_lecture_window(ui.depCode.currentText(), ui, op))

    sys.exit(app.exec_())
