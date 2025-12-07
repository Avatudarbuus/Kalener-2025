import sys
from PyQt5.QtWidgets import *
from task import loo_andmebaas, saa_taskid, muuda_toimumisaega, lisa_task
from task import task_klass as task_fid
from icalendar import Calendar
import recurring_ical_events
import requests
from pathlib import Path
import datetime
from ical_lugemine import saa_ical, saa_rida
# Main Window
värvid = {'punane': "9E2B25", 'sinine': "4F759B",
          'lilla': "822E81", 'roosa': "FFB8D1"}
värvid_index = ['9E2B25', "4F759B", "822E81", "FFB8D1"]


class App(QWidget):
    '''Klassis on pea akna parameetrid'''
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
        '''Loob telje pealkirjad ja toote'''
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
        '''Loob kõik objektid mis on andmebaasis ja ical viitega'''
        oisi_omad = self.saa_andmed()
        for too in oisi_omad:
            lisa_task(too['nimi'],too['kestvus'], too['kirjeldus'], too['tüüp'], 1,too['rida'], too['kolonn'])
        koik_taskid = saa_taskid()
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
                self.määratud_kohad.append([task['kolonn'], task['rida']])
                task_fid.lisa_kalendrisse(
                    self, [int(task['kolonn']), int(task['rida'])], task, aken)
            self.viimane_rida = row


    def taski_aken(self):
        '''saadab peaakna ja viimase rea maini (viimane rida väga ei tööta)'''
        dlg = task_fid()
        andmed = dlg.aken(self.tableWidget, self.viimane_rida)
        dlg.exec_()

    def saa_andmed(self):
        '''saab info õisist'''
        events = saa_ical(self)
        koik_taskid = []
        for event in events:
            name = event.get('SUMMARY')
            start_time = event.get('DTSTART').dt
            kolonn = start_time.weekday()

            event_type = "Unknown"
            
            categories = event.get('CATEGORIES')
            if categories:

                if not isinstance(categories, list):
                    categories = [categories]
                clean = []
                for cat in categories:
                    try:
                        text= cat.to_ical().decode('utf-8')
                        clean.append(text)
                    except:
                        clean.append(str(cat))
                event_type = ', '.join(clean)


            info = saa_rida(event)
            description = event.get('DESCRIPTION', '')
            koik_taskid.append({'nimi': name, 'tüüp': event_type, 'kirjeldus': description, 'rida': info[0], 'kolonn':kolonn, 'kestvus': info[1]})
        return koik_taskid


# SIIN ON vAJA MAIN AKENT

if __name__ == '__main__':
    '''Paneb programmi tööle'''
    loo_andmebaas()
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
