from PyQt5 import QtCore, QtGui, QtWidgets
import pypyodbc
import time
from PyQt5 import QtSql



class Ui_MainWindow(object):
    def tabmenuaktif(self):
        self.tab_2.setEnabled(True)
        self.tab_3.setEnabled(True)
        self.tab_4.setEnabled(True)
        self.tab_5.setEnabled(True)
        self.tab_6.setEnabled(True)

    def mesaj(self , baslik="UYARI" , icerik="SQL Bağlantısı Sağlandı"):
        self.msj = QtWidgets.QMessageBox()
        self.msj.setWindowTitle(baslik)
        self.msj.setText(icerik)
        self.msj.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msj.exec_()

    def baglan(self):
        try:
            self.server = self.lineEdit.text()
            self.db = self.lineEdit_2.text()
            self.kadi = self.lineEdit_3.text()
            self.sifre = self.lineEdit_4.text()

            self.conn_metni = (
                'Driver={SQL Server};'
                'Server=' + self.server + ';'
                'Database=' + self.db + ';'
                'UID=' + self.kadi + ';'
                'PWD=' + self.sifre + ';')

            self.conn = pypyodbc.connect(self.conn_metni)

            self.cursor = self.conn.cursor()

            self.mesaj()
            self.tabmenuaktif()
            self.raporsec()

        except:
            self.mesaj("UYARI" , "SQL Bağlantısı Kurulamadı")


    def hesapyazimgerial(self):
        cekno = self.lineEdit_5.text()
        self.cursor.execute("update orderheaders set FiscalKey='',FiscalStatus=0,OrderStatus=1,ingenico='' where OrderID = {}".format(cekno))
        self.cursor.execute("update orderpayments set lineDeleted=1 where OrderID = {}".format(cekno))
        self.cursor.commit()
        self.mesaj("Uyarı" , "İşlem Tamamlandı" )

    def raporseviyesi(self):
        seviye = self.comboBox.currentText()
        self.cursor.execute("UPDATE Reports SET SecurityLevel= {} ".format(seviye))
        self.cursor.commit()
        self.mesaj("Uyarı", "İşlem Tamamlandı")

    def cekkontrol(self):
        cekno = self.lineEdit_6.text()
        kontrol = self.cursor.execute("select orderstatus from orderheaders where OrderID={}".format(cekno))
        while True:
            row = kontrol.fetchone()
            if not row:
                break
            return row[0]

    def fiscal(self):
        cekno = self.lineEdit_6.text()
        if (self.radioButton.isChecked()):
            if (self.cekkontrol() == 1):
                self.mesaj("Uyarı", "Açık Çek Fiscal Yazdırılamaz")
            else:
                self.cursor.execute("update orderheaders set FiscalStatus=1 where OrderID= {}".format(cekno))
                self.cursor.commit()
                self.mesaj("Uyarı" , "İşlem Tamamlandı")
        elif(self.radioButton_2.isChecked()):
            if(self.cekkontrol() == 1):
                self.mesaj("Uyarı" , "Açık Çek üzerinde fiscal işlemi sağlanamaz")
            else:
                self.cursor.execute("update orderheaders set FiscalStatus=0 where OrderID= {}".format(cekno))
                self.cursor.commit()
                self.mesaj("Uyarı" , "İşlem Tamamlandı")
        else:
            self.mesaj("Uyarı" ,"HATA")
    def verigonder(self):
        try:
            baslangictarihi = self.lineEdit_7.text()
            bitistarihi = self.lineEdit_8.text()
            if(baslangictarihi=="" or bitistarihi==""):
                self.mesaj("Uyarı","Tarih Giriniz")
            elif(len(baslangictarihi)!=10 or len(bitistarihi)!=10):
                self.mesaj("Uyarı" , "Tarih hatalı")
            else:
                self.cursor.execute("UPDATE OrderHeaders set SendOk=0 WHERE OrderDateTime > '{}' AND OrderDateTime < '{}';".format(baslangictarihi,bitistarihi))
                self.cursor.execute("UPDATE OrderTransactions set SendOk=0 WHERE OrderDateTime > '{}' AND OrderDateTime < '{}';".format(baslangictarihi,bitistarihi))
                self.cursor.execute("UPDATE OrderPayments set SendOk=0 WHERE PaymentDateTime > '{}' AND PaymentDateTime < '{}';".format(baslangictarihi,bitistarihi))
                self.mesaj("Uyarı" , "Veri Gönderimi İçin İşlem Sağlandı")
        except:
            self.mesaj("Uyarı", "Hata oluştu tekrar deneyin")
    def yoneticigiris(self):
        zaman = time.localtime()
        yil = zaman [0] + 2
        ay = zaman [1] + 3
        gun = zaman [2] + 4
        ay2 = str(ay)
        if (len(ay2) == 1):
            ay3 = str("0" + ay2)
        else:
            ay3 = ay2
        self.mesaj("Yönetici Şifre Panel" ,"Yönetici Şifre : {} {} {}".format(yil,ay3,gun))
    def ecrislemler(self):
        zaman = time.localtime()
        yil = str(zaman [0])
        ay = zaman [1] + 2
        gun = zaman [2] + 3
        ay2 = str(ay)
        if (len(ay2)==1):
            ay3 = str("0"+ay2)
        else:
            ay3 = ay2
        yil2 = yil [2:]
        self.mesaj("ECR İşlemler Şifre Panel" , "ECR İşlemler Şifre : {} {} {}".format(ay3,gun,yil2))
    def raporsec(self):
        raporlar = self.cursor.execute("select reportname from reports")
        while True:
            row = raporlar.fetchone()
            if not row:
                break
            for i in row:
                list(i)
                self.comboBox_2.addItem(i[0:],i)
    def secilenraporudegis(self):
        seviye = self.comboBox.currentText()
        rapor = self.comboBox_2.currentText()
        self.cursor.execute("update reports set SecurityLevel={} where ReportName='{}' ".format(seviye,rapor))
        self.cursor.commit()
        self.mesaj("Uyarı","Seçilen raporun Seviyesi Değiştirildi")
    def banka(self):
        cekno = self.lineEdit_9.text()
        if(cekno == ''):
            self.mesaj("Uyarı" , "Çek No Giriniz")
        else:
            veri = self.cursor.execute("select OrderPaymentID , AmountPaid , PaymentMethodName , GlobalBankCode , GlobalBankName  from OrderPayments where OrderID={}".format(cekno))
            self.tablo.setRowCount(0)

            for rowsayi, row in enumerate(veri):
                self.tablo.insertRow(rowsayi)
                for columnsayi, colunm in enumerate(row):
                    #self.tablo.setColumnCount(5)
                    self.tablo.setItem(rowsayi, columnsayi, QtWidgets.QTableWidgetItem(str(colunm)))
            self.comboBox_3.clear()
            self.idal()

    def idal(self):
        cekno = self.lineEdit_9.text()
        opid = self.cursor.execute("select orderpaymentID from orderpayments where OrderID= {}".format(cekno))
        while True:
            row = opid.fetchone()
            if not row:
                break
            for i in row:
                self.comboBox_3.addItem(str(i))
    def paymentekle(self):
        payid = self.comboBox_3.currentText()
        if(self.radioButton_3.isChecked()):
            self.cursor.execute("update orderpayments set linedeleted=0 where OrderPaymentID={}".format(int(payid)))
            self.mesaj("Uyarı" , "Ödeme Kapatıldı")
        elif(self.radioButton_4.isChecked()):
            self.cursor.execute("update orderpayments set linedeleted=1 where OrderPaymentID={}".format((int(payid))))
            self.mesaj("Uyarı" , "Ödeme Açıldı")
        else:
            self.mesaj("Hata", "Ödeme İşlemi Seçilmedi")
    def bankadegis(self):
        bankaadi = self.lineEdit_10.text()
        payid = self.comboBox_3.currentText()
        if(self.cekkontrol() == 1):
            self.mesaj("Uyarı" , "Açık Çekte Banka Adı Değiştirilemez")
        elif(self.cekkontrol() == 0):
            self.cursor.execute("update orderpayments set GlobalBankName='{}' where OrderPaymentID={}".format(bankaadi , int(payid)))
            self.mesaj("Uyarı", "Banka Adı Değiştirilmiştir")
        else:
            self.mesaj("Hata", "Hatalı İşlem")
    def cekkontrol(self):
        payid = self.comboBox_3.currentText()
        cekkontrol = self.cursor.execute("select linedeleted from orderpayments where OrderPaymentID={}".format(int(payid)))
        while True:
            row = cekkontrol.fetchone()
            if not row:
                break
            for i in row:
                return i




    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(561, 358)
        ######################tab 1
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 541, 311))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(110, 50, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(110, 90, 81, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.tab)
        self.label_3.setGeometry(QtCore.QRect(110, 130, 161, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(110, 170, 151, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(self.tab)
        self.lineEdit.setGeometry(QtCore.QRect(306, 48, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setText(".\POSSQL")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_2.setGeometry(QtCore.QRect(306, 88, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setText("infinia")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_3.setGeometry(QtCore.QRect(306, 127, 113, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setText("sa")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.tab)
        self.lineEdit_4.setGeometry(QtCore.QRect(306, 166, 113, 20))
        self.lineEdit_4.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_4.setText("sql123_")
        self.pushButton = QtWidgets.QPushButton(self.tab)
        self.pushButton.setGeometry(QtCore.QRect(110, 200, 311, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.baglan)
        self.yoneticibuton = QtWidgets.QPushButton(self.tab)
        self.yoneticibuton.setGeometry(QtCore.QRect(0,10,85,23))
        self.yoneticibuton.setObjectName("Yoneticibuton")
        self.yoneticibuton.clicked.connect(self.yoneticigiris)
        self.ecrbuton = QtWidgets.QPushButton(self.tab)
        self.ecrbuton.setGeometry(QtCore.QRect(0,35,85,23))
        self.ecrbuton.setObjectName("ECRbuton")
        self.ecrbuton.clicked.connect(self.ecrislemler)
        #########################TAB 2
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tab_2.setEnabled(False)
        self.pushButton_2 = QtWidgets.QPushButton(self.tab_2)
        self.pushButton_2.setGeometry(QtCore.QRect(200, 150, 121, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.clicked.connect(self.hesapyazimgerial)
        self.lineEdit_5 = QtWidgets.QLineEdit(self.tab_2)
        self.lineEdit_5.setGeometry(QtCore.QRect(200, 110, 121, 20))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_5 = QtWidgets.QLabel(self.tab_2)
        self.label_5.setGeometry(QtCore.QRect(150, 114, 47, 13))
        self.label_5.setObjectName("label_5")
        self.tabWidget.addTab(self.tab_2, "")
        #############################################TAB3
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tab_3.setEnabled(False)
        self.comboBox = QtWidgets.QComboBox(self.tab_3)
        self.comboBox.setGeometry(QtCore.QRect(160, 90, 111, 22))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pushButton_3 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_3.setGeometry(QtCore.QRect(300, 90, 131, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.raporseviyesi)
        self.label_9 = QtWidgets.QLabel(self.tab_3)
        self.label_9.setGeometry(QtCore.QRect(50, 142, 51, 16))
        self.label_9.setObjectName("label_9")
        self.comboBox_2 = QtWidgets.QComboBox(self.tab_3)
        self.comboBox_2.setGeometry(QtCore.QRect(120, 140, 311, 22))
        self.comboBox_2.setObjectName("comboBox_2")
        self.pushButton_6 = QtWidgets.QPushButton(self.tab_3)
        self.pushButton_6.setGeometry(QtCore.QRect(50, 180, 381, 23))
        self.pushButton_6.setObjectName("pushButton_6")
        self.pushButton_6.clicked.connect(self.secilenraporudegis)
        self.label_10 = QtWidgets.QLabel(self.tab_3)
        self.label_10.setGeometry(QtCore.QRect(50, 90, 81, 20))
        self.label_10.setObjectName("label_10")
        self.tabWidget.addTab(self.tab_3, "")
        #####################################################TAB4
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tab_4.setEnabled(False)
        self.lineEdit_6 = QtWidgets.QLineEdit(self.tab_4)
        self.lineEdit_6.setGeometry(QtCore.QRect(202, 90, 151, 20))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.lineEdit_6.setPlaceholderText("fiscal")
        self.label_6 = QtWidgets.QLabel(self.tab_4)
        self.label_6.setGeometry(QtCore.QRect(130, 94, 47, 13))
        self.label_6.setObjectName("label_6")
        self.radioButton = QtWidgets.QRadioButton(self.tab_4)
        self.radioButton.setGeometry(QtCore.QRect(200, 130, 82, 17))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.tab_4)
        self.radioButton_2.setGeometry(QtCore.QRect(291, 130, 82, 17))
        self.radioButton_2.setObjectName("radioButton_2")
        self.pushButton_4 = QtWidgets.QPushButton(self.tab_4)
        self.pushButton_4.setGeometry(QtCore.QRect(200, 160, 151, 23))
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.fiscal) #fiscal
        self.tabWidget.addTab(self.tab_4, "")
        ##############################################################TAB5
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tab_5.setEnabled(False)
        self.lineEdit_7 = QtWidgets.QLineEdit(self.tab_5)
        self.lineEdit_7.setGeometry(QtCore.QRect(220, 70, 113, 20))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.lineEdit_7.setPlaceholderText("2019-12-30")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.tab_5)
        self.lineEdit_8.setGeometry(QtCore.QRect(220, 110, 113, 20))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.lineEdit_8.setPlaceholderText("2019-12-30")
        self.label_7 = QtWidgets.QLabel(self.tab_5)
        self.label_7.setGeometry(QtCore.QRect(120, 70, 91, 20))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.tab_5)
        self.label_8.setGeometry(QtCore.QRect(120, 110, 81, 20))
        self.label_8.setObjectName("label_8")
        self.pushButton_5 = QtWidgets.QPushButton(self.tab_5)
        self.pushButton_5.setGeometry(QtCore.QRect(117, 150, 221, 23))
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(self.verigonder)
        self.tabWidget.addTab(self.tab_5, "")
        ###############################################################TAB6
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.label_11 = QtWidgets.QLabel(self.tab_6)
        self.label_11.setGeometry(QtCore.QRect(120, 5, 81, 20))
        self.label_11.setObjectName("label_11")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_9.setGeometry(QtCore.QRect(200, 5, 113, 20))
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.pushButton_7 = QtWidgets.QPushButton(self.tab_6)
        self.pushButton_7.setGeometry(325, 5, 113, 21)
        self.pushButton_7.setObjectName("pushbutton_7")
        self.pushButton_7.clicked.connect(self.banka)
        self.tabWidget.addTab(self.tab_6, "")
        self.tablo = QtWidgets.QTableWidget(self.tab_6)
        self.tablo.setObjectName("Tablo")
        self.tablo.setGeometry(QtCore.QRect(8,30,520,150))
        self.tablo.setColumnCount(5)
        self.kolonadlari = ("ID", "Tutar", "Ödeme Tipi", "Banka Kodu", "Banka Adı")
        self.tablo.setHorizontalHeaderLabels(self.kolonadlari)
        self.label_12 = QtWidgets.QLabel(self.tab_6)
        self.label_12.setObjectName("label_12")
        self.label_12.setGeometry(QtCore.QRect(10,200,35,20))
        self.comboBox_3 = QtWidgets.QComboBox(self.tab_6)
        self.comboBox_3.setObjectName("combobox_3")
        self.comboBox_3.setGeometry(QtCore.QRect(60,200,50,20))
        self.pushButton_8 = QtWidgets.QPushButton(self.tab_6)
        self.pushButton_8.setObjectName("Buton8")
        self.pushButton_8.setGeometry(QtCore.QRect(120,200,100,22))
        self.pushButton_8.clicked.connect(self.paymentekle)
        self.radioButton_3 = QtWidgets.QRadioButton(self.tab_6)
        self.radioButton_3.setObjectName("Radiobuton3")
        self.radioButton_3.setGeometry(QtCore.QRect(10,230,100,20))
        self.radioButton_4 = QtWidgets.QRadioButton(self.tab_6)
        self.radioButton_4.setObjectName("Radiobuton4")
        self.radioButton_4.setGeometry(QtCore.QRect(130,230,100,20))
        self.label_13 = QtWidgets.QLabel(self.tab_6)
        self.label_13.setObjectName("label_13")
        self.label_13.setGeometry(QtCore.QRect(240,200,100,20))
        self.lineEdit_10 = QtWidgets.QLineEdit(self.tab_6)
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.lineEdit_10.setGeometry(QtCore.QRect(300,200,100,20))
        self.pushButton_9 = QtWidgets.QPushButton(self.tab_6)
        self.pushButton_9.setObjectName("pushbutton_9")
        self.pushButton_9.setGeometry(QtCore.QRect(410,198,100,23))
        self.pushButton_9.clicked.connect(self.bankadegis)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 561, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Tools"))
        self.label.setText(_translate("MainWindow", "SERVER"))
        self.label_2.setText(_translate("MainWindow", "DATABASE"))
        self.label_3.setText(_translate("MainWindow", "DATABASE KULLANICI ADI"))
        self.label_4.setText(_translate("MainWindow", "DATABASE KULLANICI ŞİFRE"))
        self.pushButton.setText(_translate("MainWindow", "Bağlan"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "SQL Bağlantı"))
        self.pushButton_2.setText(_translate("MainWindow", "Hesap Yazımı Geri Al"))
        self.label_5.setText(_translate("MainWindow", "Çek No"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Çek Aç"))
        self.comboBox.setItemText(0, _translate("MainWindow", "1"))
        self.comboBox.setItemText(1, _translate("MainWindow", "2"))
        self.comboBox.setItemText(2, _translate("MainWindow", "3"))
        self.comboBox.setItemText(3, _translate("MainWindow", "4"))
        self.comboBox.setItemText(4, _translate("MainWindow", "5"))
        self.comboBox.setItemText(5, _translate("MainWindow", "6"))
        self.comboBox.setItemText(6, _translate("MainWindow", "7"))
        self.comboBox.setItemText(7, _translate("MainWindow", "8"))
        self.comboBox.setItemText(8, _translate("MainWindow", "9"))
        self.comboBox.setItemText(9, _translate("MainWindow", "10"))
        self.pushButton_3.setText(_translate("MainWindow", "Tümünü Değiştir"))
        self.label_9.setText(_translate("MainWindow", "Rapor Adı"))
        self.pushButton_6.setText(_translate("MainWindow", "Seçilen Raporu Değiştir"))
        self.label_10.setText(_translate("MainWindow", "Rapor Seviyesi"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Rapor Seviyesi"))
        self.label_6.setText(_translate("MainWindow", "Çek No"))
        self.radioButton.setText(_translate("MainWindow", "Fiscal Ekle"))
        self.radioButton_2.setText(_translate("MainWindow", "Fiscal Sil"))
        self.pushButton_4.setText(_translate("MainWindow", "Fiscal Değiştir"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Fiscal Ayarla"))
        self.label_7.setText(_translate("MainWindow", "Başlangıç Tarihi"))
        self.label_8.setText(_translate("MainWindow", "Bitiş Tarihi"))
        self.pushButton_5.setText(_translate("MainWindow", "Veri Gönder"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Veri Gönder"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("MainWindow", "Banka"))
        self.ecrbuton.setText(_translate("MainWindows", "ECR Şifre"))
        self.yoneticibuton.setText(_translate("MainWindows","Yönetici Şifre"))
        self.label_11.setText(_translate("MainWindows" , "Çek No"))
        self.pushButton_7.setText(_translate("MainWindows", "Banka / Yenile"))
        self.label_12.setText(_translate("MainWindows","ID Seç"))
        self.pushButton_8.setText(_translate("MainWindows" , "Ödeme Aç / Kapat"))
        self.radioButton_3.setText(_translate("MainWindows" , "Ödeme Kapat"))
        self.radioButton_4.setText(_translate("MainWindows", "Ödeme Aç"))
        self.label_13.setText(_translate("MainWindows", "Banka Adı "))
        self.pushButton_9.setText(_translate("MainWindows" , "Banka Değiştir"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
