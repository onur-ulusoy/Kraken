import interface
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import sqlite3
import os
import requests
from bs4 import BeautifulSoup
import uiClasses
import datetime
import textwrap
import time
import pyperclip
import datetime
import locale
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from shutil import copyfile
import uuid
from google_drive_downloader import GoogleDriveDownloader as gdd
#from email.header import Header


def open_profile(ui):
    ui.frame_2.close()
    ui.frame_6.close()
    ui.frame_542.close()
    ui.scrollArea004.close()
    ui.calendar_table.close()
    ui.scrollArea_1241.close()
    ui.frameAB.close()
    ui.calendarChoseframe.close()
    ui.frame_2943.close()
    ui.scrollArea964.close()

    ui.frame_5.show()
    ui.frame_54.show()
    ui.tabName = "| PROFİL"
    ui.label_top_info_2.setText(ui.translate["| PROFİL"][ui.languageNumber])


def open_main_menu(ui):
    ui.frame_54.close()
    ui.frame_542.close()
    ui.scrollArea004.close()
    ui.calendar_table.close()
    ui.scrollArea_1241.close()
    ui.frameAB.close()
    ui.calendarChoseframe.close()
    ui.frame_2943.close()
    ui.scrollArea964.close()

    ui.frame_5.show()
    ui.frame_2.show()
    ui.frame_6.show()
    ui.tabName = "| ANA SAYFA"
    ui.label_top_info_2.setText(ui.translate["| ANA SAYFA"][ui.languageNumber])


def open_lecture_program(ui):
    ui.frame_54.close()
    ui.frame_2.close()
    ui.frame_6.close()
    ui.frame_5.close()
    ui.calendar_table.close()
    ui.scrollArea_1241.close()
    ui.frameAB.close()
    ui.calendarChoseframe.close()
    ui.frame_2943.close()
    ui.scrollArea964.close()

    ui.frame_542.show()
    ui.tabName = "| DERS PROGRAMI"
    ui.scrollArea004.show()


def open_calendar(ui):
    ui.frame_2.close()
    ui.frame_6.close()
    ui.frame_542.close()
    ui.scrollArea004.close()
    ui.frame_54.close()
    ui.scrollArea_1241.close()
    ui.frameAB.close()
    ui.frame_2943.close()
    ui.scrollArea964.close()

    ui.calendarChoseframe.show()
    ui.frame_5.show()
    ui.calendar_table.show()
    ui.tabName = "| AKD. TAKVİM"
    ui.label_top_info_2.setText(ui.translate["| AKD. TAKVİM"][ui.languageNumber])


def open_cafeteria(ui):
    ui.frame_2.close()
    ui.frame_6.close()
    ui.frame_542.close()
    ui.scrollArea004.close()
    ui.frame_54.close()
    ui.calendar_table.close()
    ui.frameAB.close()
    ui.calendarChoseframe.close()
    ui.frame_2943.close()
    ui.scrollArea964.close()

    ui.scrollArea_1241.show()
    ui.tabName = "| YEMEKHANE"
    ui.label_top_info_2.setText(ui.translate["| YEMEKHANE"][ui.languageNumber])


def open_archive(ui):
    ui.frame_2.close()
    ui.frame_6.close()
    ui.frame_542.close()
    ui.scrollArea004.close()
    ui.frame_54.close()
    ui.calendar_table.close()
    ui.scrollArea_1241.close()
    ui.calendarChoseframe.close()
    ui.frameAB.close()

    ui.frame_2943.show()
    ui.scrollArea964.show()
    ui.tabName = "| DERS ARŞİVİ"
    ui.label_top_info_2.setText(ui.translate["| DERS ARŞİVİ"][ui.languageNumber])


def open_aboutus(ui):
    ui.frame_2.close()
    ui.frame_6.close()
    ui.frame_542.close()
    ui.scrollArea004.close()
    ui.frame_54.close()
    ui.calendar_table.close()
    ui.scrollArea_1241.close()
    ui.calendarChoseframe.close()
    ui.frame_2943.close()
    ui.scrollArea964.close()

    ui.frameAB.show()
    ui.tabName = "| HAKKIMIZDA"
    ui.label_top_info_2.setText(ui.translate["| HAKKIMIZDA"][ui.languageNumber])


def edit_name(ui):
    ui.name_lineEdit.setText("")
    ui.name_lineEdit.setReadOnly(False)
    ui.editButton.close()
    ui.okButton.show()
    ui.cancelButton.show()
    ui.name_lineEdit.setFocus()
    ui.name_lineEdit.setMaximumSize(QtCore.QSize(220, 16777215))


def ok_edit(ui):
    ui.name_lineEdit.setReadOnly(True)
    ui.editButton.show()
    ui.okButton.close()
    ui.cancelButton.close()
    newName = ui.name_lineEdit.text()
    newName = newName.strip(" ")
    ui.name_lineEdit.setMaximumSize(QtCore.QSize(len(newName) * 20, 16777215))
    update_name_to_db(newName, ui)


def cancel_edit(ui):
    name, capitals = get_info_from_db("name")
    ui.name_lineEdit.setText(name)
    ui.name_lineEdit.setReadOnly(True)
    ui.editButton.show()
    ui.okButton.close()
    ui.cancelButton.close()
    ui.name_lineEdit.setMaximumSize(QtCore.QSize(len(name) * 20, 16777215))


def new_shortcut(op, ui):
    if not op.value:
        ns = interface.MoreLectureWindow(op)

        op.value = True
        change_language_ns(ui.languageNumber, ns, ui)

        profil = interface.addShortcutButton(ui, ui.translate["Profil"][ui.languageNumber])
        profil.character = "Profile"
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/user/miniProfile.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        profil.setIconSize(QtCore.QSize(50, 50))
        profil.setIcon(icon3)
        ns.verticalLayout_2.addWidget(profil)

        program = interface.addShortcutButton(ui, ui.translate["Ders Programı"][ui.languageNumber])
        program.character = "LectProgram"
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/user/programMini.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        program.setIconSize(QtCore.QSize(50, 50))
        program.setIcon(icon3)
        ns.verticalLayout_2.addWidget(program)

        yemekhane = interface.addShortcutButton(ui, ui.translate["Yemekhane"][ui.languageNumber])
        yemekhane.character = "Cafeteria"
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/user/cateringMini.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        yemekhane.setIconSize(QtCore.QSize(50, 50))
        yemekhane.setIcon(icon3)
        ns.verticalLayout_2.addWidget(yemekhane)

        takvim = interface.addShortcutButton(ui, ui.translate["Akd. Takvim"][ui.languageNumber])
        takvim.character = "Calendar"
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/user/academicMini.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        takvim.setIconSize(QtCore.QSize(50, 50))
        takvim.setIcon(icon3)
        ns.verticalLayout_2.addWidget(takvim)

        arsiv = interface.addShortcutButton(ui, ui.translate["Ders Arşivi"][ui.languageNumber])
        arsiv.character = "archive"
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/user/archiveMini.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        arsiv.setIconSize(QtCore.QSize(50, 50))
        arsiv.setIcon(icon3)
        ns.verticalLayout_2.addWidget(arsiv)

        aboutus = interface.addShortcutButton(ui, ui.translate["Hakkımızda"][ui.languageNumber])
        aboutus.character = "AboutUs"
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/user/aboutUsMini.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        aboutus.setIconSize(QtCore.QSize(50, 50))
        aboutus.setIcon(icon3)
        ns.verticalLayout_2.addWidget(aboutus)

        profil.open = False
        aboutus.open = False
        yemekhane.open = False
        takvim.open = False
        program.open = False
        arsiv.open = False

        for i in ui.shortcutButtons:
            for j in i:
                if j.character == "Profile":
                    profil.setText(ui.translate["Profil"][ui.languageNumber] + " {}".format(
                        ui.translate["(Kaldır)"][ui.languageNumber]))
                    profil.open = True
                elif j.character == "LectProgram":
                    program.setText(ui.translate["Ders Programı"][ui.languageNumber] + " {}".format(
                        ui.translate["(Kaldır)"][ui.languageNumber]))
                    program.open = True
                elif j.character == "Cafeteria":
                    yemekhane.setText(ui.translate["Yemekhane"][ui.languageNumber] + " {}".format(
                        ui.translate["(Kaldır)"][ui.languageNumber]))
                    yemekhane.open = True
                elif j.character == "Calendar":
                    takvim.setText(ui.translate["Akd. Takvim"][ui.languageNumber] + " {}".format(
                        ui.translate["(Kaldır)"][ui.languageNumber]))
                    takvim.open = True
                elif j.character == "archive":
                    arsiv.setText(ui.translate["Ders Arşivi"][ui.languageNumber] + " {}".format(
                        ui.translate["(Kaldır)"][ui.languageNumber]))
                    arsiv.open = True
                elif j.character == "AboutUs":
                    aboutus.setText(ui.translate["Hakkımızda"][ui.languageNumber] + " {}".format(
                        ui.translate["(Kaldır)"][ui.languageNumber]))
                    aboutus.open = True

        if not profil.open:
            profil.setText(ui.translate["Profil"][ui.languageNumber] + " {}".format(
                ui.translate["(Ekle)"][ui.languageNumber]))

        if not yemekhane.open:
            yemekhane.setText(ui.translate["Yemekhane"][ui.languageNumber] + " {}".format(
                ui.translate["(Ekle)"][ui.languageNumber]))

        if not takvim.open:
            takvim.setText(ui.translate["Akd. Takvim"][ui.languageNumber] + " {}".format(
                ui.translate["(Ekle)"][ui.languageNumber]))

        if not program.open:
            program.setText(ui.translate["Ders Programı"][ui.languageNumber] + " {}".format(
                ui.translate["(Ekle)"][ui.languageNumber]))

        if not arsiv.open:
            arsiv.setText(ui.translate["Ders Arşivi"][ui.languageNumber] + " {}".format(
                ui.translate["(Ekle)"][ui.languageNumber]))

        if not aboutus.open:
            aboutus.setText(ui.translate["Hakkımızda"][ui.languageNumber] + " {}".format(
                ui.translate["(Ekle)"][ui.languageNumber]))

        profil.clicked.connect(lambda: close_open_shortcut(profil, ui))
        yemekhane.clicked.connect(lambda: close_open_shortcut(yemekhane, ui))
        takvim.clicked.connect(lambda: close_open_shortcut(takvim, ui))
        program.clicked.connect(lambda: close_open_shortcut(program, ui))
        arsiv.clicked.connect(lambda: close_open_shortcut(arsiv, ui))
        aboutus.clicked.connect(lambda: close_open_shortcut(aboutus, ui))

        ns.show()

        ui.theme1.clicked.connect(lambda: change_theme_ml("1", ns))
        ui.theme2.clicked.connect(lambda: change_theme_ml("2", ns))
        ui.theme3.clicked.connect(lambda: change_theme_ml("3", ns))
        ui.theme4.clicked.connect(lambda: change_theme_ml("4", ns))

        ui.TRButton.clicked.connect(lambda: change_language_ns(0, ns, ui))
        ui.UKButton.clicked.connect(lambda: change_language_ns(1, ns, ui))
        ui.DEButton.clicked.connect(lambda: change_language_ns(2, ns, ui))


def close_open_shortcut(ns, ui):
    ns.open = not ns.open
    text = str()
    if ns.character == "Profile":
        text = "Profil"
    elif ns.character == "LectProgram":
        text = "Ders Programı"
    elif ns.character == "Calendar":
        text = "Akd. Takvim"
    elif ns.character == "Cafeteria":
        text = "Yemekhane"
    elif ns.character == "archive":
        text = "Ders Arşivi"
    elif ns.character == "AboutUs":
        text = "Hakkımızda"

    if not ns.open:
        ns.setText(ui.translate[text][ui.languageNumber] + " {}".format(
            ui.translate["(Ekle)"][ui.languageNumber]))
        for i in ui.shortcutButtons:
            for j in i:
                if j.character == ns.character:
                    ui.shortcutList.remove(text)
    else:
        ns.setText(ui.translate[text][ui.languageNumber] + " {}".format(
            ui.translate["(Kaldır)"][ui.languageNumber]))
        ui.shortcutList.insert(-1, text)

    ui.shortcutButtons[0] = list()
    ui.shortcutButtons[1] = list()
    ui.shortcutButtons[2] = list()

    (x, y) = (0, 0)

    for i in range(3):
        for j in range(3):
            ui.shortcutButtons[i].append(ui.create_shortcutButton(""))
            ui.gridLayout.addWidget(ui.shortcutButtons[i][j], i, j, 1, 1)

    for i in ui.shortcutList:
        ui.shortcutButtons[x][y] = ui.create_shortcutButton(i)
        ui.shortcutButtons[x][y].location = (x, y)
        ui.gridLayout.addWidget(ui.shortcutButtons[x][y], x, y, 1, 1)

        if y < 2:
            y += 1
        else:
            y = 0
            if x < 2:
                x += 1

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
            elif j.character == "archive":
                j.clicked.connect(lambda: open_archive(ui))
            elif j.character == "AboutUs":
                j.clicked.connect(lambda: open_aboutus(ui))

    con = sqlite3.connect("Preferences.db")
    cursor = con.cursor()
    shortcuts = ",".join(ui.shortcutList)
    cursor.execute("Update Pref set Shortcuts = ?", (shortcuts,))
    con.commit()


def get_years(ui, req=""):
    ui.yearComboBox.clear()

    if req == "":
        if ui.languageNumber == 0:
            url0 = "https://www.sis.itu.edu.tr/TR/ogrenci/akademik-takvim/akademik-takvim.php"
        else:
            url0 = "https://www.sis.itu.edu.tr/EN/student/academic-calendar/academic-calendar.php"

        try:
            ui.url_dict = dict()
            response = requests.get(url0)
            html_content = response.content
            ui.soup0 = BeautifulSoup(html_content, "html.parser")
            p_labels = ui.soup0.find_all("p")
            for i in p_labels:
                a = i.find_all("a")
                for k in a:
                    url9 = k.get("href")
                    name = k.text

                    if ui.languageNumber == 0:
                        if name.find("Takvim") != -1:
                            codee = name[0:10:1].strip(" ")
                            ui.yearComboBox.addItem(codee)
                            ui.url_dict[codee] = url9

                    else:
                        if name.find("Calendar") != -1:
                            codee = name[14:24:1].strip(" ")
                            ui.yearComboBox.addItem(codee)
                            ui.url_dict[codee] = url9

            ui.noInternet = False

        except:
            item = ui.calendar_table.horizontalHeaderItem(0)
            item.setText(ui.translate["Akademik takvimin görüntülenebilmesi için internet bağlantısı gereklidir."][ui.languageNumber])
            ui.noInternet = True
            return 0


def fill_secondComboBox(ui):
    ui.listComboBox.clear()

    try:#if len(ui.yearComboBox.currentText()) != 0:
        ui.dict2 = dict()
        url = ui.url_dict[ui.yearComboBox.currentText()]
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        labels = soup.find("div", {"class": "content-area"}).find_all("a")

        for i in labels:
            ui.listComboBox.addItem(i.text)
            ui.dict2[i.text] = i.get("href")
        get_calendar(ui)
    except:
        pass


def get_calendar(ui, req=""):
    calendar = list()
    ui.noInternet = False
    if req == "":
        try:
            url = ui.dict2[ui.listComboBox.currentText()]
            response = requests.get(url)
            html_content = response.content
            ui.soup1 = BeautifulSoup(html_content, "html.parser")


        except:
            item = ui.calendar_table.horizontalHeaderItem(0)
            item.setText(ui.translate["Akademik takvimin görüntülenebilmesi için internet bağlantısı gereklidir."][ui.languageNumber])
            ui.noInternet = True

            return 0
    if ui.noInternet:
        return 0

    soup = ui.soup1

    spanLabels = soup.find_all("h1")

    for i in spanLabels:
        text = i.text
        text = text.replace("\xa0", "")
        text = text.replace("\r", "")
        text = text.replace("\t", "")
        text = text.replace("\n", "")
        item = ui.calendar_table.horizontalHeaderItem(0)
        item.setText(text)
        break

    tdLabels = soup.find_all("td")
    m = 0
    couple = list()
    gr = False
    for i in tdLabels:

        text = i.text
        text = text.replace("\xa0", "")
        text = text.replace("\r", "")
        text = text.replace("\t", "")
        text = text.replace("\n", "")
        text = text.replace("                                ", "")
        text = text.replace("                                                     ", "")
        text = text.replace("                            ", "")
        text = text.replace("                        ", "")
        text = text.strip()
        #text = text.replace(". ", ".")
        #text = text.replace(") ", ")")
        if len(text) > 120 and m % 2 == 1 and text.find("0") == -1 and text.find("1") == -1:
            couple.append(" ")
            calendar.append(couple)
            couple = list()
            couple.append(text)
            continue
        couple.append(text)

        m += 1
        if m % 2 == 0:
            calendar.append(couple)
            couple = list()

    x = 1
    for i, j in calendar:
        #print(i, j)
        ui.calendar_table.setRowCount(x)
        item1 = QtWidgets.QTableWidgetItem()
        ui.calendar_table.setVerticalHeaderItem(x-1, item1)
        item1 = ui.calendar_table.verticalHeaderItem(x-1)
        if len(j) > 26:
            short = j[0:26] + "..."
            item1.setText(short)
        else:
            item1.setText(j)
        item1.setToolTip(j)

        if i.find(". S") != -1 or i.find(") A") != -1:
            i = "ㅤ" + i

        item = QtWidgets.QTableWidgetItem()
        item.setText(i)

        if len(i) > 220:
            item.setToolTip(i)
        item.setBackground(QtGui.QBrush(QtGui.QColor(200, 200, 200)))
        item.setTextAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)

        ui.calendar_table.setItem(0, x-1, item)
        x += 1

        if j == "DATE" or j == "TARİH" or j == "TARiH":
            item1.setText("")
            item1.setToolTip("")
            item.setForeground(QtGui.QBrush(QtGui.QColor(0, 0, 255)))


def get_date(ui):
    sdate = ui.calendarWidget.selectedDate().getDate()
    date = datetime.date(year=sdate[0], month=sdate[1], day=sdate[2])
    date_str = date.strftime("%d-%m-%y")
    try:
        ui.label_oybg.hide()
        ui.tableWidget_oy.show()
        get_oy(date_str, ui)
    except:
        ui.tableWidget_oy.hide()
        ui.label_oybg.show()
    try:
        ui.label_aybg.hide()
        ui.tableWidget_ay.show()
        get_ay(date_str, ui)
    except:
        ui.tableWidget_ay.hide()
        ui.label_aybg.show()


class y_thread(QtCore.QThread):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
    change_value = QtCore.pyqtSignal(int)

    def run(self):
        try:
            url = "https://sks.itu.edu.tr"
            response = requests.get(url)
            self.ui.intErrorLabel.hide()
        except:
            self.ui.intErrorLabel.show()

        sdate = self.ui.calendarWidget.selectedDate().getDate()

        date = datetime.date(year=sdate[0], month=sdate[1], day=sdate[2])
        date_str = date.strftime("%d-%m-%y")
        try:
            self.ui.label_oybg.hide()
            self.ui.tableWidget_oy.show()
            get_oy(date_str, self.ui)
        except:
            self.ui.tableWidget_oy.hide()
            self.ui.label_oybg.show()
        try:
            self.ui.label_aybg.hide()
            self.ui.tableWidget_ay.show()
            get_ay(date_str, self.ui)
        except:
            self.ui.tableWidget_ay.hide()
            self.ui.label_aybg.show()
        self.change_value.emit(3)

    def get_oy(cdate, ui):
        url = "https://sks.itu.edu.tr/ExternalPages/sks/yemek-menu-v2/uzerinde-calisilan/yemek-menu.aspx?tip=itu-ogle-yemegi-genel&value={}".format(
            cdate)
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        t_top = list(soup.find("table", {"class": "table table-bordered"}).find("tbody").find_all("tr"))
        t_foot = list(soup.find("table", {"class": "table table-bordered"}).find("tfoot").find_all("tr"))

        sa = 0

        ui.tableWidget_oy.setRowCount(len(t_top) + len(t_foot))

        for i in t_top:
            sutun = i.find_all("td")
            item = QtWidgets.QTableWidgetItem(sutun[0].text.strip())
            ui.tableWidget_oy.setItem(sa, 0, item)
            item = QtWidgets.QTableWidgetItem(sutun[1].text.strip())
            ui.tableWidget_oy.setItem(sa, 1, item)
            sa += 1
        for i in t_foot:
            sutun = i.find_all("th")
            item = QtWidgets.QTableWidgetItem(sutun[0].text.strip())
            ui.tableWidget_oy.setItem(sa, 0, item)
            item = QtWidgets.QTableWidgetItem(sutun[1].text.strip())
            ui.tableWidget_oy.setItem(sa, 1, item)
            sa += 1

    def get_ay(cdate, ui):
        url = "https://sks.itu.edu.tr/ExternalPages/sks/yemek-menu-v2/uzerinde-calisilan/yemek-menu.aspx?tip=itu-aksam-yemegi-genel&value={}".format(
            cdate)
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        t_top = list(soup.find("table", {"class": "table table-bordered"}).find("tbody").find_all("tr"))
        t_foot = list(soup.find("table", {"class": "table table-bordered"}).find("tfoot").find_all("tr"))

        sa = 0

        ui.tableWidget_ay.setRowCount(len(t_top) + len(t_foot))

        for i in t_top:
            sutun = i.find_all("td")
            item = QtWidgets.QTableWidgetItem(sutun[0].text.strip())
            ui.tableWidget_ay.setItem(sa, 0, item)
            item = QtWidgets.QTableWidgetItem(sutun[1].text.strip())
            ui.tableWidget_ay.setItem(sa, 1, item)
            sa += 1
        for i in t_foot:
            sutun = i.find_all("th")
            item = QtWidgets.QTableWidgetItem(sutun[0].text.strip())
            ui.tableWidget_ay.setItem(sa, 0, item)
            item = QtWidgets.QTableWidgetItem(sutun[1].text.strip())
            ui.tableWidget_ay.setItem(sa, 1, item)
            sa += 1


def get_oy(cdate, ui):
    url = "https://sks.itu.edu.tr/ExternalPages/sks/yemek-menu-v2/uzerinde-calisilan/yemek-menu.aspx?tip=itu-ogle-yemegi-genel&value={}".format(
        cdate)
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    t_top = list(soup.find("table", {"class": "table table-bordered"}).find("tbody").find_all("tr"))
    t_foot = list(soup.find("table", {"class": "table table-bordered"}).find("tfoot").find_all("tr"))

    sa = 0

    ui.tableWidget_oy.setRowCount(len(t_top) + len(t_foot))

    for i in t_top:
        sutun = i.find_all("td")
        item = QtWidgets.QTableWidgetItem(sutun[0].text.strip())
        ui.tableWidget_oy.setItem(sa, 0, item)
        item = QtWidgets.QTableWidgetItem(sutun[1].text.strip())
        ui.tableWidget_oy.setItem(sa, 1, item)
        sa += 1
    for i in t_foot:
        sutun = i.find_all("th")
        item = QtWidgets.QTableWidgetItem(sutun[0].text.strip())
        ui.tableWidget_oy.setItem(sa, 0, item)
        item = QtWidgets.QTableWidgetItem(sutun[1].text.strip())
        ui.tableWidget_oy.setItem(sa, 1, item)
        sa += 1


def get_ay(cdate, ui):
    url = "https://sks.itu.edu.tr/ExternalPages/sks/yemek-menu-v2/uzerinde-calisilan/yemek-menu.aspx?tip=itu-aksam-yemegi-genel&value={}".format(
        cdate)
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    t_top = list(soup.find("table", {"class": "table table-bordered"}).find("tbody").find_all("tr"))
    t_foot = list(soup.find("table", {"class": "table table-bordered"}).find("tfoot").find_all("tr"))

    sa = 0

    ui.tableWidget_ay.setRowCount(len(t_top) + len(t_foot))

    for i in t_top:
        sutun = i.find_all("td")
        item = QtWidgets.QTableWidgetItem(sutun[0].text.strip())
        ui.tableWidget_ay.setItem(sa, 0, item)
        item = QtWidgets.QTableWidgetItem(sutun[1].text.strip())
        ui.tableWidget_ay.setItem(sa, 1, item)
        sa += 1
    for i in t_foot:
        sutun = i.find_all("th")
        item = QtWidgets.QTableWidgetItem(sutun[0].text.strip())
        ui.tableWidget_ay.setItem(sa, 0, item)
        item = QtWidgets.QTableWidgetItem(sutun[1].text.strip())
        ui.tableWidget_ay.setItem(sa, 1, item)
        sa += 1


def create_gpa():
    con = sqlite3.connect("Gpa.db")
    cursor = con.cursor()
    con2 = sqlite3.connect("MainLectures.db")
    cursor2 = con2.cursor()
    cursor2.execute("SELECT Gpa FROM settings")
    data = cursor2.fetchall()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Gpa (depGpa TEXT, capGpa TEXT)")
    cursor.execute("INSERT INTO Gpa VALUES(?, ?)", (data[0][0], data[0][0]))
    con.commit()

    con.close()


def create_settings():
    con = sqlite3.connect("MainLectures.db")
    cursor = con.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS settings (Name TEXT, Dep TEXT, Gpa TEXT, TotalCredit TEXT, Secondary TEXT)")
    cursor.execute("INSERT INTO settings VALUES('Ad Soyad', 'Bölüm', '0.0', '0.0', 'ÇAP/YANDAL')")
    con.commit()

    con.close()


def download_file(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params={'id': id}, stream = True)
    token = get_confirm_token(response)

    if token:
        params = {'id': id, 'confirm': token}
        response = session.get(URL, params=params, stream = True)

    save_response_content(response, destination)


def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None


def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)


def update_lecture_plans():
    url = "http://www.sis.itu.edu.tr/tr/sistem/fak_bol_kodlari.html"
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    bLabels = soup.find_all("b")
    fak_bol_list = list()
    for i in bLabels:
        i = i.text
        if len(i) == 4 and i[-1] == "M":  ## YANDAL DERSLERİNİ LİSTEYE KATMA
            pass
        else:
            if i == "JDF/GEO":
                i = "GEO"
            fak_bol_list.append(i)

    con = sqlite3.connect("MainLectures.db")
    cursor = con.cursor()

    for i in fak_bol_list:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS {} (Code TEXT, Name TEXT, Credit TEXT, Term TEXT, ZS TEXT, Grade TEXT, MainLesson TEXT, Chosen TEXT)".format(
                i))
        try:
            url = "http://www.sis.itu.edu.tr/tr/dersplan/plan/{}".format(i)
            response = requests.get(url)
            html_content = response.content
            soup = BeautifulSoup(html_content, "html.parser")
            lastProgram = soup.find_all("a", {"title": "Ders Planını Görmek İçin Tıklayınız"})[-1].get("href")
            # print(i, lastProgram)
            url = "http://www.sis.itu.edu.tr/tr/dersplan/plan/{}/{}".format(i, lastProgram)
            response = requests.get(url)
            html_content = response.content
            soup = BeautifulSoup(html_content, "html.parser")
            for k in soup.find_all("table", {"class": "plan"}):

                trList = list(k.find_all("tr"))
                trList.pop(0)
                for t in trList:
                    columns = t.find_all("td")
                    # print(columns[0].text)
                    cursor.execute(
                        "INSERT INTO {} VALUES(?, ?, ?, ?, ?, ?, ?, ?)".format(i),
                        (columns[0].text, columns[1].text, columns[2].text, columns[9].text, columns[8].text, "", "",
                         ""))
                    con.commit()
                    ## Eğer Secmeli Ders ise
                    if columns[8].text == "S":
                        # print("SEÇMELİ DERS")
                        secmeli = columns[1].find().get("href")
                        s_url = "http://www.sis.itu.edu.tr/tr/dersplan/plan/{}/{}".format(i, secmeli)
                        # print(s_url)
                        s_response = requests.get(s_url)
                        s_html_content = s_response.content
                        s_soup = BeautifulSoup(s_html_content, "html.parser")
                        s_trList = list(s_soup.find("table", {"class": "plan"}).find_all("tr"))
                        s_trList.pop(0)
                        for d in s_trList:
                            s_columns = d.find_all("td")
                            # print(columns[0].text)
                            cursor.execute(
                                "INSERT INTO {} VALUES(?, ?, ?, ?, ? ,?, ?, ?)".format(i),
                                (s_columns[0].text, s_columns[1].text, s_columns[2].text, columns[9].text,
                                 columns[8].text,
                                 "", columns[1].text, ""))
                            con.commit()
        except:
            pass
    con.commit()
    con.close()


def update_dep_codes(ui):
    con = sqlite3.connect("MainLectures.db")
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    data = cursor.fetchall()

    departments = list()
    for i in data:
        departments.append(i[0])
    departments.remove("settings")
    for i in departments:
        ui.depCode.addItem(i)


def update_cap_codes(ui):
    con = sqlite3.connect("SecondaryLectures.db")
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    data = cursor.fetchall()

    departments = list()
    for i in data:
        i = list(i)
        i[0] = i[0].replace("_", "-")
        departments.append(i[0])
    for i in departments:
        ui.capCode.addItem(i)


def update_doubleMajor_plans():
    url = "http://www.sis.itu.edu.tr/tr/capprg/"
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    html_list = list()
    for i in soup.find_all("p"):
        for j in i.find_all("a"):
            href = j.get("href")
            if href.find("\\") != -1:
                href = href.replace("\\", "/")
            html_list.append(href)

    for i in html_list:
        url = "http://www.sis.itu.edu.tr/tr/capprg/{}".format(i)
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        for td_label in soup.find_all("td"):
            for a_label in td_label.find_all("a"):
                code = a_label.get("href")
                link = code
                code = code.replace("http://www.sis.itu.edu.tr/tr/capprg/", "")
                code = code.replace("INDEX_", "")
                code = code.replace(".html", "")
                code = code.replace(".htm", "")
                code = code.replace("_201610", "")
                code = code.replace("/", "_")

                con = sqlite3.connect("SecondaryLectures.db")
                cursor = con.cursor()
                cursor.execute(
                    "CREATE TABLE IF NOT EXISTS {} (Code TEXT, Name TEXT, Credit TEXT, ZS TEXT, Grade TEXT, MainLesson TEXT, Chosen TEXT)".format(
                        code))

                if link.find("http") == -1:
                    link = "http://www.sis.itu.edu.tr/tr/capprg/{}".format(link)

                response = requests.get(link)
                html_content = response.content
                soup = BeautifulSoup(html_content, "html.parser")

                link_list = list()
                if link.find("INDEX") != -1:
                    for a_label2 in soup.find_all("a"):
                        link_list.append(a_label2.get("href"))
                else:
                    link_list.append(link)

                # for i in link_list: print(i)
                if link_list != []:
                    url = link_list[-1]

                    if url.find("http") == -1:
                        if link.find("KO") == -1:
                            url = "http://www.sis.itu.edu.tr/tr/capprg/{}".format(url)
                        else:
                            url = "http://www.sis.itu.edu.tr/tr/capprg/KO/{}".format(url)
                    response = requests.get(url)
                    html_content = response.content
                    soup = BeautifulSoup(html_content, "html.parser")
                    ct = 0
                    for tr_label in soup.find_all("tr"):
                        element_list = list()
                        for td_label2 in tr_label.find_all("td"):
                            element = td_label2.text
                            if code.find("KKTC") == -1:
                                element = element.replace("\n", "")

                            if element.find("Leadership") != -1:
                                element = "Ship Management and Leadership"
                            element = element.strip()
                            # element = element.lstrip(" 		")
                            element = element.replace(" 		", " ")
                            element = element.replace("     ", " ")
                            element = element.replace("    ", " ")
                            element = element.replace("*", "")
                            element = element.replace(" 	", " ")
                            element = element.replace(" 	", " ")

                            element_list.append(element)
                            # print(element)
                            ct += 1
                            if ct == 4:
                                ct = 0
                                break

                        try:
                            element_list[3] = element_list[3].replace(",", ".")
                            # print(code, element_list[0], element_list[1], element_list[3], element_list[2])
                            cursor.execute("INSERT INTO {} VALUES(?, ?, ?, ?, ?, ?, ?)".format(code), (
                            element_list[0], element_list[1], element_list[3], element_list[2], "", "", ""))
                            con.commit()
                        except:
                            pass
                    # print("********************************************")


def update_minor_plans():
    minor_list = ["ecn", "eut3", "sbp2", "icm", "pem", "mak2", "iml", "mkne", "mknm2", "mad2", "chz2",
                  "chz_m2", "chz_j2", "pet2", "jef2", "jeo2", "kmm2", "gid", "gem", "kim", "bio2",
                  "fiz2", "fize2", "matt2", "matu2", "uck2", "uzb2", "mto2", "tek", "mut_mi", "mut_ya",
                  "mut_se", "ses_th", "ses_ts", "mtr", "etn", "tho/tho", "tho/bale", "tho/mdans",
                  "tho/adans", "tho/bar", "tho/halay", "tho/horon", "tho/kar_hora", "tho/zeybek",
                  "cab/cab_ki", "calgi/cab_ud", "calgi/cab_fl", "calgi/cab_bag", "calgi/cab_git",
                  "calgi/cab_ka", "cab/cab_komp", "cab/cab_kd", "KKTC/men", "KKTC/mtm", "KKTC/nae"]

    for index in minor_list:
        code = index.replace("2", "")
        code = code.replace("3", "")
        code = code.replace("/", "_")
        code = code.upper()

        con = sqlite3.connect("SecondaryLectures.db")
        cursor = con.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS {} (Code TEXT, Name TEXT, Credit TEXT, Grade TEXT, MainLesson TEXT, Chosen TEXT)".format(
                code))

        url = "http://www.sis.itu.edu.tr/tr/yandalprg/{}.html".format(index)
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        # print(url)
        g = 0
        for tr_labels in soup.find_all("tr"):
            element_list = list()

            for td_labels in tr_labels.find_all("td"):
                element = td_labels.text
                if element.find("KKTC") != -1:
                    element = element.replace("\n", "")

                element = element.strip()
                element = element.replace(" 					", " ")
                element = element.replace(" 		", " ")
                element = element.replace(" 			", " ")
                element = element.replace("  	", " ")
                element = element.replace("				", " ")
                element = element.replace("                 ", " ")
                element = element.replace("*", "")
                element = element.replace(" 	", " ")
                element = element.replace(" 	", " ")
                element_list.append(element)

            if g < 2:
                g += 1
                if minor_list.index(index) > 28:
                    g += 1
            else:
                try:
                    # print(element_list[0], element_list[1], element_list[2])
                    cursor.execute("INSERT INTO {} VALUES(?, ?, ?, ?, ?, ?)".format(code),
                                   (element_list[0], element_list[1], element_list[2], "", "", ""))
                    con.commit()

                except:
                    pass


class repairThread(QtCore.QThread):
    def __init__(self, ui, repairwindow):
        super().__init__()
        self.ui = ui
        self.repairwindow = repairwindow
    change_value = QtCore.pyqtSignal(int)

    def run(self):
        self.ui.Color_Button.setEnabled(False)
        self.ui.depCode.setEnabled(False)
        self.ui.capCode.setEnabled(False)
        self.ui.editButton.setEnabled(False)
        self.ui.okButton.setEnabled(False)
        self.ui.cancelButton.setEnabled(False)
        try:
            """
            if is_file_exist("MainLectures.db"):
                os.remove("MainLectures.db")
            if is_file_exist("SecondaryLectures.db"):
                os.remove("SecondaryLectures.db")
            """

            cnt = 10
            self.change_value.emit(cnt)
            download_file("1qCOWttdOaM0_23fygpYGtcCcH9uqGzYJ", "MainLectures.db")
            if os.stat("Mainlectures.db").st_size < 10000:
                exception(self.repairwindow)
                self.repairwindow.enterbutton.setEnabled(True)
                self.ui.Color_Button.setEnabled(True)
                return

            cnt = 55
            self.change_value.emit(cnt)
            create_settings()
            if is_file_exist("ExtraLectures.db"):
                os.remove("ExtraLectures.db")
            cnt = 60
            self.change_value.emit(cnt)
            download_file("1boUj3FqS8sq_7UgSbnZhidoNN10LWu7L", "SecondaryLectures.db")
            if os.stat("SecondaryLectures.db").st_size < 10000:
                exception(self.repairwindow)
                self.repairwindow.enterbutton.setEnabled(True)
                self.ui.Color_Button.setEnabled(True)
                return

            cnt = 85
            self.change_value.emit(cnt)
            if is_file_exist("Gpa.db"):
                os.remove("Gpa.db")
            create_gpa()
            cnt = 100
            self.change_value.emit(cnt)
            refresh_profile(self.ui)

        except:
            exception(self.repairwindow)

        self.repairwindow.enterbutton.setEnabled(True)
        self.ui.Color_Button.setEnabled(True)


def exception(rw):
    """
    ui.msgBox11 = QtWidgets.QMessageBox()
    ui.msgBox11.setIcon(QtWidgets.QMessageBox.Warning)
    ui.msgBox11.setText(
        "There is no Internet connection or you used repair module too much in a short period. Please try again later.")
    ui.msgBox11.setWindowTitle("An error is occurred")
    ui.msgBox11.setStandardButtons(
        QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
    returnValue = ui.msgBox11.exec()
    print("*1")
    #if returnValue == QtWidgets.QMessageBox.Ok:
        #print("**")
    print("*")
    """

    font = QtGui.QFont()
    font.setPointSize(8)
    font.setFamily("MS Shell Dlg 2")
    rw.repairbutton.setFont(font)
    rw.repairbutton.setText("There is no Internet connection or you used repair module too much in a short period.\nRepair module couldn't work properly. Please try again later.")


def refresh_profile(ui):
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

    ui.depCode.setEnabled(True)
    ui.capCode.setEnabled(True)
    ui.editButton.setEnabled(True)
    ui.okButton.setEnabled(True)
    ui.cancelButton.setEnabled(True)

    ui.total_dep_credit = 0.0
    ui.total_cap_credit = 0.0
    ui.blm_crdt = 0.0
    ui.cap_crdt = 0.0

    con = sqlite3.connect("Gpa.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM Gpa")
    data = cursor.fetchall()
    ui.blmgpa = float(data[0][0])
    ui.capgpa = float(data[0][1])

    if ui.blmgpa == 0.0:
        ui.label_blmort.setText("N/A")
    else:
        ui.label_blmort.setText(str(round(ui.blmgpa, 2)))

    if ui.capgpa == 0.0:
        ui.label_caport.setText("N/A")
    else:
        ui.label_caport.setText(str(round(ui.capgpa, 2)))


def repair(ui):
    ui.rw = RepairWindow(ui)


class RepairWindow(QtWidgets.QWidget):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.setWindowIcon(QtGui.QIcon(":/terminal/windowicon.png"))
        self.setWindowTitle("Kraken Auto Repair")
        self.vl = QtWidgets.QVBoxLayout()
        self.repairbutton = QtWidgets.QPushButton()
        self.enterbutton = QtWidgets.QPushButton()
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setFamily("MS Shell Dlg 2")
        self.repairlabel = QtWidgets.QLabel()
        self.repairlabel.setPixmap(QtGui.QPixmap(":/terminal/repair.png"))
        self.repairlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.repairbutton.setFont(font)
        self.repairbutton.setText("REPAIR")
        self.repairbutton.setMinimumHeight(75)
        self.enterbutton.setFont(font)
        self.enterbutton.setText("CONTINUE")
        self.enterbutton.setMinimumHeight(75)
        self.enterbutton.setEnabled(False)
        self.progressbar = QtWidgets.QProgressBar()
        self.progressbar.setMaximum(100)
        self.progressbar.setStyleSheet("QProgressBar {border: 2px solid grey;border-radius:8px;padding:1px}"
                                       "QProgressBar::chunk {background:rgb(15,200,15)}")
        self.vl.addWidget(self.repairlabel)
        self.vl.addWidget(self.progressbar)
        self.vl.addWidget(self.repairbutton)
        self.vl.addWidget(self.enterbutton)
        self.setLayout(self.vl)
        self.resize(640, 480)
        self.show()
        self.repairbutton.clicked.connect(self.ask_if_sure)
        self.enterbutton.clicked.connect(self.close)

    def ask_if_sure(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Warning)
        msgBox.setText("All profile related data will be reset. Do you want to proceed?")
        msgBox.setWindowTitle("Warning")
        msgBox.setStandardButtons(
            QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        buttony = msgBox.button(QtWidgets.QMessageBox.Ok)
        buttony.setText("Yes")

        # msgBox.buttonClicked.connect(msgButtonClick)

        returnValue = msgBox.exec()

        if returnValue == QtWidgets.QMessageBox.Ok:
            self.startRepair()

    def startRepair(self):
        self.repairbutton.setEnabled(False)
        self.thread = repairThread(self.ui, self)
        self.thread.change_value.connect(self.setRepairProgress)
        self.thread.start()

    def setRepairProgress(self, val):
        self.progressbar.setValue(val)


def update_my_lectures(ui):
    years = [[], [], [], []]  # => [firstYear, secondYear, thirdYear, fourthYear]
    con = sqlite3.connect("MainLectures.db")
    cursor = con.cursor()
    nextTerms = [1, 2]
    total_dep_credit = 0
    ui.blm_crdt = 0.0
    try:
        for k in years:
            cursor.execute("SELECT * FROM {} where Term = ? or Term = ?".format(ui.depCode.currentText()), nextTerms)
            nextTerms[0] += 2
            nextTerms[1] += 2
            lectures = cursor.fetchall()
            ### Secmeli derslerin ANA dersini al zorunlu derslerin de hepsini al
            for i in lectures:
                i = list(i)
                if len(i[0]) > 12:
                    ct = 0
                    previous = ""
                    for l in i[0]:
                        # print(previous, l, previous.isdigit(),l.isalpha(),ct)
                        if previous.isdigit() and l.isalpha():
                            i[0] = i[0][0:ct:1]
                            break
                        previous = l
                        ct += 1
                # print(i[0])
                if i[4] == "S" and i[6] == "":
                    # print("True")

                    s_lectures = []
                    s_lectures.append(i[1])
                    for f in lectures:
                        if f[6] == s_lectures[0]:
                            # print("VAR")
                            # print(f[1])
                            s_lectures.append(f[0] + "  " + f[1])
                    k.append(uiClasses.S_LectureFrame(s_lectures, i[0], i[1], i[2], ui.depCode.currentText(), ui))
                    total_dep_credit += float(k[-1].credit)
                    if k[-1].letterGrade != " ??":
                        ui.blm_crdt += float(k[-1].credit)

                if i[4] == "Z":
                    k.append(uiClasses.LectureFrame(i[0], i[1], i[2], ui.depCode.currentText(), ui, "MainLectures.db"))
                    total_dep_credit += float(k[-1].credit)
                    if k[-1].letterGrade != " ??":
                        ui.blm_crdt += float(k[-1].credit)

    except:
        pass
    # print(ui.depCode.currentText())
    return years, ui, total_dep_credit


def render_my_lectures(pack):
    years = pack[0]
    ui = pack[1]
    total_dep_credit = pack[2]

    for i in reversed(range(ui.verticalLayout_2.count())):
        ui.verticalLayout_2.itemAt(i).widget().deleteLater()
    for i in reversed(range(ui.verticalLayout_10.count())):
        ui.verticalLayout_10.itemAt(i).widget().deleteLater()
    for i in reversed(range(ui.verticalLayout_14.count())):
        ui.verticalLayout_14.itemAt(i).widget().deleteLater()
    for i in reversed(range(ui.verticalLayout_16.count())):
        ui.verticalLayout_16.itemAt(i).widget().deleteLater()
    for i in reversed(range(ui.verticalLayout_28.count())):
        if str(type(ui.verticalLayout_28.itemAt(i).widget())) == "<class 'uiClasses.LectureFrame'>":
            ui.verticalLayout_28.itemAt(i).widget().deleteLater()

    for i in years:
        if i == years[0]:
            for j in i:
                ui.verticalLayout_2.addWidget(j)
        elif i == years[1]:
            for j in i:
                ui.verticalLayout_10.addWidget(j)
        elif i == years[2]:
            for j in i:
                ui.verticalLayout_14.addWidget(j)
        elif i == years[3]:
            for j in i:
                ui.verticalLayout_16.addWidget(j)

    update_dep_to_db(ui.depCode.currentText())
    con = sqlite3.connect("MainLectures.db")
    cursor = con.cursor()
    cursor.execute("Select * From settings")
    data = cursor.fetchall()
    gpa = data[0][2]
    credit = data[0][3]
    ui.total_dep_credit = total_dep_credit
    ui.labelblm_crd.setText(str(round(float(credit), 2)) + "/" + str(round(total_dep_credit, 2)))
    try:
        gpa = float(gpa)
        credit = float(credit)
        if credit == 0.0:
            ui.gpaLabel.setText("N/A")
        else:
            ui.gpaLabel.setText(str(round(gpa, 2)))
    except:
        set_gpa(years, ui)

    if is_file_exist("ExtraLectures.db"):
        try:
            render_extras(ui.depCode.currentText(), ui)

        except:
            pass
    cursor.execute("SELECT TotalCredit FROM settings")
    data = cursor.fetchall()
    if data == [('0.0',)]:
        ui.gpaLabel.setText("N/A")


def update_my_secondary_lectures(ui):
    capCode = ui.capCode.currentText()
    capCode = capCode.replace("-", "_")
    ui.total_cap_credit = 0

    try:
        con = sqlite3.connect("SecondaryLectures.db")
        cursor = con.cursor()
        secondary_lectures = list()

        for i in reversed(range(ui.verticalLayout_22.count())):
            ui.verticalLayout_22.itemAt(i).widget().deleteLater()

        try:
            cursor.execute("SELECT * FROM {} ".format(capCode))
            data = cursor.fetchall()

        except:
            cursor.execute("Update settings set Secondary = ?", (capCode,))
            return None

        k = list()
        for i in data:
            k.append(uiClasses.LectureFrame(i[0], i[1], i[2], capCode, ui, "SecondaryLectures.db"))
            ui.total_cap_credit += float(k[-1].credit)
            if k[-1].letterGrade != " ??":
                ui.cap_crdt += float(k[-1].credit)

        for i in k:
            ui.verticalLayout_22.addWidget(i)
    except:
        pass
    ui.label_capcrd.setText(str(ui.cap_crdt) + "/" + str(round(ui.total_cap_credit, 2)))

    con = sqlite3.connect("MainLectures.db")
    cursor = con.cursor()
    """
    cursor.execute("Select Gpa From settings")
    data = cursor.fetchall()
    gpa = str(data[0])
    if gpa == "('0.0',)":
        ui.gpaLabel.setText("N/A")
    """

    cursor.execute("Update settings set Secondary = ?", (capCode,))
    con.commit()


def set_gpa(years, ui):
    earned = 0
    total = 0
    credit = 0

    for i in years:
        for j in i:
            if j.letterGrade == " AA":
                earned += 4 * float(j.credit)
                total += 4 * float(j.credit)
                credit += float(j.credit)
            elif j.letterGrade == " BA":
                earned += 3.5 * float(j.credit)
                total += 4 * float(j.credit)
                credit += float(j.credit)
            elif j.letterGrade == " BB":
                earned += 3 * float(j.credit)
                total += 4 * float(j.credit)
                credit += float(j.credit)
            elif j.letterGrade == " CB":
                earned += 2.5 * float(j.credit)
                total += 4 * float(j.credit)
                credit += float(j.credit)
            elif j.letterGrade == " CC":
                earned += 2 * float(j.credit)
                total += 4 * float(j.credit)
                credit += float(j.credit)
            elif j.letterGrade == " DC":
                earned += 1.5 * float(j.credit)
                total += 4 * float(j.credit)
                credit += float(j.credit)
            elif j.letterGrade == " DD":
                earned += 1 * float(j.credit)
                total += 4 * float(j.credit)
                credit += float(j.credit)
            elif j.letterGrade == " FF":
                total += 4 * float(j.credit)
                credit += float(j.credit)

    gpa = earned / total
    gpa = gpa * 4
    gpa = round(gpa, 2)
    ui.gpaLabel.setText(str(gpa))
    #print(earned, total, credit)

    con = sqlite3.connect("MainLectures.db")
    cursor = con.cursor()
    cursor.execute("Update settings set Gpa = ?, TotalCredit = ?", (gpa, credit))
    con.commit()


def update_name_to_db(upName, ui):
    con = sqlite3.connect("MainLectures.db")
    cursor = con.cursor()
    cursor.execute("Select Name From settings")
    data = cursor.fetchall()

    for i in data:
        oldName = i[0]

    cursor.execute("Update settings set Name = ? where Name = ?", (upName, oldName))
    con.commit()

    cursor.execute("Select Name From settings")
    data = cursor.fetchall()

    update_name_capitals(data, ui)


def update_dep_to_db(newDep):
    con = sqlite3.connect("MainLectures.db")
    cursor = con.cursor()
    cursor.execute("Select Dep From settings")
    data = cursor.fetchall()

    for i in data:
        oldDep = i[0]

    cursor.execute("Update settings set Dep = ? where Dep = ?", (newDep, oldDep))
    con.commit()


def update_name_capitals(data, ui):
    for i in data:
        name_surname = i[0].split(" ")
        capitals = str()
        for j in name_surname:
            for k in j:
                capitals += k.capitalize()
                break
    ui.user_icon_label.setText(capitals)
    ui.AgButton.setText(capitals)


def get_info_from_db(request=""):
    con = sqlite3.connect("MainLectures.db")
    cursor = con.cursor()

    cursor.execute("Select * From settings")
    data = cursor.fetchall()

    if data != []:
        for i in data:
            name_surname = i[0].split(" ")
            capitals = str()
            for j in name_surname:
                for k in j:
                    capitals += k.capitalize()
                    break
            if request == "name":
                return i[0], capitals
            return i[0], capitals, i[1], i[2], i[3], i[4]
    else:
        cursor.execute("INSERT INTO settings VALUES('Ad Soyad', 'Bölüm', 'Ortalama', 'Toplam Kredi', 'ÇAP/YANDAL')")
        con.commit()
        return "Ad Soyad", "AS", "BÖLÜM KODU", "0.0", "0.0", "ÇAP/YANDAL"


def is_file_exist(fileName):
    for i in os.listdir():
        if i == fileName:
            return True


class Open:
    def __init__(self):
        self.value = False


def open_more_lecture_window(dep, ui, op):
    if not op.value and len(dep) < 6:
        ml = interface.MoreLectureWindow(op)
        change_language_ml(ui.languageNumber, ml, ui)
        ml.show()
        op.value = True

        con = sqlite3.connect("MainLectures.db")
        cursor = con.cursor()

        cursor.execute("Select * From {}".format(dep))
        data = cursor.fetchall()
        for i in data:
            code = i[0]
            name = i[1]
            credit = i[2]
            term = i[3]
            ZS = i[4]
            grade = i[5]
            mainLesson = i[6]
            db = "MainLectures.db"
            if ZS == "S" and len(mainLesson) != 0:
                button = interface.MoreLectureButton(code, name, credit, dep, ui, db)
                ml.verticalLayout_2.addWidget(button)

        ui.theme1.clicked.connect(lambda: change_theme_ml("1", ml))
        ui.theme2.clicked.connect(lambda: change_theme_ml("2", ml))
        ui.theme3.clicked.connect(lambda: change_theme_ml("3", ml))
        ui.theme4.clicked.connect(lambda: change_theme_ml("4", ml))

        ui.TRButton.clicked.connect(lambda: change_language_ml(0, ml, ui))
        ui.UKButton.clicked.connect(lambda: change_language_ml(1, ml, ui))
        ui.DEButton.clicked.connect(lambda: change_language_ml(2, ml, ui))


def change_theme_ml(number, ml):
    if number == "1":
        ml.primer_color = (27, 29, 35)
        ml.hover = (33, 37, 43)
        ml.pressed = (85, 170, 255)
        ml.pressed2 = (85, 170, 255)
        ml.seconder_color = (39, 44, 54)
        ml.seconder_color2 = (39, 44, 54)
        ml.text_color = (255, 255, 255)
        ml.text_color2 = (255, 255, 255)
        ml.info_color = (98, 103, 111)
        ml.tab_background = (50, 52, 57, 1)
        ml.selected = (50, 52, 57, 1)
        ml.tab_min_background = (95, 97, 101, 1)
        ml.scrollprimer = (95, 97, 101, 1)
        ml.scrollseconder = (50, 52, 57, 1)
        ml.hover2 = (52, 59, 72)
        ml.hover3 = (33, 37, 43)
        ml.adl = (255, 255, 255, 100)
        ml.adlhover = (255, 255, 255, 150)
        ml.border = "none"

    elif number == "2":
        ml.primer_color = (9, 21, 64)
        ml.hover = (20, 32, 75)
        ml.hover2 = (20, 32, 75)
        ml.hover3 = (20, 32, 140, 125)
        ml.pressed = (19, 30, 95)
        ml.pressed2 = (9, 21, 100, 200)
        ml.seconder_color = (166, 182, 242)
        ml.seconder_color2 = (9, 21, 64)
        ml.text_color = (255, 255, 255)
        ml.text_color2 = (9, 21, 64)
        ml.info_color = (98, 103, 155)
        ml.tab_background = (140, 150, 220, 1)
        ml.selected = (90, 90, 220, 1)
        ml.tab_min_background = (120, 120, 220, 1)
        ml.scrollprimer = (120, 120, 220, 1)
        ml.scrollseconder = (90, 90, 220, 1)
        ml.adl = (255, 255, 255, 100)
        ml.adlhover = (255, 255, 255, 150)
        ml.border = "none"

    elif number == "3":
        ml.primer_color = (87, 15, 22)
        ml.hover = (95, 32, 35)
        ml.hover2 = (95, 32, 35)
        ml.hover3 = (95, 32, 35, 125)
        ml.pressed = (105, 40, 45)
        ml.pressed2 = (110, 45, 50, 200)
        ml.seconder_color = (212, 223, 199)
        ml.seconder_color2 = (87, 15, 22)
        ml.text_color = (255, 255, 255)
        ml.text_color2 = (87, 15, 22)
        ml.info_color = (98, 22, 27)
        ml.tab_background = (140, 62, 75, 1)
        ml.selected = (180, 25, 35, 1)
        ml.tab_min_background = (130, 52, 65, 1)
        ml.scrollprimer = (130, 52, 65, 1)
        ml.scrollseconder = (180, 25, 35, 1)
        ml.adl = (255, 255, 255, 100)
        ml.adlhover = (255, 255, 255, 150)
        ml.border = "none"

    elif number == "4":
        ml.primer_color = (0, 200, 153)
        ml.hover = (8, 217, 166)
        ml.hover2 = (8, 217, 166)
        ml.hover3 = (8, 217, 166, 125)
        ml.pressed = (18, 227, 176)
        ml.pressed2 = (23, 232, 181, 200)
        ml.seconder_color = (255, 255, 255)
        ml.seconder_color2 = (0, 200, 153)
        ml.text_color = (255, 255, 255)
        ml.text_color2 = (0, 0, 0)
        ml.info_color = (0, 0, 0)
        ml.tab_background = (0, 160, 123, 1)
        ml.selected = (40, 123, 83, 1)
        ml.tab_min_background = (0, 150, 113, 1)
        ml.scrollprimer = (0, 150, 113, 1)
        ml.scrollseconder = (40, 123, 83, 1)
        ml.adl = (0, 200, 153, 100)
        ml.adlhover = (0, 200, 153, 150)
        ml.border = "2px solid black"

    ml.change_theme()


def change_language_ml(number, ml, ui):
    ml.top_label.setText(ui.translate["Ekstra ders ekle"][number])


def change_language_ns(number, ml, ui):
    ml.top_label.setText(ui.translate["Kısayol Ekle/Çıkar"][number])
    for i in reversed(range(ml.verticalLayout_2.count())):
        if ml.verticalLayout_2.itemAt(i).widget().character == "Profile":
            if not ml.verticalLayout_2.itemAt(i).widget().open:
                ml.verticalLayout_2.itemAt(i).widget().setText(ui.translate["Profil"][ui.languageNumber] + " {}".format(
                    ui.translate["(Ekle)"][ui.languageNumber]))
            else:
                ml.verticalLayout_2.itemAt(i).widget().setText(ui.translate["Profil"][ui.languageNumber] + " {}".format(
                    ui.translate["(Kaldır)"][ui.languageNumber]))

        elif ml.verticalLayout_2.itemAt(i).widget().character == "LectProgram":
            if not ml.verticalLayout_2.itemAt(i).widget().open:
                ml.verticalLayout_2.itemAt(i).widget().setText(ui.translate["Ders Programı"][ui.languageNumber] + " {}".format(
                    ui.translate["(Ekle)"][ui.languageNumber]))
            else:
                ml.verticalLayout_2.itemAt(i).widget().setText(ui.translate["Ders Programı"][ui.languageNumber] + " {}".format(
                    ui.translate["(Kaldır)"][ui.languageNumber]))

        elif ml.verticalLayout_2.itemAt(i).widget().character == "Cafeteria":
            if not ml.verticalLayout_2.itemAt(i).widget().open:
                ml.verticalLayout_2.itemAt(i).widget().setText(
                    ui.translate["Yemekhane"][ui.languageNumber] + " {}".format(
                        ui.translate["(Ekle)"][ui.languageNumber]))
            else:
                ml.verticalLayout_2.itemAt(i).widget().setText(
                    ui.translate["Yemekhane"][ui.languageNumber] + " {}".format(
                        ui.translate["(Kaldır)"][ui.languageNumber]))

        elif ml.verticalLayout_2.itemAt(i).widget().character == "Calendar":
            if not ml.verticalLayout_2.itemAt(i).widget().open:
                ml.verticalLayout_2.itemAt(i).widget().setText(
                    ui.translate["Akd. Takvim"][ui.languageNumber] + " {}".format(
                        ui.translate["(Ekle)"][ui.languageNumber]))
            else:
                ml.verticalLayout_2.itemAt(i).widget().setText(
                    ui.translate["Akd. Takvim"][ui.languageNumber] + " {}".format(
                        ui.translate["(Kaldır)"][ui.languageNumber]))
        elif ml.verticalLayout_2.itemAt(i).widget().character == "AboutUs":
            if not ml.verticalLayout_2.itemAt(i).widget().open:
                ml.verticalLayout_2.itemAt(i).widget().setText(
                    ui.translate["Hakkımızda"][ui.languageNumber] + " {}".format(
                        ui.translate["(Ekle)"][ui.languageNumber]))
            else:
                ml.verticalLayout_2.itemAt(i).widget().setText(
                    ui.translate["Hakkımızda"][ui.languageNumber] + " {}".format(
                        ui.translate["(Kaldır)"][ui.languageNumber]))


def render_extras(dep, ui):
    con = sqlite3.connect("ExtraLectures.db")
    cursor = con.cursor()

    cursor.execute("Select * From {}".format(dep))
    data = cursor.fetchall()
    for i in data:
        if i[-1] != "":
            ui.blm_crdt += float(i[-2])
        #print(i)
        code = i[0]
        name = i[1]
        credit = i[2]
        grade = i[3]
        extra_lecture = uiClasses.LectureFrame(code, name, credit, dep, ui, "ExtraLectures.db", 1)
        #closeButton = QtWidgets.QPushButton()
        extra_lecture.cButton.setStyleSheet("QPushButton {\n"
                                  "border-radius:15px;\n"
                                  "background-color: transparent;\n"
                                  "image: url(:/menu/exit.png);\n}"
                                  "QPushButton:hover {\n"
                                  "background-color: rgb(52, 59, 72, 150)\n;}"
                                  "QPushButton:pressed {\n"
                                  "background-color: rgb(85, 170, 255)\n;}")
        extra_lecture.cButton.setMinimumWidth(30)
        extra_lecture.cButton.setMinimumHeight(30)
        #extra_lecture.horizontalLayout_5.addWidget(extra_lecture.cButton)

        #closeButton.clicked.connect(lambda: close_extra_lecture(extra_lecture, dep))
        #closeButton.clicked.connect(lambda: close_extra_lecture(extra_lecture, dep))
        ui.verticalLayout_28.insertWidget(0, extra_lecture)


def get_courses(ui):
    ui.regen.setEnabled(False)

    if is_file_exist("Courses.db"):
        os.remove("Courses.db")

    def convert_hours(time):
        time = time.replace("29", "30")
        time = time.replace("59", "00")

        r = time.split("/")

        sh = textwrap.wrap(r[0], 2)[0][1:2] if textwrap.wrap(r[0], 2)[0][0] == "0" else textwrap.wrap(r[0], 2)[0]
        sm = textwrap.wrap(r[0], 2)[1]

        eh = textwrap.wrap(r[1], 2)[0]
        em = textwrap.wrap(r[1], 2)[1]

        s = datetime.timedelta(hours=int(sh), minutes=int(sm))
        a = datetime.timedelta(hours=0, minutes=30)  # sabit
        list = []
        while s != datetime.timedelta(hours=int(eh), minutes=int(em)):
            b = []
            b.append(str(s)[:-3])
            s += a
            b.append(str(s)[0:-3])
            list.append(b)

        for i in range(len(list)):
            if list[i] == ['8:30', '9:00']:
                list[i] = 1
            elif list[i] == ['9:00', '9:30']:
                list[i] = 2
            elif list[i] == ['9:30', '10:00']:
                list[i] = 3
            elif list[i] == ['10:00', '10:30']:
                list[i] = 4
            elif list[i] == ['10:30', '11:00']:
                list[i] = 5
            elif list[i] == ['11:00', '11:30']:
                list[i] = 6
            elif list[i] == ['11:30', '12:00']:
                list[i] = 7
            elif list[i] == ['12:00', '12:30']:
                list[i] = 8
            elif list[i] == ['12:30', '13:00']:
                list[i] = 9
            elif list[i] == ['13:00', '13:30']:
                list[i] = 10
            elif list[i] == ['13:30', '14:00']:
                list[i] = 11
            elif list[i] == ['14:00', '14:30']:
                list[i] = 12
            elif list[i] == ['14:30', '15:00']:
                list[i] = 13
            elif list[i] == ['15:00', '15:30']:
                list[i] = 14
            elif list[i] == ['15:30', '16:00']:
                list[i] = 15
            elif list[i] == ['16:00', '16:30']:
                list[i] = 16
            elif list[i] == ['16:30', '17:00']:
                list[i] = 17
            elif list[i] == ['17:00', '17:30']:
                list[i] = 18
            elif list[i] == ['17:30', '18:00']:
                list[i] = 19
            elif list[i] == ['18:00', '18:30']:
                list[i] = 20
            elif list[i] == ['18:30', '19:00']:
                list[i] = 21
            elif list[i] == ['19:00', '19:30']:
                list[i] = 22
            elif list[i] == ['19:30', '20:00']:
                list[i] = 23
            elif list[i] == ['20:00', '20:30']:
                list[i] = 24
            elif list[i] == ['20:30', '21:00']:
                list[i] = 25
            elif list[i] == ['21:00', '21:30']:
                list[i] = 26
            else:
                list[i] = 0

        return list

    url = "http://www.sis.itu.edu.tr/tr/ders_programlari/LSprogramlar/prg.php"
    response = requests.get(url)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    course_codes = []
    for i in soup.find_all("option"):
        course_codes.append(i.get("value"))
    course_codes.pop(0)
    #print(course_codes)
    ##### BOLUM KODLARI CEKILDI
    for course in course_codes:
        #print(course)
        ui.update_label.setText("{} güncellendi.".format(course))

        con = sqlite3.connect("Courses.db")
        cursor = con.cursor()
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS {} (CRN TEXT, CourseCode TEXT, CourseTitle TEXT, Instructor TEXT, Building TEXT, Day TEXT, Time TEXT, Room TEXT, Capacity TEXT, Enrolled TEXT, Reservation TEXT, MajorRestriction TEXT, Prerequisites TEXT, ClassRestriction TEXT, GVS TEXT)".format(
                course))

        url = "http://www.sis.itu.edu.tr/tr/ders_programlari/LSprogramlar/prg.php?fb={}".format(course)
        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        table = soup.find("table", {"class": "dersprg"}).find_all("tr")
        for tr in table[2:]:
            td = tr.find_all("td")   # Satırdaki sutunların listesi

            gvs = td[5].text + td[6].text

            if len(td[5].text.strip().split(" ")) == 1:
                if td[5].text.strip() == "Pazartesi":
                    td[5] = [1]
                elif td[5].text.strip() == "Salı":
                    td[5] = [2]
                elif td[5].text.strip() == "Çarşamba":
                    td[5] = [3]
                elif td[5].text.strip() == "Perşembe":
                    td[5] = [4]
                elif td[5].text.strip() == "Cuma":
                    td[5] = [5]
                else:
                    td[5] = 0
            else:
                ntd = []
                for day in td[5].text.strip().split(" "):
                    if day == "Pazartesi":
                        ntd.append(1)
                    elif day == "Salı":
                        ntd.append(2)
                    elif day == "Çarşamba":
                        ntd.append(3)
                    elif day == "Perşembe":
                        ntd.append(4)
                    elif day == "Cuma":
                        ntd.append(5)
                    else:
                        ntd.append(0)
                td[5] = ntd

            if td[6].text.strip() == "/":
                td[6] = [0]

            elif td[6].text.strip() == "----":
                td[6] = [0]

            elif len(td[6].text.strip().split(" ")) == 1:
                td[6] = convert_hours(td[6].text.strip())
            else:
                ntd = []
                for hour in td[6].text.strip().split(" "):
                    ntd.append(convert_hours(hour))
                td[6] = ntd

            cursor.execute("INSERT INTO {} VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(course), (
                td[0].text, td[1].text, td[2].text, td[3].text, td[4].text, str(td[5]), str(td[6]), td[7].text,
                td[8].text, td[9].text, td[10].text, td[11].text, td[12].text, td[13].text, gvs))
            con.commit()
    #print("DERSLER EKLENDİ")
    ui.regen.setEnabled(True)


def create_preferences():
    con = sqlite3.connect("Preferences.db")
    cursor = con.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS pref (Theme TEXT, Language TEXT, Shortcuts TEXT, Tooltip)")
    cursor.execute("INSERT INTO pref VALUES('1', 'TR', 'Profil,Ders Programı,Yemekhane,Akd. Takvim,Ders Arşivi,Yeni Kısayol', 'True')")
    con.commit()

    con.close()


def change_language(language, ui):
    con = sqlite3.connect("Preferences.db")
    cursor = con.cursor()

    cursor.execute("Update pref set Language = ?", (language,))
    con.commit()

    con.close()

    if language == "TR":
        ui.languageNumber = 0
        ui.TRButton.setStyleSheet("QPushButton {\n"
                                    "    background-position: center;\n"
                                    "    background-repeat: no-reperat;\n"
                                    "    image:url(:/flag/tr-flagIcon.png);\n"
                                    "    border : 4px solid white;\n"
                                    "    border-radius:19px;\n"
                                    "}")
        ui.TRButton.setEnabled(False)
        ui.UKButton.setEnabled(True)
        ui.DEButton.setEnabled(True)
        ui.UKButton.setStyleSheet("QPushButton {\n"
                                    "    background-position: center;\n"
                                    "    background-repeat: no-reperat;\n"
                                    "    image:url(:/flag/uk-flagIcon.png);\n"
                                    "    border : 4px solid transparent;\n"
                                    "    border-radius:19px;\n"
                                    "}\n"
                                    "QPushButton:hover{\n"
                                    "    border : 4px solid white;\n"
                                    "    border-radius:19px;\n"
                                    "}\n"
                                    "QPushButton:pressed {    \n"
                                    "    background-color: rgb" + str(ui.pressed) + ";\n"
                                    "}")
        ui.DEButton.setStyleSheet("QPushButton {\n"
                                    "    background-position: center;\n"
                                    "    background-repeat: no-reperat;\n"
                                    "    image:url(:/flag/de-flagIcon.png);\n"
                                    "    border : 4px solid transparent;\n"
                                    "    border-radius:19px;\n"
                                    "}\n"
                                    "QPushButton:hover{\n"
                                    "    border : 4px solid white;\n"
                                    "    border-radius:19px;\n"
                                    "}\n"
                                    "QPushButton:pressed {    \n"
                                    "    background-color: rgb" + str(ui.pressed) + ";\n"
                                    "}")

    elif language == "EN":
        ui.languageNumber = 1
        ui.UKButton.setStyleSheet("QPushButton {\n"
                                  "    background-position: center;\n"
                                  "    background-repeat: no-reperat;\n"
                                  "    image:url(:/flag/uk-flagIcon.png);\n"
                                  "    border : 4px solid white;\n"
                                  "    border-radius:19px;\n"
                                  "}")
        ui.UKButton.setEnabled(False)
        ui.TRButton.setEnabled(True)
        ui.DEButton.setEnabled(True)
        ui.TRButton.setStyleSheet("QPushButton {\n"
                                  "    background-position: center;\n"
                                  "    background-repeat: no-reperat;\n"
                                  "    image:url(:/flag/tr-flagIcon.png);\n"
                                  "    border : 4px solid transparent;\n"
                                  "    border-radius:19px;\n"
                                  "}\n"
                                  "QPushButton:hover{\n"
                                  "    border : 4px solid white;\n"
                                  "    border-radius:19px;\n"
                                  "}\n"
                                  "QPushButton:pressed {    \n"
                                  "    background-color: rgb" + str(ui.pressed) + ";\n"
                                                                                  "}")
        ui.DEButton.setStyleSheet("QPushButton {\n"
                                  "    background-position: center;\n"
                                  "    background-repeat: no-reperat;\n"
                                  "    image:url(:/flag/de-flagIcon.png);\n"
                                  "    border : 4px solid transparent;\n"
                                  "    border-radius:19px;\n"
                                  "}\n"
                                  "QPushButton:hover{\n"
                                  "    border : 4px solid white;\n"
                                  "    border-radius:19px;\n"
                                  "}\n"
                                  "QPushButton:pressed {    \n"
                                  "    background-color: rgb" + str(ui.pressed) + ";\n"
                                                                                  "}")
    elif language == "DE":
        ui.languageNumber = 2
        ui.DEButton.setStyleSheet("QPushButton {\n"
                                  "    background-position: center;\n"
                                  "    background-repeat: no-reperat;\n"
                                  "    image:url(:/flag/de-flagIcon.png);\n"
                                  "    border : 4px solid white;\n"
                                  "    border-radius:19px;\n"
                                  "}")
        ui.DEButton.setEnabled(False)
        ui.UKButton.setEnabled(True)
        ui.TRButton.setEnabled(True)
        ui.UKButton.setStyleSheet("QPushButton {\n"
                                  "    background-position: center;\n"
                                  "    background-repeat: no-reperat;\n"
                                  "    image:url(:/flag/uk-flagIcon.png);\n"
                                  "    border : 4px solid transparent;\n"
                                  "    border-radius:19px;\n"
                                  "}\n"
                                  "QPushButton:hover{\n"
                                  "    border : 4px solid white;\n"
                                  "    border-radius:19px;\n"
                                  "}\n"
                                  "QPushButton:pressed {    \n"
                                  "    background-color: rgb" + str(ui.pressed) + ";\n"
                                                                                  "}")
        ui.TRButton.setStyleSheet("QPushButton {\n"
                                  "    background-position: center;\n"
                                  "    background-repeat: no-reperat;\n"
                                  "    image:url(:/flag/tr-flagIcon.png);\n"
                                  "    border : 4px solid transparent;\n"
                                  "    border-radius:19px;\n"
                                  "}\n"
                                  "QPushButton:hover{\n"
                                  "    border : 4px solid white;\n"
                                  "    border-radius:19px;\n"
                                  "}\n"
                                  "QPushButton:pressed {    \n"
                                  "    background-color: rgb" + str(ui.pressed) + ";\n"
                                                                                  "}")

    ui.retranslateUi()

    for tabButton in ui.tabButtons:
        text = ui.translate[tabButton.origin][ui.languageNumber]
        tabButton.setText(text)

    for i in ui.shortcutButtons:
        for shortcutButton in i:
            if len(shortcutButton.origin) != 0:
                text = ui.translate[shortcutButton.origin][ui.languageNumber]
                shortcutButton.setText("\n" + "\n" + "\n" + text)

    for i in reversed(range(ui.verticalLayout_002.count())):
        if str(ui.verticalLayout_002.itemAt(i).widget()).find("OpenLecture") != -1:
            ui.verticalLayout_002.itemAt(i).widget().comboBox_103.setItemText(0, ui.translate["BÖLÜM"][ui.languageNumber])
            ui.verticalLayout_002.itemAt(i).widget().comboBox_104.setItemText(0, ui.translate["DERS ADI"][ui.languageNumber])
            ui.verticalLayout_002.itemAt(i).widget().comboBox_105.setItemText(0, ui.translate["SEÇİLEN DERS"][ui.languageNumber])

    get_years(ui)
    fill_secondComboBox(ui)
    get_calendar(ui, "")


def change_theme(number, ui):
    con = sqlite3.connect("Preferences.db")
    cursor = con.cursor()

    cursor.execute("Update pref set Theme = ?", (number,))
    con.commit()

    con.close()

    if number == "1":
        ui.primer_color = (27, 29, 35)
        ui.hover = (33, 37, 43)
        ui.pressed = (85, 170, 255)
        ui.pressed2 = (85, 170, 255)
        ui.seconder_color = (39, 44, 54)
        ui.seconder_color2 = (44, 49, 60)
        ui.text_color = (255, 255, 255)
        ui.text_color2 = (255, 255, 255)
        ui.info_color = (98, 103, 111)
        ui.tab_background = (50, 52, 57, 1)
        ui.selected = (50, 52, 57, 1)
        ui.tab_min_background = (95, 97, 101, 1)
        ui.scrollprimer = (95, 97, 101, 1)
        ui.scrollseconder = (50, 52, 57, 1)
        ui.hover2 = (52, 59, 72)
        ui.hover3 = (33, 37, 43)
        ui.hover4 = (200,200,200,50)
        ui.adl = (255, 255, 255, 100)
        ui.adlhover = (255, 255, 255, 150)
        ui.border = "none"
        ui.exit = "exit.png"
        ui.plusbutton = "plus.png"
        ui.editbutton_img = "edit.png"
        ui.cancelbutton_img = "cancel.png"
        ui.okbutton_img = "ok.png"
        ui.AgBorderColor = (255, 255, 255)
        ui.theme1.setEnabled(False)
        ui.theme2.setEnabled(True)
        ui.theme3.setEnabled(True)
        ui.theme4.setEnabled(True)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/user/tick.png"), QtGui.QIcon.Disabled,
                        QtGui.QIcon.Off)
        ui.theme1.setIcon(icon)
        ui.theme2.setIcon(QtGui.QIcon())
        ui.theme3.setIcon(QtGui.QIcon())
        ui.theme4.setIcon(QtGui.QIcon())

        ui.paletteOpacity = (255, 255, 255, 50)
        ui.alternete = ui.hover3


    elif number == "2":
        ui.primer_color = (9, 21, 64)
        ui.hover = (20, 32, 75)
        ui.hover2 = (20, 32, 75)
        ui.hover3 = (20, 32, 140, 125)
        ui.pressed = (19, 30, 95)
        ui.pressed2 = (9, 21, 100, 200)
        ui.seconder_color = (166, 182, 242)
        ui.seconder_color2 = (9, 21, 64)
        ui.text_color = (255, 255, 255)
        ui.text_color2 = (9, 21, 64)
        ui.info_color = (98, 103, 155)
        ui.tab_background = (140, 150, 220, 1)
        ui.selected = (90, 90, 220, 1)
        ui.tab_min_background = (120, 120, 220, 1)
        ui.scrollprimer = (120, 120, 220, 1)
        ui.scrollseconder = (220, 220, 255, 1)
        ui.adl = (255, 255, 255, 100)
        ui.adlhover = (255, 255, 255, 150)
        ui.hover4 = ui.adlhover
        ui.border = "none"
        ui.exit = "exit.png"
        ui.plusbutton = "plus_blue.png"
        ui.editbutton_img = "edit.png"
        ui.cancelbutton_img = "cancel.png"
        ui.okbutton_img = "ok.png"
        ui.AgBorderColor = (255, 255, 255)
        ui.theme2.setEnabled(False)
        ui.theme1.setEnabled(True)
        ui.theme3.setEnabled(True)
        ui.theme4.setEnabled(True)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/user/tick_dark.png"), QtGui.QIcon.Disabled,
                       QtGui.QIcon.Off)
        ui.theme2.setIcon(icon)
        ui.theme1.setIcon(QtGui.QIcon())
        ui.theme3.setIcon(QtGui.QIcon())
        ui.theme4.setIcon(QtGui.QIcon())

        ui.paletteOpacity = (255, 255, 255, 50)
        ui.alternete = ui.adlhover

    elif number == "3":
        ui.primer_color = (87, 15, 22)
        ui.hover = (95, 32, 35)
        ui.hover2 = (95, 32, 35)
        ui.hover3 = (95, 32, 35, 125)
        ui.pressed = (105, 40, 45)
        ui.pressed2 = (110, 45, 50, 200)
        ui.seconder_color = (212, 223, 199)
        ui.seconder_color2 = (87, 15, 22)
        ui.text_color = (255, 255, 255)
        ui.text_color2 = (87, 15, 22)
        ui.info_color = (98, 22, 27)
        ui.tab_background = (140, 62, 75, 1)
        ui.selected = (180, 25, 35, 1)
        ui.tab_min_background = (130, 52, 65, 1)
        ui.scrollprimer = (130, 52, 65, 1)
        ui.scrollseconder = (255, 210, 210, 1)
        ui.adl = (255, 255, 255, 100)
        ui.adlhover = (255, 255, 255, 150)
        ui.hover4 = ui.adlhover
        ui.border = "none"
        ui.exit = "exit_dark.png"
        ui.plusbutton = "plus_red.png"
        ui.editbutton_img = "edit_grey.png"
        ui.cancelbutton_img = "cancel_grey.png"
        ui.okbutton_img = "ok_grey.png"
        ui.AgBorderColor = (155, 193, 188)
        ui.theme3.setEnabled(False)
        ui.theme2.setEnabled(True)
        ui.theme1.setEnabled(True)
        ui.theme4.setEnabled(True)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/user/tick_dark.png"), QtGui.QIcon.Disabled,
                       QtGui.QIcon.Off)
        ui.theme3.setIcon(icon)
        ui.theme2.setIcon(QtGui.QIcon())
        ui.theme1.setIcon(QtGui.QIcon())
        ui.theme4.setIcon(QtGui.QIcon())

        ui.paletteOpacity = (255, 255, 255, 50)
        ui.alternete = ui.adlhover

    elif number == "4":
        ui.primer_color = (0, 200, 153)
        ui.hover = (8, 217, 166)
        ui.hover2 = (8, 217, 166)
        ui.hover3 = (8, 217, 166, 125)
        ui.pressed = (18, 227, 176)
        ui.pressed2 = (23, 232, 181, 200)
        ui.seconder_color = (255, 255, 255)
        ui.seconder_color2 = (0, 200, 153)
        ui.text_color = (255, 255, 255)
        ui.text_color2 = (0, 0, 0)
        ui.info_color = (0, 0, 0)
        ui.tab_background = (0, 160, 123, 1)
        ui.selected = (40, 123, 83, 1)
        ui.tab_min_background = (0, 150, 113, 1)
        ui.scrollprimer = (0, 150, 113, 1)
        ui.scrollseconder = (220, 255, 220, 1)
        ui.adl = (0, 200, 153, 100)
        ui.adlhover = (0, 200, 153, 150)
        ui.hover4 = ui.adlhover
        ui.border = "2px solid black"
        ui.exit = "exit_dark.png"
        ui.plusbutton = "plus.png"
        ui.editbutton = "edit_dark.png"
        ui.editbutton_img = "edit_dark.png"
        ui.cancelbutton_img = "cancel_dark.png"
        ui.okbutton_img = "ok_dark.png"
        ui.AgBorderColor = (41, 53, 61)
        ui.theme4.setEnabled(False)
        ui.theme2.setEnabled(True)
        ui.theme3.setEnabled(True)
        ui.theme1.setEnabled(True)

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/user/tick.png"), QtGui.QIcon.Disabled,
                       QtGui.QIcon.Off)
        ui.theme4.setIcon(icon)
        ui.theme2.setIcon(QtGui.QIcon())
        ui.theme3.setIcon(QtGui.QIcon())
        ui.theme1.setIcon(QtGui.QIcon())

        ui.paletteOpacity = (255, 255, 255, 110)
        ui.alternete = (240, 240, 240)

    ui.change_theme()

    for tabButton in ui.tabButtons:
        tabButton.setStyleSheet("QPushButton {\n"
                                "    background-position: center;\n"
                                "    background-repeat: no-reperat;\n"
                                "    border: none;\n"
                                "    color:rgb" + str(ui.text_color) + ";\n"
                                "text-align: left\n"
                                "}\n"
                                "QPushButton:hover {\n"
                                "    background-color: rgb" + str(ui.hover) + ";\n"
                                "}\n"
                                "QPushButton:pressed {    \n"
                                "    background-color: rgb" + str(ui.pressed) + ";\n"
                                "}")

    for i in ui.shortcutButtons:
        for shortcutButton in i:
            setImg = str()

            if shortcutButton.character == "":
                shortcutButton.setEnabled(False)
            elif shortcutButton.character == "Profile":
                setImg = "    image: url(:/user/profile.png);\n"
            elif shortcutButton.character == "Shortcut":
                setImg = "    image: url(:/newShortcut/new.png);\n"
            elif shortcutButton.character == "Home":
                setImg = "    image: url(:/user/mainmenuSc.png);\n"
            elif shortcutButton.character == "LectProgram":
                setImg = "    image: url(:/user/programSc.png);\n"
            elif shortcutButton.character == "Calendar":
                setImg = "    image: url(:/user/academicSc.png);\n"
            elif shortcutButton.character == "Cafeteria":
                setImg = "    image: url(:/user/cateringSc.png);\n"
            elif shortcutButton.character == "archive":
                setImg = "    image: url(:/user/archiveSc.png);\n"
            elif shortcutButton.character == "AboutUs":
                setImg = "    image: url(:/user/aboutusSc.png);\n"

            shortcutButton.setStyleSheet("\n"
                                         "QPushButton {\n"
                                         "    background-position: center;\n"
                                         "    background-repeat: no-repeat;\n"
                                         "    border: none;\n" +
                                         setImg +
                                         "    color:rgb" + str(ui.text_color2) + ";\n"
                                         "    border-radius: 40px;\n"
                                         "}\n"
                                         "QPushButton:hover {\n"
                                         "    background-color: rgb" + str(ui.hover3) + ";\n"
                                         "}\n"
                                         "QPushButton:pressed {    \n"
                                         "    background-color: rgb" + str(ui.pressed2) + ";\n"
                                         "}\n"
                                         "")

    for i in reversed(range(ui.verticalLayout_002.count())):
        if str(ui.verticalLayout_002.itemAt(i).widget()).find("OpenLecture") != -1:
            ui.verticalLayout_002.itemAt(i).widget().remove_button_2.setStyleSheet("QPushButton {    \n"
                                           "    border-radius: 15px;\n"
                                           "    background-color: transparent;\n"
                                           "    image: url(:/menu/" + ui.exit + ")" + ";\n"
                                           "\n"
                                           "}\n"
                                           "QPushButton:hover {\n"
                                           "    background-color: rgb"+str(ui.hover)+";\n"
                                           "}\n"
                                           "QPushButton:pressed {    \n"
                                           "    background-color: rgb"+str(ui.pressed)+";\n"
                                           "}")

            if number == "4":
                ui.verticalLayout_002.itemAt(i).widget().comboBox_103.setStyleSheet(
                    "background-color: rgb(255, 255, 255); border: 2px solid black")
                ui.verticalLayout_002.itemAt(i).widget().comboBox_104.setStyleSheet(
                    "background-color: rgb(255, 255, 255); border: 2px solid black")
                ui.verticalLayout_002.itemAt(i).widget().comboBox_105.setStyleSheet(
                    "background-color: rgb(255, 255, 255); border: 2px solid black")

            else:
                ui.verticalLayout_002.itemAt(i).widget().comboBox_103.setStyleSheet(
                    "background-color: rgb(255, 255, 255);")
                ui.verticalLayout_002.itemAt(i).widget().comboBox_104.setStyleSheet(
                    "background-color: rgb(255, 255, 255);")
                ui.verticalLayout_002.itemAt(i).widget().comboBox_105.setStyleSheet(
                    "background-color: rgb(255, 255, 255);")


def apply_preferences(ui):
    con = sqlite3.connect("Preferences.db")
    cursor = con.cursor()

    cursor.execute("SELECT * FROM pref")
    data = cursor.fetchall()
    if data[0][0] == "1":
        ui.primer_color = (27, 29, 35)
        ui.hover = (33, 37, 43)
        ui.pressed = (85, 170, 255)
        ui.pressed2 = (85, 170, 255)
        ui.seconder_color = (39, 44, 54)
        ui.seconder_color2 = (44, 49, 60)
        ui.text_color = (255, 255, 255)
        ui.text_color2 = (255, 255, 255)
        ui.info_color = (98, 103, 111)
        ui.tab_background = (50, 52, 57, 1)
        ui.selected = (50, 52, 57, 1)
        ui.tab_min_background = (95, 97, 101, 1)
        ui.scrollprimer = (95, 97, 101, 1)
        ui.scrollseconder = (50, 52, 57, 1)
        ui.hover2 = (52, 59, 72)
        ui.hover3 = (33, 37, 43)
        ui.hover4 = (200, 200, 200, 50)
        ui.adl = (255, 255, 255, 100)
        ui.adlhover = (255, 255, 255, 150)
        ui.border = "none"
        ui.exit = "exit.png"
        ui.plusbutton = "plus.png"
        ui.editbutton_img = "edit.png"
        ui.cancelbutton_img = "cancel.png"
        ui.okbutton_img = "ok.png"
        ui.AgBorderColor = (255, 255, 255)
        ui.themeNumber = 1
        ui.paletteOpacity = (255, 255, 255, 50)
        ui.alternete = ui.hover3

    elif data[0][0] == "2":
        ui.primer_color = (9, 21, 64)
        ui.hover = (20, 32, 75)
        ui.hover2 = (20, 32, 75)
        ui.hover3 = (20, 32, 140, 125)
        ui.pressed = (19, 30, 95)
        ui.pressed2 = (9, 21, 100, 200)
        ui.seconder_color = (166, 182, 242)
        ui.seconder_color2 = (9, 21, 64)
        ui.text_color = (255, 255, 255)
        ui.text_color2 = (9, 21, 64)
        ui.info_color = (98, 103, 155)
        ui.tab_background = (140, 150, 220, 1)
        ui.selected = (90, 90, 220, 1)
        ui.tab_min_background = (120, 120, 220, 1)
        ui.scrollprimer = (120, 120, 220, 1)
        ui.scrollseconder = (220, 220, 255, 1)
        ui.adl = (255, 255, 255, 100)
        ui.adlhover = (255, 255, 255, 150)
        ui.hover4 = ui.adlhover
        ui.border = "none"
        ui.exit = "exit.png"
        ui.plusbutton = "plus_blue.png"
        ui.editbutton_img = "edit.png"
        ui.cancelbutton_img = "cancel.png"
        ui.okbutton_img = "ok.png"
        ui.AgBorderColor = (255, 255, 255)
        ui.themeNumber = 2
        ui.paletteOpacity = (255, 255, 255, 50)
        ui.alternete = ui.adlhover

    elif data[0][0] == "3":
        ui.primer_color = (87, 15, 22)
        ui.hover = (95, 32, 35)
        ui.hover2 = (95, 32, 35)
        ui.hover3 = (95, 32, 35, 125)
        ui.pressed = (105, 40, 45)
        ui.pressed2 = (110, 45, 50, 200)
        ui.seconder_color = (212, 223, 199)
        ui.seconder_color2 = (87, 15, 22)
        ui.text_color = (255, 255, 255)
        ui.text_color2 = (87, 15, 22)
        ui.info_color = (98, 22, 27)
        ui.tab_background = (140, 62, 75, 1)
        ui.selected = (180, 25, 35, 1)
        ui.tab_min_background = (130, 52, 65, 1)
        ui.scrollprimer = (130, 52, 65, 1)
        ui.scrollseconder = (255, 210, 210, 1)
        ui.adl = (255, 255, 255, 100)
        ui.adlhover = (255, 255, 255, 150)
        ui.hover4 = ui.adlhover
        ui.border = "none"
        ui.exit = "exit_dark.png"
        ui.plusbutton = "plus_red.png"
        ui.editbutton_img = "edit_grey.png"
        ui.cancelbutton_img = "cancel_grey.png"
        ui.okbutton_img = "ok_grey.png"
        ui.AgBorderColor = (155, 193, 188)
        ui.themeNumber = 3
        ui.paletteOpacity = (255, 255, 255, 50)
        ui.alternete = ui.adlhover

    elif data[0][0] == "4":
        ui.primer_color = (0, 200, 153)
        ui.hover = (8, 217, 166)
        ui.hover2 = (8, 217, 166)
        ui.hover3 = (8, 217, 166, 125)
        ui.pressed = (18, 227, 176)
        ui.pressed2 = (23, 232, 181, 200)
        ui.seconder_color = (255, 255, 255)
        ui.seconder_color2 = (0, 200, 153)
        ui.text_color = (255, 255, 255)
        ui.text_color2 = (0, 0, 0)
        ui.info_color = (0, 0, 0)
        ui.tab_background = (0, 160, 123, 1)
        ui.selected = (40, 123, 83, 1)
        ui.tab_min_background = (0, 150, 113, 1)
        ui.scrollprimer = (0, 150, 113, 1)
        ui.scrollseconder = (220, 255, 220, 1)
        ui.adl = (0, 200, 153, 100)
        ui.adlhover = (0, 200, 153, 150)
        ui.hover4 = ui.adlhover
        ui.border = "2px solid black"
        ui.exit = "exit_dark.png"
        ui.plusbutton = "plus.png"
        ui.editbutton_img = "edit_dark.png"
        ui.cancelbutton_img = "cancel_dark.png"
        ui.okbutton_img = "ok_dark.png"
        ui.AgBorderColor = (41, 53, 61)
        ui.themeNumber = 4
        ui.paletteOpacity = (255, 255, 255, 110)
        ui.alternete = (240, 240, 240)

    ui.language = data[0][1]

"""
class Change_theme(QtCore.QThread):
    def __init__(self, sayi, ui):
        super().__init__()
        self.sayi = sayi
        self.ui = ui

    change_value = QtCore.pyqtSignal(str)

    def run(self):
        print("*")
        change_theme(self.sayi, self.ui)
        self.change_value.emit("*")

"""


class get_courses_Thread(QtCore.QThread):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        self.ui.regen.setEnabled(False)
        for i in reversed(range(self.ui.verticalLayout_002.count())):
            if str(self.ui.verticalLayout_002.itemAt(i).widget()).find("OpenLecture") != -1:
                self.ui.verticalLayout_002.itemAt(i).widget().comboBox_103.setEnabled(False)
                self.ui.verticalLayout_002.itemAt(i).widget().comboBox_104.setEnabled(False)
                self.ui.verticalLayout_002.itemAt(i).widget().comboBox_105.setEnabled(False)
        self.ui.updating = True

    change_value = QtCore.pyqtSignal(str)

    def run(self):
        if is_file_exist("Courses.db"):
            os.remove("Courses.db")

        cnt = 0
        #self.ui.update_label.setText(self.ui.translate["İnternet bağlantısı gereklidir!"][self.ui.languageNumber])
        url = "https://www.sis.itu.edu.tr/TR/ogrenci/ders-programi/ders-programi.php?seviye=LS"

        response = requests.get(url)
        html_content = response.content
        soup = BeautifulSoup(html_content, "html.parser")
        donem = str()
        try:
            for i in soup.find_all("h1"):
                ls = i.text.split(" ")
                donem = ls[0][2:5:1] + ls[0][7:9:1] + " " + ls[1]
            with open("cT.txt", mode="w", encoding="utf-8") as file:
                file.write(donem)

        except:
            pass
        course_codes = []
        for i in soup.find_all("option"):
            course_codes.append(i.get("value"))
        course_codes.pop(0)
        course_codes.pop(0)
        course_codes.pop(0)
        course_codes.pop(0)
        #print(course_codes)
        ##### BOLUM KODLARI CEKILDI
        for course in course_codes:
            #if course != "ITB":
            #    continue
            #print(course)
            # ui.update_label.setText("{} güncellendi.".format(course))
            cnt += 1
            self.change_value.emit(course + " " + self.ui.translate["güncellendi."][self.ui.languageNumber])
            con = sqlite3.connect("Courses.db")
            cursor = con.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS {} (CRN TEXT, CourseCode TEXT, CourseTitle TEXT, Instructor TEXT, Building TEXT, Day TEXT, Time TEXT, Room TEXT, Capacity TEXT, Enrolled TEXT, Reservation TEXT, MajorRestriction TEXT, Prerequisites TEXT, ClassRestriction TEXT, GVS TEXT)".format(
                    course))

            url = "https://www.sis.itu.edu.tr/TR/ogrenci/ders-programi/ders-programi.php?seviye=LS&derskodu={}".format(course)
            try:
                response = requests.get(url)
            except:
                self.change_value.emit(self.ui.translate["Bir sorun oluştu."][self.ui.languageNumber])
                time.sleep(2)
                self.updating = False
                self.ui.regen.setEnabled(True)
                self.change_value.emit(self.ui.translate["İTÜ Web Site trafiği çok yoğun olduğundan ders güncellemesi tamamlanamadı. Lütfen daha sonra tekrar deneyin."][self.ui.languageNumber])
                return
            html_content = response.content
            soup = BeautifulSoup(html_content, "html.parser")
            table = soup.find("table", {"class": "table table-bordered table-striped table-hover table-responsive"}).find_all("tr")

            for tr in table[2:]:

                td = tr.find_all("td")  # Satırdaki sutunların listesi
                #print(td[0])
                gvs = td[6].text + td[7].text
                if gvs[-1] == " " and gvs[-2] == "/":
                    gvs = gvs.rstrip("/ ")
                    gvs += " " + td[7].text.rstrip("/ ")
                if len(td[6].text.strip().split(" ")) == 1:
                    if td[6].text.strip() == "Pazartesi":
                        td[6] = [1]
                    elif td[6].text.strip() == "Salı":
                        td[6] = [2]
                    elif td[6].text.strip() == "Çarşamba":
                        td[6] = [3]
                    elif td[6].text.strip() == "Perşembe":
                        td[6] = [4]
                    elif td[6].text.strip() == "Cuma":
                        td[6] = [5]
                    else:
                        td[6] = 0
                else:
                    ntd = []
                    for day in td[6].text.strip().split(" "):
                        if day == "Pazartesi":
                            ntd.append(1)
                        elif day == "Salı":
                            ntd.append(2)
                        elif day == "Çarşamba":
                            ntd.append(3)
                        elif day == "Perşembe":
                            ntd.append(4)
                        elif day == "Cuma":
                            ntd.append(5)
                        else:
                            ntd.append(0)
                    td[6] = ntd

                #print(td[7].text)
                if td[7].text.strip() == "/":
                    td[7] = [0]

                elif td[7].text.strip() == "----":
                    td[7] = [0]

                elif len(td[7].text.strip().split(" ")) == 1:
                    gr = td[7].text
                    td[7] = self.convert_hours(gr.strip())

                else:
                    gr = td[7].text
                    if gr[-1] == " " and gr[-2] == "/":
                        gr = gr.rstrip("/ ")
                        gr += " " + td[7].text.rstrip("/ ")
                    ntd = []
                    for hour in gr.strip().split(" "):
                        ntd.append(self.convert_hours(hour))
                    td[7] = ntd

                cleanse = td[2].text.replace("\'", "’")
                cursor.execute("INSERT INTO {} VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)".format(course), (
                    td[0].text, td[1].text, cleanse, td[4].text, td[5].text, str(td[6]), str(td[7]), td[8].text,
                    td[9].text, td[10].text, td[11].text, td[12].text, td[13].text, td[14].text, gvs))
                con.commit()

        #print("DERSLER EKLENDİ")
        time.sleep(0.3)
        self.change_value.emit(self.ui.translate["Tüm dersler güncellendi."][self.ui.languageNumber])
        self.ui.regen.setEnabled(True)
        con = sqlite3.connect("Courses.db")
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        data = cursor.fetchall()
        for i in reversed(range(self.ui.verticalLayout_002.count())):
            if str(self.ui.verticalLayout_002.itemAt(i).widget()).find("OpenLecture") != -1:
                self.ui.verticalLayout_002.itemAt(i).widget().comboBox_103.setEnabled(True)
                self.ui.verticalLayout_002.itemAt(i).widget().comboBox_104.setEnabled(True)
                self.ui.verticalLayout_002.itemAt(i).widget().comboBox_105.setEnabled(True)
                for depcodes in data:
                    self.ui.verticalLayout_002.itemAt(i).widget().comboBox_103.addItem(depcodes[0])

        self.ui.updating = False
        time.sleep(5)
        self.change_value.emit(donem)

    def convert_hours(self, time):
        #print(time)
        time = time.replace("29", "30")
        if time.find("59") != -1:
            yeni_basamak = int(time[-4] + time[-3]) + 1
            son_basamak = time[-2] + time[-1]
            time = time[:-4:]
            time += str(yeni_basamak) + son_basamak
        time = time.replace("59", "00")
        r = time.split("/")
        sh = textwrap.wrap(r[0], 2)[0][1:2] if textwrap.wrap(r[0], 2)[0][0] == "0" else textwrap.wrap(r[0], 2)[0]
        sm = textwrap.wrap(r[0], 2)[1]

        eh = textwrap.wrap(r[1], 2)[0]
        em = textwrap.wrap(r[1], 2)[1]

        s = datetime.timedelta(hours=int(sh), minutes=int(sm))
        a = datetime.timedelta(hours=0, minutes=30)  # sabit
        list = []
        while s != datetime.timedelta(hours=int(eh), minutes=int(em)):
            b = []
            b.append(str(s)[:-3])
            s += a
            b.append(str(s)[0:-3])
            list.append(b)

        for i in range(len(list)):

            if list[i] == ['8:30', '9:00']:
                list[i] = 1
            elif list[i] == ['9:00', '9:30']:
                list[i] = 2
            elif list[i] == ['9:30', '10:00']:
                list[i] = 3
            elif list[i] == ['10:00', '10:30']:
                list[i] = 4
            elif list[i] == ['10:30', '11:00']:
                list[i] = 5
            elif list[i] == ['11:00', '11:30']:
                list[i] = 6
            elif list[i] == ['11:30', '12:00']:
                list[i] = 7
            elif list[i] == ['12:00', '12:30']:
                list[i] = 8
            elif list[i] == ['12:30', '13:00']:
                list[i] = 9
            elif list[i] == ['13:00', '13:30']:
                list[i] = 10
            elif list[i] == ['13:30', '14:00']:
                list[i] = 11
            elif list[i] == ['14:00', '14:30']:
                list[i] = 12
            elif list[i] == ['14:30', '15:00']:
                list[i] = 13
            elif list[i] == ['15:00', '15:30']:
                list[i] = 14
            elif list[i] == ['15:30', '16:00']:
                list[i] = 15
            elif list[i] == ['16:00', '16:30']:
                list[i] = 16
            elif list[i] == ['16:30', '17:00']:
                list[i] = 17
            elif list[i] == ['17:00', '17:30']:
                list[i] = 18
            elif list[i] == ['17:30', '18:00']:
                list[i] = 19
            elif list[i] == ['18:00', '18:30']:
                list[i] = 20
            elif list[i] == ['18:30', '19:00']:
                list[i] = 21
            elif list[i] == ['19:00', '19:30']:
                list[i] = 22
            elif list[i] == ['19:30', '20:00']:
                list[i] = 23
            elif list[i] == ['20:00', '20:30']:
                list[i] = 24
            elif list[i] == ['20:30', '21:00']:
                list[i] = 25
            elif list[i] == ['21:00', '21:30']:
                list[i] = 26
            else:
                list[i] = 0

        return list


def addToClipBoard(text):
    pyperclip.copy(text)


class clock_Thread(QtCore.QThread):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        if self.ui.languageNumber == 0:
            locale.setlocale(locale.LC_ALL, 'turkish')
        elif self.ui.languageNumber == 1:
            locale.setlocale(locale.LC_ALL, 'english')
        elif self.ui.languageNumber == 2:
            locale.setlocale(locale.LC_ALL, 'german')

    change_value = QtCore.pyqtSignal(str)
    change_value2 = QtCore.pyqtSignal(str)

    def run(self):
        while True:
            if self.ui.languageNumber == 0:
                locale.setlocale(locale.LC_ALL, 'turkish')
            elif self.ui.languageNumber == 1:
                locale.setlocale(locale.LC_ALL, 'english')
            elif self.ui.languageNumber == 2:
                locale.setlocale(locale.LC_ALL, 'german')

            now = datetime.datetime.now()
            saat = now.strftime('%H:%M:%S')
            gun = datetime.datetime.strftime(now, '%A')
            ay = datetime.datetime.strftime(now, '%B')
            saat = saat[0:5]
            locale.setlocale(locale.LC_ALL, 'turkish')
            ayin_kaci = datetime.datetime.strftime(now, '%x')
            ayin_kaci = ayin_kaci[0:2]
            if ayin_kaci[-1] == ".":
                ayin_kaci = ayin_kaci.rstrip(".")
                ayin_kaci = "0" + ayin_kaci
            if ayin_kaci[0] == "0":
                ayin_kaci = ayin_kaci[-1]

            if saat[-1] == ":":
                saat = saat.rstrip(":")
                saat = "0" + saat

            if self.ui.languageNumber == 1:
                tarih = "<html><head/><body><p align=\"center\">{} {}</p><p align=\"center\">{}</p></body></html>".format(
                    ay, ayin_kaci, gun)
            else:
                tarih = "<html><head/><body><p align=\"center\">{} {}</p><p align=\"center\">{}</p></body></html>".format(ayin_kaci, ay, gun)

            self.change_value.emit(saat)
            self.change_value2.emit(tarih)

            time.sleep(2)


class credit_Thread(QtCore.QThread):
    def __init__(self, code_list):
        super().__init__()
        self.code_list = code_list

    change_value = QtCore.pyqtSignal(tuple)

    def run(self):
        total = get_credit(self.code_list)
        self.change_value.emit(total)


def get_credit(code_list):
    n = 0.0
    for code in code_list:
        url = "https://www.sis.itu.edu.tr/TR/ogrenci/lisans/ders-bilgileri/ders-bilgileri.php?subj={}&numb={}".format(
            code[0], code[1])
        try:
            response = requests.get(url)
            html_content = response.content
            soup = BeautifulSoup(html_content, "html.parser")
        except:
            return -1, []
        c = 0
        for i in soup.find_all("table", {"class": "table table-bordered"}):
            if c != 2:
                c += 1
                continue
            else:
                c = 0
                for j in i.find_all("tr"):
                    if c != 1:
                        c += 1
                        continue
                    else:
                        c = 0
                        if c != 0:
                            c += 1
                            continue
                        m = j.text.split("\n")
                        n += float(m[1])
                        #return float(m[0])
    return n, code_list


def is_connectable(url):
    try:
        response = requests.get(url)
        return True
    except:
        return False


class mail_Thread(QtCore.QThread):
    def __init__(self, textEdit):
        super().__init__()
        self.textEdit = textEdit

    change_value = QtCore.pyqtSignal(str)

    def run(self):
        send_email(self.textEdit)
        #self.textEdit.setPlainText("")
        self.change_value.emit("")


def send_email(textEdit):
    try:
        content = textEdit.toPlainText()
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login("*", "*")

        frm = "*"
        msg = MIMEMultipart('alternative')

        msg.set_charset('utf8')

        msg['FROM'] = frm

        bodyStr = content
        to = "*"
        # This solved the problem with the encode on the subject.

        msg['To'] = to

        # And this on the body
        _attach = MIMEText(bodyStr.encode('utf-8'), 'html', 'UTF-8')

        msg.attach(_attach)

        server.sendmail(frm, to, msg.as_string())

        server.quit()

    except:
        pass

def fill_archive_comboBox(ui):
    ui.donemler = dict()

    for i in os.listdir():
        if i[0] == "t":
            if os.stat(i).st_size < 10000:
                continue
            try:
                liste = i.split(" ")
                numara = liste[0].replace("t", "")
                isim = liste[1] + " " + liste[2]
                isim = isim.rstrip(".db")
                ui.donemler[int(numara)] = isim
            except:
                continue

    if len(ui.donemler) == 0:
        return 0
    sayi = 0
    l1 = sorted(ui.donemler.keys(), reverse=True)
    for i in l1:
        ui.comboBox1254.addItem(ui.donemler[i])

    sayi = l1[0]
    yol = "t" + str(sayi) + " " + ui.donemler[sayi] + ".db"
    #print(yol)
    if is_file_exist(yol):
        con = sqlite3.connect(yol)
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

        for i in cursor.fetchall():
            ui.comboBox1255.addItem(i[0])


def set_archivedCourseList(ui):

    ui.verticalLayout_2064.removeItem(ui.archiveSpacer)
    for i in reversed(range(ui.verticalLayout_2064.count())):
        #print(str(type(ui.verticalLayout_2064.itemAt(i).widget())))

        if str(type(ui.verticalLayout_2064.itemAt(i).widget())).find("archived") != -1:
            ui.verticalLayout_2064.itemAt(i).widget().deleteLater()
    if ui.comboBox1254.currentIndex() != 0 and ui.comboBox1255.currentIndex() != 0:
        ui.pushButton_2189.setEnabled(True)
        for i in os.listdir():
            if i.find(ui.comboBox1254.currentText()) != -1:
                con = sqlite3.connect(i)
                cursor = con.cursor()
                try:
                    cursor.execute("SELECT * FROM {}".format(ui.comboBox1255.currentText()))
                    for j in cursor.fetchall():
                        data = j[-1].split(" ")
                        if "" in data:
                            data.remove("")
                        saatler = data.copy()
                        gun = str()
                        for m in range(int(len(data) / 2)):
                            gun += data[m] + "\n"
                            saatler.remove(data[m])
                        gun = gun.rstrip("\n")

                        saat = str()
                        for m in saatler:
                            saat += m + "\n"
                        saat = saat.rstrip("\n")

                        doluluk = j[9] + "/" + j[8]

                        fr1 = uiClasses.archivedLecture(j[0], j[1], j[2], j[3], gun, saat, doluluk, ui)
                        ui.verticalLayout_2064.addWidget(fr1)
                except:
                    pass
                """
                except:
                    fr1 = uiClasses.archivedLecture("", "", "Veritabanı bozuk.", "", "", "", "", ui)
                    ui.verticalLayout_2064.addWidget(fr1)
                    ui.pushButton_2189.setEnabled(False)
                    ui.pushButton_3154.setEnabled(False)
                """

    elif ui.comboBox1254.currentIndex() == 0:
        ui.pushButton_2189.setEnabled(False)

    else:
        ui.pushButton_2189.setEnabled(True)

    ui.archiveSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
    ui.verticalLayout_2064.addItem(ui.archiveSpacer)


def change_courses_database(ui):
    donem = ui.comboBox1254.currentText()

    for i, j in ui.donemler.items():
        if j.find(donem) != -1:
            yol = "t" + str(i) + " " + j + ".db"
            ui.update_label.setText(j)
            with open("cT.txt", mode="w", encoding="utf-8") as file:
                file.write(j)

    copyfile(yol, "Courses.db")

    ui.comboBox_6262.setCurrentIndex(0)
    spchangednext(ui)
    open_lecture_program(ui)


def spchangednext(ui):
    # print("Değişiklikler YOK")
    ui.table_credit = 0.0
    if ui.comboBox_6262.currentText() == ui.translate["Seç"][ui.languageNumber]:
        ui.credit_label.setText(ui.translate["Toplam Kredi:"][ui.languageNumber] + " 0.0")
        # print("SELECT SEÇİLDİ SAYFA SIFIRLANACAK")
        for i in range(ui.verticalLayout_002.count() - 3):
            ui.verticalLayout_002.itemAt(i).widget().deleteLater()
        ui.items = {}
        ui.rebuildTable(ui.items)
        ui.lineEdit_6262.clear()
        ui.pushButton_6263.hide()
        ui.verticalLayout_002.insertWidget(ui.verticalLayout_002.count() - 3,
                                             uiClasses.OpenLecture(ui, str(uuid.uuid4()), "", "", "", "",
                                                                   ui.hover, ui.pressed, ui.border,
                                                                   ui.exit, ui.updating))


def refresh_old_courses(ui):
    download_file("1gw-3M86eYDTSvdnH4Ct04YLNy-Giikb5", "log.txt")
    #gdd.download_file_from_google_drive(file_id='1gw-3M86eYDTSvdnH4Ct04YLNy-Giikb5',
                                        #dest_path='./log.txt',
                                        #unzip=True)
    with open("log.txt", encoding="utf-8") as file:
        log = file.read()
        term_list = log.split("\n")
    term_dict = dict()
    for i in term_list:
        split = i.split(",")
        if len(split) < 2:
            continue
        term_dict[split[1]] = split[0]

    for i, j in term_dict.items():
        download_file(j, i)

    fill_archive_comboBox(ui)


class ref_old_dbase(QtCore.QThread):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
    change_value = QtCore.pyqtSignal(str)

    def run(self):
        self.change_value.emit(self.ui.translate["Güncelleniyor..."][self.ui.languageNumber])
        self.ui.pushButton_3154.setEnabled(False)
        self.ui.pushButton_2189.setEnabled(False)
        self.ui.comboBox1254.setEnabled(False)
        self.ui.comboBox1255.setEnabled(False)

        try:
            download_file("1gw-3M86eYDTSvdnH4Ct04YLNy-Giikb5", "log.txt")
            #gdd.download_file_from_google_drive(file_id='1gw-3M86eYDTSvdnH4Ct04YLNy-Giikb5',dest_path='./log.txt', unzip=False)
            with open("log.txt", encoding="utf-8") as file:
                log = file.read()
                if log.find("head") != -1:
                    self.ui.pushButton_3154.setEnabled(True)
                    self.ui.pushButton_2189.setEnabled(True)
                    self.ui.comboBox1254.setEnabled(True)
                    self.ui.comboBox1255.setEnabled(True)
                    self.change_value.emit(self.ui.translate["Bir sorun oluştu."][self.ui.languageNumber])
                    time.sleep(5)
                    self.change_value.emit(self.ui.translate["Veritabanlarını güncelle"][self.ui.languageNumber])
                    return

                term_list = log.split("\n")
            self.ui.comboBox1254.setCurrentIndex(0)
            self.ui.comboBox1255.setCurrentIndex(0)
            term_dict = dict()
            for i in term_list:
                split = i.split(",")
                if len(split) < 2:
                    continue
                term_dict[split[1]] = split[0]

            for i, j in term_dict.items():
                download_file(j, i)
                #gdd.download_file_from_google_drive(file_id=j, dest_path='./{}'.format(i),
                                                    #unzip=False)
                isim = i.rstrip(".db")
                isim = isim.split(" ")
                isim = isim[1] + " " + isim[2] + " {}".format(self.ui.translate["güncellendi."][self.ui.languageNumber])
                self.change_value.emit(isim)

            time.sleep(0.3)
            self.change_value.emit(self.ui.translate["Tamamı güncellendi."][self.ui.languageNumber])
            fill_archive_comboBox(self.ui)

            self.ui.pushButton_2189.setEnabled(True)
            self.ui.comboBox1254.setEnabled(True)
            self.ui.comboBox1255.setEnabled(True)

            self.ui.comboBox1254.clear()
            self.ui.comboBox1255.clear()
            self.ui.comboBox1254.addItem("")
            self.ui.comboBox1255.addItem("")
            self.ui.comboBox1254.setItemText(0, self.ui.translate["Dönem"][self.ui.languageNumber])
            self.ui.comboBox1255.setItemText(0, self.ui.translate["Bölüm kodu"][self.ui.languageNumber])
            fill_archive_comboBox(self.ui)


            time.sleep(5)
            self.ui.pushButton_3154.setEnabled(True)
            self.change_value.emit(self.ui.translate["Veritabanlarını güncelle"][self.ui.languageNumber])

        except:
            self.change_value.emit(self.ui.translate["Bir sorun oluştu."][self.ui.languageNumber])
            time.sleep(5)
            self.change_value.emit(self.ui.translate["Veritabanlarını güncelle"][self.ui.languageNumber])
            self.ui.pushButton_3154.setEnabled(True)
            self.ui.pushButton_2189.setEnabled(True)
            self.ui.comboBox1254.setEnabled(True)
            self.ui.comboBox1255.setEnabled(True)
