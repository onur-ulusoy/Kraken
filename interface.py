from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QBrush, QColor
import resource
import sys
import sqlite3
import uiClasses
import uiFunctions
import uuid
import json
import random
import os
import time
import datetime
import smtplib


class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.items = {}
        self.crn_list = list()
        self.changed = False
        self.name = "MainWindow"
        self.setWindowIcon(QtGui.QIcon(":/terminal/windowicon.png"))
        self.translate = {"Profil": ("Profil", "Profile", "Profil")
            , "Tamam": ("Tamam", "OK", "OK")
            , "Hata": ("Hata", "Error", "Error")
            , "Kaydet": ("Kaydet", "Save", "Sparen")
            , "Kaydetme": ("Kaydetme", "Don't Save", "Sparen Nicht")
            , "Değişiklikleri Kaydet?": ("Değişiklikleri Kaydet?", "Save Changes", "Sparen den Änderungen")
            , "Ders Çakışması": ("Ders Çakışması", "Overlap Courses", "Kursüberschneidung")
            , "Çakıştığı 2 Dersi Sil": ("Çakıştığı 2 Dersi Sil", "Delete Both", "Lösche Beide")
            , "Bu ders programı açılamadı. Bu program güncel değil veya Courses.db dosyası silinmiş.": ("Kayıtlı ders programı açılamadı. Bu tablo sol altta görülen güncel dönemin veritabanıyla yapılmamış. Kayıtlı tablolar sadece yapıldığı dönemin veritabanıyla görüntülenebilir.", "Saved schedule could not be opened. This table was not made with the database of current term seen in bottom left. Saved tables can only be opened with the database that it was made.", "Gespeicherter Zeitplan konnte nicht geöffnet werden. Diese Tabelle wurde nicht mit der Datenbank des aktuellen Begriffs erstellt, die unten links zu sehen ist. Gespeicherte Tabellen können nur mit der erstellten Datenbank geöffnet werden.")
            , "{} Sil": ("{} Sil", "Delete {}", "Löschen {}")
            , "Programda kaydedilmemiş değişiklikler var kaydetmek istiyor musun?": ("Programda kaydedilmemiş değişiklikler var kaydetmek istiyor musun?", "Do you want to save any unsaved changes in the table?", "Möchten Sie nicht gespeicherte Änderungen in der Tabelle speichern")
            , "{} dersini zaten seçtin!": ("{} dersini zaten seçtin!", "You have already selected a {} course.", "Sie haben bereits einen {} Kurs ausgewählt.")
            , "Bu ders {} ile çakışıyor. Bu ders programa eklenmeyecek.": (
                "Bu ders {} ile çakışıyor. Bu ders programa eklenmeyecek.",
                "This lesson overlaps with {}. This course will not be added to the schedule.", "Diese Lektion überschneidet sich mit {}. Dieser Kurs wird nicht in den Zeitplan aufgenommen.")
            , "Bu ders {} ve {} ile çakışıyor. Bu ders programa eklenmeyecek.": (
                "Bu ders {} ve {} ile çakışıyor. Bu ders programa eklenmeyecek.",
                "This lesson overlaps with {} and {}. This course will not be added to the schedule.", "Diese Lektion überschneidet sich mit {} und {}. Dieser Kurs wird nicht in den Zeitplan aufgenommen.")
            , "Aynı Ders": ("Aynı Ders", "Duplicate Course", "Doppelter Kurs")
            , "Ders Programı": ("Ders Programı", "Schedule", "Zeitplan")
            , "Yemekhane": ("Yemekhane", "Cafeteria", "Cafeteria")
            , "Akd. Takvim": ("Akd. Takvim", "Acd. Calendar", "Akd. Kalender")
            , "| AKD. TAKVİM": ("| AKD. TAKVİM", "| ACD. CALENDAR", "| AKD. KALENDER")
            , "| YEMEKHANE": ("| YEMEKHANE", "| CAFETERIA", "| CAFETERIA")
            , "| HAKKIMIZDA": ("| HAKKIMIZDA", "| ABOUT US", "ÜBER UNS")
            , "Ana Sayfa": ("Ana Sayfa", "Main Menu", "Hauptmenü")
            , "Hakkımızda": ("Hakkımızda", "About Us", "Über Uns")
            , "Yeni Kısayol": ("Yeni Kısayol", "New Shortcut", "Neue Verknüpfung")
            , "Tema": ("Tema", "Theme", "Thema")
            , "Dil & Bölge": ("Dil & Bölge", "Language", "Sprache")
            , "İpuçlarını göster": ("İpuçlarını göster", "Show tooltips", "Tooltipps anzeigen")
            , "Yazı Rengi": ("Yazı Rengi", "Font Color", "Schriftfarbe")
            , "Kısayollar": ("Kısayollar", "Shortcuts", "Verknüpfungen")
            , "Kısayol Ekle/Çıkar": ("Kısayol Ekle/Çıkar", "Add/Remove Shortcuts", "Verknüpfungen hinzufügen/entfernen")
            , "| ANA SAYFA": ("| ANA SAYFA", "| MAIN MENU", "HAUPTMENU")
            , "| DERS PROGRAMI": ("| DERS PROGRAMI", "| SCHEDULE", "| ZEITPLAN")
            , "Derslerim": ("Derslerim", "My Lectures", "Meine Vorträge")
            , "1. Sınıf": ("1. Sınıf", "1st Class", "1. Klasse")
            , "2. Sınıf": ("2. Sınıf", "2nd Class", "2. Klasse")
            , "3. Sınıf": ("3. Sınıf", "3rd Class", "3. Klasse")
            , "4. Sınıf": ("4. Sınıf", "4th Class", "4. Klasse")
            , "Ekstra ders": ("Ekstra ders", "Extras", "Extra Lektion")
            , "Tamirat modülünü çalıştır": ("Tamirat modülünü çalıştır", "Run repair module", "Reparaturmodul ausführen")
            , "Ders Ekle": ("Ders Ekle", "Add Lecture", "Vortrag hinzufügen")
            , "ÇAP/YANDAL": ("ÇAP/YANDAL", "DM/Minor", "DM/Geringer")
            , "BÖLÜM KODU": ("BÖLÜM KODU", "DEPARTMENT", "ABTEILUNG")
            , "Bölüm kodu": ("Bölüm kodu", "Department", "Abteilung")
            , "İTÜ Web Site trafiği çok yoğun olduğundan ders güncellemesi tamamlanamadı. Lütfen daha sonra tekrar deneyin.": ("İTÜ Web Site trafiği çok yoğun olduğundan ders güncellemesi tamamlanamadı. Lütfen daha sonra tekrar deneyin.", "Course update could not be completed due to heavy ITU Web Site traffic. Please try again later", "Die Kursaktualisierung konnte aufgrund des starken Verkehrs auf der ITU-Website nicht abgeschlossen werden. Bitte versuchen Sie es später erneut.")
            , "Güncelleniyor...": ("Güncelleniyor...", "Updating...", "Aktualisierung...")
            , "Bir sorun oluştu.": ("Bir sorun oluştu.", "An error occurred.", "Ein Fehler ist aufgetreten.")
            , "Ders programı yapmak için kullan": ("Ders programı yapmak için kullan", "Use to create a schedule", "Verwenden um Zeitplan zu erstellen")
            , "Veritabanlarını güncelle": ("Veritabanlarını güncelle", "Update databases", "Datenbanken aktualisieren")
            , "Seçili döneme ait veritabanını ders programına aktararak o dönemin dersleriyle program yapmaya imkan verir.": ("Seçili döneme ait veritabanını ders programına aktararak o dönemin dersleriyle program yapmaya imkan verir.", "Allows to create schedule with the courses of selected term by transferring its database to the schedule", "Ermöglicht die Erstellung eines Stundenplans mit den Kursen des ausgewählten Semesters, indem seine Datenbank in den Stundenplan übertragen wird")
            , "Eski dönemlere ait veritabanlarını internet kullanarak günceller. Yeni dönem varsa eklenir.": ("Eski dönemlere ait veritabanlarını internet kullanarak günceller. Yeni dönem varsa eklenir.", "Updates databases of old terms using the Internet. New terms are added if they are exists.", "Aktualisiert Datenbanken alter Perioden über das Internet. Neue Begriffe werden hinzugefügt, wenn sie vorhanden sind.")
            , "İTÜ Web sayfasından şuanki ders programlarını indirerek eski veritabanıyla değiştirir.": ("İTÜ Web sayfasından şuanki ders programlarını indirerek eski veritabanıyla değiştirir.", "Downloads the current course schedules from the ITU Web page and replaces them with the old database.", "Es lädt die aktuellen Kursprogramme von der ITU-Webseite herunter und ersetzt sie durch die alte Datenbank.")
            , "| PROFİL": ("| PROFİL", "| PROFILE", "| PROFIL")
            , "(Kaldır)": ("(Kaldır)", "(Remove)", "(Entfernen)")
            , "(Ekle)": ("(Ekle)", "(Add)", "(Hinzufügen)")
            , "Öğretim Üyesi": ("Öğretim Üyesi", "Instructor", "Lehrer")
            , "Gün": ("Gün", "Day", "Tag")
            , "Saat": ("Saat", "Time", "Zeit")
            , "Doluluk": ("Doluluk", "Occupacy", "Belegung")
            , "Bölüm": ("Bölüm", "Department", "Abteilung")
            , "Ders Adı": ("Ders Adı", "Course Name", "Kursname")
            , "Ders Kodu": ("Ders Kodu", "Course Code", "Kurscode")
            , "Açılmış Dersler": ("Açılmış Dersler", "Open Courses", "Offene Kurse")
            , "BÖLÜM": ("BÖLÜM", "DEPARTMENT", "ABTEILUNG")
            , "DERS ADI": ("DERS ADI", "LECTURE NAME", "VORLESUNGSNAME")
            , "SEÇİLEN DERS": ("SEÇİLEN DERS", "SELECTED COURSE", "AUSGEWÄHLTER KURS")
            , "Seç": ("Seç", "Select", "Wählen")
            , "Tabloyu Kaydet": ("Tabloyu Kaydet", "Save the Schedule", "Speichern den Zeitplan")
            , "Pazartesi": ("Pazartesi", "Monday", "Montag")
            , "Salı": ("Salı", "Tuesday", "Dienstag")
            , "Çarşamba": ("Çarşamba", "Wednesday", "Mittwoch")
            , "Perşembe": ("Perşembe", "Thursday", "Donnerstag")
            , "Cuma": ("Cuma", "Friday", "Freitag")
            , "Dönem": ("Dönem", "Term", "Zeitraum")
            , "Ders Arşivi": ("Ders Arşivi", "Course Archive", "Kursarchiv")
            , "| DERS ARŞİVİ": ("| DERS ARŞİVİ", "| COURSE ARCHIVE", "| KURSARCHIV")
            , "Mesajınız iletilmiştir.": ("Mesajınız iletilmiştir.", "Your message has been sent.", "Ihre Nachricht wurde gesendet.")
            , "Gönder": ("Gönder", "Submit", "Vorlegen")
            , "Görüş ve önerileriniz:": ("Görüş ve önerileriniz:", "Your comments and suggestions:", "Ihre Kommentare und Vorschläge:")
            , "İnternet bağlantısı gereklidir!": ("İnternet bağlantısı gereklidir!", "Internet connection is required!", "Internetverbindung ist erforderlich!")
            , "Akademik takvimin görüntülenebilmesi için internet bağlantısı gereklidir.": ("Akademik takvimin görüntülenebilmesi için internet bağlantısı gereklidir.", "In order to display academic calendar, Internet connection is required.", "Um den Akademischer Kalender anzuzeigen, ist eine Internetverbindung erforderlich.")
            , "Dersi alabilen programlar:": ("Dersi alabilen programlar:", "Major restriction:", "Hauptbeschränkung:")
            , "Dersin önşartları:": ("Dersin önşartları:", "Prerequisites:", "Grundanforderungen:")
            , "Sınıf önşartı:": ("Sınıf önşartı:", "Class restriction:", "Klassenbeschränkung:")
            , "İnternet yok": ("İnternet yok", "no Internet", "kein Internet")
            , "Toplam kredinin görülebilmesi için internet bağlantısı gereklidir.": ("Toplam kredinin görülebilmesi için internet bağlantısı gereklidir.", "In order to display total credit, Internet connection is required.", "Um das Gesamtguthaben anzuzeigen, ist eine Internetverbindung erforderlich.")
            , "Toplam Kredi:": ("Toplam Kredi:", "Total Credits:", "Gesamt Credits:")
            , "1.anadal ortalaması": ("1.anadal ortalaması", "Average point of first major", "Durchschnittspunkt des ersten Hauptfachs")
            , "2.anadal/yandal ortalaması": ("2.anadal/yandal ortalaması", "Average point of second major/minor", "Durchschnittspunkt des zweiten Dur/Moll")
            , "1.anadal başarılan kredi": ("1.anadal başarılan kredi", "First major credit achieved", "Erster großer Kredit erreicht")
            , "2.anadal/yandal başarılan kredi": ("2.anadal/yandal başarılan kredi", "Second major/minor credit achieved", "Zweiter Haupt/Nebenkredit erreicht")
            , "Genel puan ortalaması": ("Genel puan ortalaması", "General point average", "allgemeiner Punktdurchschnitt")
            , "ÖĞLE YEMEĞİ": ("ÖĞLE YEMEĞİ", "LUNCH MENU", "MITTAGSMENÜ")
            , "AKŞAM YEMEĞİ": ("AKŞAM YEMEĞİ", "DINNER MENU", "ABENDMENÜ")
            , "Akşam yemeği bilgisi girilmemiş": ("Akşam yemeği bilgisi girilmemiş", "No dinner menu", "Kein Abendmenü")
            , "Öğle yemeği bilgisi girilmemiş": ("Öğle yemeği bilgisi girilmemiş", "No lunch menu", "Kein Mittagsmenü")
            , "CRN listesi:": ("CRN listesi:", "CRN list:", "CRN liste:")
            , "JS kodu:": ("JS kodu:", "JS code:", "JS code:")
            , "Dosyayı kaydet": ("Dosyayı kaydet", "Save the file", "Speicher die Datei")
            , "Ekstra ders ekle": ("Ekstra ders ekle", "Add extra lecture", "Zusätzliche vorlesung hinzufügen")
            , "Dersleri güncelle": ("Dersleri güncelle", "Update courses", "Kurse aktualisieren")
            , "Tabloyu sil": ("Tabloyu sil", "Delete the table", "Tabelle löschen")
            , "güncellendi.": ("güncellendi.", "is updated.", "aktualisiert.")
            , "Tüm dersler güncellendi.": ("Tüm dersler güncellendi.", "All courses updated", "Alle kurse werden aktualisiert.")
            , "Tamamı güncellendi.": ("Tamamı güncellendi.", "All updated.", "Alles aktualisiert.")
            , "CRN işlemleri": ("CRN işlemleri", "CRN operations", "CRN operationen")
            , "CRN listesini belleğe kopyala": ("CRN listesini belleğe kopyala", "Copy CRN list to the clipboard", "Kopieren Sie die CRN Liste in die Zwischenablage")
            , "JS kodunu belleğe kopyala": ("JS kodunu belleğe kopyala", "Copy JS code to the clipboard", "Kopieren Sie den JS code in die Zwischenablage")
            , "CRN bilgilerini bilgisayara kaydet": (
                "CRN bilgilerini bilgisayara kaydet", "Save CRN data to the computer", "Speichern Sie CRN daten auf dem Computer")
            , "Tablonun resmini bilgisayara kaydet": (
                "Tablonun resmini bilgisayara kaydet", "Save the picture of table to the computer", "Speichern Sie das Bild der Tabelle auf dem Computer")
            , "Tablo ismi": ("Tablo ismi", "Table name", "Tabellenname")}

        # Default theme = 1
        """ 
        self.primer_color = (27, 29, 35)
        self.hover = (33, 37, 43)
        self.pressed = (85, 170, 255)
        self.pressed2 = (85, 170, 255)
        self.seconder_color = (39, 44, 54)
        self.seconder_color2 = (39, 44, 54)
        self.text_color = (255, 255, 255)
        self.text_color2 = (255, 255, 255)
        self.info_color = (98, 103, 111)
        self.tab_background = (50, 52, 57, 1)
        self.selected = (50, 52, 57, 1)
        self.tab_min_background = (95, 97, 101, 1)
        self.scrollprimer = (95, 97, 101, 1)
        self.scrollseconder = (50, 52, 57, 1)
        self.hover2 = (52, 59, 72)
        self.hover3 = (33, 37, 43)
        self.adl = (255, 255, 255, 100)
        self.adlhover = (255, 255, 255, 150)
        self.border = "none"
        """
        self.tabName = "| ANA SAYFA"
        uiFunctions.apply_preferences(self)

        if self.language == "TR":
            self.languageNumber = 0
        elif self.language == "EN":
            self.languageNumber = 1
        elif self.language == "DE":
            self.languageNumber = 2

        self.soup = None
        self.updating = False
        self.startTime()
        self.table_credit = 0.0
        self.noInternet = False
        self.programDeleted = False

        self.initUi("Profil", "Ders Programı", "Yemekhane", "Akd. Takvim", "Ders Arşivi", "Ana Sayfa", "Hakkımızda")  # ==> TABS OF THE MENU

        self.exit_button.clicked.connect(self.frame.btn_close_clicked)
        self.minimize_button.clicked.connect(self.frame.btn_min_clicked)
        self.maximize_button.clicked.connect(self.frame.maximize_restore)

        self.menu_open = False
        self.menu_button.clicked.connect(self.show_menu)
        self.settings_open = False
        self.settingsButton.clicked.connect(self.show_settings)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: rgb{};".format(self.primer_color))
        self.total_dep_credit = 0.0
        self.total_cap_credit = 0.0
        self.blm_crdt = 0.0
        self.cap_crdt = 0.0
        self.ders_kodu_list = list()
        self.tablosuz_dersler = list()
        con = sqlite3.connect("Gpa.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM Gpa")
        data = cursor.fetchall()
        self.blmgpa = float(data[0][0])
        self.capgpa = float(data[0][1])

        if self.blmgpa == 0.0:
            self.label_blmort.setText("N/A")
        else:
            self.label_blmort.setText(str(round(self.blmgpa, 2)))

        if self.capgpa == 0.0:
            self.label_caport.setText("N/A")
        else:
            self.label_caport.setText(str(round(self.capgpa, 2)))


        self._gripSize = 3  # ==> THICKNESS OF THE RESIZING FRAME
        self.sideGrips = [
            SideGrip(self, QtCore.Qt.LeftEdge),
            SideGrip(self, QtCore.Qt.TopEdge),
            SideGrip(self, QtCore.Qt.RightEdge),
            SideGrip(self, QtCore.Qt.BottomEdge),
        ]

        self.cornerGrips = [QtWidgets.QSizeGrip(self) for i in range(4)]

        for i in self.cornerGrips:
            i.setStyleSheet("background-color: rgb{};".format(self.primer_color))

    @property
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        self.setContentsMargins(*[self.gripSize] * 4)

        outRect = self.rect()
        inRect = outRect.adjusted(self.gripSize, self.gripSize,
                                  -self.gripSize, -self.gripSize)

        self.cornerGrips[0].setGeometry(
            QtCore.QRect(outRect.topLeft(), inRect.topLeft()))

        self.cornerGrips[1].setGeometry(
            QtCore.QRect(outRect.topRight(), inRect.topRight()).normalized())

        self.cornerGrips[2].setGeometry(
            QtCore.QRect(inRect.bottomRight(), outRect.bottomRight()))

        self.cornerGrips[3].setGeometry(
            QtCore.QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

        self.sideGrips[0].setGeometry(
            0, inRect.top(), self.gripSize, inRect.height())

        self.sideGrips[1].setGeometry(
            inRect.left(), 0, inRect.width(), self.gripSize)

        self.sideGrips[2].setGeometry(
            inRect.left() + inRect.width(),
            inRect.top(), self.gripSize, inRect.height())

        self.sideGrips[3].setGeometry(
            self.gripSize, inRect.top() + inRect.height(),
            inRect.width(), self.gripSize)

    def resizeEvent(self, event):
        QtWidgets.QWidget.resizeEvent(self, event)
        self.updateGrips()

    def rebuildTable(self, dat):
        self.tableWidget.clearContents()
        self.tableWidget.clearSpans()
        self.ders_kodu_list = list()

        for i in self.tablosuz_dersler:
            self.ders_kodu_list.append(i)

        for i, k in dat.items():
            if k != {} and "coordinates" in k:
                if k["coordinates"] == {} or "c" in k:
                    continue
            else:
                continue

            if "crn" in k:
                #print("ever crn mevcut")
                if k["crn"] != {}:
                    #print("OKEYYyyy")
                    con = sqlite3.connect("Courses.db")
                    cursor = con.cursor()
                    cursor.execute(
                        "SELECT CRN, CourseCode, CourseTitle, Day, Time, Instructor FROM {} WHERE CRN = '{}'".format(
                            k["dep"],
                            k["crn"]))
                    data = cursor.fetchall()
                    ders_kodu = data[0][1].split()
                    self.ders_kodu_list.append(ders_kodu)

                    #print(data)
                    #print("ekliyom bekle")
                    #print(type(data[0][3]))
                    if len(json.loads(data[0][3])) == 1:
                        self.tableWidget.setSpan(json.loads(data[0][4])[0] - 1, json.loads(data[0][3])[0] - 1,
                                                 len(json.loads(data[0][4])), 1)

                        ders = QtWidgets.QTableWidgetItem(
                            data[0][0] + "\n" + data[0][1] + "\n" + data[0][2] + "\n" + data[0][5])
                        #print("1")

                        font = QtGui.QFont()
                        font.setPointSize(11)

                        ders.setFont(font)
                        ders.setTextAlignment(QtCore.Qt.AlignCenter)
                        ders.setForeground(QBrush(QColor(255, 255, 255)))

                        #print("2")
                        ders.setBackground(
                            (QBrush(
                                QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255),
                                       200))))
                        #print("3")
                        self.tableWidget.setItem(json.loads(data[0][4])[0] - 1, json.loads(data[0][3])[0] - 1,
                                                 ders)

                        #print("4")
                    else:
                        color = QColor(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), 200)
                        #print("ÇOK GÜNLÜ")
                        for d in range(len(json.loads(data[0][3]))):
                            day = json.loads(data[0][3])[d]
                            #print("GÜN ", day)
                            self.tableWidget.setSpan(json.loads(data[0][4])[d][0] - 1, day - 1,
                                                     len(json.loads(data[0][4])[d]), 1)

                            ders = QtWidgets.QTableWidgetItem(
                                data[0][0] + "\n" + data[0][1] + "\n" + data[0][2] + "\n" + data[0][5])
                            #print("1")

                            font = QtGui.QFont()
                            font.setPointSize(11)

                            ders.setFont(font)
                            ders.setTextAlignment(QtCore.Qt.AlignCenter)
                            ders.setForeground(QBrush(QColor(255, 255, 255)))

                            #print("2")
                            ders.setBackground(
                                QBrush(
                                    color))
                            #print("3")
                            self.tableWidget.setItem(json.loads(data[0][4])[d][0] - 1, day - 1,
                                                     ders)
        self.table_credit = 0.0
        self.start_gettingCredit(self.ders_kodu_list)


    def start_gettingCredit(self, code_list):
        self.creditThread = uiFunctions.credit_Thread(code_list)
        self.creditThread.change_value.connect(self.setVal)
        self.creditThread.start()

    def setVal(self, val):
        if val[0] == -1:
            self.table_credit = -1
            self.credit_label.setText(
                self.translate["Toplam Kredi:"][self.languageNumber] + " " + self.translate["İnternet yok"][self.languageNumber])
            self.credit_label.setToolTip(self.translate["Toplam kredinin görülebilmesi için internet bağlantısı gereklidir."][self.languageNumber])

        if len(val[1]) == len(self.ders_kodu_list):
            self.credit_label.setToolTip("")
            self.table_credit = val[0]
            self.credit_label.setText(self.translate["Toplam Kredi:"][self.languageNumber] + " " + str(self.table_credit))


    def initUi(self, *tabNames):
        self.setObjectName("MainWindow")
        self.resize(1060, 666)
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.left_frame = QtWidgets.QFrame(self.centralwidget)
        self.left_frame.setMinimumSize(QtCore.QSize(70, 0))
        self.left_frame.setMaximumSize(QtCore.QSize(70, 16777215))
        self.left_frame.setStyleSheet("background-color: rgb{};".format(self.primer_color))
        self.left_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.left_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.left_frame.setObjectName("left_frame")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.left_frame)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.menu_button = QtWidgets.QPushButton(self.left_frame)
        self.menu_button.setMinimumSize(QtCore.QSize(70, 65))
        self.menu_button.setMaximumSize(QtCore.QSize(70, 65))
        self.menu_button.setStyleSheet("QPushButton {\n"
                                       "    background-image: url(:/menu/menu.png);\n"
                                       "    background-position: center;\n"
                                       "    background-repeat: no-repeat;\n"
                                       "    border: none;\n"
                                       "    background-color: rgb" + str(self.primer_color) + ";\n"
                                                                                              "}\n"
                                                                                              "QPushButton:hover {\n"
                                                                                              "    background-color: rgb" + str(
            self.hover) + ";\n"
                          "}\n"
                          "QPushButton:pressed {    \n"
                          "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                            "}")
        self.menu_button.setText("")
        self.menu_button.setObjectName("menu_button")
        self.verticalLayout_4.addWidget(self.menu_button)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem)

        self.frame_3 = QtWidgets.QFrame(self.left_frame)
        self.frame_3.setMinimumSize(QtCore.QSize(70, 80))
        self.frame_3.setMaximumSize(QtCore.QSize(70, 80))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setContentsMargins(3, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.user_icon_label = QtWidgets.QPushButton(self.frame_3)
        self.user_icon_label.setMinimumSize(QtCore.QSize(60, 60))
        self.user_icon_label.setMaximumSize(QtCore.QSize(60, 60))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.user_icon_label.setFont(font)
        self.user_icon_label.setAutoFillBackground(False)
        self.user_icon_label.setStyleSheet("QPushButton {\n"
                                           "    background-position: center;\n"
                                           "    background-repeat: no-repeat;\n"
                                           "    border-radius: 30px;\n"
                                           "    border: 5px solid rgb" + str(self.seconder_color) + ";\n"
                                                                                                    "    background-color: rgb" + str(
            self.seconder_color2) + ";\n"
                                    "    color: rgb" + str(self.text_color) + ";\n"
                                                                              "}"
                                                                              "QPushButton:hover {\n"
                                                                              "    background-color: rgb" + str(
            self.hover) + ";\n"
                          "}"
                          "QPushButton:pressed {"
                          "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                            "}")
        # self.user_icon_label.setAlignment(QtCore.Qt.AlignCenter)
        self.user_icon_label.setObjectName("user_icon_label")
        self.verticalLayout_3.addWidget(self.user_icon_label)
        self.verticalLayout_4.addWidget(self.frame_3)
        self.frame_3 = QtWidgets.QFrame(self.left_frame)
        self.frame_3.setMinimumSize(QtCore.QSize(70, 70))
        self.frame_3.setMaximumSize(QtCore.QSize(70, 70))
        self.frame_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setContentsMargins(0, 3, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_7")
        self.main_menu_button = QtWidgets.QPushButton(self.left_frame)
        self.main_menu_button.setMinimumSize(QtCore.QSize(70, 65))
        self.main_menu_button.setMaximumSize(QtCore.QSize(70, 65))
        self.main_menu_button.setStyleSheet("QPushButton {\n"
                                            "    background-image: url(:/menu/home.png);\n"
                                            "    background-position: center;\n"
                                            "    background-repeat: no-reperat;\n"
                                            "    border: none;\n"
                                            "    background-color: rgb" + str(self.primer_color) + ";\n"
                                                                                                   "}\n"
                                                                                                   "QPushButton:hover {\n"
                                                                                                   "    background-color: rgb" + str(
            self.hover) + ";\n"
                          "}\n"
                          "QPushButton:pressed {    \n"
                          "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                            "}")
        self.main_menu_button.setText("")
        self.main_menu_button.setObjectName("main_menu_button")
        self.verticalLayout_4.addWidget(self.main_menu_button)
        self.settingsButton = QtWidgets.QPushButton(self.frame_3)
        self.settingsButton.setMinimumSize(QtCore.QSize(70, 65))
        self.settingsButton.setMaximumSize(QtCore.QSize(70, 65))
        self.settingsButton.setStyleSheet("QPushButton {\n"
                                          "    background-image: url(:/menu/settings.png);\n"
                                          "    background-position: center;\n"
                                          "    background-repeat: no-reperat;\n"
                                          "    border: none;\n"
                                          "    background-color: rgb" + str(self.primer_color) + ";\n"
                                                                                                 "}\n"
                                                                                                 "QPushButton:hover {\n"
                                                                                                 "    background-color: rgb" + str(
            self.hover) + ";\n"
                          "}\n"
                          "QPushButton:pressed {    \n"
                          "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                            "}")
        self.settingsButton.setText("")
        self.settingsButton.setObjectName("settingsButton")
        self.verticalLayout_3.addWidget(self.settingsButton)
        self.verticalLayout_4.addWidget(self.frame_3)
        self.horizontalLayout_9.addWidget(self.left_frame)
        self.right_frame = QtWidgets.QFrame(self.centralwidget)
        self.right_frame.setEnabled(True)
        self.right_frame.setMinimumSize(QtCore.QSize(990, 666))
        self.right_frame.setStyleSheet("background-color: rgb{}".format(self.primer_color))
        self.right_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.right_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.right_frame.setObjectName("right_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.right_frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = FrameTitleBar(self)
        self.frame.window = self
        self.frame.setMinimumSize(QtCore.QSize(10, 43))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 43))
        self.frame.setStyleSheet("background-color: rgb{}".format(self.primer_color))
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.terminal_label = QtWidgets.QLabel(self.frame)
        self.terminal_label.setMinimumSize(QtCore.QSize(16, 16))
        self.terminal_label.setMaximumSize(QtCore.QSize(16, 16))
        self.terminal_label.setStyleSheet("\n"
                                          "background: transparent;\n"
                                          "background-image: url(:/terminal/k.png);\n"
                                          "background-position: center;\n"
                                          "background-repeat: no-repeat;\n"
                                          "")
        self.terminal_label.setText("")
        self.terminal_label.setObjectName("terminal_label")
        self.horizontalLayout_2.addWidget(self.terminal_label)
        self.top_label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.top_label.setFont(font)
        self.top_label.setStyleSheet("background: transparent;\n"
                                     "color:rgb" + str(self.text_color) + ";\n"
                                                                          "\n"
                                                                          "")
        self.top_label.setObjectName("top_label")
        self.horizontalLayout_2.addWidget(self.top_label)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.minimize_button = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.minimize_button.sizePolicy().hasHeightForWidth())
        self.minimize_button.setSizePolicy(sizePolicy)
        self.minimize_button.setMinimumSize(QtCore.QSize(40, 0))
        self.minimize_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.minimize_button.setStyleSheet("QPushButton {    \n"
                                           "    border: none;\n"
                                           "    background-color: transparent;\n"
                                           "    image: url(:/menu/minimize.png);\n"
                                           "}\n"
                                           "QPushButton:hover {\n"
                                           "    background-color: rgb" + str(self.hover2) + ";\n"
                                                                                            "}\n"
                                                                                            "QPushButton:pressed {    \n"
                                                                                            "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")
        self.minimize_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/16x16/icons/16x16/cil-window-minimize.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.minimize_button.setIcon(icon)
        self.minimize_button.setObjectName("minimize_button")
        self.horizontalLayout_2.addWidget(self.minimize_button)
        self.maximize_button = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maximize_button.sizePolicy().hasHeightForWidth())
        self.maximize_button.setSizePolicy(sizePolicy)
        self.maximize_button.setMinimumSize(QtCore.QSize(40, 0))
        self.maximize_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.maximize_button.setStyleSheet("QPushButton {    \n"
                                           "    border: none;\n"
                                           "    background-color: transparent;\n"
                                           "    image: url(:/menu/maximize.png);\n"
                                           "}\n"
                                           "QPushButton:hover {\n"
                                           "    background-color: rgb" + str(self.hover2) + ";\n"
                                                                                            "}\n"
                                                                                            "QPushButton:pressed {    \n"
                                                                                            "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")
        self.maximize_button.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/16x16/icons/16x16/cil-window-maximize.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.maximize_button.setIcon(icon1)
        self.maximize_button.setObjectName("maximize_button")
        self.horizontalLayout_2.addWidget(self.maximize_button)
        self.exit_button = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit_button.sizePolicy().hasHeightForWidth())
        self.exit_button.setSizePolicy(sizePolicy)
        self.exit_button.setMinimumSize(QtCore.QSize(40, 0))
        self.exit_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.exit_button.setStyleSheet("QPushButton {    \n"
                                       "    border: none;\n"
                                       "    background-color: transparent;\n"
                                       "    image: url(:/menu/exit.png);\n"
                                       "\n"
                                       "}\n"
                                       "QPushButton:hover {\n"
                                       "    background-color: rgb" + str(self.hover2) + ";\n"
                                                                                        "}\n"
                                                                                        "QPushButton:pressed {    \n"
                                                                                        "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")
        self.exit_button.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/16x16/icons/16x16/cil-x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exit_button.setIcon(icon2)
        self.exit_button.setObjectName("exit_button")
        self.horizontalLayout_2.addWidget(self.exit_button)
        self.verticalLayout.addWidget(self.frame)
        self.frame_12 = QtWidgets.QFrame(self.right_frame)
        self.frame_12.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.tabs_window = QtWidgets.QFrame(self.frame_12)
        self.tabs_window.setMinimumSize(QtCore.QSize(0, 0))
        self.tabs_window.setMaximumSize(QtCore.QSize(0, 16777215))
        self.tabs_window.setStyleSheet("background-color: rgb" + str(self.primer_color) + ";\n"
                                                                                          "border:none;\n"
                                                                                          "")
        self.tabs_window.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.tabs_window.setFrameShadow(QtWidgets.QFrame.Raised)
        self.tabs_window.setObjectName("tabs_window")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tabs_window)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_6.setSpacing(0)
        #############################################################
        self.tabButtons = list()
        for i in tabNames:
            self.tabButtons.append(self.create_tabButton(i))
            self.verticalLayout_6.addWidget(self.tabButtons[tabNames.index(i)])
        #############################################################
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_6.addItem(spacerItem2)
        self.horizontalLayout_8.addWidget(self.tabs_window)
        self.frame_11 = QtWidgets.QFrame(self.frame_12)
        self.frame_11.setStyleSheet("background-color: rgb{};".format(self.seconder_color))
        self.frame_11.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_11)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.frame_5 = QtWidgets.QFrame(self.frame_11)
        self.frame_5.setMaximumSize(QtCore.QSize(16777215, 41))
        self.frame_5.setStyleSheet("background-color: rgb{};".format(self.seconder_color))
        self.frame_5.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_5.setObjectName("frame_5")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.frame_5)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem3)
        self.label_top_info_2 = QtWidgets.QLabel(self.frame_5)
        self.label_top_info_2.setMinimumSize(QtCore.QSize(0, 0))
        self.label_top_info_2.setMaximumSize(QtCore.QSize(2000, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setBold(True)
        font.setWeight(75)
        self.label_top_info_2.setFont(font)
        self.label_top_info_2.setStyleSheet("color: rgb{};".format(self.info_color))
        self.label_top_info_2.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_top_info_2.setObjectName("label_top_info_2")
        self.horizontalLayout_4.addWidget(self.label_top_info_2)
        self.verticalLayout_5.addWidget(self.frame_5)
        self.frame_6 = QtWidgets.QFrame(self.frame_11)
        self.frame_6.setStyleSheet("background-color: rgb{};".format(self.seconder_color))
        self.frame_6.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_6.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6.setObjectName("frame_6")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_6)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.frame_8 = QtWidgets.QFrame(self.frame_6)
        self.frame_8.setMinimumSize(QtCore.QSize(181, 51))
        self.frame_8.setMaximumSize(QtCore.QSize(181, 51))
        self.frame_8.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_8.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_8.setObjectName("frame_8")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.frame_8)
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_2 = QtWidgets.QLabel(self.frame_8)
        self.label_2.setMinimumSize(QtCore.QSize(101, 41))
        self.label_2.setMaximumSize(QtCore.QSize(101, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet("color:rgb{};\n".format(self.text_color))
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_7.addWidget(self.label_2)
        self.horizontalLayout.addWidget(self.frame_8)
        self.program_name_label = QtWidgets.QLabel(self.frame_6)
        self.program_name_label.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.program_name_label.setFont(font)
        self.program_name_label.setStyleSheet("background: transparent;\n"
                                              "color:rgb" + str(self.text_color2) + ";\n"
                                                                                    "background-position: center;")
        self.program_name_label.setObjectName("program_name_label")
        self.horizontalLayout.addWidget(self.program_name_label)
        self.frame_7 = QtWidgets.QFrame(self.frame_6)
        self.frame_7.setMinimumSize(QtCore.QSize(181, 51))
        self.frame_7.setMaximumSize(QtCore.QSize(181, 51))
        self.frame_7.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_7.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_7.setObjectName("frame_7")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.frame_7)
        self.horizontalLayout_5.setContentsMargins(0, 0, 25, 0)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.clock_label = QtWidgets.QLabel(self.frame_7)
        self.clock_label.setMinimumSize(QtCore.QSize(101, 41))
        self.clock_label.setMaximumSize(QtCore.QSize(101, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(24)
        font.setBold(False)
        font.setWeight(50)
        self.clock_label.setFont(font)
        self.clock_label.setStyleSheet("color:rgb{};\n".format(self.text_color2))
        self.clock_label.setObjectName("clock_label")
        self.horizontalLayout_5.addWidget(self.clock_label)
        self.horizontalLayout.addWidget(self.frame_7)
        self.verticalLayout_5.addWidget(self.frame_6)
        self.frame_2 = QtWidgets.QFrame(self.frame_11)
        self.frame_2.setStyleSheet("background-color: rgb{};".format(self.seconder_color))
        self.frame_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_2)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.groupBox = QtWidgets.QGroupBox(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 0))
        self.groupBox.setMaximumSize(QtCore.QSize(99999, 99999))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("color:rgb{}".format(self.text_color2))
        # self.groupBox.setObjectName("ColoredGroupBox")
        # self.groupBox.setStyleSheet("QGroupBox#ColoredGroupBox { border: 1px solid red;}")
        # self.groupBox.setStyleSheet("QGroupBox::title {padding 0 3 px }")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        ############################################################################################
        self.shortcutButtons = list()
        self.raw1 = list()
        self.raw2 = list()
        self.raw3 = list()
        self.shortcutButtons.append(self.raw1)
        self.shortcutButtons.append(self.raw2)
        self.shortcutButtons.append(self.raw3)
        con = sqlite3.connect("Preferences.db")
        cursor = con.cursor()
        cursor.execute("SELECT Shortcuts from Pref")
        data = cursor.fetchall()
        shortcuts = data[0][0]
        self.shortcutList = shortcuts.split(",")
        for i in range(3):
            for j in range(3):
                self.shortcutButtons[i].append(self.create_shortcutButton(""))
                self.gridLayout.addWidget(self.shortcutButtons[i][j], i, j, 1, 1)
        (x, y) = (0, 0)
        for i in self.shortcutList:
            self.shortcutButtons[x][y] = self.create_shortcutButton(i)
            self.shortcutButtons[x][y].location = (x, y)
            self.gridLayout.addWidget(self.shortcutButtons[x][y], x, y, 1, 1)

            if y < 2:
                y += 1
            else:
                y = 0
                if x < 2:
                   x += 1

        cursor.execute("SELECT Tooltip from Pref")
        data2 = cursor.fetchall()
        self.Tooltip = bool(data2[0][0])
        ############################################################################################
        self.horizontalLayout_6.addWidget(self.groupBox)
        self.frame_9 = QtWidgets.QFrame(self.frame_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_9.sizePolicy().hasHeightForWidth())
        self.frame_9.setSizePolicy(sizePolicy)
        self.frame_9.setMinimumSize(QtCore.QSize(200, 0))
        self.frame_9.setMaximumSize(QtCore.QSize(200, 16777215))
        self.frame_9.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_9.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_9.setObjectName("frame_9")

        self.verticalLayout_241 = QtWidgets.QVBoxLayout(self.frame_9)
        self.verticalLayout_241.setContentsMargins(36, 0, 0, 0)
        self.verticalLayout_241.setSpacing(0)
        self.verticalLayout_241.setObjectName("verticalLayout_241")

        self.history_label = QtWidgets.QLabel(self.frame_9)
        self.history_label.setMinimumSize(QtCore.QSize(142, 90))
        self.history_label.setMaximumSize(QtCore.QSize(142, 90))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.history_label.setFont(font)
        self.history_label.setStyleSheet("color:rgb{}".format(self.text_color2))
        self.history_label.setTextFormat(QtCore.Qt.AutoText)
        self.history_label.setWordWrap(False)
        self.history_label.setIndent(-1)
        self.history_label.setObjectName("history_label")
        self.verticalLayout_241.addWidget(self.history_label)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_241.addItem(spacerItem4)
        self.horizontalLayout_6.addWidget(self.frame_9)
        self.verticalLayout_5.addWidget(self.frame_2)

        self.frame_54 = QtWidgets.QFrame(self.frame_11)
        self.frame_54.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_54.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_54.setObjectName("frame_54")
        self.frame_54.setStyleSheet("background-color: rgb{}".format(self.seconder_color))
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.frame_54)
        self.horizontalLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.frame_61 = QtWidgets.QFrame(self.frame_54)
        self.frame_61.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_61.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_61.setObjectName("frame_61")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_61)
        self.verticalLayout_8.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.frame_223 = QtWidgets.QFrame(self.frame_61)
        self.frame_223.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_223.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_223.setObjectName("frame_223")
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout(self.frame_223)
        self.horizontalLayout_25.setSpacing(25)
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.AgButton = QtWidgets.QPushButton(self.frame_223)
        self.AgButton.setMinimumSize(QtCore.QSize(100, 100))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(False)
        font.setWeight(50)
        self.AgButton.setFont(font)
        self.AgButton.setStyleSheet("QPushButton {\n"
                                    "    background-color: rgb(82, 113, 255);\n"
                                    "    border-radius: 50px;\n"
                                    "    border: 8px solid rgb" + str(self.AgBorderColor) + ";\n"
                                                                                            "    color: rgb(255, 255, 255);\n"
                                                                                            "}\n"
                                                                                            "QPushButton:hover {\n"
                                                                                            "    background-color: rgb(82, 113, 255,150);\n"
                                                                                            "}\n"
                                                                                            "QPushButton:pressed {    \n"
                                                                                            "    background-color: rgb(85, 170, 255);\n"
                                                                                            "}")
        self.AgButton.setObjectName("AgButton")
        self.horizontalLayout_25.addWidget(self.AgButton)
        self.frame_115 = QtWidgets.QFrame(self.frame_223)
        self.frame_115.setMinimumSize(QtCore.QSize(150, 60))
        self.frame_115.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame_115.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_115.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_115.setObjectName("frame_115")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_115)

        self.name_lineEdit = QtWidgets.QLineEdit(self.frame_115)
        self.name_lineEdit.setFocusPolicy(QtCore.Qt.StrongFocus)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_lineEdit.sizePolicy().hasHeightForWidth())
        self.name_lineEdit.setSizePolicy(sizePolicy)
        self.name_lineEdit.setMinimumSize(QtCore.QSize(0, 35))
        self.name_lineEdit.setMaximumSize(QtCore.QSize(220, 16777215))
        self.name_lineEdit.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.name_lineEdit.setFont(font)
        self.name_lineEdit.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.name_lineEdit.setFrame(False)
        self.name_lineEdit.setCursorPosition(11)
        self.name_lineEdit.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.name_lineEdit.setDragEnabled(False)
        self.name_lineEdit.setReadOnly(True)
        self.name_lineEdit.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.name_lineEdit.setObjectName("name_lineEdit")
        self.horizontalLayout_11.addWidget(self.name_lineEdit)
        self.editButton = QtWidgets.QPushButton(self.frame_115)
        self.editButton.setMinimumSize(QtCore.QSize(35, 35))
        self.editButton.setMaximumSize(QtCore.QSize(35, 35))
        self.editButton.setStyleSheet("QPushButton {\n"
                                      "    background-position: center;\n"
                                      "    background-repeat: no-repeat;\n"
                                      "    background-color: transparent;\n"
                                      "    border-radius: 17px;\n"
                                      "\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      "    background-color: rgb" + str(self.hover) + ";\n"
                                                                                      "}\n"
                                                                                      "QPushButton:pressed {    \n"
                                                                                      "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")
        self.editButton.setText("")
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/user/{}".format(self.editbutton_img)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.editButton.setIcon(icon4)
        self.editButton.setIconSize(QtCore.QSize(35, 35))
        self.editButton.setObjectName("editButton")
        self.horizontalLayout_11.addWidget(self.editButton)
        self.okButton = QtWidgets.QPushButton(self.frame_115)
        self.okButton.setMinimumSize(QtCore.QSize(35, 35))
        self.okButton.setMaximumSize(QtCore.QSize(35, 35))
        self.okButton.setStyleSheet("QPushButton {\n"
                                    "    background-position: center;\n"
                                    "    background-repeat: no-repeat;\n"
                                    "    background-color: transparent;\n"
                                    "    border-radius: 17px;\n"
                                    "\n"
                                    "}\n"
                                    "QPushButton:hover {\n"
                                    "    background-color: rgb" + str(self.hover) + ";\n"
                                                                                    "}\n"
                                                                                    "QPushButton:pressed {    \n"
                                                                                    "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")
        self.okButton.setText("")
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/user/{}".format(self.okbutton_img)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.okButton.setIcon(icon5)
        self.okButton.setIconSize(QtCore.QSize(35, 35))
        self.okButton.setObjectName("okButton")
        self.okButton.setShortcut(QtGui.QKeySequence("Return"))
        self.horizontalLayout_11.addWidget(self.okButton)
        self.cancelButton = QtWidgets.QPushButton(self.frame_115)
        self.cancelButton.setMinimumSize(QtCore.QSize(35, 35))
        self.cancelButton.setMaximumSize(QtCore.QSize(35, 35))
        self.cancelButton.setStyleSheet("QPushButton {\n"
                                        "    background-position: center;\n"
                                        "    background-repeat: no-repeat;\n"
                                        "    background-color: transparent;\n"
                                        "    border-radius: 17px;\n"
                                        "\n"
                                        "}\n"
                                        "QPushButton:hover {\n"
                                        "    background-color: rgb" + str(self.hover) + ";\n"
                                                                                        "}\n"
                                                                                        "QPushButton:pressed {    \n"
                                                                                        "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")
        self.cancelButton.setText("")
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/user/{}".format(self.cancelbutton_img)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancelButton.setIcon(icon6)
        self.cancelButton.setIconSize(QtCore.QSize(35, 35))
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_11.addWidget(self.cancelButton)
        self.horizontalLayout_25.addWidget(self.frame_115)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_25.addItem(spacerItem4)

        self.frame_credit = QtWidgets.QFrame(self.frame_223)
        self.frame_credit.setMinimumSize(QtCore.QSize(80, 0))
        self.frame_credit.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.frame_credit.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_credit.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_credit.setObjectName("frame_credit")
        self.verticalLayout_13 = QtWidgets.QVBoxLayout(self.frame_credit)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.labelblm_crd = QtWidgets.QLabel(self.frame_credit)
        self.labelblm_crd.setObjectName("labelblm_crd")
        self.verticalLayout_13.addWidget(self.labelblm_crd)
        self.label_capcrd = QtWidgets.QLabel(self.frame_credit)
        self.label_capcrd.setObjectName("label_capcrd")
        self.verticalLayout_13.addWidget(self.label_capcrd)
        self.horizontalLayout_25.addWidget(self.frame_credit)
        self.frame_gpas = QtWidgets.QFrame(self.frame_223)
        self.frame_gpas.setMinimumSize(QtCore.QSize(35, 0))
        self.frame_gpas.setMaximumSize(QtCore.QSize(55, 16777215))
        self.frame_gpas.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.frame_gpas.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_gpas.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_gpas.setObjectName("frame_gpas")
        self.verticalLayout_12 = QtWidgets.QVBoxLayout(self.frame_gpas)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.label_blmort = QtWidgets.QLabel(self.frame_gpas)
        self.label_blmort.setObjectName("label_blmort")
        self.verticalLayout_12.addWidget(self.label_blmort)
        self.label_caport = QtWidgets.QLabel(self.frame_gpas)
        self.label_caport.setObjectName("label_caport")
        self.verticalLayout_12.addWidget(self.label_caport)
        self.horizontalLayout_25.addWidget(self.frame_gpas)
        self.label_621 = QtWidgets.QLabel(self.frame_223)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.label_621.setFont(font)
        #self.label_621.setStyleSheet("color: rgb{};".format(self.text_color))
        self.label_621.setObjectName("label_621")
        self.horizontalLayout_25.addWidget(self.label_621)

        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        self.label_blmort.setFont(font)
        self.labelblm_crd.setFont(font)
        self.label_caport.setFont(font)
        self.label_capcrd.setFont(font)

        self.label_blmort.setStyleSheet("""QToolTip { 
                                   background-color: black; 
                                   color: white; 
                                   border: black solid 1px
                                   }""")

        self.labelblm_crd.setStyleSheet("""QToolTip { 
                                   background-color: black; 
                                   color: white; 
                                   border: black solid 1px
                                   }""")

        self.label_caport.setStyleSheet("""QToolTip { 
                                   background-color: black; 
                                   color: white; 
                                   border: black solid 1px
                                   }""")

        self.label_capcrd.setStyleSheet("""QToolTip { 
                                   background-color: black; 
                                   color: white; 
                                   border: black solid 1px
                                   }""")

        self.label_621 = QtWidgets.QLabel(self.frame_223)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(False)
        font.setWeight(50)
        self.label_621.setFont(font)
        self.label_621.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label_621.setObjectName("label_621")
        self.horizontalLayout_25.addWidget(self.label_621)
        self.gpaLabel = QtWidgets.QLabel(self.frame_223)
        font = QtGui.QFont()
        font.setPointSize(28)
        font.setBold(True)
        font.setWeight(75)
        self.gpaLabel.setFont(font)
        #self.gpaLabel.setStyleSheet("color: rgb(111,241,120);\n ")
        self.gpaLabel.setStyleSheet("QLabel {color: rgb(111,241,120);}\n"
                                        """QToolTip { 
                                           background-color: black; 
                                           color: white; 
                                           border: black solid 1px
                                           }""")
        self.gpaLabel.setObjectName("gpaLabel")
        self.horizontalLayout_25.addWidget(self.gpaLabel)
        self.verticalLayout_8.addWidget(self.frame_223)
        self.frame_330 = QtWidgets.QFrame(self.frame_61)
        self.frame_330.setMinimumSize(QtCore.QSize(0, 33))
        self.frame_330.setMaximumSize(QtCore.QSize(16777215, 33))
        self.frame_330.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_330.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_330.setObjectName("frame_330")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_330)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_321 = QtWidgets.QLabel(self.frame_330)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label_321.setFont(font)
        self.label_321.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label_321.setObjectName("label_321")
        self.horizontalLayout.addWidget(self.label_321)
        spacerItem5 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem5)
        self.depCode = QtWidgets.QComboBox(self.frame_330)
        self.depCode.setMinimumSize(QtCore.QSize(150, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.depCode.setFont(font)

        self.depCode.setStyleSheet("QComboBox {\n"
                                   "color:rgb" + str(self.text_color2) + ";\n"
                                                                         "background-color: transparent;\n"
                                                                         "selection-background-color: transparent;\n"
                                                                         "selection-color: rgb" + str(
            self.text_color2) + ";\n"
                                "}\n"
                                "QListView{\n"
                                "color:rgb" + str(self.text_color2) + ";\n"
                                                                      "}\n"
                                                                      "QScrollBar:vertical {\n"
                                                                      "     background-color: rgb" + str(
            self.scrollseconder) + ";\n"
                                   "     \n"
                                   "     border: 1px transparent #2A2929;\n"
                                   "     \n"
                                   "     width: 8px;\n"
                                   "}\n"
                                   " QScrollBar::handle:vertical {\n"
                                   "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                           "     min-height: 22px;\n"
                                                                                           "     border-radius: 4px;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-"
                                                                                           "position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n")
        self.depCode.setEditable(False)
        self.depCode.setFrame(True)
        self.depCode.setObjectName("depCode")

        self.horizontalLayout.addWidget(self.depCode)
        self.capCode = QtWidgets.QComboBox(self.frame_330)
        self.capCode.setMinimumSize(QtCore.QSize(150, 24))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.capCode.setFont(font)

        self.capCode.setStyleSheet("QComboBox {\n"
                                   "color:rgb" + str(self.text_color2) + ";\n"
                                                                         "background-color: transparent;\n"
                                                                         "selection-background-color: transparent;\n"
                                                                         "selection-color: rgb" + str(
            self.text_color2) + ";\n"
                                "}\n"
                                "QListView{\n"
                                "color:rgb" + str(self.text_color2) + ";\n"
                                                                      "}\n"
                                                                      "QScrollBar:vertical {\n"
                                                                      "     background-color: rgb" + str(
            self.scrollseconder) + ";\n"
                                   "     \n"
                                   "     border: 1px transparent #2A2929;\n"
                                   "     \n"
                                   "     width: 8px;\n"
                                   "}\n"
                                   " QScrollBar::handle:vertical {\n"
                                   "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                           "     min-height: 22px;\n"
                                                                                           "     border-radius: 4px;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-"
                                                                                           "position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n")

        self.capCode.setEditable(False)
        self.capCode.setFrame(True)
        self.capCode.setObjectName("capCode")

        self.horizontalLayout.addWidget(self.capCode)
        self.verticalLayout_8.addWidget(self.frame_330)
        self.classTab = QtWidgets.QTabWidget(self.frame_61)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.classTab.setFont(font)
        self.classTab.setStyleSheet("QTabBar::tab {\n"
                                    "  background:  rgb" + str(self.tab_min_background) + ";\n"
                                                                                          "  padding: 10px;\n"
                                                                                          "  margin-right: 5px;\n"
                                                                                          "  width: 100px;\n"
                                                                                          "  color: rgb" + str(
            self.text_color) + ";\n"
                               "  border-top-right-radius: 5px; \n"
                               "  border-top-left-radius: 5px; \n"
                               "} \n"
                               "\n"
                               "QTabBar::tab:selected { \n"
                               "  background: rgb" + str(self.selected) + ";\n"
                                                                          "}\n"
                                                                          "\n"
                                                                          "QTabWidget::pane { border: 0}")
        self.classTab.setTabPosition(QtWidgets.QTabWidget.North)
        self.classTab.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.classTab.setDocumentMode(False)
        self.classTab.setTabsClosable(False)
        self.classTab.setMovable(False)
        self.classTab.setTabBarAutoHide(False)
        self.classTab.setObjectName("classTab")
        self.class1 = QtWidgets.QWidget()
        self.class1.setStyleSheet("")
        self.class1.setObjectName("class1")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.class1)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.scrollArea = QtWidgets.QScrollArea(self.class1)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setStyleSheet("QScrollBar:vertical {\n"
                                      "     background-color: rgb" + str(self.scrollseconder) + ";\n"
                                                                                                "     \n"
                                                                                                "     border: 1px transparent #2A2929;\n"
                                                                                                "     \n"
                                                                                                "     width: 8px;\n"
                                                                                                "}\n"
                                                                                                " QScrollBar::handle:vertical {\n"
                                                                                                "     background-color: rgb" + str(
            self.scrollprimer) + ";\n"
                                 "     min-height: 5px;\n"
                                 "     border-radius: 4px;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 "")
        self.scrollArea.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.scrollArea.setLineWidth(1)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 936, 294))
        self.scrollAreaWidgetContents_2.setStyleSheet("background:  rgb" + str(self.tab_background) + ";\n"
                                                                                                      "\n"
                                                                                                      " ")
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_2)
        self.verticalLayout_2.setContentsMargins(0, 15, 0, 15)
        self.verticalLayout_2.setSpacing(10)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        # self.verticalLayout_2.addWidget(self.lectureFrame)
        ##################################################
        # => DERS EKLEME

        #################################################

        self.scrollArea.setWidget(self.scrollAreaWidgetContents_2)
        self.verticalLayout_9.addWidget(self.scrollArea)
        self.classTab.addTab(self.class1, "")
        self.class2 = QtWidgets.QWidget()
        self.class2.setObjectName("class2")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.class2)
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_11.setSpacing(7)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.class2)
        self.scrollArea_2.setStyleSheet("QScrollBar:vertical {\n"
                                        "     background-color: rgb" + str(self.scrollseconder) + ";\n"
                                                                                                  "     \n"
                                                                                                  "     border: 1px transparent #2A2929;\n"
                                                                                                  "     \n"
                                                                                                  "     width: 8px;\n"
                                                                                                  "}\n"
                                                                                                  " QScrollBar::handle:vertical {\n"
                                                                                                  "     background-color: rgb" + str(
            self.scrollprimer) + ";\n"
                                 "     min-height: 5px;\n"
                                 "     border-radius: 4px;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 "")
        self.scrollArea_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.scrollArea_2.setLineWidth(1)
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 936, 294))
        self.scrollAreaWidgetContents_3.setStyleSheet("background:  rgb" + str(self.tab_background) + ";\n"
                                                                                                      "\n"
                                                                                                      " ")
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.verticalLayout_10 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_3)
        self.verticalLayout_10.setContentsMargins(0, 15, 0, 15)
        self.verticalLayout_10.setSpacing(10)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.frame_83 = QtWidgets.QFrame(self.scrollAreaWidgetContents_3)
        self.frame_83.setMinimumSize(QtCore.QSize(0, 11))
        self.frame_83.setMaximumSize(QtCore.QSize(16777215, 11))
        self.frame_83.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_83.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_83.setObjectName("frame_83")
        # self.verticalLayout_10.addWidget(self.frame_83)
        self.frame_133 = QtWidgets.QFrame(self.scrollAreaWidgetContents_3)
        self.frame_133.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_133.setMaximumSize(QtCore.QSize(16777215, 55))
        self.frame_133.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_133.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_133.setObjectName("frame_133")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.frame_133)
        self.horizontalLayout_12.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        # self.verticalLayout_10.addWidget(self.frame_133)
        spacerItem9 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.verticalLayout_10.addItem(spacerItem9)
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout_11.addWidget(self.scrollArea_2)
        self.classTab.addTab(self.class2, "")
        self.class3 = QtWidgets.QWidget()
        self.class3.setObjectName("class3")
        self.verticalLayout_15 = QtWidgets.QVBoxLayout(self.class3)
        self.verticalLayout_15.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_15.setObjectName("verticalLayout_15")
        self.scrollArea_3 = QtWidgets.QScrollArea(self.class3)
        self.scrollArea_3.setStyleSheet("QScrollBar:vertical {\n"
                                        "     background-color: rgb" + str(self.scrollseconder) + ";\n"
                                                                                                  "     \n"
                                                                                                  "     border: 1px transparent #2A2929;\n"
                                                                                                  "     \n"
                                                                                                  "     width: 8px;\n"
                                                                                                  "}\n"
                                                                                                  " QScrollBar::handle:vertical {\n"
                                                                                                  "     background-color: rgb" + str(
            self.scrollprimer) + ";\n"
                                 "     min-height: 5px;\n"
                                 "     border-radius: 4px;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 "")
        self.scrollArea_3.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.scrollArea_3.setLineWidth(1)
        self.scrollArea_3.setWidgetResizable(True)
        self.scrollArea_3.setObjectName("scrollArea_3")
        self.scrollAreaWidgetContents_6 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_6.setGeometry(QtCore.QRect(0, 0, 936, 294))
        self.scrollAreaWidgetContents_6.setStyleSheet("background:  rgb" + str(self.tab_background) + ";\n"
                                                                                                      "\n"
                                                                                                      " ")
        self.scrollAreaWidgetContents_6.setObjectName("scrollAreaWidgetContents_6")
        self.verticalLayout_14 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_6)
        self.verticalLayout_14.setContentsMargins(0, 15, 0, 15)
        self.verticalLayout_14.setSpacing(10)
        self.verticalLayout_14.setObjectName("verticalLayout_14")
        self.frame_192 = QtWidgets.QFrame(self.scrollAreaWidgetContents_6)
        self.frame_192.setMinimumSize(QtCore.QSize(0, 11))
        self.frame_192.setMaximumSize(QtCore.QSize(16777215, 11))
        self.frame_192.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_192.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_192.setObjectName("frame_192")
        # self.verticalLayout_14.addWidget(self.frame_192)
        self.frame_201 = QtWidgets.QFrame(self.scrollAreaWidgetContents_6)
        self.frame_201.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_201.setMaximumSize(QtCore.QSize(16777215, 55))
        self.frame_201.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_201.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_201.setObjectName("frame_201")
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout(self.frame_201)
        self.horizontalLayout_15.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        # self.verticalLayout_14.addWidget(self.frame_201)
        spacerItem10 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.verticalLayout_14.addItem(spacerItem10)
        self.scrollArea_3.setWidget(self.scrollAreaWidgetContents_6)
        self.verticalLayout_15.addWidget(self.scrollArea_3)
        self.classTab.addTab(self.class3, "")
        self.class4 = QtWidgets.QWidget()
        self.class4.setObjectName("class4")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.class4)
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.scrollArea_4 = QtWidgets.QScrollArea(self.class4)
        self.scrollArea_4.setStyleSheet("QScrollBar:vertical {\n"
                                        "     background-color: rgb" + str(self.scrollseconder) + ";\n"
                                                                                                  "     \n"
                                                                                                  "     border: 1px transparent #2A2929;\n"
                                                                                                  "     \n"
                                                                                                  "     width: 8px;\n"
                                                                                                  "}\n"
                                                                                                  " QScrollBar::handle:vertical {\n"
                                                                                                  "     background-color: rgb" + str(
            self.scrollprimer) + ";\n"
                                 "     min-height: 5px;\n"
                                 "     border-radius: 4px;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 "")
        self.scrollArea_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.scrollArea_4.setLineWidth(1)
        self.scrollArea_4.setWidgetResizable(True)
        self.scrollArea_4.setObjectName("scrollArea_4")
        self.scrollAreaWidgetContents_7 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_7.setGeometry(QtCore.QRect(0, 0, 936, 294))
        self.scrollAreaWidgetContents_7.setStyleSheet("background:  rgb" + str(self.tab_background) + ";\n"
                                                                                                      "\n"
                                                                                                      " ")
        self.scrollAreaWidgetContents_7.setObjectName("scrollAreaWidgetContents_7")
        self.verticalLayout_16 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_7)
        self.verticalLayout_16.setContentsMargins(0, 15, 0, 15)
        self.verticalLayout_16.setSpacing(10)
        self.verticalLayout_16.setObjectName("verticalLayout_16")
        self.frame_218 = QtWidgets.QFrame(self.scrollAreaWidgetContents_7)
        self.frame_218.setMinimumSize(QtCore.QSize(0, 11))
        self.frame_218.setMaximumSize(QtCore.QSize(16777215, 11))
        self.frame_218.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_218.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_218.setObjectName("frame_218")
        # self.verticalLayout_16.addWidget(self.frame_218)
        self.frame_271 = QtWidgets.QFrame(self.scrollAreaWidgetContents_7)
        self.frame_271.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_271.setMaximumSize(QtCore.QSize(16777215, 55))
        self.frame_271.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_271.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_271.setObjectName("frame_271")
        self.horizontalLayout_16 = QtWidgets.QHBoxLayout(self.frame_271)
        self.horizontalLayout_16.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_16.setObjectName("horizontalLayout_16")
        # self.verticalLayout_16.addWidget(self.frame_271)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.verticalLayout_16.addItem(spacerItem11)
        self.scrollArea_4.setWidget(self.scrollAreaWidgetContents_7)
        self.verticalLayout_20.addWidget(self.scrollArea_4)
        self.classTab.addTab(self.class4, "")

        self.ITBSNT = QtWidgets.QWidget()
        self.ITBSNT.setObjectName("ITBSNT")
        self.verticalLayout_206 = QtWidgets.QVBoxLayout(self.ITBSNT)
        self.verticalLayout_206.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_206.setObjectName("verticalLayout_206")
        self.scrollArea_49 = QtWidgets.QScrollArea(self.ITBSNT)
        self.scrollArea_49.setStyleSheet("QScrollBar:vertical {\n"
                                         "     background-color: rgb" + str(self.scrollseconder) + ";\n"
                                                                                                   "     \n"
                                                                                                   "     border: 1px transparent #2A2929;\n"
                                                                                                   "     \n"
                                                                                                   "     width: 8px;\n"
                                                                                                   "}\n"
                                                                                                   " QScrollBar::handle:vertical {\n"
                                                                                                   "     background-color: rgb" + str(
            self.primer_color) + ";\n"
                                 "     min-height: 5px;\n"
                                 "     border-radius: 4px;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 "")
        self.scrollArea_49.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_49.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.scrollArea_49.setLineWidth(1)
        self.scrollArea_49.setWidgetResizable(True)
        self.scrollArea_49.setObjectName("scrollArea_49")
        self.scrollAreaWidgetContents_75 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_75.setGeometry(QtCore.QRect(0, 0, 936, 294))
        self.scrollAreaWidgetContents_75.setStyleSheet("background:  rgb" + str(self.tab_background) + ";\n"
                                                                                                       "\n"
                                                                                                       " ")
        self.scrollAreaWidgetContents_75.setObjectName("scrollAreaWidgetContents_75")
        self.verticalLayout_28 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_75)
        self.verticalLayout_28.setContentsMargins(0, 15, 0, 15)
        self.verticalLayout_28.setSpacing(10)
        self.verticalLayout_28.setObjectName("verticalLayout_28")
        self.frame_2181 = QtWidgets.QFrame(self.scrollAreaWidgetContents_75)
        self.frame_2181.setMinimumSize(QtCore.QSize(0, 11))
        self.frame_2181.setMaximumSize(QtCore.QSize(16777215, 11))
        self.frame_2181.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2181.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2181.setObjectName("frame_2181")
        # self.verticalLayout_16.addWidget(self.frame_218)
        self.frame_2711 = QtWidgets.QFrame(self.scrollAreaWidgetContents_75)
        self.frame_2711.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_2711.setMaximumSize(QtCore.QSize(16777215, 55))
        self.frame_2711.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2711.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2711.setObjectName("frame_2711")
        self.horizontalLayout_23 = QtWidgets.QHBoxLayout(self.frame_2711)
        self.horizontalLayout_23.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_23.setObjectName("horizontalLayout_23")
        # self.verticalLayout_16.addWidget(self.frame_271)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.verticalLayout_16.addItem(spacerItem11)
        self.scrollArea_49.setWidget(self.scrollAreaWidgetContents_75)
        self.verticalLayout_206.addWidget(self.scrollArea_49)
        self.plusButton = QtWidgets.QPushButton()
        self.plusButton.setMaximumHeight(48)
        self.plusButton.setMinimumHeight(48)
        self.plusButton.setStyleSheet("\n"
                                      "QPushButton {\n"
                                      "    background-image: url(:/menu/plus.png);\n"
                                      "    background-position: center;\n"
                                      "    background-repeat: no-repeat;\n"
                                      "    border-radius: 20px;\n"
                                      "    background-color: rgb(255, 255, 255,100);\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      "    background-color: rgb(255, 255, 255,150);\n"
                                      "}\n"
                                      "QPushButton:pressed {    \n"
                                      "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                                        "}")

        self.verticalLayout_28.addWidget(self.plusButton)
        spacerItem16 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_28.addItem(spacerItem16)
        self.verticalLayout_28.setContentsMargins(0, 15, 0, 15)
        self.classTab.addTab(self.ITBSNT, "")

        self.CAP = QtWidgets.QWidget()
        self.CAP.setObjectName("CAP")
        self.verticalLayout_202 = QtWidgets.QVBoxLayout(self.CAP)
        self.verticalLayout_202.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_202.setObjectName("verticalLayout_202")
        self.scrollArea_43 = QtWidgets.QScrollArea(self.CAP)
        self.scrollArea_43.setStyleSheet("QScrollBar:vertical {\n"
                                         "     background-color: rgb" + str(self.scrollseconder) + ";\n"
                                                                                                   "     \n"
                                                                                                   "     border: 1px transparent #2A2929;\n"
                                                                                                   "     \n"
                                                                                                   "     width: 8px;\n"
                                                                                                   "}\n"
                                                                                                   " QScrollBar::handle:vertical {\n"
                                                                                                   "     background-color: rgb" + str(
            self.scrollprimer) + ";\n"
                                 "     min-height: 5px;\n"
                                 "     border-radius: 4px;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 "")
        self.scrollArea_43.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scrollArea_43.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.scrollArea_43.setLineWidth(1)
        self.scrollArea_43.setWidgetResizable(True)
        self.scrollArea_43.setObjectName("scrollArea_43")
        self.scrollAreaWidgetContents_71 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_71.setGeometry(QtCore.QRect(0, 0, 936, 294))
        self.scrollAreaWidgetContents_71.setStyleSheet("background:  rgb" + str(self.tab_background) + ";\n"
                                                                                                       "\n"
                                                                                                       " ")
        self.scrollAreaWidgetContents_71.setObjectName("scrollAreaWidgetContents_71")
        self.verticalLayout_22 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_71)
        self.verticalLayout_22.setContentsMargins(0, 15, 0, 15)
        self.verticalLayout_22.setSpacing(10)
        self.verticalLayout_22.setObjectName("verticalLayout_22")
        self.frame_2189 = QtWidgets.QFrame(self.scrollAreaWidgetContents_71)
        self.frame_2189.setMinimumSize(QtCore.QSize(0, 11))
        self.frame_2189.setMaximumSize(QtCore.QSize(16777215, 11))
        self.frame_2189.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2189.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2189.setObjectName("frame_2189")
        # self.verticalLayout_16.addWidget(self.frame_218)
        self.frame_2719 = QtWidgets.QFrame(self.scrollAreaWidgetContents_71)
        self.frame_2719.setMinimumSize(QtCore.QSize(0, 0))
        self.frame_2719.setMaximumSize(QtCore.QSize(16777215, 55))
        self.frame_2719.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_2719.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2719.setObjectName("frame_2719")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout(self.frame_2719)
        #self.horizontalLayout_22.setContentsMargins(-1, 0, -1, 0)
        #self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        # self.verticalLayout_16.addWidget(self.frame_271)
        spacerItem11 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        # self.verticalLayout_16.addItem(spacerItem11)
        self.scrollArea_43.setWidget(self.scrollAreaWidgetContents_71)
        self.verticalLayout_202.addWidget(self.scrollArea_43)
        self.classTab.addTab(self.CAP, "")

        self.verticalLayout_8.addWidget(self.classTab)
        self.horizontalLayout_6.addWidget(self.frame_61)
        self.verticalLayout_5.addWidget(self.frame_54)
        self.frame_54.close()

        self.frame_542 = QtWidgets.QFrame(self.frame_11)
        self.frame_542.setMaximumSize(QtCore.QSize(16777215, 52))
        self.frame_542.setStyleSheet("background: transparent;")
        self.frame_542.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_542.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_542.setObjectName("frame_542")
        self.horizontalLayout_440 = QtWidgets.QHBoxLayout(self.frame_542)
        self.horizontalLayout_440.setContentsMargins(-1, 5, -1, 11)
        self.horizontalLayout_440.setSpacing(14)
        self.horizontalLayout_440.setObjectName("horizontalLayout_440")
        self.label_043 = QtWidgets.QLabel(self.frame_542)
        self.label_043.setMinimumSize(QtCore.QSize(105, 0))
        self.label_043.setMaximumSize(QtCore.QSize(105, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label_043.setFont(font)
        self.label_043.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label_043.setObjectName("label_043")
        self.horizontalLayout_440.addWidget(self.label_043)
        self.label_067 = QtWidgets.QLabel(self.frame_542)
        self.label_067.setMinimumSize(QtCore.QSize(200, 0))
        self.label_067.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label_067.setFont(font)
        self.label_067.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label_067.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_067.setObjectName("label_067")
        self.horizontalLayout_440.addWidget(self.label_067)
        self.label_0043 = QtWidgets.QLabel(self.frame_542)
        self.label_0043.setMinimumSize(QtCore.QSize(550, 0))
        self.label_0043.setMaximumSize(QtCore.QSize(2000, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label_0043.setFont(font)
        self.label_0043.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label_0043.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_0043.setObjectName("label_0043")
        self.horizontalLayout_440.addWidget(self.label_0043)
        self.label_top_info_234 = QtWidgets.QLabel(self.frame_542)
        self.label_top_info_234.setMinimumSize(QtCore.QSize(0, 0))
        self.label_top_info_234.setMaximumSize(QtCore.QSize(2000, 20))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setBold(True)
        font.setWeight(75)
        self.label_top_info_234.setFont(font)
        self.label_top_info_234.setStyleSheet("color: rgb{};".format(self.info_color))
        self.label_top_info_234.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_top_info_234.setObjectName("label_top_info_234")
        self.horizontalLayout_440.addWidget(self.label_top_info_234)
        self.verticalLayout_5.addWidget(self.frame_542)
        self.scrollArea004 = QtWidgets.QScrollArea(self.frame_11)

        self.scrollArea004.setWidgetResizable(True)
        self.scrollArea004.setObjectName("scrollArea004")
        self.scrollArea004.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.scrollArea004.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.scrollArea004.setLineWidth(1)

        self.scrollArea004.setStyleSheet(
            "QScrollArea > QWidget > QWidget { background: rgb" + str(self.seconder_color) + ";\n}"
                                                                                             "QScrollBar:vertical {\n"
                                                                                             "     background-color: rgb" + str(
                self.scrollseconder) + ";\n"
                                       "     \n"
                                       "     border: 1px transparent #2A2929;\n"
                                       "     \n"
                                       "     width: 8px;\n"
                                       "}\n"
                                       " QScrollBar::handle:vertical {\n"
                                       "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                               "     min-height: 5px;\n"
                                                                                               "     border-radius: 4px;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:vertical {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: top;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:vertical {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: bottom;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: top;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: bottom;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"

                                                                                               "QScrollBar:horizontal {\n"
                                                                                               "     background-color: rgb" + str(
                self.scrollseconder) + ";\n"
                                       "     \n"
                                       "     border: 1px transparent #2A2929;\n"
                                       "     \n"
                                       "     height: 8px;\n"
                                       "}\n"
                                       " QScrollBar::handle:horizontal {\n"
                                       "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                               "     min-width: 5px;\n"
                                                                                               "     border-radius: 4px;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:horizontal {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: left;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:horizontal {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: right;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:horizontal:hover,QScrollBar::sub-line:horizontal:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: left;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: right;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"
                                                                                               ""
        )
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 984, 538))
        self.scrollAreaWidgetContents.setStyleSheet("")
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_002 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_002.setContentsMargins(10, 0, 0, 0)
        self.verticalLayout_002.setSpacing(0)
        self.verticalLayout_002.setObjectName("verticalLayout_002")
        ################3

        self.verticalLayout_002.addWidget(
            uiClasses.OpenLecture(self, str(uuid.uuid4()), "", "", "", "", self.hover, self.pressed, self.border,
                                  self.exit, self.updating))
        #print(self.items)

        #############333
        self.frame_062 = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.frame_062.setMinimumSize(QtCore.QSize(0, 80))

        self.frame_062.setStyleSheet("background:transparent;")
        self.frame_062.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_062.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_062.setObjectName("frame_062")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_062)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addLecture = QtWidgets.QPushButton(self.frame_062)
        self.addLecture.setMinimumSize(QtCore.QSize(0, 50))
        self.addLecture.setMaximumSize(QtCore.QSize(175, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.addLecture.setFont(font)
        self.addLecture.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.addLecture.setStyleSheet("QPushButton {\n"
                                      "    background-position: center;\n"
                                      "    background-repeat: no-reperat;\n"
                                      "    border: none;\n"
                                      "    background-color: rgb" + str(self.adl) + ";\n"
                                                                                    "    color: rgb" + str(
            self.text_color2) + ";\n"
                                "    border-radius: 22px;\n"
                                "}\n"
                                "QPushButton:hover {\n"
                                "    background-color: rgb" + str(self.adlhover) + ";\n"
                                                                                   "    background-image: url(:/menu/" + self.plusbutton + ")" + ";\n"
                                                                                                                                                 "    color: transparent;\n"
                                                                                                                                                 "}\n"
                                                                                                                                                 "QPushButton:pressed {    \n"
                                                                                                                                                 "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")
        self.addLecture.setIconSize(QtCore.QSize(20, 20))
        self.addLecture.setObjectName("addLecture")
        self.addLecture.clicked.connect(
            lambda: self.verticalLayout_002.insertWidget(self.verticalLayout_002.count() - 3,
                                                         uiClasses.OpenLecture(self, str(uuid.uuid4()), "", "", "", "",
                                                                               self.hover, self.pressed, self.border,
                                                                               self.exit, self.updating)))
        self.horizontalLayout.addWidget(self.addLecture)
        self.verticalLayout_002.addWidget(self.frame_062)

        self.tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents)
        self.tableWidget.setFocusPolicy(QtCore.Qt.NoFocus)

        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)

        self.tableWidget.setMinimumHeight(700)

        self.tableWidget.setStyleSheet(
            " QTableWidget"
            "{"
            " margin-right: 10px;"
            "background-color: rgb" + str(self.seconder_color) + ";\n"
                                                                 "border: none;"

                                                                 "}"



                                                                 "QScrollBar:vertical {\n"
                                                                 "                                           background-color: rgb" + str(
                self.scrollseconder) + ";\n"
                                       "                                           \n"
                                       "                                           border: 1px transparent #2A2929;\n"
                                       "                                           \n"
                                       "                                           width: 8px;\n"
                                       "                                      }\n"
                                       "                                       QScrollBar::handle:vertical {\n"
                                       "                                           background-color: rgb" + str(
                self.scrollprimer) + ";\n"
                                     "                                           min-height: 5px;\n"
                                     "                                           border-radius: 4px;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::sub-line:vertical {\n"
                                     "                                           margin: 3px 0px 3px 0px;\n"
                                     "                                           border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                     "                                           height: 10px;\n"
                                     "                                           width: 10px;\n"
                                     "                                           subcontrol-position: top;\n"
                                     "                                           subcontrol-origin: margin;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::add-line:vertical {\n"
                                     "                                           margin: 3px 0px 3px 0px;\n"
                                     "                                           border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                     "                                           height: 10px;\n"
                                     "                                           width: 10px;\n"
                                     "                                           subcontrol-position: bottom;\n"
                                     "                                           subcontrol-origin: margin;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                     "                                           border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                     "                                           height: 10px;\n"
                                     "                                           width: 10px;\n"
                                     "                                           subcontrol-position: top;\n"
                                     "                                           subcontrol-origin: margin;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                     "                                           border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                     "                                           height: 10px;\n"
                                     "                                           width: 10px;\n"
                                     "                                           subcontrol-position: bottom;\n"
                                     "                                           subcontrol-origin: margin;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                     "                                           background: none;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                     "                                           background: none;\n"
                                     "                                      }\n"
                                     "\n"
                                     "QHeaderView::section{ \n"
                                     "             border-top:0px solid #D8D8D8; \n"
                                     "             border-left:0px solid #D8D8D8; \n"
                                     "             border-right:1px solid #D8D8D8; \n"
                                     "             border-bottom: 1px solid #D8D8D8; \n"
                                     "             background-color:white; \n"
                                     "             padding:4px; \n"
                                     "         } \n"
                                     "         QTableCornerButton::section{ \n"
                                     "             border-top:0px solid #D8D8D8; \n"
                                     "             border-left:0px solid #D8D8D8; \n"
                                     "             border-right:1px solid #D8D8D8; \n"
                                     "             border-bottom: 1px solid #D8D8D8; \n"
                                     "             background-color:white; \n"
                                     "         } ")
        self.tableWidget.setEditTriggers(
            QtWidgets.QAbstractItemView.AnyKeyPressed | QtWidgets.QAbstractItemView.EditKeyPressed)
        self.tableWidget.setShowGrid(True)
        self.tableWidget.setGridStyle(QtCore.Qt.NoPen)
        self.tableWidget.setCornerButtonEnabled(True)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(20)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(14, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(15, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(16, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(17, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(18, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(19, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.verticalHeader().setVisible(True)
        self.verticalLayout_002.addWidget(self.tableWidget)
        self.scrollArea004.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_5.addWidget(self.scrollArea004)
        ####################################################################################
        self.calendarChoseframe = QtWidgets.QFrame(self.frame_11)
        self.yearComboBox = QtWidgets.QComboBox()
        self.listComboBox = QtWidgets.QComboBox()
        self.calendarSet = QtWidgets.QHBoxLayout()
        self.calendarSet.setContentsMargins(10, 0, 0, 0)
        self.calendarSet.addWidget(self.yearComboBox)
        self.calendarSet.addWidget(self.listComboBox)
        self.yearComboBox.setMinimumHeight(50)
        self.yearComboBox.setMaximumWidth(140)
        self.calendarChoseframe.setLayout(self.calendarSet)
        self.verticalLayout_5.addWidget(self.calendarChoseframe)

        font = QtGui.QFont()
        font.setPointSize(10)
        #font.setWeight(75)
        font.setFamily("Segoe UI")

        self.yearComboBox.setFont(font)
        self.listComboBox.setFont(font)

        self.calendarChoseframe.setStyleSheet("background-color: rgb" + str(self.seconder_color) + "\n")
        self.yearComboBox.setStyleSheet("QComboBox {\n"
                                        "color:rgb" + str(self.text_color2) + ";\n"
                                                                              "background-color: transparent;\n"
                                                                              "selection-background-color: transparent;\n"
                                                                              "selection-color: rgb" + str(
            self.text_color2) + ";\n"
                                "}\n"
                                "QListView{\n"
                                "color:rgb" + str(self.text_color2) + ";\n"
                                                                      "}\n"
                                                                      "QScrollBar:vertical {\n"
                                                                      "     background-color: rgb" + str(
            self.scrollseconder) + ";\n"
                                   "     \n"
                                   "     border: 1px transparent #2A2929;\n"
                                   "     \n"
                                   "     width: 8px;\n"
                                   "}\n"
                                   " QScrollBar::handle:vertical {\n"
                                   "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                           "     min-height: 22px;\n"
                                                                                           "     border-radius: 4px;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-"
                                                                                           "position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n")

        self.listComboBox.setStyleSheet("QComboBox {\n"
                                        "color:rgb" + str(self.text_color2) + ";\n"
                                                                              "background-color: transparent;\n"
                                                                              "selection-background-color: transparent;\n"
                                                                              "selection-color: rgb" + str(
            self.text_color2) + ";\n"
                                "}\n"
                                "QListView{\n"
                                "color:rgb" + str(self.text_color2) + ";\n"
                                                                      "}\n"
                                                                      "QScrollBar:vertical {\n"
                                                                      "     background-color: rgb" + str(
            self.scrollseconder) + ";\n"
                                   "     \n"
                                   "     border: 1px transparent #2A2929;\n"
                                   "     \n"
                                   "     width: 8px;\n"
                                   "}\n"
                                   " QScrollBar::handle:vertical {\n"
                                   "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                           "     min-height: 22px;\n"
                                                                                           "     border-radius: 4px;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-"
                                                                                           "position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n")

        self.calendarChoseframe.close()


        self.calendar_table = QtWidgets.QTableWidget(self.frame_11)
        self.calendar_table.setFocusPolicy(QtCore.Qt.NoFocus)
        self.calendar_table.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.calendar_table.setFrameShadow(QtWidgets.QFrame.Raised)
        self.calendar_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.calendar_table.setTabKeyNavigation(False)
        self.calendar_table.setProperty("showDropIndicator", False)
        self.calendar_table.setDragDropOverwriteMode(False)
        self.calendar_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.calendar_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.calendar_table.setGridStyle(QtCore.Qt.SolidLine)
        self.calendar_table.setObjectName("calendar_table")
        self.calendar_table.setColumnCount(1)
        self.calendar_table.setRowCount(0)

        self.calendar_table.setStyleSheet("QScrollBar:vertical {\n"
                                                                      "     background-color: rgb" + str(
            self.scrollseconder) + ";\n"
                                   "     \n"
                                   "     border: 1px transparent #2A2929;\n"
                                   "     \n"
                                   "     width: 8px;\n"
                                   "}\n"
                                   " QScrollBar::handle:vertical {\n"
                                   "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                           "     min-height: 22px;\n"
                                                                                           "     border-radius: 4px;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-"
                                                                                           "position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n")

        item = QtWidgets.QTableWidgetItem()
        self.calendar_table.setHorizontalHeaderItem(0, item)

        self.calendar_table.horizontalHeader().setCascadingSectionResizes(False)
        self.calendar_table.horizontalHeader().setSortIndicatorShown(False)
        self.calendar_table.horizontalHeader().setStretchLastSection(True)
        self.calendar_table.verticalHeader().setCascadingSectionResizes(False)
        self.calendar_table.verticalHeader().setStretchLastSection(False)

        uiFunctions.get_years(self)
        uiFunctions.fill_secondComboBox(self)
        self.calendar_table.close()
        ###########################################################################
        self.verticalLayout_5.addWidget(self.calendar_table)
        ###########################################################################

        self.scrollArea_1241 = QtWidgets.QScrollArea(self.frame_11)
        self.scrollArea_1241.setWidgetResizable(True)
        self.scrollArea_1241.setObjectName("scrollArea_1241")
        self.scrollAreaWidget_y = QtWidgets.QWidget()
        self.scrollAreaWidget_y.setGeometry(QtCore.QRect(0, 0, 965, 774))
        self.scrollAreaWidget_y.setObjectName("scrollAreaWidget_y")
        self.scrollArea_1241.setStyleSheet(
                                    "QScrollArea {border: none;}"
                                        "QScrollBar:vertical {\n"
                                      "     background-color: rgb" + str(self.scrollseconder) + ";\n"
                                                                                                "     \n"
                                                                                                "     border: 1px transparent #2A2929;\n"
                                                                                                "     \n"
                                                                                                "     width: 8px;\n"
                                                                                                "}\n"
                                                                                                " QScrollBar::handle:vertical {\n"
                                                                                                "     background-color: rgb" + str(
            self.scrollprimer) + ";\n"
                                 "     min-height: 5px;\n"
                                 "     border-radius: 4px;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 
                                 "QScrollBar:horizontal {\n"
                                                                                               "     background-color: rgb" + str(
                self.scrollseconder) + ";\n"
                                       "     \n"
                                       "     border: 1px transparent #2A2929;\n"
                                       "     \n"
                                       "     height: 8px;\n"
                                       "}\n"
                                       " QScrollBar::handle:horizontal {\n"
                                       "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                               "     min-width: 5px;\n"
                                                                                               "     border-radius: 4px;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:horizontal {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: left;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:horizontal {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: right;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:horizontal:hover,QScrollBar::sub-line:horizontal:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: left;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: right;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n")

        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.scrollAreaWidget_y)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.scrollAreaWidget_y)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.calendarWidget.sizePolicy().hasHeightForWidth())
        self.calendarWidget.setSizePolicy(sizePolicy)
        self.calendarWidget.setGridVisible(False)
        self.calendarWidget.setHorizontalHeaderFormat(QtWidgets.QCalendarWidget.LongDayNames)
        self.calendarWidget.setObjectName("calendarWidget")
        self.verticalLayout_11.addWidget(self.calendarWidget)
        self.label_oy = QtWidgets.QLabel(self.scrollAreaWidget_y)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_oy.setFont(font)

        self.label_oy.setObjectName("label_oy")
        self.verticalLayout_11.addWidget(self.label_oy)
        self.label_oybg = QtWidgets.QLabel(self.scrollAreaWidget_y)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_oybg.setFont(font)

        self.label_oybg.setObjectName("label_oy")
        self.label_oybg.setText("Öğle yemeği bilgisi girilmemiş")
        self.verticalLayout_11.addWidget(self.label_oybg)
        self.tableWidget_oy = QtWidgets.QTableWidget(self.scrollAreaWidget_y)
        self.tableWidget_oy.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_oy.sizePolicy().hasHeightForWidth())
        self.tableWidget_oy.setSizePolicy(sizePolicy)
        self.tableWidget_oy.setAutoFillBackground(False)

        self.tableWidget_oy.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget_oy.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget_oy.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_oy.setAutoScrollMargin(0)
        self.tableWidget_oy.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_oy.setTabKeyNavigation(False)
        self.tableWidget_oy.setProperty("showDropIndicator", False)
        self.tableWidget_oy.setDragDropOverwriteMode(False)
        self.tableWidget_oy.setAlternatingRowColors(False)
        self.tableWidget_oy.setShowGrid(True)
        self.tableWidget_oy.setWordWrap(True)
        self.tableWidget_oy.setCornerButtonEnabled(True)
        self.tableWidget_oy.setObjectName("tableWidget_oy")
        self.tableWidget_oy.setColumnCount(2)
        self.tableWidget_oy.setRowCount(2)
        self.tableWidget_oy.horizontalHeader().setVisible(False)
        self.tableWidget_oy.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_oy.horizontalHeader().setDefaultSectionSize(250)
        self.tableWidget_oy.horizontalHeader().setHighlightSections(True)
        self.tableWidget_oy.horizontalHeader().setMinimumSectionSize(50)
        self.tableWidget_oy.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget_oy.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_oy.verticalHeader().setVisible(False)
        self.tableWidget_oy.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_11.addWidget(self.tableWidget_oy)
        self.label_ay = QtWidgets.QLabel(self.scrollAreaWidget_y)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_ay.setFont(font)

        self.label_ay.setObjectName("label_ay")
        self.verticalLayout_11.addWidget(self.label_ay)
        self.label_aybg = QtWidgets.QLabel(self.scrollAreaWidget_y)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_aybg.setFont(font)

        self.label_aybg.setObjectName("label_oy")
        self.label_aybg.setText("Akşam yemeği bilgisi girilmemiş")
        self.verticalLayout_11.addWidget(self.label_aybg)
        self.tableWidget_ay = QtWidgets.QTableWidget(self.scrollAreaWidget_y)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tableWidget_ay.sizePolicy().hasHeightForWidth())
        self.tableWidget_ay.setSizePolicy(sizePolicy)
        self.tableWidget_ay.setAutoFillBackground(False)

        self.tableWidget_ay.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget_ay.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tableWidget_ay.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.tableWidget_ay.setAutoScrollMargin(0)
        self.tableWidget_ay.setShowGrid(True)
        self.tableWidget_ay.setObjectName("tableWidget_ay")
        self.tableWidget_ay.setColumnCount(2)
        self.tableWidget_ay.setRowCount(2)
        self.tableWidget_ay.horizontalHeader().setVisible(False)
        self.tableWidget_ay.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_ay.horizontalHeader().setDefaultSectionSize(250)
        self.tableWidget_ay.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget_ay.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_ay.verticalHeader().setStretchLastSection(False)
        self.tableWidget_ay.verticalHeader().setVisible(False)
        self.verticalLayout_11.addWidget(self.tableWidget_ay)
        self.scrollArea_1241.setWidget(self.scrollAreaWidget_y)
        self.verticalLayout_5.addWidget(self.scrollArea_1241)

        self.tableWidget_ay.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_oy.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget_ay.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableWidget_oy.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        #######################################################################
        self.intErrorLabel = QtWidgets.QLabel(self.translate["İnternet bağlantısı gereklidir!"][self.languageNumber])

        font = QtGui.QFont()
        font.setPointSize(36)
        self.intErrorLabel.setFont(font)
        self.intErrorLabel.hide()
        self.verticalLayout_11.addWidget(self.intErrorLabel)

        self.label_oy.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.label_oybg.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.tableWidget_oy.setStyleSheet("QTableWidget{\n"
                                          "    border: none;\n"
                                          "}\n"
                                          "QTableWidget::item {\n"
                                          "    color: rgb" + str(self.text_color2) + ";\n"
                                          "}")
        self.label_ay.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.label_aybg.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.tableWidget_ay.setStyleSheet("QTableWidget{\n"
                                          "    border: none;\n"
                                          "}\n"
                                          "QTableWidget::item {\n"
                                          "    color: rgb" + str(self.text_color2) + ";\n"
                                          "}")
        self.intErrorLabel.setStyleSheet("color: rgb{}".format(self.text_color2))
        #self.calendarWidget.setStyleSheet("QCalendarWidget { color: rgb{}; }".format(self.text_color2)
        #                                  "QMenu { background-color: rgb(0,0,0);}")

        self.calendarWidget.setStyleSheet("color: rgb{}; alternate-background-color:rgb{};".format(self.text_color2, self.alternete))


        self.startYemekhane()

        #self.horizontalLayout_8.addWidget(self.frame_11)
        #uiFunctions.get_date(self)
        self.scrollArea_1241.close()
        self.calendarWidget.selectionChanged.connect(self.startYemekhane)

        #self.verticalLayout.addWidget(self.frame_12)

        ####################################################################################################################
        self.frameAB = QtWidgets.QFrame(self.frame_11)
        self.frameAB.setStyleSheet("")
        self.frameAB.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frameAB.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frameAB.setObjectName("frameAB")
        self.verticalLayout_255 = QtWidgets.QVBoxLayout(self.frameAB)
        self.verticalLayout_255.setObjectName("verticalLayout_255")

        self.name_label_5 = QtWidgets.QLabel(self.frameAB)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.name_label_5.setFont(font)
        self.name_label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label_5.setObjectName("name_label_5")
        self.verticalLayout_255.addWidget(self.name_label_5)
        self.name_label = QtWidgets.QLabel(self.frameAB)
        self.name_label_1 = QtWidgets.QLabel(self.frameAB)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.name_label_1.setFont(font)
        self.name_label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label_1.setObjectName("name_label_1")
        self.verticalLayout_255.addWidget(self.name_label_1)
        self.name_label_2 = QtWidgets.QLabel(self.frameAB)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.name_label_2.setFont(font)
        self.name_label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label_2.setObjectName("name_label_2")
        self.verticalLayout_255.addWidget(self.name_label_2)
        self.name_label_3 = QtWidgets.QLabel(self.frameAB)
        font = QtGui.QFont()
        font.setPointSize(36)
        self.name_label_3.setFont(font)
        self.name_label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.name_label_3.setObjectName("name_label_3")
        self.verticalLayout_255.addWidget(self.name_label_3)
        self.name_label_4 = QtWidgets.QLabel(self.frameAB)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.name_label_4.setFont(font)
        self.name_label_4.setAlignment(QtCore.Qt.AlignLeft)
        self.name_label_4.setObjectName("name_label_4")
        self.verticalLayout_255.addWidget(self.name_label_4)


        self.textEdit = QtWidgets.QTextEdit(self.frameAB)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.textEdit.setFont(font)
        self.textEdit.setAlignment(QtCore.Qt.AlignLeft)
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setStyleSheet("QTextEdit{ color: rgb(255, 255, 255)}\n"
                                       "QScrollBar:vertical {\n"
                                       "     background-color: rgb" + str(
                self.scrollseconder) + ";\n"
                                       "     \n"
                                       "     border: 1px transparent #2A2929;\n"
                                       "     \n"
                                       "     width: 8px;\n"
                                       "}\n"
                                       " QScrollBar::handle:vertical {\n"
                                       "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                               "     min-height: 5px;\n"
                                                                                               "     border-radius: 4px;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:vertical {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: top;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:vertical {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: bottom;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: top;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: bottom;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"

                                                                                               "QScrollBar:horizontal {\n"
                                                                                               "     background-color: rgb" + str(
                self.scrollseconder) + ";\n"
                                       "     \n"
                                       "     border: 1px transparent #2A2929;\n"
                                       "     \n"
                                       "     height: 8px;\n"
                                       "}\n"
                                       " QScrollBar::handle:horizontal {\n"
                                       "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                               "     min-width: 5px;\n"
                                                                                               "     border-radius: 4px;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:horizontal {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: left;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:horizontal {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: right;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:horizontal:hover,QScrollBar::sub-line:horizontal:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: left;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: right;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n")


        self.verticalLayout_255.addWidget(self.textEdit)
        
        self.submitButton = QtWidgets.QPushButton(self.frameAB)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.submitButton.setFont(font)
        self.submitButton.setObjectName("submitButton")
        self.submitButton.setMaximumHeight(48)
        self.submitButton.setMinimumHeight(36)
        self.submitButton.setStyleSheet("\n"
                                  "QPushButton {\n"
                                  "    background-position: center;\n"
                                  "    background-repeat: no-repeat;\n"
                                  "    background-color: rgb" + str(self.primer_color) + ";\n"
                                  "    color: rgb(255, 255, 255);\n"
                                  "    border: 0px solid white;\n"
                                  "    border-radius: 10px;\n"
                                  "}\n"
                                  "QPushButton:hover {\n"
                                  "    background-color: rgb" + str(self.hover) + ";\n"
                                  "}\n"
                                  "QPushButton:pressed {    \n"
                                  "    background-color: rgb" + str(self.pressed) + ";\n"
                                  "}")

        self.verticalLayout_255.addWidget(self.submitButton)

        self.verticalLayout_5.addWidget(self.frameAB)


        self.frameAB.setStyleSheet("background-color: rgb{}".format(self.seconder_color))
        self.name_label_5.setText("İTÜ KRAKEN 2021")
        self.name_label_1.setText("Onur Ulusoy")
        self.name_label_2.setText("Adem Geçgel")
        self.name_label_3.setText("Onurhan Şan")
        #print(self.textEdit.toPlainText()
        self.name_label_1.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.name_label_2.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.name_label_3.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.name_label_4.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.name_label_5.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.submitButton.clicked.connect(self.mail_progress)

        self.frameAB.close()

        self.scrollArea964 = QtWidgets.QScrollArea(self.frame_11)
        self.scrollArea964.setWidgetResizable(True)
        self.scrollArea964.setObjectName("scrollArea964")
        self.scrollArea964.setStyleSheet(
            "QScrollArea { background: rgb" + str(self.seconder_color) + ";\n border: none;\n}"
                                                                                             "QScrollBar:vertical {\n"
                                                                                             "     background-color: rgb" + str(
                self.scrollseconder) + ";\n"
                                       "     \n"
                                       "     border: 1px transparent #2A2929;\n"
                                       "     \n"
                                       "     width: 8px;\n"
                                       "}\n"
                                       " QScrollBar::handle:vertical {\n"
                                       "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                               "     min-height: 5px;\n"
                                                                                               "     border-radius: 4px;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:vertical {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: top;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:vertical {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: bottom;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: top;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: bottom;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"

                                                                                               "QScrollBar:horizontal {\n"
                                                                                               "     background-color: rgb" + str(
                self.scrollseconder) + ";\n"
                                       "     \n"
                                       "     border: 1px transparent #2A2929;\n"
                                       "     \n"
                                       "     height: 8px;\n"
                                       "}\n"
                                       " QScrollBar::handle:horizontal {\n"
                                       "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                               "     min-width: 5px;\n"
                                                                                               "     border-radius: 4px;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:horizontal {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: left;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:horizontal {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: right;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:horizontal:hover,QScrollBar::sub-line:horizontal:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: left;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: right;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n")

        self.tableWidget.setStyleSheet(
            " QTableWidget"
            "{"
            " margin-right: 10px;"
            "background-color: rgb" + str(self.seconder_color) + ";\n"
                                                                 "border: none;"

                                                                 "}"



                                                                 "QScrollBar:vertical {\n"
                                                                 "                                           background-color: rgb" + str(
                self.scrollseconder) + ";\n"
                                       "                                           \n"
                                       "                                           border: 1px transparent #2A2929;\n"
                                       "                                           \n"
                                       "                                           width: 8px;\n"
                                       "                                      }\n"
                                       "                                       QScrollBar::handle:vertical {\n"
                                       "                                           background-color: rgb" + str(
                self.scrollprimer) + ";\n"
                                     "                                           min-height: 5px;\n"
                                     "                                           border-radius: 4px;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::sub-line:vertical {\n"
                                     "                                           margin: 3px 0px 3px 0px;\n"
                                     "                                           border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                     "                                           height: 10px;\n"
                                     "                                           width: 10px;\n"
                                     "                                           subcontrol-position: top;\n"
                                     "                                           subcontrol-origin: margin;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::add-line:vertical {\n"
                                     "                                           margin: 3px 0px 3px 0px;\n"
                                     "                                           border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                     "                                           height: 10px;\n"
                                     "                                           width: 10px;\n"
                                     "                                           subcontrol-position: bottom;\n"
                                     "                                           subcontrol-origin: margin;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                     "                                           border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                     "                                           height: 10px;\n"
                                     "                                           width: 10px;\n"
                                     "                                           subcontrol-position: top;\n"
                                     "                                           subcontrol-origin: margin;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                     "                                           border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                     "                                           height: 10px;\n"
                                     "                                           width: 10px;\n"
                                     "                                           subcontrol-position: bottom;\n"
                                     "                                           subcontrol-origin: margin;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                     "                                           background: none;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                     "                                           background: none;\n"
                                     "                                      }\n"
                                     "\n"
                                     "QHeaderView::section{ \n"
                                     "             border-top:0px solid #D8D8D8; \n"
                                     "             border-left:0px solid #D8D8D8; \n"
                                     "             border-right:1px solid #D8D8D8; \n"
                                     "             border-bottom: 1px solid #D8D8D8; \n"
                                     "             background-color:white; \n"
                                     "             padding:4px; \n"
                                     "         } \n"
                                     "         QTableCornerButton::section{ \n"
                                     "             border-top:0px solid #D8D8D8; \n"
                                     "             border-left:0px solid #D8D8D8; \n"
                                     "             border-right:1px solid #D8D8D8; \n"
                                     "             border-bottom: 1px solid #D8D8D8; \n"
                                     "             background-color:white; \n"
                                     "         } ")

        self.scrollAreaWidgetContents43 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents43.setGeometry(QtCore.QRect(0, 0, 984, 499))
        self.scrollAreaWidgetContents43.setStyleSheet("")
        self.scrollAreaWidgetContents43.setObjectName("scrollAreaWidgetContents43")
        self.verticalLayout_2064 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents43)
        self.verticalLayout_2064.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2064.setSpacing(9)
        self.verticalLayout_2064.setObjectName("verticalLayout_2064")
        self.frame_54587 = QtWidgets.QFrame(self.scrollAreaWidgetContents43)
        self.frame_54587.setMinimumSize(QtCore.QSize(0, 75))
        self.frame_54587.setMaximumSize(QtCore.QSize(16777215, 75))
        self.frame_54587.setStyleSheet("background: transparent;")
        self.frame_54587.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_54587.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_54587.setObjectName("frame_54587")
        self.horizontalLayout_1442 = QtWidgets.QHBoxLayout(self.frame_54587)
        self.horizontalLayout_1442.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout_1442.setContentsMargins(-1, 0, -1, 0)
        self.horizontalLayout_1442.setSpacing(14)
        self.horizontalLayout_1442.setObjectName("horizontalLayout_1442")
        self.label010 = QtWidgets.QLabel(self.frame_54587)
        self.label010.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label010.sizePolicy().hasHeightForWidth())
        self.label010.setSizePolicy(sizePolicy)
        self.label010.setMinimumSize(QtCore.QSize(0, 0))
        self.label010.setMaximumSize(QtCore.QSize(70, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label010.setFont(font)
        self.label010.setStyleSheet("color: white;")
        self.label010.setObjectName("label010")
        self.horizontalLayout_1442.addWidget(self.label010)
        self.label011 = QtWidgets.QLabel(self.frame_54587)
        self.label011.setMaximumSize(QtCore.QSize(115, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label011.setFont(font)
        self.label011.setStyleSheet("color: white;")
        self.label011.setObjectName("label011")
        self.horizontalLayout_1442.addWidget(self.label011)
        self.label000 = QtWidgets.QLabel(self.frame_54587)
        self.label000.setMinimumSize(QtCore.QSize(0, 0))
        self.label000.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label000.setFont(font)
        self.label000.setStyleSheet("color: white;")
        self.label000.setObjectName("label000")
        self.horizontalLayout_1442.addWidget(self.label000)
        self.label001 = QtWidgets.QLabel(self.frame_54587)
        self.label001.setMaximumSize(QtCore.QSize(180, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label001.setFont(font)
        self.label001.setStyleSheet("color: white;")
        self.label001.setObjectName("label001")
        self.horizontalLayout_1442.addWidget(self.label001)
        self.label002 = QtWidgets.QLabel(self.frame_54587)
        self.label002.setMaximumSize(QtCore.QSize(105, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label002.setFont(font)
        self.label002.setStyleSheet("color: white;")
        self.label002.setObjectName("label002")
        self.horizontalLayout_1442.addWidget(self.label002)
        self.label003 = QtWidgets.QLabel(self.frame_54587)
        self.label003.setMaximumSize(QtCore.QSize(105, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label003.setFont(font)
        self.label003.setStyleSheet("color: white;")
        self.label003.setObjectName("label003")
        self.horizontalLayout_1442.addWidget(self.label003)
        self.label004 = QtWidgets.QLabel(self.frame_54587)
        self.label004.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label004.setFont(font)
        self.label004.setStyleSheet("color: white;")
        self.label004.setObjectName("label004")
        self.horizontalLayout_1442.addWidget(self.label004)
        self.verticalLayout_2064.addWidget(self.frame_54587)
        #
        self.scrollArea964.setWidget(self.scrollAreaWidgetContents43)
        self.verticalLayout_5.addWidget(self.scrollArea964)

        self.frame_2943 = QtWidgets.QFrame(self.frame_11)
        self.frame_2943.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2943.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2943.setObjectName("frame_2943")
        self.horizontalLayout030002 = QtWidgets.QHBoxLayout(self.frame_2943)
        self.horizontalLayout030002.setContentsMargins(11, 0, 11, 0)
        self.horizontalLayout030002.setSpacing(25)
        self.horizontalLayout030002.setObjectName("horizontalLayout030002")
        self.comboBox1254 = QtWidgets.QComboBox(self.frame_2943)
        self.comboBox1254.setMinimumSize(QtCore.QSize(0, 30))
        #self.frame_2943.setMinimumSize(QtCore.QSize(0, 60))
        self.comboBox1254.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.comboBox1254.setFont(font)
        self.comboBox1254.setStyleSheet("color: white;")
        self.comboBox1254.setObjectName("comboBox1254")
        self.comboBox1254.addItem("")

        self.comboBox1254.setStyleSheet("QComboBox {\n"
                                        "color:rgb" + str(self.text_color2) + ";\n"
                                                                              "background-color: transparent;\n"
                                                                              "selection-background-color: transparent;\n"
                                                                              "selection-color: rgb" + str(
            self.text_color2) + ";\n"
                                "}\n"
                                "QListView{\n"
                                "color:rgb" + str(self.text_color2) + ";\n"
                                                                      "}\n"
                                                                      "QScrollBar:vertical {\n"
                                                                      "     background-color: rgb" + str(
            self.scrollseconder) + ";\n"
                                   "     \n"
                                   "     border: 1px transparent #2A2929;\n"
                                   "     \n"
                                   "     width: 8px;\n"
                                   "}\n"
                                   " QScrollBar::handle:vertical {\n"
                                   "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                           "     min-height: 22px;\n"
                                                                                           "     border-radius: 4px;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-"
                                                                                           "position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n")

        self.horizontalLayout030002.addWidget(self.comboBox1254)

        self.comboBox1255 = QtWidgets.QComboBox(self.frame_2943)
        self.comboBox1255.setMinimumSize(QtCore.QSize(0, 30))
        self.comboBox1255.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.comboBox1255.setFont(font)
        self.comboBox1255.setStyleSheet("color: white;")
        self.comboBox1255.setObjectName("comboBox1255")
        self.comboBox1255.addItem("")

        self.comboBox1255.setStyleSheet("QComboBox {\n"
                                        "color:rgb" + str(self.text_color2) + ";\n"
                                                                              "background-color: transparent;\n"
                                                                              "selection-background-color: transparent;\n"
                                                                              "selection-color: rgb" + str(
            self.text_color2) + ";\n"
                                "}\n"
                                "QListView{\n"
                                "color:rgb" + str(self.text_color2) + ";\n"
                                                                      "}\n"
                                                                      "QScrollBar:vertical {\n"
                                                                      "     background-color: rgb" + str(
            self.scrollseconder) + ";\n"
                                   "     \n"
                                   "     border: 1px transparent #2A2929;\n"
                                   "     \n"
                                   "     width: 8px;\n"
                                   "}\n"
                                   " QScrollBar::handle:vertical {\n"
                                   "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                           "     min-height: 22px;\n"
                                                                                           "     border-radius: 4px;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-"
                                                                                           "position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n")

        self.horizontalLayout030002.addWidget(self.comboBox1255)

        self.pushButton_2189 = QtWidgets.QPushButton(self.frame_2943)
        self.pushButton_2189.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_2189.setMaximumSize(QtCore.QSize(320, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.pushButton_2189.setFont(font)
        self.pushButton_2189.setObjectName("pushButton_2189")
        self.horizontalLayout030002.addWidget(self.pushButton_2189)
        self.pushButton_2189.setEnabled(False)
        self.pushButton_3154 = QtWidgets.QPushButton(self.frame_2943)
        self.pushButton_3154.setMinimumSize(QtCore.QSize(0, 30))
        self.pushButton_3154.setMaximumSize(QtCore.QSize(280, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.pushButton_3154.setFont(font)
        self.pushButton_3154.setObjectName("pushButton_3154")
        self.horizontalLayout030002.addWidget(self.pushButton_3154)

        #self.pushButton_2189.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.pushButton_2189.setStyleSheet("QPushButton {\n"
                                    "    color: rgb"+ str(self.text_color2) + ";\n"
                                    "}\n"
                                    "QPushButton:hover {\n"
                                    "    background-color: rgb"+ str(self.hover4) + ";\n"
                                    "}\n"
                                    "QPushButton:pressed {    \n"
                                    "    background-color: rgb"+ str(self.pressed2) + ";\n"
                                    "}")

        self.pushButton_3154.setStyleSheet("QPushButton {\n"
                                           "    color: rgb" + str(self.text_color2) + ";\n"
                                                                                      "}\n"
                                                                                      "QPushButton:hover {\n"
                                                                                      "    background-color: rgb" + str(
            self.hover4) + ";\n"
                             "}\n"
                             "QPushButton:pressed {    \n"
                             "    background-color: rgb" + str(self.pressed2) + ";\n"
                                                                                "}")

        #self.pushButton_3154.setStyleSheet("color: white;")

        self.pushButton_3154.clicked.connect(self.startDownloadProgress)

        self.verticalLayout_5.addWidget(self.frame_2943)

        self.frame_2943.close()
        self.scrollArea964.close()

        uiFunctions.fill_archive_comboBox(self)

        self.label010.setText("CRN")
        """
        self.label011.setText(self.translate["Ders Kodu"][self.languageNumber])
        self.label000.setText(self.translate["Ders Adı"][self.languageNumber])
        self.label001.setText(self.translate["Öğretim Üyesi"][self.languageNumber])
        self.label002.setText(self.translate["Gün"][self.languageNumber])
        self.label003.setText(self.translate["Saat"][self.languageNumber])
        self.label004.setText(self.translate["Doluluk"][self.languageNumber])
        """
        self.label000.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label001.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label002.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label003.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label004.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label010.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label011.setStyleSheet("color: rgb{};".format(self.text_color2))
        #self.fr1 = uiClasses.archivedLecture()
        #self.verticalLayout_2064.addWidget(self.fr1)

        self.archiveSpacer = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2064.addItem(self.archiveSpacer)
        ####################################################################################################################
        self.frame_4 = QtWidgets.QFrame(self.frame_11)
        self.frame_4.setMaximumSize(QtCore.QSize(16777215, 51))
        self.frame_4.setStyleSheet("background: transparent;")
        self.frame_4.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame_4)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.label_version = QtWidgets.QLabel(self.frame_4)
        self.label_version.setMaximumSize(QtCore.QSize(2000, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        self.label_version.setFont(font)
        self.label_version.setStyleSheet("color: rgb{};".format(self.info_color))
        self.label_version.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_version.setObjectName("label_version")
        self.horizontalLayout_3.addWidget(self.label_version)
        self.verticalLayout_5.addWidget(self.frame_4)
        self.verticalLayout.addWidget(self.frame_12)
        self.horizontalLayout_9.addWidget(self.right_frame)

        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

        verticalHeader = self.tableWidget.verticalHeader()
        verticalHeader.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(6, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(7, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(8, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(9, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(10, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(11, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(12, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(13, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(14, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(15, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(16, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(17, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(18, QtWidgets.QHeaderView.Stretch)
        verticalHeader.setSectionResizeMode(19, QtWidgets.QHeaderView.Stretch)

        # PROGRAM KAYDET
        self.frame_6262 = QtWidgets.QFrame()
        self.frame_6262.setStyleSheet("background:transparent;border:none;")
        # self.frame_6262.setMinimumHeight(40)
        self.frame_6262.setFixedHeight(50)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_6262.sizePolicy().hasHeightForWidth())
        self.frame_6262.setSizePolicy(sizePolicy)
        self.frame_6262.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_6262.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_6262.setObjectName("frame_6262")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.frame_6262)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setContentsMargins(0, 10, 10, 10)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBox_6262 = QtWidgets.QComboBox(self.frame_6262)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboBox_6262.sizePolicy().hasHeightForWidth())
        self.comboBox_6262.setSizePolicy(sizePolicy)
        self.comboBox_6262.setMinimumSize(QtCore.QSize(100, 0))
        self.comboBox_6262.setStyleSheet("background-color: rgb(255, 255, 255); border: " + self.border + ";\n")
        self.comboBox_6262.setObjectName("comboBox_6262")
        self.horizontalLayout.addWidget(self.comboBox_6262)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)

        # self.horizontalLayout.addSpacerItem(spacerItem1)
        self.regen = QtWidgets.QPushButton(self.frame_6262)

        self.regen.setStyleSheet("QPushButton:disabled {\n"
                                 "background-color: #dddddd;\n"
                                 "}\n"
                                 "QPushButton:enabled {\n"
                                 "background-color: rgb(26, 80, 50);\n"
                                 "color: rgb(255, 255, 255);\n"
                                 "}\n"

                                 "border-radius: 2px;\n")

        self.regen.setMinimumSize(QtCore.QSize(120, 0))
        self.regen.setMaximumSize(QtCore.QSize(120, 30))

        self.horizontalLayout.addWidget(self.regen)

        self.update_label = QtWidgets.QLabel(self.frame_6262)
        self.update_label.setStyleSheet("background: transparent; color: rgb{}".format(self.text_color2))

        try:
            with open("cT.txt", encoding="utf-8") as file:
                data1 = file.read()
                self.update_label.setText(data1)
        except:
            pass

        self.horizontalLayout.addWidget(self.update_label)

        self.horizontalLayout.addSpacerItem(spacerItem)
        self.credit_label = QtWidgets.QLabel(self.frame_6262)
        self.credit_label.setText(self.translate["Toplam Kredi:"][self.languageNumber] + " 0.0")
        self.credit_label.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.horizontalLayout.addWidget(self.credit_label)

        self.pushButton_crn = QtWidgets.QPushButton(self.frame_6262)
        self.crnMenu = QtWidgets.QMenu()
        self.crnitem1 = QtWidgets.QAction()
        self.crnitem2 = QtWidgets.QAction()
        self.crnitem3 = QtWidgets.QAction()
        self.crnitem4 = QtWidgets.QAction()

        self.crnMenu.addAction(self.crnitem1)
        self.crnMenu.addAction(self.crnitem2)
        self.crnMenu.addAction(self.crnitem3)
        self.crnMenu.addAction(self.crnitem4)

        self.crnitem1.triggered.connect(self.copy_crn)
        self.crnitem2.triggered.connect(self.copy_JSCode)
        self.crnitem3.triggered.connect(self.save_to_computer)
        self.crnitem4.triggered.connect(self.save_table_ss)

        self.pushButton_crn.setMenu(self.crnMenu)

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_crn.sizePolicy().hasHeightForWidth())
        self.pushButton_crn.setSizePolicy(sizePolicy)
        self.pushButton_crn.setMinimumSize(QtCore.QSize(120, 0))
        self.pushButton_crn.setStyleSheet("QPushButton {\n"
                                          "background-color: #16CA64;\n"
                                          "color: rgb(255, 255, 255);\n"
                                          "}\n"

                                          "border-radius: 2px;\n")
        self.pushButton_crn.setObjectName("pushButton_crn")
        self.horizontalLayout.addWidget(self.pushButton_crn)
        # self.horizontalLayout.addSpacerItem(spacerItem1)

        self.lineEdit_6262 = QtWidgets.QLineEdit(self.frame_6262)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_6262.sizePolicy().hasHeightForWidth())
        self.lineEdit_6262.setSizePolicy(sizePolicy)
        self.lineEdit_6262.setMinimumSize(QtCore.QSize(150, 0))
        self.lineEdit_6262.setMaximumSize(QtCore.QSize(150, 30))
        self.lineEdit_6262.setStyleSheet("background-color: rgb(255, 255, 255); border: " + self.border + ";\n")
        self.lineEdit_6262.setInputMask("")
        self.lineEdit_6262.setText("")
        self.lineEdit_6262.setObjectName("lineEdit_6262")
        self.horizontalLayout.addWidget(self.lineEdit_6262)

        # self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_6262 = QtWidgets.QPushButton(self.frame_6262)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6262.sizePolicy().hasHeightForWidth())
        self.pushButton_6262.setSizePolicy(sizePolicy)
        self.pushButton_6262.setMinimumSize(QtCore.QSize(120, 0))
        self.pushButton_6262.setStyleSheet("QPushButton:disabled {\n"
                                           "background-color:#dddddd;\n"
                                           "}\n"
                                           "QPushButton:enabled {\n"
                                           "background-color: rgb(85, 170, 255);\n"
                                           "color: rgb(255, 255, 255);\n"
                                           "}\n"

                                           "border-radius: 2px;\n")
        self.pushButton_6262.setObjectName("pushButton_6262")
        self.horizontalLayout.addWidget(self.pushButton_6262)

        # self.horizontalLayout.addItem(spacerItem1)
        self.pushButton_6263 = QtWidgets.QPushButton(self.frame_6262)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_6263.sizePolicy().hasHeightForWidth())
        self.pushButton_6263.setSizePolicy(sizePolicy)
        self.pushButton_6263.setMinimumSize(QtCore.QSize(120, 0))
        self.pushButton_6263.setStyleSheet("background-color: red;\n"
                                           "color: rgb(255, 255, 255);\n"
                                           "border-radius: 2px;\n")
        self.pushButton_6263.setObjectName("pushButton_6263")
        self.horizontalLayout.addWidget(self.pushButton_6263)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setContentsMargins(0, 10, 30, 10)
        self.horizontalLayout.setStretch(1, 1)
        self.pushButton_6263.hide()
        uiFunctions.get_calendar(self)
        self.stdata = []

        def updateSavedTables():
            con = sqlite3.connect("SavedTables.db")
            cursor = con.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            data = cursor.fetchall()
            #print(data)

            if data != []:
                cursor.execute("SELECT Name, Data FROM Saves")
                self.stdata = cursor.fetchall()
                #print(self.stdata)

                if self.stdata != []:
                    self.comboBox_6262.blockSignals(True)
                    self.comboBox_6262.clear()
                    self.comboBox_6262.blockSignals(False)
                    self.comboBox_6262.addItem(self.translate["Seç"][self.languageNumber])
                    for a in self.stdata:
                        self.comboBox_6262.addItem(a[0])
                    #print(self.stdata[0][0])
                else:
                    self.comboBox_6262.blockSignals(True)
                    self.comboBox_6262.clear()
                    self.comboBox_6262.blockSignals(False)
                    self.comboBox_6262.addItem(self.translate["Seç"][self.languageNumber])
                    self.comboBox_6262.setCurrentText(self.translate["Seç"][self.languageNumber])
            else:
                self.comboBox_6262.blockSignals(True)
                self.comboBox_6262.clear()
                self.comboBox_6262.blockSignals(False)
                self.comboBox_6262.addItem(self.translate["Seç"][self.languageNumber])
                self.comboBox_6262.setCurrentText(self.translate["Seç"][self.languageNumber])

        updateSavedTables()

        if self.comboBox_6262.currentText() == self.translate["Seç"][self.languageNumber]:
            #print("s")
            self.pushButton_6262.setDisabled(True)

        def svdoe():
            if self.lineEdit_6262.text() == "":
                #print("EVET BOŞ")
                self.pushButton_6262.setDisabled(True)
            else:
                self.pushButton_6262.setEnabled(True)
            if self.lineEdit_6262.text() == self.comboBox_6262.currentText():
                self.pushButton_6262.setDisabled(True)
            else:
                self.pushButton_6262.setEnabled(True)

        self.lineEdit_6262.textChanged.connect(svdoe)

        def spchanged():
            try:
                selected = self.comboBox_6262.currentText()
                if self.changed == True and not self.programDeleted:
                    #print("DEĞİŞİKLKLER VAR")
                    msgBox = QtWidgets.QMessageBox()
                    msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                    msgBox.setText(self.translate["Programda kaydedilmemiş değişiklikler var kaydetmek istiyor musun?"][self.languageNumber])
                    msgBox.setWindowTitle(self.translate["Değişiklikleri Kaydet?"][self.languageNumber])
                    msgBox.setStandardButtons(
                        QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.No | QtWidgets.QMessageBox.Cancel)
                    buttony = msgBox.button(QtWidgets.QMessageBox.Ok)
                    buttony.setText(self.translate["Kaydet"][self.languageNumber])

                    buttonz = msgBox.button(QtWidgets.QMessageBox.No)
                    buttonz.setText(self.translate["Kaydetme"][self.languageNumber])
                    # msgBox.buttonClicked.connect(msgButtonClick)

                    returnValue = msgBox.exec()

                    if returnValue == QtWidgets.QMessageBox.Ok:
                        #print("KAYDEDİLCEK")
                        #print("KAYDEDİYORUM")
                        #print(self.lineEdit_6262.text())
                        #print(self.items)
                        con = sqlite3.connect("SavedTables.db")
                        cursor = con.cursor()
                        cursor.execute(
                            "CREATE TABLE IF NOT EXISTS Saves (Name TEXT PRIMARY KEY, Data TEXT)")

                        cursor.execute("INSERT OR IGNORE INTO Saves VALUES(?,?)",
                                       (self.lineEdit_6262.text(), str(self.items)))

                        cursor.execute("UPDATE Saves SET Data = ? WHERE Name= ?",
                                       (str(self.items), self.lineEdit_6262.text()))
                        con.commit()
                        con.close()

                        self.changed = False
                        updateSavedTables()
                        self.comboBox_6262.setCurrentText(selected)
                        spchangednext()

                    if returnValue == QtWidgets.QMessageBox.No:
                        #print("Kaydedilmeyecek")
                        self.changed = False
                        spchangednext()

                    if returnValue == QtWidgets.QMessageBox.Cancel:
                        #print("Hiç bi şey yapılmayacak")
                        return

                else:
                    self.programDeleted = False
                    spchangednext()
            except:
                #print("AÇAMIYORUM HÜÜÜÜÜÜ")
                msgBox = QtWidgets.QMessageBox()
                msgBox.setIcon(QtWidgets.QMessageBox.Warning)
                msgBox.setText(self.translate["Bu ders programı açılamadı. Bu program güncel değil veya Courses.db dosyası silinmiş."][self.languageNumber])
                msgBox.setWindowTitle(self.translate["Hata"][self.languageNumber])
                msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                buttony = msgBox.button(QtWidgets.QMessageBox.Ok)
                buttony.setText(self.translate["{} Sil"][
                    self.languageNumber].format(
                    self.comboBox_6262.currentText()))
                buttonz = msgBox.button(QtWidgets.QMessageBox.Cancel)
                buttonz.setText(self.translate["Tamam"][self.languageNumber])
                # msgBox.buttonClicked.connect(msgButtonClick)

                returnValue = msgBox.exec()

                if returnValue == QtWidgets.QMessageBox.Ok:
                    deleteprogram()

                else:
                    #print("HİÇ Bİ ŞEY YAPILMAYACAK")
                    self.comboBox_6262.setCurrentIndex(0)


        def spchangednext():
            #print("Değişiklikler YOK")
            self.tablosuz_dersler = list()
            self.table_credit = 0.0
            if self.comboBox_6262.currentText() == self.translate["Seç"][self.languageNumber]:
                self.credit_label.setText(self.translate["Toplam Kredi:"][self.languageNumber] + " 0.0")
                #print("SELECT SEÇİLDİ SAYFA SIFIRLANACAK")
                for i in range(self.verticalLayout_002.count() - 3):
                    self.verticalLayout_002.itemAt(i).widget().deleteLater()
                self.items = {}
                self.rebuildTable(self.items)
                self.lineEdit_6262.clear()
                self.pushButton_6263.hide()
                self.verticalLayout_002.insertWidget(self.verticalLayout_002.count() - 3,
                                                     uiClasses.OpenLecture(self, str(uuid.uuid4()), "", "", "", "",
                                                                           self.hover, self.pressed, self.border,
                                                                           self.exit, self.updating))

            else:
                for i in range(self.verticalLayout_002.count() - 3):
                    self.verticalLayout_002.itemAt(i).widget().deleteLater()
                #print("DATABASEDEN GELEN VERİ")
                #print(self.stdata)
                s = [item for item in self.stdata if item[0] == self.comboBox_6262.currentText()]
                map = json.loads(s[0][1].replace("'", '"').replace("True", 'true').replace("False", 'false'))
                self.items = map

                for k, v in map.items():
                    if v != {} and "c" not in v:
                        self.verticalLayout_002.insertWidget(self.verticalLayout_002.count() - 3,
                                                             uiClasses.OpenLecture(self, k, v["dep"], v["name"],
                                                                                   v["crn"], v, self.hover,
                                                                                   self.pressed, self.border,
                                                                                   self.exit, self.updating))
                    elif "c" in v:
                        cakisan_ders = uiClasses.OpenLecture(self, k, v["dep"], v["name"],
                                                                                   v["crn"], v, self.hover,
                                                                                   self.pressed, self.border,
                                                                                   self.exit, self.updating)
                        cakisan_ders.setStyleSheet("background: red; border:none")
                        self.verticalLayout_002.insertWidget(self.verticalLayout_002.count() - 3, cakisan_ders)
                ci = self.comboBox_6262.currentIndex() - 1

                for i in self.items.values():
                    if i["coordinates"] == {}:
                        con = sqlite3.connect("Courses.db")
                        cursor = con.cursor()
                        cursor.execute(
                            "SELECT CourseCode FROM {} WHERE CRN = '{}'".format(i["dep"], i["crn"]))
                        data = cursor.fetchall()
                        ders_kodu = data[0][0].split()
                        self.tablosuz_dersler.append(ders_kodu)

                self.rebuildTable(map)
                self.lineEdit_6262.setText(self.comboBox_6262.currentText())
                self.pushButton_6263.show()
                self.pushButton_6262.setDisabled(True)

        self.comboBox_6262.currentIndexChanged.connect(spchanged)

        def addprogram():
            #print("KAYDEDİYORUM")
            #print(self.lineEdit_6262.text())
            for i, k in self.items.copy().items():
                if "crn" not in k:
                    del self.items[i]
            con = sqlite3.connect("SavedTables.db")
            cursor = con.cursor()
            cursor.execute(
                "CREATE TABLE IF NOT EXISTS Saves (Name TEXT PRIMARY KEY, Data TEXT)")

            cursor.execute("INSERT OR IGNORE INTO Saves VALUES(?,?)", (self.lineEdit_6262.text(), str(self.items)))

            cursor.execute("UPDATE Saves SET Data = ? WHERE Name= ?", (str(self.items), self.lineEdit_6262.text()))
            con.commit()
            con.close()
            self.changed = False
            updateSavedTables()
            self.comboBox_6262.setCurrentText(self.lineEdit_6262.text())

        self.pushButton_6262.clicked.connect(addprogram)

        def deleteprogram():
            self.programDeleted = True
            #print("SİL")
            #print(self.comboBox_6262.currentText())
            con = sqlite3.connect("SavedTables.db")
            cursor = con.cursor()
            cursor.execute("DELETE FROM Saves WHERE Name = ?", (self.comboBox_6262.currentText(),))
            con.commit()
            con.close()
            updateSavedTables()
            self.pushButton_6263.hide()
            self.comboBox_6262.setCurrentIndex(0)

        self.pushButton_6263.clicked.connect(deleteprogram)

        self.verticalLayout_002.addWidget(self.frame_6262)

        ###############

        self.frame_542.setStyleSheet("background-color: rgb{};".format(self.seconder_color))
        self.frame_4.setStyleSheet("background-color: rgb{};".format(self.seconder_color))
        self.frame_542.close()
        self.scrollArea004.close()

        self.verticalLayout.addWidget(self.frame_12)
        self.horizontalLayout_9.addWidget(self.right_frame)
        # self.setCentralWidget(self.centralwidget)

        self.settings_window = QtWidgets.QFrame(self.frame_11)
        self.settings_window.setMinimumSize(QtCore.QSize(0, 0))
        self.settings_window.setMaximumSize(QtCore.QSize(9999, 0))
        self.settings_window.setStyleSheet("background-color: rgb" + str(self.primer_color) + ";\n"
                                                                                              "border:none;")
        self.settings_window.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.settings_window.setFrameShadow(QtWidgets.QFrame.Raised)
        self.settings_window.setObjectName("settings_window")
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout(self.settings_window)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.frame_18 = QtWidgets.QFrame(self.settings_window)
        self.frame_18.setMinimumSize(QtCore.QSize(351, 191))
        self.frame_18.setMaximumSize(QtCore.QSize(351, 191))
        self.frame_18.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_18.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_18.setObjectName("frame_18")
        self.verticalLayout_11 = QtWidgets.QVBoxLayout(self.frame_18)
        self.verticalLayout_11.setContentsMargins(-1, 0, -1, -1)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.frame_17 = QtWidgets.QFrame(self.frame_18)
        self.frame_17.setStyleSheet("background-color: transparent;\n"
                                    "    border-radius: 30px;")
        self.frame_17.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_17.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_17.setObjectName("frame_17")
        self.verticalLayout_258 = QtWidgets.QVBoxLayout(self.frame_17)
        self.verticalLayout_258.setSpacing(0)
        self.verticalLayout_258.setObjectName("verticalLayout_258")
        self.frame_13 = QtWidgets.QFrame(self.frame_17)
        self.frame_13.setMinimumSize(QtCore.QSize(289, 0))
        self.frame_13.setMaximumSize(QtCore.QSize(9999, 51))
        self.frame_13.setStyleSheet("background-color:rgb" + str(self.paletteOpacity) + ";\n"
                                                                                        "    border: 5px solid rgb" + str(
            self.seconder_color) + ";\n"
                                   "    border-radius: 25px;")
        self.frame_13.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_13.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_13.setObjectName("frame_13")
        self.horizontalLayout_101 = QtWidgets.QHBoxLayout(self.frame_13)
        self.horizontalLayout_101.setContentsMargins(0, 0, 26, 0)
        self.horizontalLayout_101.setObjectName("horizontalLayout_101")
        self.frame_14 = QtWidgets.QFrame(self.frame_13)
        self.frame_14.setMinimumSize(QtCore.QSize(85, 59))
        self.frame_14.setMaximumSize(QtCore.QSize(16777215, 59))
        self.frame_14.setStyleSheet("background-color:transparent;\n"
                                    "border: none;")
        self.frame_14.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_14.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_14.setObjectName("frame_14")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_14)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 23)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label = QtWidgets.QLabel(self.frame_14)
        self.label.setMinimumSize(QtCore.QSize(90, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label.setStyleSheet("color:rgb" + str(self.text_color) + ";\n"
                                                                      "background-color:transparent;\n"
                                                                      "border:none;\n"
                                                                      "")
        self.label.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.verticalLayout_8.addWidget(self.label)
        self.horizontalLayout_101.addWidget(self.frame_14)
        self.theme1 = QtWidgets.QPushButton(self.frame_13)
        self.theme1.setMinimumSize(QtCore.QSize(35, 35))
        self.theme1.setMaximumSize(QtCore.QSize(35, 35))
        self.theme1.setStyleSheet("\n"
                                  "QPushButton {\n"
                                  "    background-position: center;\n"
                                  "    background-repeat: no-repeat;\n"
                                  "    background-color: rgb(39, 44, 54);\n"
                                  "    border: 7px solid  rgb(27, 29, 35);\n"
                                  "    border-radius: 10px;\n"
                                  "}\n"
                                  "QPushButton:hover {\n"
                                  "    background-color: rgb(69, 74, 84);\n"
                                  "}\n"
                                  "QPushButton:pressed {    \n"
                                  "    background-color: rgb(85, 170, 255);\n"
                                  "}")

        self.theme1.setText("")
        self.theme1.setObjectName("theme1")
        self.horizontalLayout_101.addWidget(self.theme1)
        self.theme2 = QtWidgets.QPushButton(self.frame_13)
        self.theme2.setMinimumSize(QtCore.QSize(35, 35))
        self.theme2.setMaximumSize(QtCore.QSize(35, 35))
        self.theme2.setStyleSheet("\n"
                                  "QPushButton {\n"
                                  "    background-position: center;\n"
                                  "    background-repeat: no-repeat;\n"
                                  "    background-color: rgb(166, 182, 242);\n"
                                  "    border: 7px solid  rgb(9, 21, 64);\n"
                                  "    border-radius: 10px;\n"
                                  "}\n"
                                  "QPushButton:hover {\n"
                                  "    background-color: rgb(186, 202, 255);\n"
                                  "}\n"
                                  "QPushButton:pressed {    \n"
                                  "    background-color: rgb(9, 21, 100, 200);\n"
                                  "}")
        self.theme2.setText("")
        self.theme2.setObjectName("theme2")
        self.horizontalLayout_101.addWidget(self.theme2)
        self.theme3 = QtWidgets.QPushButton(self.frame_13)
        self.theme3.setMinimumSize(QtCore.QSize(35, 35))
        self.theme3.setMaximumSize(QtCore.QSize(35, 35))
        self.theme3.setStyleSheet("\n"
                                  "QPushButton {\n"
                                  "    background-position: center;\n"
                                  "    background-repeat: no-repeat;\n"
                                  "    background-color: rgb(212, 223, 199);\n"
                                  "    border: 7px solid  rgb(87, 15, 22);\n"
                                  "    border-radius: 10px;\n"
                                  "}\n"
                                  "QPushButton:hover {\n"
                                  "    background-color: rgb(242, 253, 229);\n"
                                  "}\n"
                                  "QPushButton:pressed {    \n"
                                  "    background-color: rgb(110, 45, 50, 200);\n"
                                  "}")
        self.theme3.setText("")
        self.theme3.setObjectName("theme3")
        self.horizontalLayout_101.addWidget(self.theme3)
        self.theme4 = QtWidgets.QPushButton(self.frame_13)
        self.theme4.setMinimumSize(QtCore.QSize(35, 35))
        self.theme4.setMaximumSize(QtCore.QSize(35, 35))
        self.theme4.setStyleSheet("\n"
                                  "QPushButton {\n"
                                  "    background-position: center;\n"
                                  "    background-repeat: no-repeat;\n"
                                  "    background-color: rgb(255, 255, 255);\n"
                                  "    border: 7px solid  rgb(0, 200, 153);\n"
                                  "    border-radius: 10px;\n"
                                  "}\n"
                                  "QPushButton:hover {\n"
                                  "    background-color: rgb(230, 230, 230);\n"
                                  "}\n"
                                  "QPushButton:pressed {    \n"
                                  "    background-color: rgb(230, 230, 230, 200);\n"
                                  "}")
        self.theme4.setText("")
        self.theme4.setObjectName("theme4")
        self.horizontalLayout_101.addWidget(self.theme4)

        if self.themeNumber == 1:
            self.theme1.setEnabled(False)
            self.theme2.setEnabled(True)
            self.theme3.setEnabled(True)
            self.theme4.setEnabled(True)

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/user/tick.png"), QtGui.QIcon.Disabled,
                           QtGui.QIcon.Off)
            self.theme1.setIcon(icon)
            self.theme2.setIcon(QtGui.QIcon())
            self.theme3.setIcon(QtGui.QIcon())
            self.theme4.setIcon(QtGui.QIcon())

        elif self.themeNumber == 2:
            self.theme2.setEnabled(False)
            self.theme1.setEnabled(True)
            self.theme3.setEnabled(True)
            self.theme4.setEnabled(True)

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/user/tick_dark.png"), QtGui.QIcon.Disabled,
                           QtGui.QIcon.Off)
            self.theme2.setIcon(icon)
            self.theme1.setIcon(QtGui.QIcon())
            self.theme3.setIcon(QtGui.QIcon())
            self.theme4.setIcon(QtGui.QIcon())

        elif self.themeNumber == 3:
            self.theme3.setEnabled(False)
            self.theme2.setEnabled(True)
            self.theme1.setEnabled(True)
            self.theme4.setEnabled(True)

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/user/tick_dark.png"), QtGui.QIcon.Disabled,
                           QtGui.QIcon.Off)
            self.theme3.setIcon(icon)
            self.theme2.setIcon(QtGui.QIcon())
            self.theme1.setIcon(QtGui.QIcon())
            self.theme4.setIcon(QtGui.QIcon())

        elif self.themeNumber == 4:
            self.theme4.setEnabled(False)
            self.theme2.setEnabled(True)
            self.theme3.setEnabled(True)
            self.theme1.setEnabled(True)

            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap(":/user/tick.png"), QtGui.QIcon.Disabled,
                           QtGui.QIcon.Off)
            self.theme4.setIcon(icon)
            self.theme2.setIcon(QtGui.QIcon())
            self.theme3.setIcon(QtGui.QIcon())
            self.theme1.setIcon(QtGui.QIcon())

        self.verticalLayout_258.addWidget(self.frame_13)
        self.frame_15 = QtWidgets.QFrame(self.frame_17)
        self.frame_15.setMaximumSize(QtCore.QSize(9999, 51))
        self.frame_15.setStyleSheet("")
        self.frame_15.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_15.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_15.setObjectName("frame_15")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame_15)
        self.horizontalLayout_11.setContentsMargins(15, 0, 20, 0)
        self.horizontalLayout_11.setSpacing(12)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.frame_16 = QtWidgets.QFrame(self.frame_15)
        self.frame_16.setMinimumSize(QtCore.QSize(150, 41))
        self.frame_16.setMaximumSize(QtCore.QSize(16777215, 59))
        self.frame_16.setStyleSheet("background-color:transparent;\n"
                                    "border: none;")
        self.frame_16.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_16.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_16.setObjectName("frame_16")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.frame_16)
        self.verticalLayout_9.setContentsMargins(0, 0, 32, 0)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.label_3 = QtWidgets.QLabel(self.frame_16)
        self.label_3.setMinimumSize(QtCore.QSize(120, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.label_3.setStyleSheet("color:rgb" + str(self.text_color) + ";\n"
                                                                        "background-color:transparent;\n"
                                                                        "border:none;\n"
                                                                        "")
        self.label_3.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_9.addWidget(self.label_3)
        self.horizontalLayout_11.addWidget(self.frame_16)
        self.TRButton = QtWidgets.QPushButton(self.frame_15)
        self.TRButton.setMinimumSize(QtCore.QSize(38, 38))
        self.TRButton.setMaximumSize(QtCore.QSize(38, 38))
        self.TRButton.setText("")
        self.TRButton.setObjectName("TRButton")
        self.horizontalLayout_11.addWidget(self.TRButton)
        self.UKButton = QtWidgets.QPushButton(self.frame_15)
        self.UKButton.setMinimumSize(QtCore.QSize(38, 38))
        self.UKButton.setMaximumSize(QtCore.QSize(38, 38))
        self.UKButton.setText("")
        self.UKButton.setObjectName("UKButton")
        self.horizontalLayout_11.addWidget(self.UKButton)
        self.DEButton = QtWidgets.QPushButton(self.frame_15)
        self.DEButton.setMinimumSize(QtCore.QSize(38, 38))
        self.DEButton.setMaximumSize(QtCore.QSize(38, 38))
        self.DEButton.setText("")
        self.DEButton.setObjectName("DEButton")
        self.horizontalLayout_11.addWidget(self.DEButton)

        if self.languageNumber == 0:
            self.TRButton.setStyleSheet("QPushButton {\n"
                                        "    background-position: center;\n"
                                        "    background-repeat: no-reperat;\n"
                                        "    image:url(:/flag/tr-flagIcon.png);\n"
                                        "    border : 4px solid white;\n"
                                        "    border-radius:19px;\n"
                                        "}")
            self.TRButton.setEnabled(False)
            self.UKButton.setEnabled(True)
            self.DEButton.setEnabled(True)
            self.UKButton.setStyleSheet("QPushButton {\n"
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
                                        "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                                          "}")
            self.DEButton.setStyleSheet("QPushButton {\n"
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
                                        "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                                          "}")

        elif self.languageNumber == 1:
            self.UKButton.setStyleSheet("QPushButton {\n"
                                        "    background-position: center;\n"
                                        "    background-repeat: no-reperat;\n"
                                        "    image:url(:/flag/uk-flagIcon.png);\n"
                                        "    border : 4px solid white;\n"
                                        "    border-radius:19px;\n"
                                        "}")
            self.UKButton.setEnabled(False)
            self.TRButton.setEnabled(True)
            self.DEButton.setEnabled(True)
            self.TRButton.setStyleSheet("QPushButton {\n"
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
                                        "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                                          "}")
            self.DEButton.setStyleSheet("QPushButton {\n"
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
                                        "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                                          "}")
        elif self.languageNumber == 2:
            self.DEButton.setStyleSheet("QPushButton {\n"
                                        "    background-position: center;\n"
                                        "    background-repeat: no-reperat;\n"
                                        "    image:url(:/flag/de-flagIcon.png);\n"
                                        "    border : 4px solid white;\n"
                                        "    border-radius:19px;\n"
                                        "}")
            self.DEButton.setEnabled(False)
            self.UKButton.setEnabled(True)
            self.DEButton.setEnabled(True)
            self.UKButton.setStyleSheet("QPushButton {\n"
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
                                        "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                                          "}")
            self.TRButton.setStyleSheet("QPushButton {\n"
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
                                        "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                                          "}")

        self.verticalLayout_258.addWidget(self.frame_15)
        self.frame_19 = QtWidgets.QFrame(self.frame_17)
        self.frame_19.setMaximumSize(QtCore.QSize(9999, 51))
        self.frame_19.setStyleSheet("")
        self.frame_19.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_19.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_19.setObjectName("frame_19")
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout(self.frame_19)
        self.horizontalLayout_19.setContentsMargins(35, 0, 0, 0)
        self.horizontalLayout_19.setSpacing(0)
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.horizontalLayout_19.setAlignment(QtCore.Qt.AlignHCenter)
        self.frame_29 = QtWidgets.QFrame(self.frame_19)
        self.frame_29.setMinimumSize(QtCore.QSize(150, 24))
        self.frame_29.setMaximumSize(QtCore.QSize(280, 41))
        self.frame_29.setStyleSheet("background-color:transparent;\n"
                                    "border: none;")
        self.frame_29.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_29.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_29.setObjectName("frame_29")
        self.verticalLayout_24 = QtWidgets.QVBoxLayout(self.frame_29)
        self.verticalLayout_24.setContentsMargins(0, 0, 48, 0)
        self.verticalLayout_24.setSpacing(0)
        self.verticalLayout_24.setObjectName("verticalLayout_24")

        self.label_11 = QtWidgets.QCheckBox(self.frame_29)
        self.label_11.setMinimumSize(QtCore.QSize(90, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label_11.setFont(font)
        self.label_11.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.label_11.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)

        #self.label_11.setStyleSheet()
        """
        self.label_11.setStyleSheet("QCheckBox"
                               "{"
                               "color:rgb" + str(self.text_color) + ";\n"
                               #"border : 2px solid clack;"
                               "}"
                               "QCheckBox::indicator"
                               "{"
                               "width : 17px;"
                               "height : 17px;"
                               "padding : 4px;"
                               "}")
        """
        self.label_11.setStyleSheet("color:rgb" + str(self.text_color) + ";\n"
                                                                         "background-color:transparent;\n"
                                                                         "border:none;\n"
                                                                         "")
        #self.label_11.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_11.setObjectName("label_11")
        self.verticalLayout_24.addWidget(self.label_11)

        self.label_11.setChecked(self.Tooltip)
        #spacerItem29 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.horizontalLayout_19.addItem(spacerItem29)
        self.horizontalLayout_19.addWidget(self.frame_29)
        #spacerItem29 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.horizontalLayout_19.addItem(spacerItem29)
        #self.frame_21 = QtWidgets.QFrame(self.frame_19)
        #self.frame_21.setMinimumSize(QtCore.QSize(180, 0))
        #self.frame_21.setMaximumSize(QtCore.QSize(16777215, 41))
        #self.frame_21.setFrameShape(QtWidgets.QFrame.NoFrame)
        #self.frame_21.setFrameShadow(QtWidgets.QFrame.Raised)
        #self.frame_21.setObjectName("frame_21")
        #self.verticalLayout_23 = QtWidgets.QVBoxLayout(self.frame_21)
        #self.verticalLayout_23.setContentsMargins(0, 0, 0, 0)
        #self.verticalLayout_23.setSpacing(0)
        #self.verticalLayout_23.setObjectName("verticalLayout_23")
        #self.comboBox_font = QtWidgets.QComboBox(self.frame_21)
        #self.comboBox_font.setMinimumSize(QtCore.QSize(135, 24))
        #self.comboBox_font.setStyleSheet("border: 3px solid rgb" + str(self.seconder_color) + ";\n"
        #                                                                                      "border-radius: 0px;\n"
        #                                                                                      "color:rgb" + str(
        #    self.text_color) + ";\n")
        #self.comboBox_font.setEditable(False)
        #self.comboBox_font.setFrame(True)
        #self.comboBox_font.setObjectName("comboBox_font")
        #self.comboBox_font.addItem("")
        #self.comboBox_font.addItem("")
        #self.comboBox_font.addItem("")
        #self.comboBox_font.addItem("")
        #self.comboBox_font.addItem("")
        #self.comboBox_font.addItem("")
        #self.verticalLayout_23.addWidget(self.comboBox_font)
        #self.horizontalLayout_19.addWidget(self.frame_21)
        self.verticalLayout_258.addWidget(self.frame_19)
        self.frame_37 = QtWidgets.QFrame(self.frame_17)
        self.frame_37.setMaximumSize(QtCore.QSize(9999, 51))
        self.frame_37.setStyleSheet("")
        self.frame_37.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_37.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_37.setObjectName("frame_37")
        self.horizontalLayout_22 = QtWidgets.QHBoxLayout(self.frame_37)
        self.horizontalLayout_22.setContentsMargins(25, 0, 5, 0)
        self.horizontalLayout_22.setSpacing(0)
        self.horizontalLayout_22.setObjectName("horizontalLayout_22")
        #self.frame_42 = QtWidgets.QFrame(self.frame_37)
        #self.frame_42.setMinimumSize(QtCore.QSize(85, 24))
        #self.frame_42.setMaximumSize(QtCore.QSize(16777215, 41))
        #self.frame_42.setStyleSheet("background-color:transparent;\n"
        #                            "border: none;")
        #self.frame_42.setFrameShape(QtWidgets.QFrame.NoFrame)
        #self.frame_42.setFrameShadow(QtWidgets.QFrame.Raised)
        #self.frame_42.setObjectName("frame_42")
        #self.verticalLayout_29 = QtWidgets.QVBoxLayout(self.frame_42)
        #self.verticalLayout_29.setContentsMargins(0, 0, 0, 0)
        #self.verticalLayout_29.setSpacing(0)
        #self.verticalLayout_29.setObjectName("verticalLayout_29")
        #self.label_14 = QtWidgets.QLabel(self.frame_42)
        #self.label_14.setMinimumSize(QtCore.QSize(90, 0))
        #font = QtGui.QFont()
        #font.setFamily("Segoe UI")
        #font.setPointSize(14)
        #self.label_14.setFont(font)
        #self.label_14.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        #self.label_14.setStyleSheet("color:rgb" + str(self.text_color) + ";\n"
        #                                                                 "background-color:transparent;\n"
        #                                                                 "border:none;\n"
        #                                                                "")
        #self.label_14.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        #self.label_14.setObjectName("label_14")
        #self.verticalLayout_29.addWidget(self.label_14)
        #self.horizontalLayout_22.addWidget(self.frame_42)
        self.frame_43 = QtWidgets.QFrame(self.frame_37)
        self.frame_43.setMinimumSize(QtCore.QSize(290, 0))
        self.frame_43.setMaximumSize(QtCore.QSize(16777215, 55))
        self.frame_43.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_43.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_43.setObjectName("frame_43")
        self.verticalLayout_30 = QtWidgets.QVBoxLayout(self.frame_43)
        self.verticalLayout_30.setContentsMargins(40, 5, 85, 0)
        self.verticalLayout_30.setSpacing(0)
        self.verticalLayout_30.setObjectName("verticalLayout_30")
        self.Color_Button = QtWidgets.QPushButton(self.frame_43)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(8)

        self.Color_Button.setMinimumSize(QtCore.QSize(0, 26))
        self.Color_Button.setStyleSheet("QPushButton {\n"
                                        "    color: rgb" + str(self.text_color) + ";\n"
                                        "    background-position: center;\n"
                                        "    background-repeat: no-reperat;\n"
                                        #"    border: 5px solid black;\n"
                                        "    border-radius:12px;\n"
                                        "    background-color: rgb" + str(self.paletteOpacity) + ";\n"
                                                                                             "}\n"
                                                                                             "\n"
                                        "QPushButton:hover {    \n"
                                                                                             "    background-color: rgb" + str(
            self.hover2) + ";}\n"
                                                                                             "QPushButton:pressed {    \n"
                                                                                             "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")
        self.Color_Button.setText("")
        self.Color_Button.setObjectName("Color_Button")
        self.verticalLayout_30.addWidget(self.Color_Button)
        self.horizontalLayout_22.addWidget(self.frame_43)
        self.verticalLayout_258.addWidget(self.frame_37)
        self.verticalLayout_11.addWidget(self.frame_17)
        self.horizontalLayout_12.addWidget(self.frame_18)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem6)
        self.verticalLayout_5.addWidget(self.settings_window)
        self.horizontalLayout_8.addWidget(self.frame_11)
        self.verticalLayout.addWidget(self.frame_12)

        #self.frame_19.close()
        #self.frame_37.close()

        self.okButton.close()
        self.cancelButton.close()

        self.capCode.addItem(self.translate["ÇAP/YANDAL"][self.languageNumber])
        self.depCode.addItem(self.translate["BÖLÜM KODU"][self.languageNumber])

        self.retranslateUi()
        self.regen.clicked.connect(self.startProgress)
        QtCore.QMetaObject.connectSlotsByName(self)

    def show_menu(self):
        if not self.menu_open:

            self.menu_anim = QtCore.QPropertyAnimation(self.tabs_window, b"minimumWidth")
            self.menu_anim.setDuration(300)
            self.menu_anim.setStartValue(0)
            self.menu_anim.setEndValue(200)
            self.menu_anim.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.menu_anim.start()
            self.menu_open = True

        else:
            self.menu_anim = QtCore.QPropertyAnimation(self.tabs_window, b"minimumWidth")
            self.menu_anim.setDuration(300)
            self.menu_anim.setStartValue(200)
            self.menu_anim.setEndValue(0)
            self.menu_anim.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.menu_anim.start()
            self.menu_open = False

    def show_settings(self):
        if not self.settings_open:

            self.settings_anim = QtCore.QPropertyAnimation(self.settings_window, b"maximumHeight")
            self.settings_anim.setDuration(300)
            self.settings_anim.setStartValue(0)
            self.settings_anim.setEndValue(200)
            self.settings_anim.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.settings_anim.start()
            self.settings_open = True

        else:
            self.settings_anim = QtCore.QPropertyAnimation(self.settings_window, b"maximumHeight")
            self.settings_anim.setDuration(300)
            self.settings_anim.setStartValue(200)
            self.settings_anim.setEndValue(0)
            self.settings_anim.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
            self.settings_anim.start()
            self.settings_open = False

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.top_label.setText(_translate("MainWindow", "İTÜ Kraken"))
        self.minimize_button.setToolTip(_translate("MainWindow", "Minimize"))
        self.maximize_button.setToolTip(_translate("MainWindow", "Maximize"))
        self.exit_button.setToolTip(_translate("MainWindow", "Close"))
        self.label_top_info_2.setText(_translate("MainWindow", self.translate[self.tabName][self.languageNumber]))
        self.program_name_label.setText(
            _translate("MainWindow", "<html><head/><body><p align=\"center\">KRAKEN</p></body></html>"))
        # self.clock_label.setText(_translate("MainWindow", "10:38"))
        self.groupBox.setTitle(_translate("MainWindow", self.translate["Kısayollar"][self.languageNumber]))
        # self.history_label.setText(_translate("MainWindow",
        # "<html><head/><body><p align=\"center\">26 Ekim</p><p align=\"center\">Perşembe</p></body></html>"))
        self.label_version.setText(_translate("MainWindow", "v1.0.5"))

        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p align=\"center\">{}</p></body></html>".format(
                                          self.translate["Tema"][self.languageNumber])))
        self.label_3.setText(
            _translate("MainWindow", "<html><head/><body><p align=\"center\">{}</p></body></html>".format(
                self.translate["Dil & Bölge"][self.languageNumber])))
        self.label_11.setText(
            _translate("MainWindow","{}").format(
                self.translate["İpuçlarını göster"][self.languageNumber]))
        #self.comboBox_font.setItemText(0, _translate("MainWindow", " Segoe UI"))
        #self.comboBox_font.setItemText(1, _translate("MainWindow", " Times New Roman"))
        #self.comboBox_font.setItemText(2, _translate("MainWindow", " Arial"))
        #self.comboBox_font.setItemText(3, _translate("MainWindow", " Calibri"))
        #self.comboBox_font.setItemText(4, _translate("MainWindow", " Comic Sans MS"))
        #self.comboBox_font.setItemText(5, _translate("MainWindow", " MS Shell Dlg 2"))
        #self.label_14.setText(
        #    _translate("MainWindow", "<html><head/><body><p align=\"center\">{}</p></body></html>".format(
        #        self.translate["Yazı Rengi"][self.languageNumber])))

        # self.AgButton.setText(_translate("MainWindow", "AG"))
        # self.name_lineEdit.setText(_translate("MainWindow", "Adem Geçgel"))
        self.label_621.setText(_translate("MainWindow", "GPA:"))
        # self.gpaLabel.setText(_translate("MainWindow", "3.20"))
        self.label_321.setText(_translate("MainWindow", self.translate["Derslerim"][self.languageNumber]))
        # self.depCode.setItemText(0, _translate("MainWindow", "BÖLÜM KODU"))
        # self.depCode.setItemText(1, _translate("MainWindow", "MAK"))
        # self.capCode.setItemText(0, _translate("MainWindow", "ÇAP/YANDAL"))
        # self.capCode.setItemText(1, _translate("MainWindow", "MAK - KOM"))

        self.classTab.setTabText(self.classTab.indexOf(self.class1),
                                 _translate("MainWindow", self.translate["1. Sınıf"][self.languageNumber]))
        self.classTab.setTabText(self.classTab.indexOf(self.class2),
                                 _translate("MainWindow", self.translate["2. Sınıf"][self.languageNumber]))
        self.classTab.setTabText(self.classTab.indexOf(self.class3),
                                 _translate("MainWindow", self.translate["3. Sınıf"][self.languageNumber]))
        self.classTab.setTabText(self.classTab.indexOf(self.class4),
                                 _translate("MainWindow", self.translate["4. Sınıf"][self.languageNumber]))
        self.classTab.setTabText(self.classTab.indexOf(self.ITBSNT),
                                 _translate("MainWindow", self.translate["Ekstra ders"][self.languageNumber]))
        self.classTab.setTabText(self.classTab.indexOf(self.CAP),
                                 _translate("MainWindow", self.translate["ÇAP/YANDAL"][self.languageNumber]))
        self.label_version.setText(_translate("MainWindow", "v1.0.5"))

        self.label_043.setText(_translate("MainWindow", self.translate["Bölüm"][self.languageNumber]))
        self.label_067.setText(_translate("MainWindow", self.translate["Ders Adı"][self.languageNumber]))
        self.label_0043.setText(_translate("MainWindow", self.translate["Açılmış Dersler"][self.languageNumber]))
        self.label_top_info_234.setText(
            _translate("MainWindow", self.translate["| DERS PROGRAMI"][self.languageNumber]))

        self.addLecture.setText(_translate("MainWindow", self.translate["Ders Ekle"][self.languageNumber]))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "8.30 - 9.00"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "9.00 - 9.30"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "9.30 - 10.00"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "10.00 - 10.30"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "10.30 - 11.00"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "11.00 - 11.30"))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "11.30 - 12.00"))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "12.00 - 12.30"))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "12.30 - 13.00"))
        item = self.tableWidget.verticalHeaderItem(9)
        item.setText(_translate("MainWindow", "13.00 - 13.30"))
        item = self.tableWidget.verticalHeaderItem(10)
        item.setText(_translate("MainWindow", "13.30 - 14.00"))
        item = self.tableWidget.verticalHeaderItem(11)
        item.setText(_translate("MainWindow", "14.00 - 14.30"))
        item = self.tableWidget.verticalHeaderItem(12)
        item.setText(_translate("MainWindow", "14.30 - 15.00"))
        item = self.tableWidget.verticalHeaderItem(13)
        item.setText(_translate("MainWindow", "15.00 - 15.30"))
        item = self.tableWidget.verticalHeaderItem(14)
        item.setText(_translate("MainWindow", "15.30 - 16.00"))
        item = self.tableWidget.verticalHeaderItem(15)
        item.setText(_translate("MainWindow", "16.00 - 16.30"))
        item = self.tableWidget.verticalHeaderItem(16)
        item.setText(_translate("MainWindow", "16.30 - 17.00"))
        item = self.tableWidget.verticalHeaderItem(17)
        item.setText(_translate("MainWindow", "17.00 - 17.30"))
        item = self.tableWidget.verticalHeaderItem(18)
        item.setText(_translate("MainWindow", "17.30 - 18.00"))
        item = self.tableWidget.verticalHeaderItem(19)
        item.setText(_translate("MainWindow", "18.00 - 18.30"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", self.translate["Pazartesi"][self.languageNumber]))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", self.translate["Salı"][self.languageNumber]))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", self.translate["Çarşamba"][self.languageNumber]))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", self.translate["Perşembe"][self.languageNumber]))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", self.translate["Cuma"][self.languageNumber]))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)

        self.lineEdit_6262.setPlaceholderText(
            _translate("MainWindow", self.translate["Tablo ismi"][self.languageNumber]))
        self.pushButton_6262.setText(_translate("MainWindow", self.translate["Tabloyu Kaydet"][self.languageNumber]))
        self.comboBox_6262.setPlaceholderText(_translate("MainWindow", self.translate["Seç"][self.languageNumber]))

        self.capCode.setItemText(0, self.translate["ÇAP/YANDAL"][self.languageNumber])
        self.depCode.setItemText(0, self.translate["BÖLÜM KODU"][self.languageNumber])
        self.comboBox_6262.setItemText(0, self.translate["Seç"][self.languageNumber])
        self.pushButton_6263.setText(self.translate["Tabloyu sil"][self.languageNumber])
        self.pushButton_crn.setText(self.translate["CRN işlemleri"][self.languageNumber])
        self.crnitem1.setText(self.translate["CRN listesini belleğe kopyala"][self.languageNumber])
        self.crnitem2.setText(self.translate["JS kodunu belleğe kopyala"][self.languageNumber])
        self.crnitem3.setText(self.translate["CRN bilgilerini bilgisayara kaydet"][self.languageNumber])
        self.crnitem4.setText(self.translate["Tablonun resmini bilgisayara kaydet"][self.languageNumber])
        self.regen.setText(self.translate["Dersleri güncelle"][self.languageNumber])

        self.label_oy.setText(self.translate["ÖĞLE YEMEĞİ"][self.languageNumber])
        self.label_ay.setText(self.translate["AKŞAM YEMEĞİ"][self.languageNumber])
        self.label_aybg.setText(self.translate["Akşam yemeği bilgisi girilmemiş"][self.languageNumber])
        self.label_oybg.setText(self.translate["Öğle yemeği bilgisi girilmemiş"][self.languageNumber])

        self.label_blmort.setToolTip(self.translate["1.anadal ortalaması"][self.languageNumber])
        self.label_caport.setToolTip(self.translate["2.anadal/yandal ortalaması"][self.languageNumber])
        self.labelblm_crd.setToolTip(self.translate["1.anadal başarılan kredi"][self.languageNumber])
        self.label_capcrd.setToolTip(self.translate["2.anadal/yandal başarılan kredi"][self.languageNumber])
        self.gpaLabel.setToolTip(self.translate["Genel puan ortalaması"][self.languageNumber])
        if self.table_credit == -1:
            self.credit_label.setText(
                self.translate["Toplam Kredi:"][self.languageNumber] + " " + self.translate["İnternet yok"][
                    self.languageNumber])
            self.credit_label.setToolTip(
                self.translate["Toplam kredinin görülebilmesi için internet bağlantısı gereklidir."][
                    self.languageNumber])
        else:
            self.credit_label.setText(self.translate["Toplam Kredi:"][self.languageNumber] + " " + str(self.table_credit))
            self.credit_label.setToolTip("")

        if self.noInternet:
            item = self.calendar_table.horizontalHeaderItem(0)
            item.setText(self.translate["Akademik takvimin görüntülenebilmesi için internet bağlantısı gereklidir."][self.languageNumber])

        if self.languageNumber == 0:
            self.calendarWidget.setLocale(QtCore.QLocale(QtCore.QLocale.Turkish))
        elif self.languageNumber == 1:
            self.calendarWidget.setLocale(QtCore.QLocale(QtCore.QLocale.English))
        elif self.languageNumber == 2:
            self.calendarWidget.setLocale(QtCore.QLocale(QtCore.QLocale.German))

        self.intErrorLabel.setText(self.translate["İnternet bağlantısı gereklidir!"][self.languageNumber])

        self.submitButton.setText(self.translate["Gönder"][self.languageNumber])
        self.name_label_4.setText(self.translate["Görüş ve önerileriniz:"][self.languageNumber])

        self.label011.setText(self.translate["Ders Kodu"][self.languageNumber])
        self.label000.setText(self.translate["Ders Adı"][self.languageNumber])
        self.label001.setText(self.translate["Öğretim Üyesi"][self.languageNumber])
        self.label002.setText(self.translate["Gün"][self.languageNumber])
        self.label003.setText(self.translate["Saat"][self.languageNumber])
        self.label004.setText(self.translate["Doluluk"][self.languageNumber])

        self.comboBox1254.setItemText(0, self.translate["Dönem"][self.languageNumber])
        self.comboBox1255.setItemText(0, self.translate["Bölüm kodu"][self.languageNumber])
        self.pushButton_2189.setText(self.translate["Ders programı yapmak için kullan"][self.languageNumber])
        self.pushButton_3154.setText(self.translate["Veritabanlarını güncelle"][self.languageNumber])
        self.Color_Button.setText(self.translate["Tamirat modülünü çalıştır"][self.languageNumber])

        self.setTooltips()

    def create_tabButton(self, text):
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        icon3 = QtGui.QIcon()
        tabButton = QtWidgets.QPushButton(self.tabs_window)
        tabButton.setMinimumSize(QtCore.QSize(200, 53))
        tabButton.setFont(font)
        tabButton.setStyleSheet("QPushButton {\n"
                                "    background-position: center;\n"
                                "    background-repeat: no-reperat;\n"
                                "    border: none;\n"
                                "    color:rgb" + str(self.text_color) + ";\n"
                                                                         "text-align: left\n"
                                                                         "}\n"
                                                                         "QPushButton:hover {\n"
                                                                         "    background-color: rgb" + str(
            self.hover) + ";\n"
                          "}\n"
                          "QPushButton:pressed {    \n"
                          "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                            "}")

        tabButton.setIconSize(QtCore.QSize(50, 50))
        tabButton.setFlat(False)
        tabButton.setObjectName("tabButton")
        tabButton.character = str()
        if text == "Profil":
            tabButton.character = "Profile"
            icon3.addPixmap(QtGui.QPixmap(":/user/miniProfile.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        elif text == "Ana Sayfa":
            tabButton.character = "Home"
            icon3.addPixmap(QtGui.QPixmap(":/user/mainMenuMini.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        elif text == "Ders Programı":
            tabButton.character = "LectProgram"
            icon3.addPixmap(QtGui.QPixmap(":/user/programMini.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        elif text == "Akd. Takvim":
            tabButton.character = "Calendar"
            icon3.addPixmap(QtGui.QPixmap(":/user/academicMini.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        elif text == "Yemekhane":
            tabButton.character = "Cafeteria"
            icon3.addPixmap(QtGui.QPixmap(":/user/cateringMini.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        elif text == "Ders Arşivi":
            tabButton.character = "archive"
            icon3.addPixmap(QtGui.QPixmap(":/user/archiveMini.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        elif text == "Hakkımızda":
            tabButton.character = "AboutUs"
            icon3.addPixmap(QtGui.QPixmap(":/user/aboutUsMini.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)

        tabButton.setIcon(icon3)
        tabButton.origin = text
        text = self.translate[text][self.languageNumber]
        tabButton.setText(text)

        return tabButton

    def create_shortcutButton(self, text):
        shortcutButton = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        shortcutButton.setMinimumSize(QtCore.QSize(0, 0))
        shortcutButton.setMaximumSize(QtCore.QSize(9999, 9999))
        sizePolicy.setHeightForWidth(shortcutButton.sizePolicy().hasHeightForWidth())
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        shortcutButton.setSizePolicy(sizePolicy)

        shortcutButton.setFont(font)
        setImg = str()
        shortcutButton.setObjectName("shortcutButton")

        shortcutButton.setText("\n" + "\n" + "\n" + text)

        shortcutButton.character = str()

        if text == "":
            shortcutButton.setEnabled(False)
            shortcutButton.character = ""
        elif text == "Profil":
            shortcutButton.character = "Profile"
            setImg = "    image: url(:/user/profile.png);\n"
        elif text == "Yeni Kısayol":
            shortcutButton.character = "Shortcut"
            setImg = "    image: url(:/newShortcut/new.png);\n"
        elif text == "Ana Sayfa":
            shortcutButton.character = "Home"
            setImg = "    image: url(:/user/mainmenuSc.png);\n"
        elif text == "Ders Programı":
            shortcutButton.character = "LectProgram"
            setImg = "    image: url(:/user/programSc.png);\n"
        elif text == "Akd. Takvim":
            shortcutButton.character = "Calendar"
            setImg = "    image: url(:/user/academicSc.png);\n"
        elif text == "Yemekhane":
            shortcutButton.character = "Cafeteria"
            setImg = "    image: url(:/user/cateringSc.png);\n"
        elif text == "Ders Arşivi":
            shortcutButton.character = "archive"
            setImg = "    image: url(:/user/archiveSc.png);\n"
        elif text == "Hakkımızda":
            shortcutButton.character = "AboutUs"
            setImg = "    image: url(:/user/aboutusSc.png);\n"

        shortcutButton.setStyleSheet("\n"
                                     "QPushButton {\n"
                                     "    background-position: center;\n"
                                     "    background-repeat: no-repeat;\n"
                                     "    border: none;\n" +
                                     setImg +
                                     "    color:rgb" + str(self.text_color2) + ";\n"
                                                                               "    border-radius: 40px;\n"
                                                                               "}\n"
                                                                               "QPushButton:hover {\n"
                                                                               "    background-color: rgb" + str(
            self.hover3) + ";\n"
                           "}\n"
                           "QPushButton:pressed {    \n"
                           "    background-color: rgb" + str(self.pressed2) + ";\n"
                                                                              "}\n"
                                                                              "")

        shortcutButton.origin = text
        if len(text) != 0:
            text = self.translate[text][self.languageNumber]

        shortcutButton.setText("\n" + "\n" + "\n" + text)

        return shortcutButton

    def copy_crn(self):
        for i in self.items.values():
            if 'crn' in i.keys():
                self.crn_list.append(i['crn'])
        text = str()
        for i in self.crn_list:
            if self.crn_list[-1] != i:
                text += i + ", "
            else:
                text += i
        uiFunctions.addToClipBoard(text)
        self.crn_list = list()

    def copy_JSCode(self):
        for i in self.items.values():
            if 'crn' in i.keys():
                self.crn_list.append(i['crn'])
        text = str()
        for i in self.crn_list:
            if self.crn_list[-1] != i:
                text += i + ", "
            else:
                text += i

        text = "javascript: (function()" + "{" + "var crn=[" + text + "]; for (var i=0;i < crn.length;i++)" + "{" + "var d = document.getElementById(\"crn_id\" + (i + 1)); d.value = crn[i];}void(0);})();"

        uiFunctions.addToClipBoard(text)
        self.crn_list = list()

    def save_to_computer(self):
        for i in self.items.values():
            if 'crn' in i.keys():
                self.crn_list.append(i['crn'])
        text = str()
        for i in self.crn_list:
            if self.crn_list[-1] != i:
                text += i + ", "
            else:
                text += i

        text2 = "javascript: (function()" + "{" + "var crn=[" + text + "]; for (var i=0;i < crn.length;i++)" + "{" + "var d = document.getElementById(\"crn_id\" + (i + 1)); d.value = crn[i];}void(0);})();"

        self.crn_list = list()

        file_name = QtWidgets.QFileDialog.getSaveFileName(self, self.translate["Dosyayı kaydet"][self.languageNumber],
                                                          os.getenv("HOME"), "Text files (*.txt)")
        if file_name[0] != "":
            with open(file_name[0], "w") as file:
                file.write(self.translate["CRN listesi:"][self.languageNumber] + "\n")
                file.write(text + "\n\n")
                file.write(self.translate["JS kodu:"][self.languageNumber] + "\n")
                file.write(text2 + "\n")

    def save_table_ss(self):
        self.showFullScreen()

        time.sleep(0.1)
        screen = QtWidgets.QApplication.primaryScreen()
        screenshot = screen.grabWindow(self.tableWidget.winId())

        time.sleep(0.2)
        self.showNormal()

        file_name = QtWidgets.QFileDialog.getSaveFileName(self, self.translate["Dosyayı kaydet"][self.languageNumber],
                                                          os.getenv("HOME"), "PNG (*.png)")
        if file_name[0] != "":
            screenshot.save(file_name[0], 'png')

    def startProgress(self):
        if not uiFunctions.is_connectable("https://www.sis.itu.edu.tr/TR/ogrenci/ders-programi/ders-programi.php?seviye=LS"):
            self.update_label.setText(self.translate["İnternet bağlantısı gereklidir!"][self.languageNumber])
            return 0

        self.thread = uiFunctions.get_courses_Thread(self)
        self.thread.change_value.connect(self.setProgressVal)
        self.thread.start()

    def setProgressVal(self, val):
        self.update_label.setText(str(val))

    def startTime(self):
        self.thread2 = uiFunctions.clock_Thread(self)
        self.thread2.change_value.connect(self.getTime)
        self.thread2.change_value2.connect(self.getDate)
        self.thread2.start()

    def getTime(self, val):
        self.clock_label.setText(val)

    def getDate(self, val):
        self.history_label.setText(val)

    def startYemekhane(self):
        self.threadyemekhane = uiFunctions.y_thread(self)
        self.threadyemekhane.change_value.connect(self.setYemekhane)
        self.threadyemekhane.start()

    def setYemekhane(self, val):
        pass #loading mesajı olabilirdi

    def mail_progress(self):
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
        except:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText(self.translate["İnternet bağlantısı gereklidir!"][self.languageNumber])
            msgBox.setWindowTitle("İTÜ Kraken")
            msgBox.setWindowIcon(QtGui.QIcon(":/terminal/windowicon.png"))
            msgBox.show()
            returnValue = msgBox.exec()
            return 0


        self.mail_thread = uiFunctions.mail_Thread(self.textEdit)
        self.mail_thread.change_value.connect(self.set_emptyString)
        self.mail_thread.start()

        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(self.translate["Mesajınız iletilmiştir."][self.languageNumber])
        msgBox.setWindowTitle("Kraken")
        msgBox.setWindowIcon(QtGui.QIcon(":/terminal/windowicon.png"))
        msgBox.show()
        returnValue = msgBox.exec()

        self.textEdit.hide()
        self.submitButton.hide()
        self.name_label_4.hide()

    def startDownloadProgress(self):
        self.dow_thread = uiFunctions.ref_old_dbase(self)
        self.dow_thread.change_value.connect(self.setDownloadval)
        self.dow_thread.start()

    def setDownloadval(self, val):
        self.pushButton_3154.setText(val)
    
    def set_emptyString(self, val):
        self.textEdit.setPlainText(val)
    """
    def startChange(self, sayi):
        self.thread15 = uiFunctions.Change_theme(sayi, self)
        self.thread15.change_value.connect(self.setChange)
        self.thread15.start()

    def setChange(self, val):
        pass
    """
    def setToolTipStatus(self):
        self.Tooltip = bool(self.label_11.checkState())
        con = sqlite3.connect("Preferences.db")
        cursor = con.cursor()
        cursor.execute("Update Pref set Tooltip = ?", (self.Tooltip,))
        con.commit()
        self.setTooltips()

    def setTooltips(self):
        if self.Tooltip:
            self.pushButton_2189.setToolTip(self.translate["Seçili döneme ait veritabanını ders programına aktararak o dönemin dersleriyle program yapmaya imkan verir."][self.languageNumber])
            self.pushButton_3154.setToolTip(self.translate[
                                                "Eski dönemlere ait veritabanlarını internet kullanarak günceller. Yeni dönem varsa eklenir."][
                                                self.languageNumber])
            self.regen.setToolTip(self.translate[
                                                "İTÜ Web sayfasından şuanki ders programlarını indirerek eski veritabanıyla değiştirir."][
                                                self.languageNumber])
        else:
            self.pushButton_2189.setToolTip("")
            self.pushButton_3154.setToolTip("")
            self.regen.setToolTip("")

    def change_theme(self):
        self.setStyleSheet("background-color: rgb{};".format(self.primer_color))
        for i in self.cornerGrips:
            i.setStyleSheet("background-color: rgb{};".format(self.primer_color))
        self.left_frame.setStyleSheet("background-color: rgb{};".format(self.primer_color))
        self.menu_button.setStyleSheet("QPushButton {\n"
                                       "    background-image: url(:/menu/menu.png);\n"
                                       "    background-position: center;\n"
                                       "    background-repeat: no-repeat;\n"
                                       "    border: none;\n"
                                       "    background-color: rgb" + str(self.primer_color) + ";\n"
                                                                                              "}\n"
                                                                                              "QPushButton:hover {\n"
                                                                                              "    background-color: rgb" + str(
            self.hover) + ";\n"
                          "}\n"
                          "QPushButton:pressed {    \n"
                          "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                            "}")
        self.user_icon_label.setStyleSheet("QPushButton {\n"
                                           "    background-position: center;\n"
                                           "    background-repeat: no-repeat;\n"
                                           "    border-radius: 30px;\n"
                                           "    border: 5px solid rgb" + str(self.seconder_color) + ";\n"
                                                                                                    "    background-color: rgb" + str(
            self.seconder_color2) + ";\n"
                                    "    color: rgb" + str(self.text_color) + ";\n"
                                                                              "}"
                                                                              "QPushButton:hover {\n"
                                                                              "    background-color: rgb" + str(
            self.hover) + ";\n"
                          "}"
                          "QPushButton:pressed {"
                          "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                            "}")
        self.main_menu_button.setStyleSheet("QPushButton {\n"
                                            "    background-image: url(:/menu/home.png);\n"
                                            "    background-position: center;\n"
                                            "    background-repeat: no-reperat;\n"
                                            "    border: none;\n"
                                            "    background-color: rgb" + str(self.primer_color) + ";\n"
                                                                                                   "}\n"
                                                                                                   "QPushButton:hover {\n"
                                                                                                   "    background-color: rgb" + str(
            self.hover) + ";\n"
                          "}\n"
                          "QPushButton:pressed {    \n"
                          "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                    "}")
        self.frame_gpas.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.frame_credit.setStyleSheet("color: rgb{};".format(self.text_color2))

        self.settingsButton.setStyleSheet("QPushButton {\n"
                                          "    background-image: url(:/menu/settings.png);\n"
                                          "    background-position: center;\n"
                                          "    background-repeat: no-reperat;\n"
                                          "    border: none;\n"
                                          "    background-color: rgb" + str(self.primer_color) + ";\n"
                                                                                                 "}\n"
                                                                                                 "QPushButton:hover {\n"
                                                                                                 "    background-color: rgb" + str(
            self.hover) + ";\n"
                          "}\n"
                          "QPushButton:pressed {    \n"
                          "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                            "}")
        self.right_frame.setStyleSheet("background-color: rgb{}".format(self.primer_color))
        self.frame.setStyleSheet("background-color: rgb{}".format(self.primer_color))
        self.top_label.setStyleSheet("background: transparent;\n"
                                     "color:rgb" + str(self.text_color) + ";\n"
                                                                          "\n"
                                                                          "")
        self.minimize_button.setStyleSheet("QPushButton {    \n"
                                           "    border: none;\n"
                                           "    background-color: transparent;\n"
                                           "    image: url(:/menu/minimize.png);\n"
                                           "}\n"
                                           "QPushButton:hover {\n"
                                           "    background-color: rgb" + str(self.hover2) + ";\n"
                                                                                            "}\n"
                                                                                            "QPushButton:pressed {    \n"
                                                                                            "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")
        self.maximize_button.setStyleSheet("QPushButton {    \n"
                                           "    border: none;\n"
                                           "    background-color: transparent;\n"
                                           "    image: url(:/menu/maximize.png);\n"
                                           "}\n"
                                           "QPushButton:hover {\n"
                                           "    background-color: rgb" + str(self.hover2) + ";\n"
                                                                                            "}\n"
                                                                                            "QPushButton:pressed {    \n"
                                                                                            "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")
        self.exit_button.setStyleSheet("QPushButton {    \n"
                                       "    border: none;\n"
                                       "    background-color: transparent;\n"
                                       "    image: url(:/menu/exit.png);\n"
                                       "\n"
                                       "}\n"
                                       "QPushButton:hover {\n"
                                       "    background-color: rgb" + str(self.hover2) + ";\n"
                                                                                        "}\n"
                                                                                        "QPushButton:pressed {    \n"
                                                                                        "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")
        self.tabs_window.setStyleSheet("background-color: rgb" + str(self.primer_color) + ";\n"
                                                                                          "border:none;\n"
                                                                                           "")
        self.credit_label.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.frame_11.setStyleSheet("background-color: rgb{};".format(self.seconder_color))
        self.frame_5.setStyleSheet("background-color: rgb{};".format(self.seconder_color))
        self.label_top_info_2.setStyleSheet("color: rgb{};".format(self.info_color))
        self.frame_6.setStyleSheet("background-color: rgb{};".format(self.seconder_color))
        self.label_2.setStyleSheet("color:rgb{};\n".format(self.text_color))
        self.program_name_label.setStyleSheet("background: transparent;\n"
                                              "color:rgb" + str(self.text_color2) + ";\n"
                                                                                    "background-position: center;")
        self.clock_label.setStyleSheet("color:rgb{};\n".format(self.text_color2))
        self.frame_2.setStyleSheet("background-color: rgb{};".format(self.seconder_color))
        self.groupBox.setStyleSheet("color:rgb{}".format(self.text_color2))
        self.history_label.setStyleSheet("color:rgb{}".format(self.text_color2))
        self.frame_54.setStyleSheet("background-color: rgb{}".format(self.seconder_color))
        self.AgButton.setStyleSheet("QPushButton {\n"
                                    "    background-color: rgb(82, 113, 255);\n"
                                    "    border-radius: 50px;\n"
                                    "    border: 8px solid rgb(255, 255, 255);\n"
                                    "    color: rgb(255, 255, 255);\n"
                                    "}\n"
                                    "QPushButton:hover {\n"
                                    "    background-color: rgb(82, 113, 255,150);\n"
                                    "}\n"
                                    "QPushButton:pressed {    \n"
                                    "    background-color: rgb(85, 170, 255);\n"
                                    "}")
        self.name_lineEdit.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.editButton.setStyleSheet("QPushButton {\n"
                                      "    background-position: center;\n"
                                      "    background-repeat: no-reperat;\n"
                                      "    background-color: transparent;\n"
                                      "    border-radius: 17px;\n"
                                      "\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      "    background-color: rgb" + str(self.hover) + ";\n"
                                                                                      "}\n"
                                                                                      "QPushButton:pressed {    \n"
                                                                                      "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")
        self.okButton.setStyleSheet("QPushButton {\n"
                                    "    background-position: center;\n"
                                    "    background-repeat: no-reperat;\n"
                                    "    background-color: transparent;\n"
                                    "    border-radius: 17px;\n"
                                    "\n"
                                    "}\n"
                                    "QPushButton:hover {\n"
                                    "    background-color: rgb" + str(self.hover) + ";\n"
                                                                                    "}\n"
                                                                                    "QPushButton:pressed {    \n"
                                                                                    "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")
        self.cancelButton.setStyleSheet("QPushButton {\n"
                                        "    background-position: center;\n"
                                        "    background-repeat: no-reperat;\n"
                                        "    background-color: transparent;\n"
                                        "    border-radius: 17px;\n"
                                        "\n"
                                        "}\n"
                                        "QPushButton:hover {\n"
                                        "    background-color: rgb" + str(self.hover) + ";\n"
                                                                                        "}\n"
                                                                                        "QPushButton:pressed {    \n"
                                                                                        "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")
        self.label_621.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label_321.setStyleSheet("color: rgb{};".format(self.text_color2))

        self.yearComboBox.setStyleSheet("QComboBox {\n"
                                        "color:rgb" + str(self.text_color2) + ";\n"
                                                                              "background-color: transparent;\n"
                                                                              "selection-background-color: transparent;\n"
                                                                              "selection-color: rgb" + str(
            self.text_color2) + ";\n"
                                "}\n"
                                "QListView{\n"
                                "color:rgb" + str(self.text_color2) + ";\n"
                                                                      "}\n"
                                                                      "QScrollBar:vertical {\n"
                                                                      "     background-color: rgb" + str(
            self.scrollseconder) + ";\n"
                                   "     \n"
                                   "     border: 1px transparent #2A2929;\n"
                                   "     \n"
                                   "     width: 8px;\n"
                                   "}\n"
                                   " QScrollBar::handle:vertical {\n"
                                   "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                           "     min-height: 22px;\n"
                                                                                           "     border-radius: 4px;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-"
                                                                                           "position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n")

        self.listComboBox.setStyleSheet("QComboBox {\n"
                                        "color:rgb" + str(self.text_color2) + ";\n"
                                                                              "background-color: transparent;\n"
                                                                              "selection-background-color: transparent;\n"
                                                                              "selection-color: rgb" + str(
            self.text_color2) + ";\n"
                                "}\n"
                                "QListView{\n"
                                "color:rgb" + str(self.text_color2) + ";\n"
                                                                      "}\n"
                                                                      "QScrollBar:vertical {\n"
                                                                      "     background-color: rgb" + str(
            self.scrollseconder) + ";\n"
                                   "     \n"
                                   "     border: 1px transparent #2A2929;\n"
                                   "     \n"
                                   "     width: 8px;\n"
                                   "}\n"
                                   " QScrollBar::handle:vertical {\n"
                                   "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                           "     min-height: 22px;\n"
                                                                                           "     border-radius: 4px;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-"
                                                                                           "position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n")
        self.calendarChoseframe.setStyleSheet("background-color: rgb" + str(self.seconder_color) + "\n")
        self.depCode.setStyleSheet("QComboBox {\n"
                                   "color:rgb" + str(self.text_color2) + ";\n"
                                                                         "background-color: transparent;\n"
                                                                         "selection-background-color: transparent;\n"
                                                                         "selection-color: rgb" + str(
            self.text_color2) + ";\n"
                                "}\n"
                                "QListView{\n"
                                "color:rgb" + str(self.text_color2) + ";\n"
                                                                      "}\n"
                                                                      "QScrollBar:vertical {\n"
                                                                      "     background-color: rgb" + str(
            self.scrollseconder) + ";\n"
                                   "     \n"
                                   "     border: 1px transparent #2A2929;\n"
                                   "     \n"
                                   "     width: 8px;\n"
                                   "}\n"
                                   " QScrollBar::handle:vertical {\n"
                                   "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                           "     min-height: 22px;\n"
                                                                                           "     border-radius: 4px;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-"
                                                                                           "position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n")
        self.capCode.setStyleSheet("QComboBox {\n"
                                   "color:rgb" + str(self.text_color2) + ";\n"
                                                                         "background-color: transparent;\n"
                                                                         "selection-background-color: transparent;\n"
                                                                         "selection-color: rgb" + str(
            self.text_color2) + ";\n"
                                "}\n"
                                "QListView{\n"
                                "color:rgb" + str(self.text_color2) + ";\n"
                                                                      "}\n"
                                                                      "QScrollBar:vertical {\n"
                                                                      "     background-color: rgb" + str(
            self.scrollseconder) + ";\n"
                                   "     \n"
                                   "     border: 1px transparent #2A2929;\n"
                                   "     \n"
                                   "     width: 8px;\n"
                                   "}\n"
                                   " QScrollBar::handle:vertical {\n"
                                   "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                           "     min-height: 22px;\n"
                                                                                           "     border-radius: 4px;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-"
                                                                                           "position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                        "}\n")
        self.calendar_table.setStyleSheet("QScrollBar:vertical {\n"
                                          "     background-color: rgb" + str(
            self.scrollseconder) + ";\n"
                                   "     \n"
                                   "     border: 1px transparent #2A2929;\n"
                                   "     \n"
                                   "     width: 8px;\n"
                                   "}\n"
                                   " QScrollBar::handle:vertical {\n"
                                   "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                           "     min-height: 22px;\n"
                                                                                           "     border-radius: 4px;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-"
                                                                                           "position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n")
        self.classTab.setStyleSheet("QTabBar::tab {\n"
                                    "  background:  rgb" + str(self.tab_min_background) + ";\n"
                                                                                          "  padding: 10px;\n"
                                                                                          "  margin-right: 5px;\n"
                                                                                          "  width: 100px;\n"
                                                                                          "  color: rgb" + str(
            self.text_color) + ";\n"
                               "  border-top-right-radius: 5px; \n"
                               "  border-top-left-radius: 5px; \n"
                               "} \n"
                               "\n"
                               "QTabBar::tab:selected { \n"
                               "  background: rgb" + str(self.selected) + ";\n"
                                                                          "}\n"
                                                                          "\n"
                                                                          "QTabWidget::pane { border: 0}")
        self.scrollArea.setStyleSheet("QScrollBar:vertical {\n"
                                      "     background-color: rgb" + str(self.scrollseconder) + ";\n"
                                                                                                "     \n"
                                                                                                "     border: 1px transparent #2A2929;\n"
                                                                                                "     \n"
                                                                                                "     width: 8px;\n"
                                                                                                "}\n"
                                                                                                " QScrollBar::handle:vertical {\n"
                                                                                                "     background-color: rgb" + str(
            self.scrollprimer) + ";\n"
                                 "     min-height: 5px;\n"
                                 "     border-radius: 4px;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 "")
        self.scrollAreaWidgetContents_2.setStyleSheet("background:  rgb" + str(self.tab_background) + ";\n"
                                                                                                      "\n"
                                                                                                      " ")
        self.scrollArea_2.setStyleSheet("QScrollBar:vertical {\n"
                                        "     background-color: rgb" + str(self.scrollseconder) + ";\n"
                                                                                                  "     \n"
                                                                                                  "     border: 1px transparent #2A2929;\n"
                                                                                                  "     \n"
                                                                                                  "     width: 8px;\n"
                                                                                                  "}\n"
                                                                                                  " QScrollBar::handle:vertical {\n"
                                                                                                  "     background-color: rgb" + str(
            self.scrollprimer) + ";\n"
                                 "     min-height: 5px;\n"
                                 "     border-radius: 4px;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 "")
        self.scrollAreaWidgetContents_3.setStyleSheet("background:  rgb" + str(self.tab_background) + ";\n"
                                                                                                      "\n"
                                                                                                      " ")
        self.scrollArea_3.setStyleSheet("QScrollBar:vertical {\n"
                                        "     background-color: rgb" + str(self.scrollseconder) + ";\n"
                                                                                                  "     \n"
                                                                                                  "     border: 1px transparent #2A2929;\n"
                                                                                                  "     \n"
                                                                                                  "     width: 8px;\n"
                                                                                                  "}\n"
                                                                                                  " QScrollBar::handle:vertical {\n"
                                                                                                  "     background-color: rgb" + str(
            self.scrollprimer) + ";\n"
                                 "     min-height: 5px;\n"
                                 "     border-radius: 4px;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 "")
        self.scrollAreaWidgetContents_6.setStyleSheet("background:  rgb" + str(self.tab_background) + ";\n"
                                                                                                      "\n"
                                                                                                      " ")
        self.scrollArea_4.setStyleSheet("QScrollBar:vertical {\n"
                                        "     background-color: rgb" + str(self.scrollseconder) + ";\n"
                                                                                                  "     \n"
                                                                                                  "     border: 1px transparent #2A2929;\n"
                                                                                                  "     \n"
                                                                                                  "     width: 8px;\n"
                                                                                                  "}\n"
                                                                                                  " QScrollBar::handle:vertical {\n"
                                                                                                  "     background-color: rgb" + str(
            self.scrollprimer) + ";\n"
                                 "     min-height: 5px;\n"
                                 "     border-radius: 4px;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 "")
        self.scrollAreaWidgetContents_7.setStyleSheet("background:  rgb" + str(self.tab_background) + ";\n"
                                                                                                      "\n"
                                                                                                      " ")
        self.scrollArea_49.setStyleSheet("QScrollBar:vertical {\n"
                                         "     background-color: rgb" + str(self.scrollseconder) + ";\n"
                                                                                                   "     \n"
                                                                                                   "     border: 1px transparent #2A2929;\n"
                                                                                                   "     \n"
                                                                                                   "     width: 8px;\n"
                                                                                                   "}\n"
                                                                                                   " QScrollBar::handle:vertical {\n"
                                                                                                   "     background-color: rgb" + str(
            self.primer_color) + ";\n"
                                 "     min-height: 5px;\n"
                                 "     border-radius: 4px;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 "")
        self.scrollAreaWidgetContents_75.setStyleSheet("background:  rgb" + str(self.tab_background) + ";\n"
                                                                                                       "\n"
                                                                                                       " ")
        self.plusButton.setStyleSheet("\n"
                                      "QPushButton {\n"
                                      "    background-image: url(:/menu/plus.png);\n"
                                      "    background-position: center;\n"
                                      "    background-repeat: no-repeat;\n"
                                      "    border-radius: 20px;\n"
                                      "    background-color: rgb(255, 255, 255,100);\n"
                                      "}\n"
                                      "QPushButton:hover {\n"
                                      "    background-color: rgb(255, 255, 255,150);\n"
                                      "}\n"
                                      "QPushButton:pressed {    \n"
                                      "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                                        "}")
        self.scrollArea_43.setStyleSheet("QScrollBar:vertical {\n"
                                         "     background-color: rgb" + str(self.scrollseconder) + ";\n"
                                                                                                   "     \n"
                                                                                                   "     border: 1px transparent #2A2929;\n"
                                                                                                   "     \n"
                                                                                                   "     width: 8px;\n"
                                                                                                   "}\n"
                                                                                                   " QScrollBar::handle:vertical {\n"
                                                                                                   "     background-color: rgb" + str(
            self.scrollprimer) + ";\n"
                                 "     min-height: 5px;\n"
                                 "     border-radius: 4px;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 "")
        self.scrollAreaWidgetContents_71.setStyleSheet("background:  rgb" + str(self.tab_background) + ";\n"
                                                                                                       "\n"
                                                                                                       " ")
        self.label_043.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label_067.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label_0043.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label_top_info_234.setStyleSheet("color: rgb{};".format(self.info_color))
        self.scrollArea004.setStyleSheet(
            "QScrollArea > QWidget > QWidget { background: rgb" + str(self.seconder_color) + ";\n}"
                                                                                             "QScrollBar:vertical {\n"
                                                                                             "     background-color: rgb" + str(
                self.scrollseconder) + ";\n"
                                       "     \n"
                                       "     border: 1px transparent #2A2929;\n"
                                       "     \n"
                                       "     width: 8px;\n"
                                       "}\n"
                                       " QScrollBar::handle:vertical {\n"
                                       "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                               "     min-height: 5px;\n"
                                                                                               "     border-radius: 4px;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:vertical {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: top;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:vertical {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: bottom;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: top;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: bottom;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"

                                                                                               "QScrollBar:horizontal {\n"
                                                                                               "     background-color: rgb" + str(
                self.scrollseconder) + ";\n"
                                       "     \n"
                                       "     border: 1px transparent #2A2929;\n"
                                       "     \n"
                                       "     height: 8px;\n"
                                       "}\n"
                                       " QScrollBar::handle:horizontal {\n"
                                       "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                               "     min-width: 5px;\n"
                                                                                               "     border-radius: 4px;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:horizontal {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: left;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:horizontal {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: right;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:horizontal:hover,QScrollBar::sub-line:horizontal:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: left;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: right;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n")

        self.tableWidget.setStyleSheet(
            " QTableWidget"
            "{"
            " margin-right: 10px;"
            "background-color: rgb" + str(self.seconder_color) + ";\n"
                                                                 "border: none;"

                                                                 "}"



                                                                 "QScrollBar:vertical {\n"
                                                                 "                                           background-color: rgb" + str(
                self.scrollseconder) + ";\n"
                                       "                                           \n"
                                       "                                           border: 1px transparent #2A2929;\n"
                                       "                                           \n"
                                       "                                           width: 8px;\n"
                                       "                                      }\n"
                                       "                                       QScrollBar::handle:vertical {\n"
                                       "                                           background-color: rgb" + str(
                self.scrollprimer) + ";\n"
                                     "                                           min-height: 5px;\n"
                                     "                                           border-radius: 4px;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::sub-line:vertical {\n"
                                     "                                           margin: 3px 0px 3px 0px;\n"
                                     "                                           border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                     "                                           height: 10px;\n"
                                     "                                           width: 10px;\n"
                                     "                                           subcontrol-position: top;\n"
                                     "                                           subcontrol-origin: margin;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::add-line:vertical {\n"
                                     "                                           margin: 3px 0px 3px 0px;\n"
                                     "                                           border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                     "                                           height: 10px;\n"
                                     "                                           width: 10px;\n"
                                     "                                           subcontrol-position: bottom;\n"
                                     "                                           subcontrol-origin: margin;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                     "                                           border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                     "                                           height: 10px;\n"
                                     "                                           width: 10px;\n"
                                     "                                           subcontrol-position: top;\n"
                                     "                                           subcontrol-origin: margin;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                     "                                           border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                     "                                           height: 10px;\n"
                                     "                                           width: 10px;\n"
                                     "                                           subcontrol-position: bottom;\n"
                                     "                                           subcontrol-origin: margin;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                     "                                           background: none;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                     "                                           background: none;\n"
                                     "                                      }\n"
                                     "\n"
                                     "QHeaderView::section{ \n"
                                     "             border-top:0px solid #D8D8D8; \n"
                                     "             border-left:0px solid #D8D8D8; \n"
                                     "             border-right:1px solid #D8D8D8; \n"
                                     "             border-bottom: 1px solid #D8D8D8; \n"
                                     "             background-color:white; \n"
                                     "             padding:4px; \n"
                                     "         } \n"
                                     "         QTableCornerButton::section{ \n"
                                     "             border-top:0px solid #D8D8D8; \n"
                                     "             border-left:0px solid #D8D8D8; \n"
                                     "             border-right:1px solid #D8D8D8; \n"
                                     "             border-bottom: 1px solid #D8D8D8; \n"
                                     "             background-color:white; \n"
                                     "         } ")

        self.scrollArea964.setStyleSheet(
            "QScrollArea { background: rgb" + str(self.seconder_color) + ";\n border: none;\n}"
                                                                                             "QScrollBar:vertical {\n"
                                                                                             "     background-color: rgb" + str(
                self.scrollseconder) + ";\n"
                                       "     \n"
                                       "     border: 1px transparent #2A2929;\n"
                                       "     \n"
                                       "     width: 8px;\n"
                                       "}\n"
                                       " QScrollBar::handle:vertical {\n"
                                       "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                               "     min-height: 5px;\n"
                                                                                               "     border-radius: 4px;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:vertical {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: top;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:vertical {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: bottom;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: top;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     subcontrol-position: bottom;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"

                                                                                               "QScrollBar:horizontal {\n"
                                                                                               "     background-color: rgb" + str(
                self.scrollseconder) + ";\n"
                                       "     \n"
                                       "     border: 1px transparent #2A2929;\n"
                                       "     \n"
                                       "     height: 8px;\n"
                                       "}\n"
                                       " QScrollBar::handle:horizontal {\n"
                                       "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                               "     min-width: 5px;\n"
                                                                                               "     border-radius: 4px;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:horizontal {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: left;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:horizontal {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: right;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:horizontal:hover,QScrollBar::sub-line:horizontal:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: left;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: right;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n")

        self.tableWidget.setStyleSheet(
            " QTableWidget"
            "{"
            " margin-right: 10px;"
            "background-color: rgb" + str(self.seconder_color) + ";\n"
                                                                 "border: none;"

                                                                 "}"



                                                                 "QScrollBar:vertical {\n"
                                                                 "                                           background-color: rgb" + str(
                self.scrollseconder) + ";\n"
                                       "                                           \n"
                                       "                                           border: 1px transparent #2A2929;\n"
                                       "                                           \n"
                                       "                                           width: 8px;\n"
                                       "                                      }\n"
                                       "                                       QScrollBar::handle:vertical {\n"
                                       "                                           background-color: rgb" + str(
                self.scrollprimer) + ";\n"
                                     "                                           min-height: 5px;\n"
                                     "                                           border-radius: 4px;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::sub-line:vertical {\n"
                                     "                                           margin: 3px 0px 3px 0px;\n"
                                     "                                           border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                     "                                           height: 10px;\n"
                                     "                                           width: 10px;\n"
                                     "                                           subcontrol-position: top;\n"
                                     "                                           subcontrol-origin: margin;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::add-line:vertical {\n"
                                     "                                           margin: 3px 0px 3px 0px;\n"
                                     "                                           border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                     "                                           height: 10px;\n"
                                     "                                           width: 10px;\n"
                                     "                                           subcontrol-position: bottom;\n"
                                     "                                           subcontrol-origin: margin;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                     "                                           border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                     "                                           height: 10px;\n"
                                     "                                           width: 10px;\n"
                                     "                                           subcontrol-position: top;\n"
                                     "                                           subcontrol-origin: margin;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                     "                                           border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                     "                                           height: 10px;\n"
                                     "                                           width: 10px;\n"
                                     "                                           subcontrol-position: bottom;\n"
                                     "                                           subcontrol-origin: margin;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                     "                                           background: none;\n"
                                     "                                      }\n"
                                     "                                       QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                     "                                           background: none;\n"
                                     "                                      }\n"
                                     "\n"
                                     "QHeaderView::section{ \n"
                                     "             border-top:0px solid #D8D8D8; \n"
                                     "             border-left:0px solid #D8D8D8; \n"
                                     "             border-right:1px solid #D8D8D8; \n"
                                     "             border-bottom: 1px solid #D8D8D8; \n"
                                     "             background-color:white; \n"
                                     "             padding:4px; \n"
                                     "         } \n"
                                     "         QTableCornerButton::section{ \n"
                                     "             border-top:0px solid #D8D8D8; \n"
                                     "             border-left:0px solid #D8D8D8; \n"
                                     "             border-right:1px solid #D8D8D8; \n"
                                     "             border-bottom: 1px solid #D8D8D8; \n"
                                     "             background-color:white; \n"
                                     "         } ")

        self.comboBox1254.setStyleSheet("QComboBox {\n"
                                        "color:rgb" + str(self.text_color2) + ";\n"
                                                                              "background-color: transparent;\n"
                                                                              "selection-background-color: transparent;\n"
                                                                              "selection-color: rgb" + str(
            self.text_color2) + ";\n"
                                "}\n"
                                "QListView{\n"
                                "color:rgb" + str(self.text_color2) + ";\n"
                                                                      "}\n"
                                                                      "QScrollBar:vertical {\n"
                                                                      "     background-color: rgb" + str(
            self.scrollseconder) + ";\n"
                                   "     \n"
                                   "     border: 1px transparent #2A2929;\n"
                                   "     \n"
                                   "     width: 8px;\n"
                                   "}\n"
                                   " QScrollBar::handle:vertical {\n"
                                   "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                           "     min-height: 22px;\n"
                                                                                           "     border-radius: 4px;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-"
                                                                                           "position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n")

        self.comboBox1255.setStyleSheet("QComboBox {\n"
                                        "color:rgb" + str(self.text_color2) + ";\n"
                                                                              "background-color: transparent;\n"
                                                                              "selection-background-color: transparent;\n"
                                                                              "selection-color: rgb" + str(
            self.text_color2) + ";\n"
                                "}\n"
                                "QListView{\n"
                                "color:rgb" + str(self.text_color2) + ";\n"
                                                                      "}\n"
                                                                      "QScrollBar:vertical {\n"
                                                                      "     background-color: rgb" + str(
            self.scrollseconder) + ";\n"
                                   "     \n"
                                   "     border: 1px transparent #2A2929;\n"
                                   "     \n"
                                   "     width: 8px;\n"
                                   "}\n"
                                   " QScrollBar::handle:vertical {\n"
                                   "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                           "     min-height: 22px;\n"
                                                                                           "     border-radius: 4px;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-"
                                                                                           "position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n")

        self.label_version.setStyleSheet("color: rgb{};".format(self.info_color))
        self.frame_542.setStyleSheet("background-color: rgb{};".format(self.seconder_color))
        self.frame_4.setStyleSheet("background-color: rgb{};".format(self.seconder_color))
        self.settings_window.setStyleSheet("background-color: rgb" + str(self.primer_color) + ";\n"
                                                                                              "border:none;")
        self.frame_13.setStyleSheet("background-color:rgb" + str(self.paletteOpacity) + ";\n"
                                                                                        "    border: 5px solid rgb" + str(
            self.seconder_color) + ";\n"
                                   "    border-radius: 25px;")
        self.label.setStyleSheet("color:rgb" + str(self.text_color) + ";\n"
                                                                      "background-color:transparent;\n"
                                                                      "border:none;\n"
                                                                      "")
        self.label_3.setStyleSheet("color:rgb" + str(self.text_color) + ";\n"
                                                                        "background-color:transparent;\n"
                                                                        "border:none;\n"
                                                                        "")

        self.label_11.setStyleSheet("color:rgb" + str(self.text_color) + ";\n"
                                                                         "background-color:transparent;\n"
                                                                         "border:none;\n"
                                                                         "")


        self.Color_Button.setStyleSheet("QPushButton {\n"
                                        "    color: rgb" + str(self.text_color) + ";\n"
                                                                                   "    background-position: center;\n"
                                                                                   "    background-repeat: no-reperat;\n"
                                        # "    border: 5px solid black;\n"
                                                                                   "    border-radius:12px;\n"
                                                                                   "    background-color: rgb" + str(
            self.paletteOpacity) + ";\n"
                                   "}\n"
                                   "\n"
                                   "QPushButton:hover {    \n"
                                   "    background-color: rgb" + str(
            self.hover2) + ";}\n"
                           "QPushButton:pressed {    \n"
                           "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")

        self.addLecture.setStyleSheet("QPushButton {\n"
                                      "    background-position: center;\n"
                                      "    background-repeat: no-reperat;\n"
                                      "    border: none;\n"
                                      "    background-color: rgb" + str(self.adl) + ";\n"
                                                                                    "    color: rgb" + str(
            self.text_color2) + ";\n"
                                "    border-radius: 22px;\n"
                                "}\n"
                                "QPushButton:hover {\n"
                                "    background-color: rgb" + str(self.adlhover) + ";\n"
                                                                                   "    background-image: url(:/menu/" + self.plusbutton + ")" + ";\n"
                                                                                                                                                 "    color: transparent;\n"
                                                                                                                                                 "}\n"
                                                                                                                                                 "QPushButton:pressed {    \n"
                                                                                                                                                 "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")

        self.comboBox_6262.setStyleSheet("background-color: rgb(255, 255, 255); border: " + self.border + ";\n")
        self.lineEdit_6262.setStyleSheet("background-color: rgb(255, 255, 255); border: " + self.border + ";\n")

        self.pushButton_2189.setStyleSheet("QPushButton {\n"
                                           "    color: rgb" + str(self.text_color2) + ";\n"
                                                                                      "}\n"
                                                                                      "QPushButton:hover {\n"
                                                                                      "    background-color: rgb" + str(
            self.hover4) + ";\n"
                             "}\n"
                             "QPushButton:pressed {    \n"
                             "    background-color: rgb" + str(self.pressed2) + ";\n"
                                                                                "}")

        self.pushButton_3154.setStyleSheet("QPushButton {\n"
                                           "    color: rgb" + str(self.text_color2) + ";\n"
                                                                                      "}\n"
                                                                                      "QPushButton:hover {\n"
                                                                                      "    background-color: rgb" + str(
            self.hover4) + ";\n"
                             "}\n"
                             "QPushButton:pressed {    \n"
                             "    background-color: rgb" + str(self.pressed2) + ";\n"
                                                                                "}")

        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(":/user/{}".format(self.editbutton_img)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.editButton.setIcon(icon4)

        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(":/user/{}".format(self.okbutton_img)), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.okButton.setIcon(icon5)

        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(":/user/{}".format(self.cancelbutton_img)), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.cancelButton.setIcon(icon6)
        self.update_label.setStyleSheet("background: transparent; color: rgb{}".format(self.text_color2))
        self.AgButton.setStyleSheet("QPushButton {\n"
                                    "    background-color: rgb(82, 113, 255);\n"
                                    "    border-radius: 50px;\n"
                                    "    border: 8px solid rgb" + str(self.AgBorderColor) + ";\n"
                                                                                            "    color: rgb(255, 255, 255);\n"
                                                                                            "}\n"
                                                                                            "QPushButton:hover {\n"
                                                                                            "    background-color: rgb(82, 113, 255,150);\n"
                                                                                            "}\n"
                                                                                            "QPushButton:pressed {    \n"
                                                                                            "    background-color: rgb(85, 170, 255);\n"
                                                                                            "}")

        if self.languageNumber == 0:
            self.TRButton.setStyleSheet("QPushButton {\n"
                                        "    background-position: center;\n"
                                        "    background-repeat: no-reperat;\n"
                                        "    image:url(:/flag/tr-flagIcon.png);\n"
                                        "    border : 4px solid white;\n"
                                        "    border-radius:19px;\n"
                                        "}")
            self.TRButton.setEnabled(False)
            self.UKButton.setEnabled(True)
            self.DEButton.setEnabled(True)
            self.UKButton.setStyleSheet("QPushButton {\n"
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
                                        "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                                          "}")
            self.DEButton.setStyleSheet("QPushButton {\n"
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
                                        "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                                          "}")

        elif self.languageNumber == 1:
            self.UKButton.setStyleSheet("QPushButton {\n"
                                        "    background-position: center;\n"
                                        "    background-repeat: no-reperat;\n"
                                        "    image:url(:/flag/uk-flagIcon.png);\n"
                                        "    border : 4px solid white;\n"
                                        "    border-radius:19px;\n"
                                        "}")
            self.UKButton.setEnabled(False)
            self.TRButton.setEnabled(True)
            self.DEButton.setEnabled(True)
            self.TRButton.setStyleSheet("QPushButton {\n"
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
                                        "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                                          "}")
            self.DEButton.setStyleSheet("QPushButton {\n"
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
                                        "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                                          "}")
        elif self.languageNumber == 2:
            self.DEButton.setStyleSheet("QPushButton {\n"
                                        "    background-position: center;\n"
                                        "    background-repeat: no-reperat;\n"
                                        "    image:url(:/flag/de-flagIcon.png);\n"
                                        "    border : 4px solid white;\n"
                                        "    border-radius:19px;\n"
                                        "}")
            self.DEButton.setEnabled(False)
            self.UKButton.setEnabled(True)
            self.DEButton.setEnabled(True)
            self.UKButton.setStyleSheet("QPushButton {\n"
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
                                        "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                                          "}")
            self.TRButton.setStyleSheet("QPushButton {\n"
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
                                        "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                                          "}")

        self.scrollArea_1241.setStyleSheet(
            "QScrollArea {border: none;}"
            "QScrollBar:vertical {\n"
            "     background-color: rgb" + str(self.scrollseconder) + ";\n"
                                                                      "     \n"
                                                                      "     border: 1px transparent #2A2929;\n"
                                                                      "     \n"
                                                                      "     width: 8px;\n"
                                                                      "}\n"
                                                                      " QScrollBar::handle:vertical {\n"
                                                                      "     background-color: rgb" + str(
                self.scrollprimer) + ";\n"
                                     "     min-height: 5px;\n"
                                     "     border-radius: 4px;\n"
                                     "}\n"
                                     " QScrollBar::sub-line:vertical {\n"
                                     "     margin: 3px 0px 3px 0px;\n"
                                     "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                     "     height: 10px;\n"
                                     "     width: 10px;\n"
                                     "     subcontrol-position: top;\n"
                                     "     subcontrol-origin: margin;\n"
                                     "}\n"
                                     " QScrollBar::add-line:vertical {\n"
                                     "     margin: 3px 0px 3px 0px;\n"
                                     "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                     "     height: 10px;\n"
                                     "     width: 10px;\n"
                                     "     subcontrol-position: bottom;\n"
                                     "     subcontrol-origin: margin;\n"
                                     "}\n"
                                     " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                     "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                     "     height: 10px;\n"
                                     "     width: 10px;\n"
                                     "     subcontrol-position: top;\n"
                                     "     subcontrol-origin: margin;\n"
                                     "}\n"
                                     " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                     "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                     "     height: 10px;\n"
                                     "     width: 10px;\n"
                                     "     subcontrol-position: bottom;\n"
                                     "     subcontrol-origin: margin;\n"
                                     "}\n"
                                     " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                     "     background: none;\n"
                                     "}\n"
                                     " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                     "     background: none;\n"
                                     "}\n"

                                     "QScrollBar:horizontal {\n"
                                     "     background-color: rgb" + str(
                self.scrollseconder) + ";\n"
                                       "     \n"
                                       "     border: 1px transparent #2A2929;\n"
                                       "     \n"
                                       "     height: 8px;\n"
                                       "}\n"
                                       " QScrollBar::handle:horizontal {\n"
                                       "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                               "     min-width: 5px;\n"
                                                                                               "     border-radius: 4px;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:horizontal {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: left;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:horizontal {\n"
                                                                                               "     margin: 3px 0px 3px 0px;\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: right;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::sub-line:horizontal:hover,QScrollBar::sub-line:horizontal:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: left;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on {\n"
                                                                                               "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                               "     width: 10px;\n"
                                                                                               "     height: 10px;\n"
                                                                                               "     subcontrol-position: right;\n"
                                                                                               "     subcontrol-origin: margin;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n"
                                                                                               " QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
                                                                                               "     background: none;\n"
                                                                                               "}\n")

        self.frameAB.setStyleSheet("background-color: rgb{}".format(self.seconder_color))
        self.name_label_1.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.name_label_2.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.name_label_3.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.name_label_4.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.name_label_5.setStyleSheet("color: rgb{}".format(self.text_color2))

        self.textEdit.setStyleSheet("QTextEdit{ color: rgb(255, 255, 255)}\n"
                                    "QScrollBar:vertical {\n"
                                    "     background-color: rgb" + str(
            self.scrollseconder) + ";\n"
                                   "     \n"
                                   "     border: 1px transparent #2A2929;\n"
                                   "     \n"
                                   "     width: 8px;\n"
                                   "}\n"
                                   " QScrollBar::handle:vertical {\n"
                                   "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                           "     min-height: 5px;\n"
                                                                                           "     border-radius: 4px;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: top;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     subcontrol-position: bottom;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n"

                                                                                           "QScrollBar:horizontal {\n"
                                                                                           "     background-color: rgb" + str(
            self.scrollseconder) + ";\n"
                                   "     \n"
                                   "     border: 1px transparent #2A2929;\n"
                                   "     \n"
                                   "     height: 8px;\n"
                                   "}\n"
                                   " QScrollBar::handle:horizontal {\n"
                                   "     background-color: rgb" + str(self.scrollprimer) + ";\n"
                                                                                           "     min-width: 5px;\n"
                                                                                           "     border-radius: 4px;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:horizontal {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     subcontrol-position: left;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:horizontal {\n"
                                                                                           "     margin: 3px 0px 3px 0px;\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     subcontrol-position: right;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::sub-line:horizontal:hover,QScrollBar::sub-line:horizontal:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     subcontrol-position: left;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-line:horizontal:hover, QScrollBar::add-line:horizontal:on {\n"
                                                                                           "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                                                                           "     width: 10px;\n"
                                                                                           "     height: 10px;\n"
                                                                                           "     subcontrol-position: right;\n"
                                                                                           "     subcontrol-origin: margin;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n"
                                                                                           " QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {\n"
                                                                                           "     background: none;\n"
                                                                                           "}\n")
        self.submitButton.setStyleSheet("\n"
                                        "QPushButton {\n"
                                        "    background-position: center;\n"
                                        "    background-repeat: no-repeat;\n"
                                        "    background-color: rgb" + str(self.primer_color) + ";\n"
                                                                                               "    color: rgb(255, 255, 255);\n"
                                                                                               "    border: 0px solid white;\n"
                                                                                               "    border-radius: 10px;\n"
                                                                                               "}\n"
                                                                                               "QPushButton:hover {\n"
                                                                                               "    background-color: rgb" + str(
            self.hover) + ";\n"
                          "}\n"
                          "QPushButton:pressed {    \n"
                          "    background-color: rgb" + str(self.pressed) + ";\n"
                                                                            "}")

        self.label000.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label001.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label002.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label003.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label004.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label010.setStyleSheet("color: rgb{};".format(self.text_color2))
        self.label011.setStyleSheet("color: rgb{};".format(self.text_color2))

        self.label_oy.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.label_oybg.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.tableWidget_oy.setStyleSheet("QTableWidget{\n"
                                          "    border: none;\n"
                                          "}\n"
                                          "QTableWidget::item {\n"
                                          "    color: rgb" + str(self.text_color2) + ";\n"
                                                                                     "}")
        self.label_ay.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.label_aybg.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.tableWidget_ay.setStyleSheet("QTableWidget{\n"
                                          "    border: none;\n"
                                          "}\n"
                                          "QTableWidget::item {\n"
                                          "    color: rgb" + str(self.text_color2) + ";\n"
                                                                                     "}")
        self.intErrorLabel.setStyleSheet("color: rgb{}".format(self.text_color2))
        self.calendarWidget.setStyleSheet("color: rgb{}; alternate-background-color:rgb{};".format(self.text_color2, self.alternete))
        #self.calendarWidget.setStyleSheet("QCalendarWidget QTableView { background-color: rgb" + str(self.text_color2) + ";\n"
        #                                  "alternate-background-color:rgb(128,128,128);}")

        for i in reversed(range(self.verticalLayout_2064.count())):
            # print(str(type(ui.verticalLayout_2064.itemAt(i).widget())))
            if str(type(self.verticalLayout_2064.itemAt(i).widget())).find("archived") != -1:
                self.verticalLayout_2064.itemAt(i).widget().label00.setStyleSheet("color: rgb{};".format(self.text_color2))
                self.verticalLayout_2064.itemAt(i).widget().label01.setStyleSheet(
                    "color: rgb{};".format(self.text_color2))
                self.verticalLayout_2064.itemAt(i).widget().label02.setStyleSheet(
                    "color: rgb{};".format(self.text_color2))
                self.verticalLayout_2064.itemAt(i).widget().label03.setStyleSheet(
                    "color: rgb{};".format(self.text_color2))
                self.verticalLayout_2064.itemAt(i).widget().label04.setStyleSheet(
                    "color: rgb{};".format(self.text_color2))
                self.verticalLayout_2064.itemAt(i).widget().label05.setStyleSheet(
                    "color: rgb{};".format(self.text_color2))
                self.verticalLayout_2064.itemAt(i).widget().label06.setStyleSheet(
                    "color: rgb{};".format(self.text_color2))


class FrameTitleBar(QtWidgets.QFrame):
    def __init__(self, ui):
        super().__init__()
        self.window = ui
        self.start = QtCore.QPoint(0, 0)
        self.name = ui.name
        self.k = False
        self.oldh = self.window.height()
        self.oldw = self.window.width()
        self.oldx = self.window.x()
        self.oldy = self.window.y()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.offset = event.pos()
        else:
            super().mousePressEvent(event)
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            # QtCore.QTimer.singleShot(250, self.maximize_restore())
            self.maximize_restore()

    def mouseMoveEvent(self, event):
        try:
            if self.offset is not None and event.buttons() == QtCore.Qt.LeftButton:
                self.window.move(self.window.pos() + event.pos() - self.offset)
                if self.window.width() > 1919 and self.window.height() > 1000:
                    self.window.setGeometry(self.oldx, self.oldy, self.oldw, self.oldh)
                    self.k = False
            else:
                super().mouseMoveEvent(event)
        except:
            pass

    def mouseReleaseEvent(self, event):
        self.offset = None
        super().mouseReleaseEvent(event)

    def btn_close_clicked(self):
        if self.name == "MainWindow":
            sys.exit()
        elif self.name == "MoreLecture":
            self.window.close()

    def btn_min_clicked(self):
        self.window.showMinimized()

    def maximize_restore(self):
        if not self.k:
            self.oldh = self.window.height()
            self.oldw = self.window.width()
            self.oldx = self.window.x()
            self.oldy = self.window.y()
            self.window.setGeometry(0, 0, 1920, 1030)
            self.k = True
        else:
            self.window.setGeometry(self.oldx, self.oldy, self.oldw, self.oldh)
            self.k = False

    def dobleClickMaximizeRestore(event):
        pass


class SideGrip(QtWidgets.QFrame):
    def __init__(self, parent, edge):
        QtWidgets.QWidget.__init__(self, parent)
        self.setStyleSheet("background-color: transparent;")

        if edge == QtCore.Qt.LeftEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.resizeFunc = self.resizeLeft
        elif edge == QtCore.Qt.TopEdge:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.resizeFunc = self.resizeTop
        elif edge == QtCore.Qt.RightEdge:
            self.setCursor(QtCore.Qt.SizeHorCursor)
            self.resizeFunc = self.resizeRight
        else:
            self.setCursor(QtCore.Qt.SizeVerCursor)
            self.resizeFunc = self.resizeBottom
        self.mousePos = None

    def resizeLeft(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() - delta.x())
        geo = window.geometry()
        geo.setLeft(geo.right() - width)
        window.setGeometry(geo)

    def resizeTop(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() - delta.y())
        geo = window.geometry()
        geo.setTop(geo.bottom() - height)
        window.setGeometry(geo)

    def resizeRight(self, delta):
        window = self.window()
        width = max(window.minimumWidth(), window.width() + delta.x())
        window.resize(width, window.height())

    def resizeBottom(self, delta):
        window = self.window()
        height = max(window.minimumHeight(), window.height() + delta.y())
        window.resize(window.width(), height)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.mousePos = event.pos()

    def mouseMoveEvent(self, event):
        if self.mousePos is not None:
            delta = event.pos() - self.mousePos
            self.resizeFunc(delta)

    def mouseReleaseEvent(self, event):
        self.mousePos = None


class MoreLectureWindow(QtWidgets.QWidget):

    def __init__(self, op):
        super().__init__()
        self.name = "MoreLecture"
        uiFunctions.apply_preferences(self)
        self.setWindowIcon(QtGui.QIcon(":/terminal/windowicon.png"))
        self.op = op
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self)
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_9.setSpacing(0)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.right_frame = QtWidgets.QFrame(self)
        self.right_frame.setEnabled(True)
        self.right_frame.setMinimumSize(QtCore.QSize(463, 333))
        self.right_frame.setStyleSheet("background-color: rgb{};".format(self.seconder_color))
        self.right_frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.right_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.right_frame.setObjectName("right_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.right_frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = FrameTitleBar(self)
        self.frame.window = self
        self.frame.setMinimumSize(QtCore.QSize(10, 28))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 28))
        self.frame.setStyleSheet("background-color: rgb{};".format(self.primer_color))
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.top_label = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.top_label.setFont(font)
        self.top_label.setStyleSheet("background: transparent;\n"
                                     "color:rgb" + str(self.text_color) + ";\n"
                                                                          "\n"
                                                                          "")
        self.top_label.setObjectName("top_label")
        self.horizontalLayout_2.addWidget(self.top_label)
        #spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        #self.horizontalLayout_2.addItem(spacerItem)
        self.exit_button = QtWidgets.QPushButton(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.exit_button.sizePolicy().hasHeightForWidth())
        self.exit_button.setSizePolicy(sizePolicy)
        self.exit_button.setMinimumSize(QtCore.QSize(40, 0))
        self.exit_button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.exit_button.setStyleSheet("QPushButton {    \n"
                                       "    border: none;\n"
                                       "    background-color: transparent;\n"
                                       "    image: url(:/menu/exit.png);\n"
                                       "\n"
                                       "}\n"
                                       "QPushButton:hover {\n"
                                       "    background-color: rgb" + str(self.hover2) + ";\n"
                                                                                        "}\n"
                                                                                        "QPushButton:pressed {    \n"
                                                                                        "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")
        self.exit_button.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/16x16/icons/16x16/cil-x.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.exit_button.setIcon(icon)
        self.exit_button.setObjectName("exit_button")
        self.horizontalLayout_2.addWidget(self.exit_button)
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout_2.setContentsMargins(11, 0, 0, 0)
        self.frame_12 = QtWidgets.QFrame(self.right_frame)
        self.frame_12.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_12.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_12.setObjectName("frame_12")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.frame_12)
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_8.setSpacing(0)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.frame_11 = QtWidgets.QFrame(self.frame_12)
        self.frame_11.setStyleSheet("background-color: rgb{};".format(self.seconder_color))
        self.frame_11.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame_11.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_11.setObjectName("frame_11")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.frame_11)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.scrollArea = QtWidgets.QScrollArea(self.frame_11)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollArea.setStyleSheet("QScrollBar:vertical {\n"
                                      "     background-color: rgb" + str(self.scrollseconder) + ";\n"
                                                                                                "     \n"
                                                                                                "     border: 1px transparent #2A2929;\n"
                                                                                                "     \n"
                                                                                                "     width: 8px;\n"
                                                                                                "}\n"
                                                                                                " QScrollBar::handle:vertical {\n"
                                                                                                "     background-color: rgb" + str(
            self.scrollprimer) + ";\n"
                                 "     min-height: 52px;\n"
                                 "     border-radius: 4px;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-"
                                 "position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                 "     background: none;\n"
                                 "}\n")

        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 455, 282))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        # self.lectureButton = MoreLectureButton("ITB 210", "Ottoman History")
        # self.verticalLayout_2.addWidget(self.lectureButton)

        #spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        #self.verticalLayout_2.addItem(spacerItem1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout_5.addWidget(self.scrollArea)
        self.horizontalLayout_8.addWidget(self.frame_11)
        self.verticalLayout.addWidget(self.frame_12)
        self.horizontalLayout_9.addWidget(self.right_frame)
        # self.setCentralWidget(self.centralwidget)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.exit_button.clicked.connect(self.frame.btn_close_clicked)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: rgb{};".format(self.primer_color))

        self._gripSize = 3  # ==> THICKNESS OF THE RESIZING FRAME
        self.sideGrips = [
            SideGrip(self, QtCore.Qt.LeftEdge),
            SideGrip(self, QtCore.Qt.TopEdge),
            SideGrip(self, QtCore.Qt.RightEdge),
            SideGrip(self, QtCore.Qt.BottomEdge),
        ]

        self.cornerGrips = [QtWidgets.QSizeGrip(self) for i in range(4)]

        for i in self.cornerGrips:
            i.setStyleSheet("background-color: rgb{};".format(self.primer_color))

    @property
    def gripSize(self):
        return self._gripSize

    def setGripSize(self, size):
        if size == self._gripSize:
            return
        self._gripSize = max(2, size)
        self.updateGrips()

    def updateGrips(self):
        self.setContentsMargins(*[self.gripSize] * 4)

        outRect = self.rect()
        inRect = outRect.adjusted(self.gripSize, self.gripSize,
                                  -self.gripSize, -self.gripSize)

        self.cornerGrips[0].setGeometry(
            QtCore.QRect(outRect.topLeft(), inRect.topLeft()))

        self.cornerGrips[1].setGeometry(
            QtCore.QRect(outRect.topRight(), inRect.topRight()).normalized())

        self.cornerGrips[2].setGeometry(
            QtCore.QRect(inRect.bottomRight(), outRect.bottomRight()))

        self.cornerGrips[3].setGeometry(
            QtCore.QRect(outRect.bottomLeft(), inRect.bottomLeft()).normalized())

        self.sideGrips[0].setGeometry(
            0, inRect.top(), self.gripSize, inRect.height())

        self.sideGrips[1].setGeometry(
            inRect.left(), 0, inRect.width(), self.gripSize)

        self.sideGrips[2].setGeometry(
            inRect.left() + inRect.width(),
            inRect.top(), self.gripSize, inRect.height())

        self.sideGrips[3].setGeometry(
            self.gripSize, inRect.top() + inRect.height(),
            inRect.width(), self.gripSize)

    def resizeEvent(self, event):
        QtWidgets.QWidget.resizeEvent(self, event)
        self.updateGrips()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.top_label.setText(_translate("MainWindow", "Ekstra ders ekle"))
        self.exit_button.setToolTip(_translate("MainWindow", "Close"))

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.op.value = False

    def change_theme(self):
        self.right_frame.setStyleSheet("background-color: rgb{};".format(self.seconder_color))
        self.frame.setStyleSheet("background-color: rgb{};".format(self.primer_color))
        self.top_label.setStyleSheet("background: transparent;\n"
                                     "color:rgb" + str(self.text_color) + ";\n"
                                                                          "\n"
                                                                          "")
        self.exit_button.setStyleSheet("QPushButton {    \n"
                                       "    border: none;\n"
                                       "    background-color: transparent;\n"
                                       "    image: url(:/menu/exit.png);\n"
                                       "\n"
                                       "}\n"
                                       "QPushButton:hover {\n"
                                       "    background-color: rgb" + str(self.hover2) + ";\n"
                                                                                        "}\n"
                                                                                        "QPushButton:pressed {    \n"
                                                                                        "    background-color: rgb" + str(
            self.pressed) + ";\n"
                            "}")
        self.frame_11.setStyleSheet("background-color: rgb{};".format(self.seconder_color))
        self.scrollArea.setStyleSheet("QScrollBar:vertical {\n"
                                      "     background-color: rgb" + str(self.scrollseconder) + ";\n"
                                                                                                "     \n"
                                                                                                "     border: 1px transparent #2A2929;\n"
                                                                                                "     \n"
                                                                                                "     width: 8px;\n"
                                                                                                "}\n"
                                                                                                " QScrollBar::handle:vertical {\n"
                                                                                                "     background-color: rgb" + str(
            self.scrollprimer) + ";\n"
                                 "     min-height: 52px;\n"
                                 "     border-radius: 4px;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical {\n"
                                 "     margin: 3px 0px 3px 0px;\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow_disabled.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::sub-line:vertical:hover,QScrollBar::sub-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/up_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-"
                                 "position: top;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::add-line:vertical:hover, QScrollBar::add-line:vertical:on {\n"
                                 "     border-image: url(:/qss_icons/rc/down_arrow.png);\n"
                                 "     height: 10px;\n"
                                 "     width: 10px;\n"
                                 "     subcontrol-position: bottom;\n"
                                 "     subcontrol-origin: margin;\n"
                                 "}\n"
                                 " QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
                                 "     background: none;\n"
                                 "}\n"
                                 " QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
                                 "     background: none;\n"
                                 "}\n")
        self.setStyleSheet("background-color: rgb{};".format(self.primer_color))
        for i in self.cornerGrips:
            i.setStyleSheet("background-color: rgb{};".format(self.primer_color))


class MoreLectureButton(QtWidgets.QPushButton):

    def __init__(self, code, name, credit, dep, ui, db):
        super().__init__()
        self.code = code
        self.name = name
        self.credit = credit
        self.dep = dep
        self.ui = ui
        self.db = db

        self.setMinimumSize(QtCore.QSize(230, 45))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.setFont(font)
        text = self.code + " " + self.name
        self.setText(text)
        self.setStyleSheet("QPushButton {\n"
                           "    background-position: center;\n"
                           "    background-repeat: no-reperat;\n"
                           "    border: none;\n"
                           "    background-color: rgb(255, 255, 255,200);\n"
                           "    border-radius: 5px;\n"
                           "}\n"
                           "QPushButton:hover {\n"
                           "    background-color: rgb(255, 255, 255,240);\n"
                           "}\n"
                           "QPushButton:pressed {    \n"
                           "    background-color: rgb(200,200,200,240);\n"

                                                                             "}")

        self.clicked.connect(self.render_the_lecture)

    def render_the_lecture(self):
        con = sqlite3.connect("ExtraLectures.db")
        cursor = con.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS {} (Code TEXT, Name TEXT, Credit TEXT, Grade TEXT)".format(self.dep))
        cursor.execute("INSERT INTO {} VALUES(?, ?, ?, '')".format(self.dep), (self.code, self.name, self.credit))
        con.commit()
        con.close()

        extra_lecture = uiClasses.LectureFrame(self.code, self.name, self.credit, self.dep, self.ui, "ExtraLectures.db")
        self.closeButton = QtWidgets.QPushButton()
        self.closeButton.setMinimumWidth(30)
        self.closeButton.setMinimumHeight(30)
        self.closeButton.setStyleSheet("QPushButton {\n"
                                       "border-radius:15px;\n"
                                       "background-color: transparent;\n"
                                       "image: url(:/menu/exit.png);\n}"
                                       "QPushButton:hover {\n"
                                       "background-color: rgb(52, 59, 72, 150)\n;}"
                                       "QPushButton:pressed {\n"
                                       ";\n")

        extra_lecture.horizontalLayout_5.addWidget(self.closeButton)
        self.closeButton.clicked.connect(lambda: self.close_extra_lecture(extra_lecture))

        self.ui.verticalLayout_28.insertWidget(0, extra_lecture)

        con = sqlite3.connect("MainLectures.db")
        cursor = con.cursor()
        cursor.execute("SELECT TotalCredit FROM settings")
        data = cursor.fetchall()
        if data == [('0.0',)]:
            self.ui.gpaLabel.setText("N/A")

    def close_extra_lecture(self, lecture):

        index = lecture.letterGrade_comboBox.findText(" ??", QtCore.Qt.MatchFixedString)
        if index >= 0:
            lecture.letterGrade_comboBox.setCurrentIndex(index)

        lecture.close()
        con = sqlite3.connect("ExtraLectures.db")
        cursor = con.cursor()
        cursor.execute("DELETE FROM {} where Name = ?".format(self.dep), (lecture.name,))
        con.commit()
        con.close()

        con = sqlite3.connect("MainLectures.db")
        cursor = con.cursor()
        cursor.execute("SELECT TotalCredit FROM settings")
        data = cursor.fetchall()
        if data == [('0.0',)]:
            self.ui.gpaLabel.setText("N/A")


class addShortcutButton(QtWidgets.QPushButton):
    def __init__(self, ui, text):
        super().__init__()

        self.ui = ui
        self.setMinimumSize(QtCore.QSize(230, 45))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.setFont(font)
        self.setText(text)
        self.setStyleSheet("QPushButton {\n"
                           "    background-position: center;\n"
                           "    background-repeat: no-reperat;\n"
                           "    border: none;\n"
                           "    background-color: rgb(255, 255, 255,200);\n"
                           "    border-radius: 5px;\n"
                           "}\n"
                           "QPushButton:hover {\n"
                           "    background-color: rgb(255, 255, 255,240);\n"
                           "}\n"
                           "QPushButton:pressed {    \n"
                           "    background-color: rgb(200,200,200,240);\n"

                                                                             "}")