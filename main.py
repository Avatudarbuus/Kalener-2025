import sys
from PyQt5.QtWidgets import *
from task import loo_andmebaas, saa_taskid, muuda_toimumisaega
from task import task_klass as task_fid
import icalendar

# Main Window
värvid = {'punane': "9E2B25", 'sinine': "4F759B",
          'lilla': "822E81", 'roosa': "FFB8D1"}
värvid_index = ['9E2B25', "4F759B", "822E81", "FFB8D1"]


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.akna_nim = 'Kalender'
        self.vasak = 0
        self.ules = 0
        self.laius = 900
        self.korgus = 600
        self.viimane_rida = 1
        self.määratud_kohad = []
        self.setWindowTitle(self.akna_nim)
        self.setGeometry(self.vasak, self.ules, self.laius, self.korgus)
        self.createTable()
        

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)
        # Show window
        self.show()

    # Create table
    def createTable(self):
        self.tableWidget = QTableWidget()

        # Row count
        # Kalendrisse saab plaane panna 7st 22ni
        self.tableWidget.setRowCount(15)
        # Column count
        self.tableWidget.setColumnCount(8)
        aeg = 7
        indeks = 1
        ajad = []
        for _ in range(17):
            ajad += [f"{aeg}.00 - {aeg+1}.00"]
            aeg += 1
            indeks += 1

        self.tableWidget.setHorizontalHeaderLabels(
            ["Esmaspäev", "Teisipäev", "Kolmapäev", "Neljapäev", "Reede", "Laupäev", "Pühapäev", "To-Do"])
        self.tableWidget.setVerticalHeaderLabels(ajad)
        loo_task = QPushButton("Loo tegevus", self)
        self.tableWidget.setCellWidget(0, 7, loo_task)
        loo_task.raise_()
        loo_task.clicked.connect(self.taski_aken)
        self.tableWidget.setColumnWidth(7, 400)
        

        self.to_do_aken(self.tableWidget)

    def to_do_aken(self, aken):
        koik_taskid = saa_taskid()
        print(koik_taskid)
        arv = len(koik_taskid)
        if arv > 15:
            print('Liiga palju lisatud taske')
        for row, task in enumerate(koik_taskid, start=1):
            if task['rida'] == 'NONE' or task['kolonn'] == 'NONE':
            # task_data = [task['kestvus'],task['nimi'], task['kirjeldus'], task['tüüp'], task['värv'], task['toimumis_aeg']]
                nupp = QPushButton(f'{task['kestvus']}, {task['nimi']}', self)
                aken.setCellWidget(row, 7, nupp)
                nupp.clicked.connect(
                    lambda checked, data=task: task_fid.naita_andmeid(self, data, self.tableWidget))
            else:
                self.määratud_kohad.append([task['kolonn'],task['rida']])
                task_fid.lisa_kalendrisse(self,[int(task['kolonn']),int(task['rida'])],task, aken)
            self.viimane_rida = row

    ''' def naita_andmeid(self, task):
            global paigutus
            print(f'Naitan andmeid kohas: {task}')
            self.naitan_andmeid = QWidget()
            self.naitan_andmeid.setFixedWidth(400)
            self.naitan_andmeid.setFixedHeight(500)
            self.naitan_andmeid.setWindowTitle(f'{'nimi'}')
            self.naitan_andmeid.setStyleSheet(
                f'background-color: #{värvid_index[int(task['värv'])]};')
            paigutus = QVBoxLayout()
            paigutus.addWidget(QLabel(f'Nimi: {task['nimi']}'))
            paigutus.addWidget(QLabel(f'Kestvus: {int(task['kestvus']) +1}'))
            paigutus.addWidget(QLabel(f'Tüüp: {task['tüüp']}'))
            paigutus.addWidget(QLabel(f'Kirjeldus: {task['kirjeldus']}'))
            #paigutus.addWidget(QLabel(f'Toimumis aeg: {task['toimumis_aeg']}'))
            lisa_kalendrisse_nupp = QPushButton(
                f'Lisa kalendrisse')
            lisa_kalendrisse_nupp.setStyleSheet(
                f'background-color: #{värvid_index[int(task['värv'])]};')
            paigutus.addWidget(lisa_kalendrisse_nupp)

            lisa_kalendrisse_nupp.clicked.connect(
                lambda checked, data=task: self.tee_kohad(data)
            )
            self.naitan_andmeid.setLayout(paigutus)
            self.naitan_andmeid.show()'''



    def taski_aken(self):
        dlg = task_fid()
        andmed = dlg.aken(self.tableWidget, self.viimane_rida)
        dlg.exec_()
        

#SIIN ON vAJA MAIN AKENT
        
if __name__ == '__main__':
    loo_andmebaas()
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
