COME AVVIARE SOLITARIO:


Windows:
- Installa la versione più recente di Python

- Apri il prompt dei comandi: 
	digita 'cmd' nel menu Start

- Naviga nella directory del file: 
	Utilizza il comando 'cd' seguito dal percorso della cartella, 
	esempio: cd C:\Users\utente\Desktop\Solitario\

- Installa le dipendenze (salta se già installate):
	Digita nel cmd: 'pip install -r .\require.txt' (senza virgolette)

- Esegui il file:
	Digita nel cmd: 'python3 solitario.py' (senza virgolette)
	ATTENZIONE: se con 'python3' non avvia, prova a sostituirlo con 'python' o 'py'


Linux:
Dovrai creare un ambiente virtuale (venv) in cui installare le dipendenze.

- Installa la versione più recente di Python

- Apri un terminale

- Naviga nella directory del file:
	Utilizza il comando 'cd' seguito dal percorso della cartella, 
	esempio: cd /home/utente/solitario

- Crea un ambiente virtuale (venv):
	Digita nel terminale: 'python3 -m venv nome_ambiente' (senza virgolette, sostituisci nome_ambiente con il nome che preferisci)

- Attiva l'ambiente virtuale (venv):
	Digita nel terminale: 'source nome_ambiente/bin/activate'

- Installa le dipendenze (salta se già installate nello stesso venv):
	Digita nel cmd: 'pip install -r .\require.txt' (senza virgolette)

- Esegui il file python:
	Digita nel terminale: 'python3 solitario.py' oppure 'python solitario.py'

- Per disattivare l'ambiente virtuale (venv) utilizza il comando: 'deactivate'

- ATTENZIONE:
	Se crei un nuovo Ambiente Virtuale (venv), dovrai reinstallare le dipendenze.

----------------------------------------------------------------------------------------------------------------------

COME GIOCARE A SOLITARIO:

Troverai le regole e i comandi di Solitario all'interno del programma.

Puoi spostare le carte premendo il tasto '1'
Ti verrà chiesto di selezionare una colonna, puoi farlo utilizzando FRECCIA IN SU e FRECCIA IN GIU'.

Puoi selezionarlo anche attraverso i comandi rapidi:
I TASTI da 1-7 selezioneranno le COLONNE da 1-7
Il tasto 'R' selezionerà la COLONNA DI RISERVA
Il tasto 'F' selezionerà la COLONNA FINALE 1

Se nella colonna selezionata c'è più di una carta spostabile"
Puoi selezionare la carta di partenza utilizzando FRECCIA A DESTRA e FRECCIA A SINISTRA"

Per confermare la selezione premi INVIO

Per pescare una carta premi il tasto '2'

Per visualizzare le regole premi il tasto '3'

Per visualizzare i comandi premi il tasto '4'

Puoi uscire dal gioco premendo il tasto '5'

----------------------------------------------------------------------------------------------------------------------

DESCRIZIONE DEL PROGRAMMA:

Il gioco è scritto in Python.
Per una descrizione riga per riga, leggere i commenti nello script.
Per una descrizione dettagliata di ogni funzione continuare a leggere questo documento.


Una volta avviato il MainGame(), crea un mazzo di 52 carte attraverso la funzione Generate_Deck()
Generate_Deck() definisce i quattro semi, e crea 13 carte dal valore 1 al valore 13 per ogni seme (13 * 4 = 52)

Le carte vengono create secondo la Classe Carta
In questa classe si definiscono i seguenti valori:

"valore": il valore della carta da 1 a 13
"seme": il seme della carta, cuori, diamanti, picche o fiori
"altvalore": cioè un valore con uno scopo visivo e grafico, in cui i valori 1, 11, 12 e 13 vengono sostituiti con A, J, Q, K, questo valore verrà utilizzato durante la stampa delle colonne a schermo
"colore": definendo i semi Cuori e Diamanti come ROSSO, mentre i semi Picche e Fiori come NERO
"scoperta": se una carta è visibile al giocatore, vengono messe tutte come False, verrà cambiato nella generazione delle colonne per far scoprire le ultime di ogni colonna.
"simbolo": associa ad ogni seme il simbolo corrispettivo

Nel __repr__ si verifica se la visualizzazione dei semi in simboli è attiva


Successivamente alla creazione del mazzo, quest'ultimo viene mescolato utilizzando la funzione "shuffle()" importata da "random"

Una volta completato, si passa alla creazione delle colonne.

Vengono create 13 colonne:
    0, 1, 2, 3, 4, 5, 6 COLONNE DI GIOCO
    7 MAZZO RISERVA PIENO
    8 MAZZO RISERVA VUOTO
    9, 10, 11, 12 MAZZI FINALI 

Le prime 28 carte verranno inserite nelle colonne di gioco, il restante nel mazzo di riserva pieno
Il mazzo riserva vuoto verrà utilizzato nella funzione Pesca(), descritta successivamente nel documento


Ora parte il gioco in sè
Verranno stampate le colonne attraverso Stampa_Colonne()

Stampa_Colonne() inizialmente pulisce lo schermo utilizzando la funzione ClearScreen()
Poi stampa tutte le colonne utilizzabili:
	CR (Colonna Riserva), CF (Colonna Finale), C (Colonna di gioco)

Ogni carta viene stampata seguendo la funzione dentro la print: colored() che viene fornita dalla dipendenza 'termcolor'
Se il valore colore è rosso allora stampa la carta con il colore red, definito all'inizio della funzione
Se il valore colore è nero, stamperà la carta di nero seguendo la stessa logica.

Attraverso le impostazioni c'è la possibilità di cambiare la VISUALIZZAZIONE dei SEMI
da TESTO a SIMBOLI, e di attivare i COLORI AD ALTO CONTRASTO. 

Se la carta non è scoperta allora sarà stampata al suo posto la scritta 'NASCOSTA'

A dividere ogni carta troviamo ' | ', che non verrà visualizzato dopo l'ultima carta.


Il programma ora attende un input del giocatore con la funzione getch_str()

getch_str() è una funzione creata per garantire una compatibilità cross-platform.

in cui legge un carattere da tastiera con la funzione getch()
getch() è importata dalla libreria 'msvcrt' se si è su Windows, se eseguiamo su Linux verrà utilizzata la libreria 'getch'

la funzione getch_str() ha il compito di decodificare il carattere dal formato bytes in stringa

Nel MainGame(), subito dopo l'input dell'utente il programma lo gestisce secondo i comandi definiti

Premendo '1' il giocatore avrà la possibilità di spostare le carte con la funzione Sposta()

La funzione Sposta() ha il compito di far scegliere all'utente una colonna di origine e una colonna di destinazione, 
nel caso che nella colonna d'origine ci sia più di una carta spostabile, il giocatore sceglierà da quale partire

La variabile 'x' è la colonna di origine, richiamerà la funzione GetSpostaInput() per ricevere la colonna scelta dall'utente

Nella funzione GetSpostaInput() ritroviamo subito la variabile LINE_CLEAR, è un ANSI Sequence che serve per pulire la linea
utilizzata insieme a end='\r' nella print che porterà il cursore all'inizio del rigo

GetSpostaInput() fa scegliere all'utente la colonna attraverso l'utilizzo delle FRECCETTE.
Per gestire l'input da tastiera dell'utente utilizzeremo get_input()

get_input() memorizza in una variabile x il tasto premuto,
successivamente utilizza la variabile is_Windows (definita all'inizio dello script) per capire su quale Sistema Operativo ci troviamo,
e utilizzerà il giusto metodo per ottenere il tasto premuto

get_input() ritornerà un valore stringa nel caso sia premuta una freccetta o invio,
in tutti gli altri casi ritorna direttamente la x, cioè il valore da tastiera.

Tornando in GetSpostaInput(), la variabile appena ottenuta verrà verificata, nel caso sia 'DOWN' (freccia in giù), diminuirà l'index
index è la colonna selezionata.
se index sarà 0 allora la riporterà a 13 facendo scegliere tutte le colonne continuamente.
Nel caso sia 8, lo imposterà direttamente a 6, poichè la colonna 7 è la colonna di riserva già riempita in cui l'utente non può accedervi.

la stessa logica viene utilizzata in caso la freccia premuta sia 'UP'

Se il tasto premuto è 'ENTER' confermerà la selezione.

Successivamente nella funzione ritroviamo i tasti rapidi:
Se il tasto premuto è 'F' o 'f' porterà l'index alla colonna desiderata
e così via con i tasti definiti nei comandi.

Una volta confermata la selezione, l'index verrà memorizzato nella variabile x di Sposta()

subito dopo c'è un check nel caso la x sia 13, in questo caso 13 non è una colonna ma è associato ad ANNULLA la selezione
ciò annulla il Sposta() e riportà il giocatore ai comandi inziali

Il removeIndex è la distanza dell'elemento dall'ultimo della lista
l'ultimo è -1, penultimo -2, e cosi via
Viene fatto un esempio più avanti nel documento

viene utilizzato per capire da quale elemento rimuovere nella lista,
-1 vuol dire che solo l'ultima carta sarà selezionata.

questo è il caso della Colonna di Riserva in cui è possibile prendere solo l'ultima carta pescata

altrimenti verrà fatto un check per capire quante carte siano spostabili,
verrà verificato controllando quante carte in quella colonna siano visibili
essendo spostabili solo le carte visibili

Se ritroviamo più di una carta allora il removeIndex viene definito dalla funzione Sposta_Colonna()

In Sposta_Colonna() crea una lista vuota chiamata 'spostabili'
In spostabili verranno aggiunte tutte le carte spostabili

Successivamente verrà chiesto all'utente di selezionare da quale carta partire
utilizzando la funzione get_input() e le FRECCE a SINISTRA o a DESTRA

Sposta_Colonna() calcolerà e ritornerà il removeIndex
il removeIndex è calcolato prendendo l'index della carta in spostabili, sottraendolo, alla lunghezza della lista spostabili

Facendo un esempio pratico:

una lista di elementi 0, 1, 2
selezionato l'elemento 2:
	index = 2
	len(selezionabili) = 3
	removeIndex = 2 - 3 = -1
	2 è l'ultimo elemento della lista
	-1 prenderà l'ultimo elemento della lista
selezionato l'elemento 0:
	index = 0
	len(selezionabili) = 3
	removeIndex = 0 - 3 = -3
	2 è il terz'ultimo elemento della lista

Questo removeIndex sarà restituito alla funzione Sposta()
altrimenti se ritroviamo una sola carta il removeIndex è impostato a -1

Successivamente verrà chiesta la colonna di destinazione

in cui verrà solo verificato se viene selezionato ANNULLA

una volta selezionate le colonne
il programma eseguirà un check per verificare che lo sposta sia conforme alle regole del gioco
attravero Check_Sposta()

Check_Sposta() ritornerà True se lo sposta è regolare, False se non lo è

Se è True, Sposta() effettuerà lo spostamento di carte
Prenderà tutti gli elementi dal removeIndex fino a -1
Per ogni carta aggiungerà alla colonna di destinazione la carta, e la rimuoverà dalla colonna di origine.

Se rimangono carte nella colonna di origine: scoprirà l'ultima carta


Terminato lo Sposta
L'altro comando disponibile è il Pesca()

Pesca() sposterà un elemento alla volta, dalla colonna 7 alla 8
Nel Stampa_Colonne() verrà visualizzato, se presente, solo l'ultimo elemento della colonna 8
Stessa logica per lo Sposta()

Se sono finite le carte nella colonna 7, ma sono presenti nella 8
Il programma copia tutti gli elementi dalla 8 alla 7
Cancella l'intera colonna 8
E rimescola la colonna 7

Gli altri comandi mostreranno le schermate di Regole, Comandi, Impostazioni ed Uscita.

Le impostazioni danno la possibilità all'utente
di cambiare la visualizzazione dei SEMI in TESTO o in SIMBOLI
e di attivare i COLORI AD ALTO CONTRASTO

La schermata di Uscita da' la possibilità all'utente di annullare, tornare al menu principale e terminare il programma

Il programma al termine di ogni Sposta o Pesca, verificherà attraverso la funzione Check_Win() la vittoria del gioco

Check_Win() semplicemente verificherà se in tutte le colonne finali saranno presenti 13 carte
Se sì vuol dire che tutte le carte sono state spostate correttamente e il gioco finisce.
