from PyQt5.QtWidgets import *

from andmebaas import *


värvid = {'punane': "9E2B25", 'sinine': "4F759B",
          'lilla': "822E81", 'roosa': "FFB8D1"}
värvid_index = ['9E2B25', "4F759B", "822E81", "FFB8D1"]


class task_klass(QDialog):
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
        lisa_task(nimi, kestvus, kirjeldus, tüüp, värv)
        self.to_do_nupp(aken, viimane_rida)
        self.accept()

    def to_do_nupp(self, aken, viimane_rida):
        task = saa_task()
        nimi = task['nimi']
        kestvus = task['kestvus']

        värv = task['värv']
        nupp = QPushButton(f'{kestvus+1}h, {nimi}', aken)
        nupp.setStyleSheet(f'background-color: #{värvid_index[int(värv)]}')
        aken.setCellWidget(viimane_rida+1, 7, nupp)
        nupp.clicked.connect(
            lambda checked, data=task, pea_aken=aken: self.naita_andmeid(data, pea_aken))

    def naita_andmeid(self, task, pea_aken):
        self.kast = QWidget()
        self.kast.setWindowTitle(f'{task['nimi']}')
        self.kast.setStyleSheet(
            f'background-color: #{värvid_index[int(task['värv'])]};')
        paigutus = QVBoxLayout()
        paigutus.addWidget(QLabel(f'Nimi: {task['nimi']}'))
        paigutus.addWidget(QLabel(f'Kestvus: {task['kestvus']}'))
        paigutus.addWidget(QLabel(f'Tüüp: {task['tüüp']}'))
        paigutus.addWidget(QLabel(f'Kirjeldus: {task['kirjeldus']}'))
        lisa_kalendrisse_nupp = QPushButton(
            f'Lisa kalendrisse')
        lisa_kalendrisse_nupp.setStyleSheet(
            f'background-color: #{värvid_index[int(task['värv'])]};')
        paigutus.addWidget(lisa_kalendrisse_nupp)

        lisa_kalendrisse_nupp.clicked.connect(
            lambda checked, data=task, aken=pea_aken: task_klass.tee_kohad(
                self, data, aken)
        )

        self.kast.setLayout(paigutus)
        self.kast.show()

    # aeg ? [column, row] #SIIN ON VAJA MAIN AKENT
    def lisa_kalendrisse(self, aeg, task, pea_aken):

        nupp = QPushButton(f'{task['kestvus']+1}h, {task['nimi']}', self)
        nupp.setStyleSheet(
            f'background-color: #{värvid_index[int(task['värv'])]};')
        pea_aken.setCellWidget(aeg[1], aeg[0], nupp)
        add = 0
        if task['kestvus'] != 0:
            add = 1
        pea_aken.setSpan(aeg[1], aeg[0], add+task['kestvus'], 1)
        muuda_toimumisaega(task['id'], int(aeg[0]), int(aeg[1]))
        nupp.clicked.connect(
            lambda checked, data=task: task_klass.naita_andmeid(self, data, pea_aken))

    def tee_kohad(self, data, pea_aken):  # SIIN ON KA VAJA MAIN AKENT
        self.nupud = []
        print(self.määratud_kohad)
        for column in range(7):
            for rida in range(15):
                olemasolev_asi = pea_aken.cellWidget(rida, column)
                on_hõivatud = (olemasolev_asi is not None) or ([int(column), int(rida)] in self.määratud_kohad)
                if not on_hõivatud:
                    nupp_l = QPushButton('nupp', self)
                    nupp_l._pos = (rida, column)
                    self.nupud.append(nupp_l)
                    pea_aken.setCellWidget(rida, column, nupp_l)
                    asukoha_info = [column, rida]
                    nupp_l.clicked.connect(
                        lambda checked, asukoht=asukoha_info, task=data: task_klass.saada_asukoht(self, asukoht, task, pea_aken))

    def saada_asukoht(self, asukoht, task, pea_aken):
        self.määratud_kohad.append(asukoht)  
        for nupp in self.nupud:
            pos = getattr(nupp, '_pos', None)
            if pos is not None:
                row, col = pos
                pea_aken.setCellWidget(row, col, None)
            nupp.setParent(None)
            nupp.deleteLater()
        self.nupud.clear()
        # SIIN ON vAJA MAIN AKENT
        task_klass.lisa_kalendrisse(self, asukoht, task, pea_aken)
