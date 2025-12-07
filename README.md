Kalender

Eesmärk:
Võimalik on teha omale to-do list ja näha seda kalendri kõrvalt. 
Kalendrit näed nädala kaupa. ICal viitega loodud asjad on juba automaatselt kalendris.
To-do list on plokkidena ja neile on kasutaja määranud kui kaua antud ülesandega läheb. 
Edasi saab kasutaja asetada to-do listi plokke kalendrisse.

Kasutusjuhend:
Alustuseks on vaja installida vajalikud teegid. Selleks saab jooksutada käsureal, kui olla õiges kaustas pip install -r requirements.txt
Selleks, et lisada iCal viide peab õisist selle kopeerima faili ical_lugemine.py kohta url =. Programmi käivitades saab vajutada 'Loo task' ja alustada to_do listi tegemisega. Pärast saab nende peale vajutada ja lisada kalendrisse.

Teekidest:
icalendar: Loeb iCal viitest infot meile arusaadavaks
recurring_ical_events: loeb ical viitest välja mitmeid kordi toimuvad üritused nädala jooksul
requests - annab minu ical viitele ligipääsu internetile ja loeb sealt sellega infot
PyQt5 - loob meile tabeli ja nupud, tänu millele saab asju kalendrisse panna (kasutajaliides)

Litsentsist:
Litsentsiks valin GNU General Public License v3.0, sest kasutan PyQt5 teeki, mis on sama litsensiga. Selleks, et teha koodile litsentsi, mis kasutab eelnevalt mainitud teeki peab olema kooskõplas GPL litsensiga ja seega on seda kõige mõistlikum kasutada.
Täispikk litsentsi tekst (https://www.gnu.org/licenses/gpl-3.0.en.html) on lisatud faili nimeka LICENSE.

Pythoni virtuaalkeskkond:
Venv on isoleeritud kaust kus on projekti jaoks vajalikud teegid nii, et neid ei peaks tervesse masinasse alla laadima. Kui ma tahan kasutada ühe projekti jaoks vanemat versiooni ja teise ptojekti jaoks uuemat siis võivad mõlemad arvutisse laetult üktseist segada.
