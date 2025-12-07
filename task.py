from PyQt5.QtWidgets import *

from andmebaas import *





värvid = {'punane': "9E2B25", 'sinine': "4F759B", 'lilla': "822E81", 'roosa': "FFB8D1"}
värvid_index = ['9E2B25', "4F759B", "822E81", "FFB8D1"]

class task(QDialog):
    def __init__(self):
        super().__init__()
        self.widget = QWidget()
        self.setFixedHeight(600)
        self.setFixedWidth(600)
        self.määratud_kohad = []

    def aken(self, aken, viimane):

        paigutus = QVBoxLayout()
        paigutus.addWidget(QLabel("Kestus"))
        self.setGeometry(10, 10, 500, 500)
        self.aja_valik = QButtonGroup(self)
        self.valikud = []
        for i, valik in enumerate([1, 2, 3, 4]):
            valik = QRadioButton(str(valik))
            self.aja_valik.addButton(valik, i)
            paigutus.addWidget(valik)
            self.valikud.append(valik)
        self.varvid_nupud = QButtonGroup(self)
        self.värvi_valikud = []
        for i, varv in enumerate(värvid.keys()):
            valik = QRadioButton(varv)
            self.varvid_nupud.addButton(valik, i)
            paigutus.addWidget(valik)
            self.värvi_valikud.append(valik)
        self.nimi = QLineEdit()
        self.nimi.setPlaceholderText("Sisesta tegevuse nimi")
        paigutus.addWidget(self.nimi)
        self.kirjeldus = QTextEdit()
        paigutus.addWidget(self.kirjeldus)
        self.tüüp = QLineEdit()
        paigutus.addWidget(self.tüüp)
        self.kinnita = QPushButton('Kinnita')
        self.kinnita.clicked.connect(lambda: self.edasta_andmed(aken, viimane))

        paigutus.addWidget(self.kinnita)
        self.setLayout(paigutus)
        self.toimumis_aeg = None


    def edasta_andmed(self, aken, viimane_rida):

        kestvus = self.aja_valik.checkedId()
        värv = self.varvid_nupud.checkedId()
        nimi = self.nimi.text()
        kirjeldus = self.kirjeldus.toPlainText()
        tüüp = self.tüüp.text()
        toimumis_aeg = None
        lisa_task(nimi,kestvus, kirjeldus, tüüp, värv)
        self.accept()
        self.to_do_nupp(aken, viimane_rida)

    
    
    def to_do_nupp(self,aken, viimane_rida):
        task = saa_task()
        nimi = task['nimi']
        kestvus = task['kestvus']

        kirjeldus = task['kirjeldus']
        tüüp = task['tüüp']
        värv = task['värv']
        nupp = QPushButton(f'{kestvus+1}h, {nimi}', aken)
        nupp.setStyleSheet(f'background-color: #{värvid_index[int(värv)]}')
        aken.setCellWidget(viimane_rida, 7, nupp)
        nupp.clicked.connect(
            lambda checked, data=task: self.naita_andmeid(data))


    def naita_andmeid(self,task):
        self.kast = QWidget()
        self.kast.setWindowTitle(f'{task['nimi']}')
        self.kast.setStyleSheet(f'background-color: #{värvid_index[int(task['värv'])]};')
        paigutus = QVBoxLayout()
        paigutus.addWidget(QLabel(f'Nimi: {task['nimi']}'))
        paigutus.addWidget(QLabel(f'Kestvus: {task['kestvus']}'))
        paigutus.addWidget(QLabel(f'Tüüp: {task['tüüp']}'))
        paigutus.addWidget(QLabel(f'Kirjeldus: {task['kirjeldus']}'))
        #paigutus.addWidget(QLabel(f'Toimumis aeg: {task['toimumis_aeg']}'))

        self.kast.setLayout(paigutus)
        self.kast.show()
            

