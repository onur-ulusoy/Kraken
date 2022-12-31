from PyQt5 import QtCore, QtGui, QtWidgets
import sqlite3
from PyQt5.QtGui import QBrush, QColor, QFont
import interface
import json
import random

Undetermined = (115, 89, 100)
AA = (51, 255, 51)
BA = (102, 255, 102)
BB = (153, 255, 153)
CB = (255, 232, 51)
CC = (255, 232, 102)
DC = (255, 153, 153)
DD = (255, 102, 102)
FF = (255, 51, 51)
BL = (51, 255, 51)
BZ = (255, 51, 51)


class OpenLecture(QtWidgets.QFrame):
    def __init__(self, ui, uid, c1text, c2text, c3text, data, hover, pressed, border, exit, updating):
        super().__init__()

        self.hover = hover
        self.pressed = pressed
        self.border = border
        self.exit = exit

        self.uid = uid
        self.ui = ui
        self.c1text = c1text
        self.c2text = c2text
        self.c3text = c3text
        self.ui.items[uid] = {}
        if data != "":
            self.ui.items[uid] = data
        self.setMinimumSize(QtCore.QSize(0, 35))
        self.setMaximumSize(QtCore.QSize(16777215, 35))
        self.setStyleSheet("background: transparent; border:none")
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.setObjectName("frame_544")
        self.horizontalLayout_443 = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout_443.setContentsMargins(0, 0, 10, 0)
        self.horizontalLayout_443.setSpacing(14)
        # self.horizontalLayout_443.setObjectName("horizontalLayout_443")
        self.comboBox_103 = QtWidgets.QComboBox(self)
        self.comboBox_103.setMinimumSize(QtCore.QSize(105, 25))
        self.comboBox_103.setMaximumSize(QtCore.QSize(105, 16777215))
        self.comboBox_103.setStyleSheet("background-color: rgb(255, 255, 255); border:" + self.border + ";\n")
        # self.comboBox_103.setObjectName("comboBox_103")

        self.horizontalLayout_443.addWidget(self.comboBox_103)

        con = sqlite3.connect("Courses.db")
        cursor = con.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        data = cursor.fetchall()
        #print(data)

        self.comboBox_103.addItem(ui.translate["BÖLÜM"][ui.languageNumber])

        for depcodes in data:
            self.comboBox_103.addItem(depcodes[0])

        self.comboBox_104 = QtWidgets.QComboBox(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_104.sizePolicy().hasHeightForWidth())
        self.comboBox_104.setSizePolicy(sizePolicy)
        self.comboBox_104.setMinimumSize(QtCore.QSize(200, 25))
        self.comboBox_104.setMaximumSize(QtCore.QSize(200, 16777215))
        self.comboBox_104.setStyleSheet("background-color: rgb(255, 255, 255); border:" + self.border + ";\n"
                                                                                                        "\n"
                                                                                                        "QComboBox { max-width: 50px; min-height: 40px;}\n"
                                                                                                        "QComboBox QAbstractItemView::item { min-height: 150px;}\n"
                                                                                                        "QListView::item:selected { color: red; background-color: lightgray; min-width: 1000px;}")
        self.comboBox_104.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToMinimumContentsLength)
        self.comboBox_104.setMinimumContentsLength(0)
        self.comboBox_104.setObjectName("comboBox_104")
        self.comboBox_104.addItem(self.ui.translate["DERS ADI"][self.ui.languageNumber])
        self.horizontalLayout_443.addWidget(self.comboBox_104)
        self.comboBox_105 = QtWidgets.QComboBox(self)
        self.comboBox_105.setMinimumSize(QtCore.QSize(550, 25))
        self.comboBox_105.setMaximumSize(QtCore.QSize(2000, 16777215))
        self.comboBox_105.setStyleSheet("background-color: rgb(255, 255, 255); border:" + self.border + ";\n")
        self.comboBox_105.setObjectName("comboBox_105")
        self.comboBox_105.addItem(self.ui.translate["SEÇİLEN DERS"][self.ui.languageNumber])

        self.comboBox_103.setEnabled(not updating)
        self.comboBox_104.setEnabled(not updating)
        self.comboBox_105.setEnabled(not updating)

        self.horizontalLayout_443.addWidget(self.comboBox_105)
        self.remove_button_2 = QtWidgets.QPushButton(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.remove_button_2.sizePolicy().hasHeightForWidth())
        self.remove_button_2.setSizePolicy(sizePolicy)
        self.remove_button_2.setMinimumSize(QtCore.QSize(30, 30))
        self.remove_button_2.setMaximumSize(QtCore.QSize(30, 30))
        self.remove_button_2.setStyleSheet("QPushButton {    \n"
                                           "    border-radius: 15px;\n"
                                           "    background-color: transparent;\n"
                                           "    image: url(:/menu/" + ui.exit + ")" + ";\n"
                                                                                      "\n"
                                                                                      "}\n"
                                                                                      "QPushButton:hover {\n"
                                                                                      "    background-color: rgb" + str(
            self.hover) + ";\n"
                          "}\n"
                          "QPushButton:pressed {    \n"
                          "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                            "}")
        self.remove_button_2.setText("")
        # self.remove_button_2.setIcon(icon2)
        self.remove_button_2.setObjectName("remove_button_2")
        self.horizontalLayout_443.addWidget(self.remove_button_2)

        if self.c1text != "":
            # index = combo.findText(text, QtCore.Qt.MatchFixedString)
            self.comboBox_103.setCurrentText(self.c1text)
            con = sqlite3.connect("Courses.db")
            con.row_factory = lambda cursor, row: row[0]
            cursor = con.cursor()
            cursor.execute("SELECT DISTINCT CourseTitle FROM {}".format(self.c1text))
            data = cursor.fetchall()
            #print(data)
            # self.comboBox_104.addItem("DERS ADI")
            self.comboBox_104.addItems(data)

            self.comboBox_104.setCurrentText(self.c2text)

            con = sqlite3.connect("Courses.db")
            cursor = con.cursor()
            cursor.execute(
                "SELECT CRN, CourseCode, CourseTitle, Instructor, Building, GVS, Enrolled, Capacity, MajorRestriction, Prerequisites, ClassRestriction FROM {} WHERE CourseTitle = '{}'".format(
                    self.c1text, self.c2text))
            data = cursor.fetchall()

            data = list(map(list, data))
            #print(data)

            # self.comboBox_105.addItem("SECILEN DERS")

            for l in range(len(data)):
                enrolled = str(data[l][6]) + "/" + str(data[l][7])
                data[l].pop(7)
                data[l][6] = enrolled

            index = 1
            for classes in data:
                k, l, m = classes[7], classes[8], classes[9]
                tooltip = "{} {}\n{} {}\n{} {}".format(
                    self.ui.translate["Dersi alabilen programlar:"][self.ui.languageNumber],
                    k, self.ui.translate["Dersin önşartları:"][self.ui.languageNumber],
                    l, self.ui.translate["Sınıf önşartı:"][self.ui.languageNumber], m)
                classes.pop(-1)
                classes.pop(-1)
                classes.pop(-1)

                self.comboBox_105.addItem(" | ".join(classes))
                self.comboBox_105.setItemData(index, tooltip, QtCore.Qt.ToolTipRole)
                index += 1

            index = self.comboBox_105.findText(self.c3text, QtCore.Qt.MatchStartsWith)
            #print(index)
            self.comboBox_105.setCurrentIndex(index)

        self.remove_button_2.clicked.connect(self.deleteButton)

        self.comboBox_103.currentTextChanged.connect(self.getCourseNames)
        self.comboBox_104.currentTextChanged.connect(self.getCourses)
        self.comboBox_105.currentTextChanged.connect(self.addToTable)

    def deleteButton(self):

        self.ui.pushButton_6262.setEnabled(True)
        self.ui.changed = True
        self.setParent(None)

        #kırmızı dersin koordinatlarını al
        kd = ""
        redc = []
        #kırmızı ders ve silinen hariç koordinatlar
        coordinates = []

        con = sqlite3.connect("Courses.db")
        cursor = con.cursor()
        cursor.execute(
            "SELECT CourseCode FROM {} WHERE CRN = '{}'".format(
                self.ui.items[self.uid]["dep"],
                self.ui.items[self.uid]["crn"]))
        data = cursor.fetchall()
        ders_kodu = data[0][0].split()

        try:
            self.ui.ders_kodu_list.remove(ders_kodu)
            self.ui.tablosuz_dersler.remove(ders_kodu)
        except:
            pass

        del self.ui.items[self.uid]

        try:
            for key, value in self.ui.items.copy().items():
                if value != {}:
                    if "c" in value:
                        redc = value["coordinates"]
                        kd = value["name"]

                    if "c" not in value:
                        for c in value["coordinates"]:
                            coordinates.append(c)
        except:
            pass


        #print("KIRMIZI VE SİLİNEN HARİÇ KOORDİNATLAR ", coordinates)
        #print("KIRMIZI KOORDİNATLAR ", redc)

        if any(x in redc for x in coordinates):
            pass# !!!!!!!!!!!!!!!!!!!!!!111111
            #print("KIRMIZI DERS HALA ÇAKIŞIYOR")

        else:
            for i in range(self.ui.verticalLayout_002.count()):
                if str(self.ui.verticalLayout_002.itemAt(i).widget()).find("OpenLecture") != -1:
                    if self.ui.verticalLayout_002.itemAt(i).widget().comboBox_104.currentText() == kd:
                        kcrn = self.ui.verticalLayout_002.itemAt(i).widget().comboBox_105.currentText()[:5]
                        self.ui.verticalLayout_002.itemAt(i).widget().setStyleSheet(
                            "background: transparent; border:none")

                        for key, value in self.ui.items.copy().items():
                            if value["name"] == kd:
                                del self.ui.items[key]["c"]
                                self.ui.items[key]["crn"] = kcrn

        #print("BİR DERS SİLİNDİ ", self.ui.items)
        try:
            self.ui.rebuildTable(self.ui.items)
        except:
            pass

    def getCourseNames(self):
        self.ui.pushButton_6262.setEnabled(True)
        self.ui.changed = True

        if self.comboBox_103.currentIndex() != 0:
            #print("1. DEĞİŞTİ")
            self.bolum = self.comboBox_103.currentText()
            self.ui.items[self.uid]["dep"] = self.comboBox_103.currentText()
            self.ui.items[self.uid]["name"] = ""
            #print(self.ui.items)
            self.comboBox_104.blockSignals(True)
            self.comboBox_104.clear()

            #print("55555555")

            con = sqlite3.connect("Courses.db")
            con.row_factory = lambda cursor, row: row[0]
            cursor = con.cursor()
            cursor.execute("SELECT DISTINCT CourseTitle FROM {}".format(self.bolum))
            data = cursor.fetchall()
            #print(data)
            self.comboBox_104.addItem(self.ui.translate["DERS ADI"][self.ui.languageNumber])
            self.comboBox_104.addItems(data)

            self.comboBox_104.blockSignals(False)

    def getCourses(self):
        self.ui.pushButton_6262.setEnabled(True)
        self.ui.changed = True

        #print("2.COMBOBOX DEĞİŞTİ")
        #print(self.comboBox_104.currentText())
        if self.comboBox_104.currentIndex() != 0:
            check = False
            try:
                check = any(d['name'] == self.comboBox_104.currentText() for d in self.ui.items.values())
            except:
                pass
            if check:
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.ui.translate["{} dersini zaten seçtin!"][self.ui.languageNumber].format(self.comboBox_104.currentText()))
                msgBox.setWindowTitle(self.ui.translate["Aynı Ders"][self.ui.languageNumber])
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Cancel)
                buttonz = msgBox.button(QtWidgets.QMessageBox.Cancel)
                buttonz.setText(self.ui.translate["Tamam"][self.ui.languageNumber])
                # msgBox.buttonClicked.connect(msgButtonClick)

                returnValue = msgBox.exec()

                if returnValue == QtWidgets.QMessageBox.Cancel:
                    self.comboBox_104.setCurrentIndex(0)
            else:
                #print("2. ÇALIŞMAYA BAŞLADI!")
                selectedcourse = self.comboBox_104.currentText()
                self.ui.items[self.uid]["name"] = selectedcourse
                ### SİNYALİ KES
                self.comboBox_105.blockSignals(True)
                self.comboBox_105.clear()
                self.bolum = self.comboBox_103.currentText()
                con = sqlite3.connect("Courses.db")
                cursor = con.cursor()
                cursor.execute(
                    "SELECT CRN, CourseCode, CourseTitle, Instructor, Building, GVS, Enrolled, Capacity, MajorRestriction, Prerequisites, ClassRestriction FROM {} WHERE CourseTitle = '{}'".format(
                        self.bolum, selectedcourse))
                data = cursor.fetchall()
                data = list(map(list, data))
                #print(data)
                enrolled = data

                #print(self.ui.items)

                self.comboBox_105.addItem(self.ui.translate["SEÇİLEN DERS"][self.ui.languageNumber])

                for l in range(len(data)):
                    enrolled = str(data[l][6]) + "/" + str(data[l][7])
                    data[l].pop(7)
                    data[l][6] = enrolled
                index = 1
                for classes in data:
                    k, l, m = classes[7], classes[8], classes[9]
                    tooltip = "{} {}\n{} {}\n{} {}".format(
                        self.ui.translate["Dersi alabilen programlar:"][self.ui.languageNumber],
                        k, self.ui.translate["Dersin önşartları:"][self.ui.languageNumber],
                        l, self.ui.translate["Sınıf önşartı:"][self.ui.languageNumber], m)
                    classes.pop(-1)
                    classes.pop(-1)
                    classes.pop(-1)

                    self.comboBox_105.addItem(" | ".join(classes))
                    self.comboBox_105.setItemData(index, tooltip, QtCore.Qt.ToolTipRole)
                    index += 1
                self.comboBox_105.blockSignals(False)

    def addToTable(self):

        self.ui.pushButton_6262.setEnabled(True)
        self.ui.changed = True

        #print("3.DEĞİŞTİ")
        if self.comboBox_105.currentIndex() != 0:

            cakisanliste = []


            self.ui.items[self.uid]["crn"] = self.comboBox_105.currentText()[:5]
            self.ui.items[self.uid]["coordinates"] = {}

            # CAKISMA :D
            con = sqlite3.connect("Courses.db")
            cursor = con.cursor()
            cursor.execute(
                "SELECT Day, Time FROM {} WHERE CRN = '{}'".format(
                    self.ui.items[self.uid]["dep"],
                    self.ui.items[self.uid]["crn"]))
            listh = cursor.fetchall()[0]

            #print(listh)
            coordinates = []

            #print(self.ui.items)
            if listh != ('0', '[0]'):
                for d in range(len(json.loads(listh[0]))):
                    if len(json.loads(listh[0])) == 1:
                        for t in range(len(json.loads(listh[1]))):
                            coordinates.append([json.loads(listh[0])[d], json.loads(listh[1])[t]])
                    else:
                        for g in range(len(json.loads(listh[1])[d])):
                            coordinates.append([json.loads(listh[0])[d], json.loads(listh[1])[d][g]])

                #print(coordinates)

                # HANGI KUTUCUKLARI DOLDURACAK?

                #print(self.ui.items)

                for key, value in self.ui.items.items():
                    if "coordinates" in value:
                        if any(x in coordinates for x in value["coordinates"]):
                            # !!!!!!!!!!!!!!!!!!!!!!111111
                            cakisanliste.append(value["name"])

                #print("ÇAKIŞAN DERSLER LİSTESİ", cakisanliste)

                if cakisanliste != []:
                    self.setStyleSheet("background: red; border:none")
                    msgBox = QtWidgets.QMessageBox()
                    msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                    if len(cakisanliste) == 1:
                        msgBox.setText(self.ui.translate["Bu ders {} ile çakışıyor. Bu ders programa eklenmeyecek."][
                            self.ui.languageNumber].format(
                            cakisanliste[0]))
                    if len(cakisanliste) == 2:
                        msgBox.setText(
                            self.ui.translate["Bu ders {} ve {} ile çakışıyor. Bu ders programa eklenmeyecek."][
                                self.ui.languageNumber].format(
                                cakisanliste[0], cakisanliste[1]))
                    msgBox.setWindowTitle(self.ui.translate["Ders Çakışması"][self.ui.languageNumber])
                    msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                    buttony = msgBox.button(QtWidgets.QMessageBox.Ok)
                    if len(cakisanliste) == 1:
                        buttony.setText(self.ui.translate["{} Sil"][
                            self.ui.languageNumber].format(
                            cakisanliste[0]))
                    if len(cakisanliste) == 2:
                        buttony.setText(self.ui.translate["Çakıştığı 2 Dersi Sil"][self.ui.languageNumber])
                    buttonz = msgBox.button(QtWidgets.QMessageBox.Cancel)
                    buttonz.setText(self.ui.translate["Tamam"][self.ui.languageNumber])
                    # msgBox.buttonClicked.connect(msgButtonClick)
                    returnValue = msgBox.exec()

                    if returnValue == QtWidgets.QMessageBox.Ok:
                        #print('ÇAKIŞAN DERS YA DA DERSLER SİLİNECEK')

                        for l in cakisanliste:
                            for key, value in self.ui.items.copy().items():
                                if "name" in value:
                                    if value["name"] == l:
                                        del self.ui.items[key]

                            for i in range(self.ui.verticalLayout_002.count()):
                                if str(self.ui.verticalLayout_002.itemAt(i).widget()).find("OpenLecture") != -1:
                                    if self.ui.verticalLayout_002.itemAt(i).widget().comboBox_104.currentText() == l:
                                        self.ui.verticalLayout_002.itemAt(i).widget().deleteLater()

                        self.setStyleSheet("background: transparent; border:none")

                    self.ui.rebuildTable(self.ui.items)

                    if returnValue == QtWidgets.QMessageBox.Cancel:
                        #del self.ui.items[self.uid]["coordinates"]
                        #del self.ui.items[self.uid]["crn"]
                        self.ui.items[self.uid]["c"] = True
                        #print('İlk ders kalacak Sonraki silinecek')
                        # break

                #print(coordinates)
                # ekle

                #print(self.ui.items)

                if cakisanliste == []:
                    self.ui.items[self.uid]["coordinates"] = coordinates
                    ctes = []
                    kuid = ""
                    for key, value in self.ui.items.items():
                        if "coordinates" in value:
                            if "c" in value:
                                #print("Kırmızılı ders")
                                kuid = key

                                pass
                            else:
                                for j in value["coordinates"]:
                                    ctes.append(j)

                    redc = False

                    for a, b in self.ui.items.items():
                        try:
                            if b["c"] is True:

                                #print("Kırmızı arkaplanlı ders var")
                                for key, value in self.ui.items.items():
                                    #print(key)
                                    if key != a:
                                        if not any(x in b["coordinates"] for x in ctes):
                                            redc = True

                        except:
                            pass

                    if redc:
                        #print("ARTIK ÇAKIŞMIYOR")
                        del self.ui.items[kuid]["c"]
                        kcrn = ""
                        for i in range(self.ui.verticalLayout_002.count() - 3):
                            if self.ui.verticalLayout_002.itemAt(i).widget().uid == kuid:
                                kcrn = self.ui.verticalLayout_002.itemAt(i).widget().comboBox_105.currentText()[:5]
                                self.ui.verticalLayout_002.itemAt(i).widget().setStyleSheet(
                                    "background: transparent; border:none")

                        self.ui.items[kuid]["crn"] = kcrn

                    #print(self.ui.items)
                    self.ui.rebuildTable(self.ui.items)
                    self.setStyleSheet("background: transparent; border:none")
                else:
                    self.ui.items[self.uid]["coordinates"] = coordinates
                    #print(self.ui.items)
                    self.ui.rebuildTable(self.ui.items)

            else:
                con = sqlite3.connect("Courses.db")
                cursor = con.cursor()
                cursor.execute(
                    "SELECT CourseCode FROM {} WHERE CRN = '{}'".format(
                        self.ui.items[self.uid]["dep"],
                        self.ui.items[self.uid]["crn"]))
                data = cursor.fetchall()
                ders_kodu = data[0][0].split()

                self.ui.ders_kodu_list.append(ders_kodu)
                self.ui.tablosuz_dersler.append(ders_kodu)
                self.ui.start_gettingCredit(self.ui.ders_kodu_list)

        else:
            #print("Select Seçildi")
            try:
                del self.ui.items[self.uid]["coordinates"]
                del self.ui.items[self.uid]["crn"]
            except:
                pass
            self.ui.rebuildTable(self.ui.items)
        #print(self.ui.items)


class LectureFrame(QtWidgets.QFrame):
    def __init__(self, text, i1, credit, dep, ui, db, extra=0, starter=0):
        super().__init__()

        self.setMinimumSize(QtCore.QSize(0, 0))
        self.setMaximumSize(QtCore.QSize(16777215, 48))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dep = dep
        self.code = text
        self.name = i1
        self.credit = credit
        self.starter = starter
        self.mstarter = 0
        if self.credit.find("/") != -1:
            credit_elements = self.credit.split("/")
            self.credit = float(credit_elements[0]) / float(credit_elements[1])
            self.credit = str(self.credit)

        self.ui = ui
        self.db = db
        # self.setObjectName("lectureFrame")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout_10.setContentsMargins(-1, 0, -1, 0)
        # self.horizontalLayout_10.setObjectName("horizontalLayout_10")

        self.lectFeatures = QtWidgets.QFrame()
        self.lectFeatures.setMinimumSize(QtCore.QSize(0, 0))  # 255,89,100
        self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                        "border-radius: 5px;".format(Undetermined))
        self.lectFeatures.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lectFeatures.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.lectFeatures.setObjectName("lectFeatures")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.lectFeatures)
        # self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lectureCode = QtWidgets.QLabel(self.lectFeatures)
        self.lectureCode.setMinimumSize(QtCore.QSize(90, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lectureCode.setFont(font)
        self.lectureCode.setStyleSheet("color: rgb(255, 255, 255);")
        # self.lectureCode.setObjectName("lectureCode")
        self.horizontalLayout_5.addWidget(self.lectureCode)
        self.lectureName = QtWidgets.QLabel(self.lectFeatures)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lectureName.setFont(font)
        self.lectureName.setStyleSheet("color: rgb(255, 255, 255);")
        # self.lectureName.setObjectName("lectureName")
        self.horizontalLayout_5.addWidget(self.lectureName)
        self.horizontalLayout_5.addStretch()
        self.letterGrade_comboBox = QtWidgets.QComboBox(self.lectFeatures)
        self.letterGrade_comboBox.setMinimumSize(QtCore.QSize(60, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.letterGrade_comboBox.setFont(font)
        self.letterGrade_comboBox.setStyleSheet("color:rgb(255, 255, 255);\n"
                                                "background-color: transparent;\n"
                                                "selection-background-color: transparent;")
        self.letterGrade_comboBox.setEditable(False)
        self.letterGrade_comboBox.setDuplicatesEnabled(False)
        self.letterGrade_comboBox.setFrame(True)
        # self.letterGrade_comboBox.setObjectName("letterGrade_comboBox")
        if credit != "0":
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")

            self.letterGrade_comboBox.setItemText(0, " ??")
            self.letterGrade_comboBox.setItemText(1, " AA")
            self.letterGrade_comboBox.setItemText(2, " BA")
            self.letterGrade_comboBox.setItemText(3, " BB")
            self.letterGrade_comboBox.setItemText(4, " CB")
            self.letterGrade_comboBox.setItemText(5, " CC")
            self.letterGrade_comboBox.setItemText(6, " DC")
            self.letterGrade_comboBox.setItemText(7, " DD")
            self.letterGrade_comboBox.setItemText(8, " FF")
        else:
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")

            self.letterGrade_comboBox.setItemText(0, " ??")
            self.letterGrade_comboBox.setItemText(1, " BL")
            self.letterGrade_comboBox.setItemText(2, " BZ")

        self.horizontalLayout_5.addWidget(self.letterGrade_comboBox)
        self.horizontalLayout_10.addWidget(self.lectFeatures, 50 + eval(credit) * 10)
        self.horizontalLayout_10.addStretch(50 - eval(credit) * 10)

        self.lectureCode.setText(text)
        self.lectureName.setText(i1)

        con = sqlite3.connect(self.db)
        cursor = con.cursor()
        cursor.execute("SELECT Grade FROM {} where Name = ?".format(self.dep), (self.name,))
        data = cursor.fetchall()
        self.letterGrade = str(data[0])
        self.letterGrade = self.letterGrade.replace("(", "")
        self.letterGrade = self.letterGrade.replace(")", "")
        self.letterGrade = self.letterGrade.replace(",", "")
        self.letterGrade = self.letterGrade.replace("'", "")

        if self.letterGrade == "":
            self.letterGrade = " ??"
        else:
            self.letterGrade = " " + self.letterGrade

        index = self.letterGrade_comboBox.findText(self.letterGrade, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.letterGrade_comboBox.setCurrentIndex(index)
            self.setColor()

        self.letterGrade_comboBox.currentTextChanged.connect(self.setColor)

        if extra:
            self.cButton = QtWidgets.QPushButton()
            self.horizontalLayout_5.addWidget(self.cButton)
            self.cButton.clicked.connect(self.close_extra_lecture)

    def setColor(self):
        temp = self.letterGrade
        self.temp = temp
        k = 0
        t = 0
        if temp == " AA":
            k = 4
        elif temp == " BA":
            k = 3.5
        elif temp == " BB":
            k = 3
        elif temp == " CB":
            k = 2.5
        elif temp == " CC":
            k = 2
        elif temp == " DC":
            k = 1.5
        elif temp == " DD":
            k = 1

        self.letterGrade = self.letterGrade_comboBox.currentText()
        if self.letterGrade == " AA" or self.letterGrade == " BL":
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(AA))
            t = 4
        elif self.letterGrade == " BA":
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(BA))
            t = 3.5
        elif self.letterGrade == " BB":
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(BB))
            t = 3
        elif self.letterGrade == " CB":
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(CB))
            t = 2.5
        elif self.letterGrade == " CC":
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(CC))
            t = 2
        elif self.letterGrade == " DC":
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(DC))
            t = 1.5
        elif self.letterGrade == " DD":
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(DD))
            t = 1
        elif self.letterGrade == " FF" or self.letterGrade == " BZ":
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(FF))
        else:
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(Undetermined))
        self.update_grade_to_db(self.letterGrade)

        con = sqlite3.connect("MainLectures.db")
        cursor = con.cursor()
        cursor.execute("Select * From settings")
        data = cursor.fetchall()

        try:
            oldGpa = data[0][2]
            oldGpa = float(oldGpa)
            oldCredit = data[0][3]
            oldCredit = float(oldCredit)
            if temp != " ??":
                Credit = oldCredit - float(self.credit)
                if Credit == 0.0:
                    Gpa = 0.0
                else:
                    Gpa = (oldGpa * oldCredit - k * float(self.credit)) / Credit

                if self.letterGrade != " ??":
                    newCredit = Credit + float(self.credit)
                    newGpa = (Gpa * Credit + t * float(self.credit)) / newCredit
                    cursor.execute("Update settings set Gpa = ?, TotalCredit = ?", (newGpa, newCredit))
                    con.commit()
                    # print(newGpa, newCredit)
                    self.ui.gpaLabel.setText(str(abs(round(newGpa, 2))))

                else:
                    newCredit = Credit
                    newGpa = Gpa

                    cursor.execute("Update settings set Gpa = ?, TotalCredit = ?", (newGpa, newCredit))
                    con.commit()
                    # print(newGpa, newCredit)
                    if newCredit == 0.0:
                        self.ui.gpaLabel.setText("N/A")
                    else:
                        self.ui.gpaLabel.setText(str(abs(round(newGpa, 2))))

            else:
                if self.letterGrade != " ??":
                    newCredit = oldCredit + float(self.credit)
                    newGpa = (oldGpa * oldCredit + t * float(self.credit)) / newCredit
                    cursor.execute("Update settings set Gpa = ?, TotalCredit = ?", (newGpa, newCredit))
                    con.commit()
                    # print(newGpa, newCredit)
                    self.ui.gpaLabel.setText(str(abs(round(newGpa, 2))))
                else:
                    self.ui.gpaLabel.setText(str(abs(round(oldGpa, 2))))
        except:
            self.ui.gpaLabel.setText("N/A")
            cursor.execute("Update settings set Gpa = ?, TotalCredit = ?", ("0.0", "0.0"))
            con.commit()
        """
        if self.mstarter != 0:
            con2 = sqlite3.connect("Gpa.db")
            cursor2 = con2.cursor()
            cursor2.execute("Update Gpa set depGpa = ?", (str(self.ui.blmgpa),))
            con2.commit()
            cursor2.execute("Update Gpa set capGpa = ?", (str(self.ui.capgpa),))
            con2.commit()
            print(abs(round(self.ui.blmgpa, 2)), abs(round(self.ui.capgpa, 2)))
        """

        con = sqlite3.connect("MainLectures.db")
        cursor = con.cursor()
        cursor.execute("SELECT TotalCredit FROM settings")
        data = cursor.fetchall()
        credit = data[0][0]
        gr = self.ui.blm_crdt
        gr2 = self.ui.cap_crdt
        if self.temp != self.letterGrade and (self.temp == " ??" or self.letterGrade == " ??"):
            self.starter = 5
        else:
            self.starter = 0

        if self.starter != 0:
            if self.db != "SecondaryLectures.db":
                if self.letterGrade != " ??":
                    self.ui.blm_crdt += float(self.credit)
                else:
                    self.ui.blm_crdt -= float(self.credit)
            else:
                if self.letterGrade != " ??":
                    self.ui.cap_crdt += float(self.credit)
                else:
                    self.ui.cap_crdt -= float(self.credit)

        self.ui.labelblm_crd.setText(str(self.ui.blm_crdt) + "/" + str(round(self.ui.total_dep_credit, 2)))
        self.ui.label_capcrd.setText(str(self.ui.cap_crdt) + "/" + str(round(self.ui.total_cap_credit, 2)))
        if credit == "0.0":
            self.ui.gpaLabel.setText("N/A")
        if self.mstarter != 0:
            if self.db != "SecondaryLectures.db":
                self.calculate(k, t, temp, gr, "depGpa")
            elif self.db == "SecondaryLectures.db":
                self.calculate(k, t, temp, gr2, "capGpa")
        self.mstarter = 5

    def calculate(self, k, t, temp, gr, code):

        con2 = sqlite3.connect("Gpa.db")
        cursor2 = con2.cursor()

        try:
            oldGpa = None
            _gpa = 0.0
            if code == "depGpa":
                oldGpa = self.ui.blmgpa
            elif code == "capGpa":
                oldGpa = self.ui.capgpa

            oldCredit = gr
            if temp != " ??":
                Credit = oldCredit - float(self.credit)
                if Credit == 0.0:
                    Gpa = 0.0
                else:
                    Gpa = (oldGpa * oldCredit - k * float(self.credit)) / Credit

                if self.letterGrade != " ??":
                    newCredit = Credit + float(self.credit)
                    newGpa = (Gpa * Credit + t * float(self.credit)) / newCredit
                    _gpa = newGpa
                    #print(Gpa, Credit, t, self.credit, newCredit)
                    cursor2.execute("Update Gpa set {} = ?".format(code), (newGpa,))
                    con2.commit()
                    # print(newGpa, newCredit)
                    #self.ui.gpaLabel.setText(str(abs(round(newGpa, 2))))

                else:
                    newCredit = Credit
                    newGpa = Gpa
                    _gpa = newGpa
                    cursor2.execute("Update Gpa set {} = ?".format(code), (newGpa,))
                    con2.commit()
                    # print(newGpa, newCredit)
                    if newCredit == 0.0:
                        _gpa = 0.0
                        cursor2.execute("Update Gpa set {} = ?".format(code), ("0.0",))
                        con2.commit()
                        pass #self.ui.gpaLabel.setText("N/A")
                    else:
                        pass #self.ui.gpaLabel.setText(str(abs(round(newGpa, 2))))

            else:
                if self.letterGrade != " ??":
                    newCredit = oldCredit + float(self.credit)
                    newGpa = (oldGpa * oldCredit + t * float(self.credit)) / newCredit
                    _gpa = newGpa
                    cursor2.execute("Update Gpa set {} = ?".format(code), (newGpa,))
                    con2.commit()
                    # print(newGpa, newCredit)

                    #self.ui.gpaLabel.setText(str(abs(round(newGpa, 2))))
                else:
                    pass#self.ui.gpaLabel.setText(str(abs(round(oldGpa, 2))))

            if code == "depGpa":
                self.ui.blmgpa = _gpa
                if self.ui.blm_crdt == 0.0:
                    self.ui.label_blmort.setText("N/A")
                else:
                    self.ui.label_blmort.setText(str(abs(round(self.ui.blmgpa, 2))))
            elif code == "capGpa":
                self.ui.capgpa = _gpa
                if self.ui.cap_crdt == 0.0:
                    self.ui.label_caport.setText("N/A")
                else:
                    self.ui.label_caport.setText(str(abs(round(self.ui.capgpa, 2))))

        except:
            #self.ui.gpaLabel.setText("N/A")
            cursor2.execute("Update Gpa set {} = ?".format(code), ("0.0",))
            con2.commit()
            if code == "depGpa":
                self.ui.blmgpa = 0.0
            elif code == "capGpa":
                self.ui.capgpa = 0.0

    def update_grade_to_db(self, currentText):
        currentText = currentText.strip(" ")
        con = sqlite3.connect(self.db)
        cursor = con.cursor()
        if currentText == "??":
            cursor.execute("Update {} set Grade = ? where Name = ?".format(self.dep), ("", self.name))
        else:
            cursor.execute("Update {} set Grade = ? where Name = ?".format(self.dep), (currentText, self.name))
        con.commit()

    def close_extra_lecture(self):
        index = self.letterGrade_comboBox.findText(" ??", QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.letterGrade_comboBox.setCurrentIndex(index)

        self.close()
        con = sqlite3.connect("ExtraLectures.db")
        cursor = con.cursor()
        cursor.execute("DELETE FROM {} where Name = ?".format(self.dep), (self.name,))
        con.commit()
        con.close()

        con = sqlite3.connect("MainLectures.db")
        cursor = con.cursor()
        cursor.execute("SELECT TotalCredit FROM settings")
        data = cursor.fetchall()
        if data == [('0.0',)]:
            self.ui.gpaLabel.setText("N/A")


class S_LectureFrame(QtWidgets.QFrame):
    def __init__(self, dersler, text, i1, credit, dep, ui, starter=0):
        super().__init__()
        self.mstarter = 0
        self.setMinimumSize(QtCore.QSize(0, 0))
        self.setMaximumSize(QtCore.QSize(16777215, 55))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.dep = dep
        self.code = text
        self.name = i1
        self.credit = credit
        self.starter = starter
        if self.credit.find("/") != -1:
            credit_elements = self.credit.split("/")
            self.credit = float(credit_elements[0]) / float(credit_elements[1])
            self.credit = str(self.credit)

        self.ui = ui

        # self.setObjectName("lectureFrame")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout_10.setContentsMargins(-1, 0, -1, 0)
        # self.horizontalLayout_10.setObjectName("horizontalLayout_10")

        self.lectFeatures = QtWidgets.QFrame()
        self.lectFeatures.setMinimumSize(QtCore.QSize(0, 0))
        self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                        "border-radius: 5px;".format(Undetermined))
        self.lectFeatures.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.lectFeatures.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.lectFeatures.setObjectName("lectFeatures")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.lectFeatures)
        # self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.lectureCode = QtWidgets.QLabel(self.lectFeatures)
        self.lectureCode.setMinimumSize(QtCore.QSize(90, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lectureCode.setFont(font)
        self.lectureCode.setStyleSheet("color: rgb(255, 255, 255);")
        # self.lectureCode.setObjectName("lectureCode")
        self.horizontalLayout_5.addWidget(self.lectureCode)
        self.lectureName = QtWidgets.QComboBox(self.lectFeatures)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lectureName.setFont(font)
        # self.lectureName.setObjectName("lectureName")

        self.lectureName.setMinimumSize(QtCore.QSize(60, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lectureName.setFont(font)
        self.lectureName.setStyleSheet("color:rgb(255, 255, 255);\n"
                                       "background-color: transparent;\n"
                                       "selection-background-color: transparent;")
        self.lectureName.setEditable(False)
        self.lectureName.setDuplicatesEnabled(False)
        self.lectureName.setFrame(True)
        # self.letterGrade_comboBox.setObjectName("letterGrade_comboBox")
        for i in dersler:
            self.lectureName.addItem("")

        self.horizontalLayout_5.addWidget(self.lectureName)
        self.horizontalLayout_5.addStretch()
        self.letterGrade_comboBox = QtWidgets.QComboBox(self.lectFeatures)
        self.letterGrade_comboBox.setMinimumSize(QtCore.QSize(60, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.letterGrade_comboBox.setFont(font)
        self.letterGrade_comboBox.setStyleSheet("color:rgb(255, 255, 255);\n"
                                                "background-color: transparent;\n"
                                                "selection-background-color: transparent;")
        self.letterGrade_comboBox.setEditable(False)
        self.letterGrade_comboBox.setDuplicatesEnabled(False)
        self.letterGrade_comboBox.setFrame(True)
        # self.letterGrade_comboBox.setObjectName("letterGrade_comboBox")

        if credit != "0":
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")

            self.letterGrade_comboBox.setItemText(0, " ??")
            self.letterGrade_comboBox.setItemText(1, " AA")
            self.letterGrade_comboBox.setItemText(2, " BA")
            self.letterGrade_comboBox.setItemText(3, " BB")
            self.letterGrade_comboBox.setItemText(4, " CB")
            self.letterGrade_comboBox.setItemText(5, " CC")
            self.letterGrade_comboBox.setItemText(6, " DC")
            self.letterGrade_comboBox.setItemText(7, " DD")
            self.letterGrade_comboBox.setItemText(8, " FF")
        else:
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")
            self.letterGrade_comboBox.addItem("")

            self.letterGrade_comboBox.setItemText(0, " ??")
            self.letterGrade_comboBox.setItemText(1, " BL")
            self.letterGrade_comboBox.setItemText(2, " BZ")

        self.horizontalLayout_5.addWidget(self.letterGrade_comboBox)
        self.horizontalLayout_10.addWidget(self.lectFeatures, 50 + eval(credit) * 10)
        self.horizontalLayout_10.addStretch(50 - eval(credit) * 10)

        self.lectureCode.setText("SECMELI")
        length = len(dersler)

        for x in range(length):
            # print("Çalışıyo")

            self.lectureName.setItemText(x, dersler[x])

        con = sqlite3.connect("MainLectures.db")
        cursor = con.cursor()
        cursor.execute("SELECT Grade FROM {} where Name = ?".format(self.dep), (self.name,))
        data = cursor.fetchall()
        cursor.execute("SELECT Chosen FROM {} where Name = ?".format(self.dep), (self.name,))
        data2 = cursor.fetchall()
        self.Chosen = str(data2[0])
        self.Chosen = self.Chosen.replace("(", "")
        self.Chosen = self.Chosen.replace(")", "")
        self.Chosen = self.Chosen.replace(",", "")
        self.Chosen = self.Chosen.replace("'", "")
        if self.Chosen != "":
            index = self.lectureName.findText(self.Chosen, QtCore.Qt.MatchFixedString)
            if index >= 0:
                self.lectureName.setCurrentIndex(index)

        self.letterGrade = str(data[0])
        self.letterGrade = self.letterGrade.replace("(", "")
        self.letterGrade = self.letterGrade.replace(")", "")
        self.letterGrade = self.letterGrade.replace(",", "")
        self.letterGrade = self.letterGrade.replace("'", "")

        if self.letterGrade == "":
            self.letterGrade = " ??"
        else:
            self.letterGrade = " " + self.letterGrade

        index = self.letterGrade_comboBox.findText(self.letterGrade, QtCore.Qt.MatchFixedString)
        if index >= 0:
            self.letterGrade_comboBox.setCurrentIndex(index)
            self.setColor()

        self.letterGrade_comboBox.currentTextChanged.connect(self.setColor)
        self.lectureName.currentTextChanged.connect(self.update_sname_to_db)

    def setColor(self):
        temp = self.letterGrade
        self.temp = temp
        k = 0
        t = 0
        if temp == " AA":
            k = 4
        elif temp == " BA":
            k = 3.5
        elif temp == " BB":
            k = 3
        elif temp == " CB":
            k = 2.5
        elif temp == " CC":
            k = 2
        elif temp == " DC":
            k = 1.5
        elif temp == " DD":
            k = 1

        self.letterGrade = self.letterGrade_comboBox.currentText()
        if self.letterGrade == " AA" or self.letterGrade == " BL":
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(AA))
            t = 4
        elif self.letterGrade == " BA":
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(BA))
            t = 3.5
        elif self.letterGrade == " BB":
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(BB))
            t = 3
        elif self.letterGrade == " CB":
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(CB))
            t = 2.5
        elif self.letterGrade == " CC":
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(CC))
            t = 2
        elif self.letterGrade == " DC":
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(DC))
            t = 1.5
        elif self.letterGrade == " DD":
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(DD))
            t = 1
        elif self.letterGrade == " FF" or self.letterGrade == " BZ":
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(FF))
        else:
            self.lectFeatures.setStyleSheet("background-color: rgb{};\n"
                                            "border-radius: 5px;".format(Undetermined))
        self.update_grade_to_db(self.letterGrade)

        con = sqlite3.connect("MainLectures.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM settings")
        data = cursor.fetchall()
        credit = data[0][0]
        gr = self.ui.blm_crdt
        gr2 = self.ui.cap_crdt
        #print(data[0][2])
        try:
            oldGpa = data[0][2]
            oldGpa = float(oldGpa)
            oldCredit = data[0][3]
            oldCredit = float(oldCredit)
            if temp != " ??":
                Credit = oldCredit - float(self.credit)
                if Credit == 0.0:
                    Gpa = 0.0
                else:
                    Gpa = (oldGpa * oldCredit - k * float(self.credit)) / Credit

                if self.letterGrade != " ??":
                    newCredit = Credit + float(self.credit)
                    newGpa = (Gpa * Credit + t * float(self.credit)) / newCredit
                    cursor.execute("Update settings set Gpa = ?, TotalCredit = ?", (newGpa, newCredit))
                    con.commit()
                    # print(newGpa, newCredit)
                    self.ui.gpaLabel.setText(str(abs(round(newGpa, 2))))
                else:
                    newCredit = Credit
                    newGpa = Gpa

                    cursor.execute("Update settings set Gpa = ?, TotalCredit = ?", (newGpa, newCredit))
                    con.commit()
                    # print(newGpa, newCredit)
                    if newCredit == 0.0:
                        self.ui.gpaLabel.setText("N/A")
                    else:
                        self.ui.gpaLabel.setText(str(abs(round(newGpa, 2))))

            else:
                if self.letterGrade != " ??":
                    newCredit = oldCredit + float(self.credit)
                    newGpa = (oldGpa * oldCredit + t * float(self.credit)) / newCredit
                    cursor.execute("Update settings set Gpa = ?, TotalCredit = ?", (newGpa, newCredit))
                    con.commit()
                    # print(newGpa, newCredit)
                    self.ui.gpaLabel.setText(str(abs(round(newGpa, 2))))
                else:
                    self.ui.gpaLabel.setText(str(abs(round(oldGpa, 2))))
        except:
            self.ui.gpaLabel.setText("N/A")
            cursor.execute("Update settings set Gpa = ?, TotalCredit = ?", ("0.0", "0.0"))
            con.commit()

        if self.temp != self.letterGrade and (self.temp == " ??" or self.letterGrade == " ??"):
            self.starter = 5
        else:
            self.starter = 0

        if self.starter != 0:
            if self.letterGrade != " ??":
                self.ui.blm_crdt += float(self.credit)
            else:
                self.ui.blm_crdt -= float(self.credit)

        self.ui.labelblm_crd.setText(str(self.ui.blm_crdt) + "/" + str(self.ui.total_dep_credit))

        if self.mstarter != 0:
            self.calculate(k, t, temp, gr, "depGpa")
        self.mstarter = 5

    def calculate(self, k, t, temp, gr, code):

        con2 = sqlite3.connect("Gpa.db")
        cursor2 = con2.cursor()

        try:
            oldGpa = None
            _gpa = 0.0
            if code == "depGpa":
                oldGpa = self.ui.blmgpa
            elif code == "capGpa":
                oldGpa = self.ui.capgpa

            oldCredit = gr
            if temp != " ??":
                Credit = oldCredit - float(self.credit)
                if Credit == 0.0:
                    Gpa = 0.0
                else:
                    Gpa = (oldGpa * oldCredit - k * float(self.credit)) / Credit

                if self.letterGrade != " ??":
                    newCredit = Credit + float(self.credit)
                    newGpa = (Gpa * Credit + t * float(self.credit)) / newCredit
                    _gpa = newGpa
                    # print(Gpa, Credit, t, self.credit, newCredit)
                    cursor2.execute("Update Gpa set {} = ?".format(code), (newGpa,))
                    con2.commit()
                    # print(newGpa, newCredit)
                    # self.ui.gpaLabel.setText(str(abs(round(newGpa, 2))))

                else:
                    newCredit = Credit
                    newGpa = Gpa
                    _gpa = newGpa
                    cursor2.execute("Update Gpa set {} = ?".format(code), (newGpa,))
                    con2.commit()
                    # print(newGpa, newCredit)
                    if newCredit == 0.0:
                        _gpa = 0.0
                        cursor2.execute("Update Gpa set {} = ?".format(code), ("0.0",))
                        con2.commit()
                        pass  # self.ui.gpaLabel.setText("N/A")
                    else:
                        pass  # self.ui.gpaLabel.setText(str(abs(round(newGpa, 2))))

            else:
                if self.letterGrade != " ??":
                    newCredit = oldCredit + float(self.credit)
                    newGpa = (oldGpa * oldCredit + t * float(self.credit)) / newCredit
                    _gpa = newGpa
                    cursor2.execute("Update Gpa set {} = ?".format(code), (newGpa,))
                    con2.commit()
                    # print(newGpa, newCredit)

                    # self.ui.gpaLabel.setText(str(abs(round(newGpa, 2))))
                else:
                    pass  # self.ui.gpaLabel.setText(str(abs(round(oldGpa, 2))))

            if code == "depGpa":
                self.ui.blmgpa = _gpa
                if self.ui.blm_crdt == 0.0:
                    self.ui.label_blmort.setText("N/A")
                else:
                    self.ui.label_blmort.setText(str(abs(round(self.ui.blmgpa, 2))))
            elif code == "capGpa":
                self.ui.capgpa = _gpa
                if self.ui.cap_crdt == 0.0:
                    self.ui.label_caport.setText("N/A")
                else:
                    self.ui.label_caport.setText(str(abs(round(self.ui.capgpa, 2))))
        except:
            #self.ui.gpaLabel.setText("N/A")
            cursor2.execute("Update Gpa set {} = ?".format(code), ("0.0",))
            con2.commit()
            if code == "depGpa":
                self.ui.blmgpa = 0.0
            elif code == "capGpa":
                self.ui.capgpa = 0.0

    def update_grade_to_db(self, currentText):
        currentText = currentText.strip(" ")
        con = sqlite3.connect("MainLectures.db")
        cursor = con.cursor()
        if currentText == "??":
            cursor.execute("Update {} set Grade = ? where Name = ?".format(self.dep), ("", self.name))
        else:
            cursor.execute("Update {} set Grade = ? where Name = ?".format(self.dep), (currentText, self.name))
        con.commit()

    def update_sname_to_db(self):
        con = sqlite3.connect("MainLectures.db")
        cursor = con.cursor()
        cursor.execute("Update {} set Chosen = ? where Name = ?".format(self.dep),
                       (self.lectureName.currentText(), self.name))
        con.commit()


class archivedLecture(QtWidgets.QFrame):

    def __init__(self, crn, kod, ad, hoca, gun, saat, doluluk, ui):
        super().__init__()
        b = gun.split("\n")
        b = len(b)
        if b == 4:
            b = 107
        elif b == 5:
            b = 150
        else:
            b = 80

        t = str()
        hoca = hoca.replace("  ", " ")
        if "," in hoca:
            hocalar = hoca.split(",")
            if "" in hocalar:
                hocalar.remove("")
            for i in hocalar:
                i = i.lstrip(" ")
                t += i + ",\n"
            t = t.rstrip(",\n")

        elif len(hoca) > 17:

            g = hoca.split(" ")
            copy = g.copy()
            for i in copy:
                m = t
                if i != copy[0]:
                    t += " "
                t += i

                if len(t) > 17:
                    t = m

                    break
                g.remove(i)
            t += "\n"

            for i in g:
                if i != g[0]:
                    t += " "
                t += i

        else:
            t = hoca

        tt = str()
        ad = ad.replace("  ", " ")
        ad = ad.replace(",", ", ")
        ad = ad.replace(".", ". ")
        if len(ad) > 16:
            g = ad.split(" ")
            copy = g.copy()
            for i in copy:
                m = tt
                if i != copy[0]:
                    tt += " "
                tt += i

                if len(tt) > 16:
                    tt = m

                    break
                g.remove(i)
            tt += "\n"

            for i in g:
                if i != g[0]:
                    tt += " "
                tt += i

        else:
            tt = ad

        self.setMinimumSize(QtCore.QSize(0, b))
        self.setMaximumSize(QtCore.QSize(16777215, b))
        self.setStyleSheet("background: transparent;")
        self.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.horizontalLayout_1441 = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout_1441.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_1441.setSpacing(14)
        self.horizontalLayout_1441.setObjectName("horizontalLayout_1441")
        self.label00 = QtWidgets.QLabel(self)
        self.label00.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label00.setFont(font)
        self.label00.setObjectName("label00")
        self.horizontalLayout_1441.addWidget(self.label00)
        self.label01 = QtWidgets.QLabel(self)
        self.label01.setMaximumSize(QtCore.QSize(115, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label01.setFont(font)
        self.label01.setObjectName("label01")
        self.horizontalLayout_1441.addWidget(self.label01)
        self.label04 = QtWidgets.QLabel(self)
        self.label04.setMinimumSize(QtCore.QSize(0, 0))
        self.label04.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label04.setFont(font)
        self.label04.setObjectName("label04")
        self.horizontalLayout_1441.addWidget(self.label04)
        self.label02 = QtWidgets.QLabel(self)
        self.label02.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label02.setFont(font)
        self.label02.setObjectName("label02")
        self.horizontalLayout_1441.addWidget(self.label02)
        self.label03 = QtWidgets.QLabel(self)
        self.label03.setMaximumSize(QtCore.QSize(105, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label03.setFont(font)
        self.label03.setObjectName("label03")
        self.horizontalLayout_1441.addWidget(self.label03)
        self.label05 = QtWidgets.QLabel(self)
        self.label05.setMaximumSize(QtCore.QSize(105, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label05.setFont(font)
        self.label05.setObjectName("label05")
        self.horizontalLayout_1441.addWidget(self.label05)
        self.label06 = QtWidgets.QLabel(self)
        self.label06.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label06.setFont(font)
        self.label06.setObjectName("label06")
        self.horizontalLayout_1441.addWidget(self.label06)
        #spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        #self.verticalLayout_2064.addItem(spacerItem2)

        #self.label05.setStyleSheet("border: 2px solid white;\n color: white;")

        self.label00.setStyleSheet("color: rgb{};".format(ui.text_color2))
        self.label01.setStyleSheet("color: rgb{};".format(ui.text_color2))
        self.label02.setStyleSheet("color: rgb{};".format(ui.text_color2))
        self.label03.setStyleSheet("color: rgb{};".format(ui.text_color2))
        self.label04.setStyleSheet("color: rgb{};".format(ui.text_color2))
        self.label05.setStyleSheet("color: rgb{};".format(ui.text_color2))
        self.label06.setStyleSheet("color: rgb{};".format(ui.text_color2))

        self.label00.setText(crn)
        self.label01.setText(kod)
        self.label04.setText(tt)
        self.label02.setText(t)
        self.label03.setText(gun)
        self.label05.setText(saat)
        self.label06.setText(doluluk)
