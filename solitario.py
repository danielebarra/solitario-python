from random import shuffle
import os
from termcolor import colored
import sys
is_Windows = sys.platform.startswith('win')     # Verifica se il sistema operativo è WINDOWS

try:
    from msvcrt import getch    # Windows
except ImportError:
    from getch import getch     # type: ignore | Linux


def getch_str():
    # Legge un carattere dalla tastiera
    c = getch()
    # Se il carattere è in formato bytes (tipico su Windows), decodifica in stringa
    if isinstance(c, bytes):
        return c.decode(errors="ignore")
    # Altrimenti restituisce direttamente la stringa
    return c

# OPTIONS
isSimboliSelected = True
isHighContrast = False


selezionabili = {
        0: "C1",
        1: "C2",
        2: "C3",
        3: "C4",
        4: "C5",
        5: "C6",
        6: "C7",
        8: "CR",
        9: "CF1",
        10: "CF2",
        11: "CF3",
        12: "CF4",
        13: "ANNULLA"
    }



# Classe di Carta definisce come è composta ogni carta
class Carta:
    def __init__(self, valore, seme):
        # Valore della carta
        self.valore = valore
        
        # AltValore è un valore alternativo con uno scopo visivo, per rendere all'utente la visualizzazione della carta secondo le figure
        valori_speciali = {1: "A", 11: "J", 12: "Q", 13: "K"}
        self.altvalore = valori_speciali.get(self.valore, str(self.valore))
        
        # Seme della carta
        self.seme = seme
        
        # Colore della carta
        if seme in ["Cuori", "Diamanti"]:
            self.colore = "rosso"
        else:
            self.colore = "nero"
        
        # Definisce se la carta è visibile al giocatore o no
        self.scoperta = False
        
        # Imposta il simbolo della carta
        simboli = {"Cuori": "♥", "Diamanti": "♦", "Picche": "♠", "Fiori": "♣"}
        self.simbolo = simboli.get(self.seme, str(self.seme))
        
        
    def __repr__(self):
        if isSimboliSelected:
            return self.altvalore + " " + self.simbolo
        return self.altvalore + " di " + self.seme


# Genera il mazzo di carte
def Generate_Deck():

    # Definisce i colori del mazzo di carte
    semi = ['Cuori', 'Diamanti', 'Picche', 'Fiori']

    # Crea il mazzo di carte
    deck = [Carta(valore, seme) for valore in range (1, 14) for seme in semi]
    
    # Mescola il mazzo
    Shuffle_Deck(deck)
    
    return deck

# Mescola il mazzo di carte
def Shuffle_Deck(deck):
    
    shuffle(deck)
    
    return deck

# Genera le colonne di gioco
def Crea_Colonne(deck):
    colonne = [[] for _ in range(13)] 

    # 0, 1, 2, 3, 4, 5, 6 COLONNE DI GIOCO
    # 7 MAZZO RISERVA PIENO
    # 8 MAZZO RISERVA VUOTO
    # 9, 10, 11, 12 MAZZI FINALI 

    n = 0

    # CREA LE 7 COLONNE DI GIOCO
    for i in range(7):
        for j in range(i + 1):
            deck[n].scoperta = (j == i)
            colonne[i].append(deck[n])
            n += 1
    
    # CREA IL MAZZO DI RISERVA
    for i in range (28, 52):
        colonne[7].append(deck[i])
        deck[i].scoperta = True
        
    return colonne

# Controlla la vittoria del giocatore
def Check_Win(colonne):
    
    # Se in tutte le colonne finali sono presenti 13 carte allora il giocatore ha vinto
    for i in range(9, 13):
        n = 0

        for j in colonne[i]:
            n += 1

        if n != 13:
            return False
    return True

# Pulisce lo schermo, in base al Sistema Operativo
def ClearScreen():
    if os.name == 'nt':  # Windows
        os.system('cls')
    else:  # Linux/Mac
        os.system('clear')

# Mostra tutte le colonne a schermo
def Stampa_Colonne(colonne):
    
    # Gestisce i colori delle carte
    if isHighContrast:
        red = (255, 102, 102)
        black = (111, 158, 251)
    else:
        red = "red"
        black = (65, 105, 225)
    
    
    ClearScreen()

    print()
    print()

    print("Mazzo di Riserva: ")

    print("CR: ", end="")
    if len(colonne[8]) != 0:
        carta = colonne[8][-1]                          # Prende l'ultimo elemento della colonna di Pesca
        if carta.colore == "rosso":                     
            print(colored(carta, red), end="")          # Se la carta è rossa allora stampa in un colore "red" già definito
        else:
            print(colored(carta, black), end="")        # Se la carta è nera stampa in un colore "black" già definito
    
    print()
    print()
    print("Mazzi Finali:")
    
    for i in range(9, 13):
        print(f"CF{i - 8}: ", end="")
        if len(colonne[i]) == 0:
            print("VUOTA", end="")                          # print VUOTA se la colonna è vuota
        else:
            for j in range(len(colonne[i])):
                carta = colonne[i][j]

                if carta.colore == "rosso":
                    print(colored(carta, red), end="")
                else:
                    print(colored(carta, black), end="")

                if j < len(colonne[i]) - 1:             
                    print(" | ", end="")                    # Stampa " | " tra le carte, se è l'ultima carta allora non lo stampa
        print()
    
    print()
    print("Colonne di gioco:")

    # Stampa le colonne di gioco
    for i in range(len(colonne) - 6):
        print("C", i + 1, ": ", sep="", end="")
        
        for j in range(len(colonne[i])):
            carta = colonne[i][j]
            if carta.scoperta:                                  # Se la carta è scoperta allora la stampa
                if carta.colore == "rosso":
                    print(colored(carta, red), end="")
                else:
                    print(colored(carta, black), end="")
            else:
                print("NASCOSTA", end="")                       # Se la carta è coperta stampa NASCOSTA

            if j < len(colonne[i]) - 1:
                print(" | ", end="")
                
        print("")

# Funzione Pesca tra le carte, colonne 7 (riempita all'inizio) e 8 (da riempire)
def Pesca(colonne):

    # Sposta la carta dall'inizio della colonna 7, alla fine della 8
    if len(colonne[7]) != 0:
        carta = colonne[7][0]
        colonne[8].append(carta)
        del colonne[7][0]
    else:
        # Se sono finite le carte nella colonna 7
        if len(colonne[8]) != 0:
            colonne[7].extend(colonne[8])           # Copia l'intera lista della colonna 8 nella 7
            colonne[8].clear()                      # Cancella la colonna 8
            shuffle(colonne[7])                     # Mescola la colonna 7


# Controlla se lo sposta è valido, secondo le regole del gioco
def Check_Sposta(x, y, index, colonne):
    if x == y:
        print("Non puoi muovere nella STESSA colonna")
        return False
    
    if y == 8:
        print("Non puoi muovere all'interno del mazzo di RISERVA")
        return False
    
    if len(colonne[x]) == 0:
        print("Non puoi muovere da una colonna VUOTA")
        return False


    carta_x = colonne[x][index]
    
    # Se la destinazione è una colonna finale
    if y >= 9 and y <= 12:
        
        # Controlla che, se spostato un gruppo di carte, tutte le carte siano dello stesso seme
        if index != -1 and x != 8:
            seme_colonna = set()

            for i in colonne[x]:
                seme_colonna.add(i.seme)
            
            if len(seme_colonna) > 1:
                print("L'intera sequenza deve avere lo stesso seme")
                return False

        # Controlla se la carta può essere spostata in una colonna finale
        if len(colonne[y]) != 0:
            carta_y = colonne[y][-1]
            if carta_x.seme == carta_y.seme:                          # Se le carte hanno lo stesso seme
                if carta_x.valore == carta_y.valore + 1:              # Se la carta da spostare è immediatamente superiore alla carta di destinazione
                    return True
                else:
                    print("Puoi aggiungere solo il valore immediatamente superiore della carta presente")
                    return False
            else:
                print("Devi aggiungere una carta dello stesso seme")
                return False
        else:
            if carta_x.valore == 1:
                return True
            else:
                print("Devi inziare dall'ASSO")
                return False

    # Controlla se una carta può essere spostata in una colonna di gioco
    if len(colonne[y]) != 0: 
        carta_y = colonne[y][-1]
    else:
        # Se la colonna è vuota, può essere spostato solo il RE (carta con valore 13)
        if carta_x.valore == 13:
            return True
        else:
            print("Puoi spostare solo i RE nelle caselle vuote")
            return False

    # Se la carta da spostare è immediatamente inferiore alla carta di destinazione
    if carta_x.valore == carta_y.valore - 1:
        # Se le carte hanno colore opposto
        if carta_x.colore != carta_y.colore:
            return True
        else:
            print("Devi spostarla ad una col colore opposto")
    else:
        print("Devi spostarla ad una col valore immediatamente inferiore")
        
    return False
            
# Gestisce l'input da tastiera
def get_input():
    x = getch_str()
    
    # Se l'OS è Windows
    if is_Windows:
        # Gestisce l'inserimento delle freccette
        if x == '':
            x = getch_str()
            if x == 'H':
                return 'UP'
            elif x == 'P':
                return 'DOWN'
            elif x == 'K':
                return 'LEFT'
            elif x == 'M':
                return 'RIGHT'
        # Gestisce l'inserimento di INVIO
        if x == '\r':
            return 'ENTER'
    else: 
        # Se l'OS è Linux
        # Gestisce l'inserimento delle freccette
        if x == '\x1b':
            x = getch_str()
            if x == '[':
                x = getch_str()
                if x == 'A':
                    return 'UP'
                elif x == 'B':
                    return 'DOWN'
                elif x == 'C':
                    return 'RIGHT'
                elif x == 'D':
                    return 'LEFT'
        # Gestisce l'inserimento di INVIO
        elif x == '\n':
            return 'ENTER'
        
    # Ritorna ogni altro valore inserito da tastiera
    return x         
            
# Gestisce lo spostamento di più carte contemporaneamente
def Sposta_Colonna(colonna):
    spostabili = []

    # Definisce che le carte sono spostabili quando sono scoperte
    for i in colonna:
        if i.scoperta:
            spostabili.append(i)
    
    print("Da quale carta vuoi iniziare a spostare? (FRECCE e INVIO per selezionare)")


    LINE_CLEAR = '\x1b[2K' # ANSI Sequence per pulire la linea
    index = 0

    print(spostabili[index], end='\r')

    # Scorre tra le carte selezionabili
    while True:
        x = get_input()
        
        if x == 'LEFT':
            if index == 0:
                index = len(spostabili) - 1
            else:
                index -= 1
            print(end=LINE_CLEAR)
            print(spostabili[index], end='\r')
            
        elif x == 'RIGHT':
            if index == len(spostabili) - 1:
                index = 0
            else:
                index += 1
            print(end=LINE_CLEAR)
            print(spostabili[index], end='\r')
        
        # Conferma la selezione
        elif x == 'ENTER':
            print(end=LINE_CLEAR)
            break

    print(spostabili[index])
    
    # Il removeIndex è la distanza dell'elemento dall'ultimo della lista
    # L'ultimo è -1, penultimo -2, e cosi via
    
    removeIndex = index - len(spostabili)

    return removeIndex

# Gestisce la selezione delle colonne
def GetSpostaInput():
    
    LINE_CLEAR = '\x1b[2K' # ANSI Sequence per pulire la linea
    index = 0

    print(selezionabili[index], end='\r')

    # Scorre attraverso le FRECCETTE o secondo delle SCORCIATOIE
    while True:
        x = get_input()
        
        if x == 'DOWN':
            if index == 0:
                index = 13
            elif index == 8:
                index = 6
            else:
                index -= 1
        elif x == 'UP':
            if index == 13:
                index = 0
            elif index == 6:
                index = 8
            else:
                index += 1
        else:
            # Conferma Selezione
            if x == 'ENTER':
                return index
            # CF1
            elif x in ['F', 'f']:
                index = 9
            # CR
            elif x in ['R', 'r']:
                index = 8
            # C1 - ... - C7
            elif x in ['1','2','3','4','5','6','7']:
                index = int(x) - 1

        print(end=LINE_CLEAR)
        print(selezionabili[index], end='\r')
         
# Gestisce lo spostamento tra le colonne
def Sposta(colonne):
    
    Stampa_Colonne(colonne)
    
    # Chiede all'utente di selezionare colonna di origine e di destinazione
    while True:
        print("\nChe colonna vuoi spostare?")

        # Colonna di origine
        x = GetSpostaInput()

        # 13 è ANNULLA
        if x == 13:
            return None

        print("Hai scelto la colonna", selezionabili[x])

        # Se è CR allora prende l'ultimo elemento della colonna
        if x == 8:
            removeIndex = -1
        else:
            j = 0
            
            for i in colonne[x]:
                # Conta quante carte spostabili ci sono
                if i.scoperta:
                    j += 1
                    
                # Se c'è più di una carta, chiama Sposta_Colonna per gestirlo
                if j > 1:
                    removeIndex = Sposta_Colonna(colonne[x])
                    break
                
                # Altrimenti se c'è solo una carta prende l'ultimo e unico elemento (che è anche il primo essendo l'unico)
                else:
                    removeIndex = -1
        

        print("\nIn che colonna la vuoi spostare?")

        # Colonna di destinazione
        y = GetSpostaInput()

        # 13 è ANNULLA
        if y == 13:
            return None
            
        print("Hai scelto la colonna", selezionabili[y], end="\n\n")


        if Check_Sposta(x, y, removeIndex, colonne):    # Chiama Check_Sposta, se è TRUE esegue lo sposta
            
            # Dall'elemento selezionato secondo il removeIndex fino all'ultimo (-1) 
            for i in range(removeIndex, 0):
                colonne[y].append(colonne[x][i])        # Aggiunge la carta nella colonna di destinazione
                colonne[x].pop(i)                       # La rimuove da quella di origine

            # Se dopo lo sposta rimangono carte nella colonna di origine
            if len(colonne[x]) != 0:
                    colonne[x][-1].scoperta = True      # Scopre l'ultima carta
                    
            break 
              
# La schermata delle Regole
def RegoleScreen():
    
    ClearScreen()
    
    print()
    print("Ecco le REGOLE DEL GIOCO:")
    print()
    print("Si gioca con un mazzo standard di 52 carte")
    print()
    print("Vengono create 7 colonne, la prima con una carta, la seconda con due, e così via")
    print("con l'ultima carta di ogni colonna scoperta e le altre coperte")
    print("Il resto delle carte va nella COLONNA DI RISERVA, in cui è possibile pescare senza limiti")
    print()
    print("Lo scopo del gioco è inserire in ordine tutte le carte nelle COLONNE FINALI")
    print("Dall'ASSO fino al RE, ogni colonna finale può contenere solo un SEME")
    print()
    print("ATTENZIONE!")
    print("Puoi spostare solo le carte che sono in ordine DECRESCENTE")
    print("e devono essere posizionate in colori alternati")
    print()
    print("Nelle colonne vuote puoi spostare solo i RE")
    print()
    print("Quando sposti l'ultima carta scoperta da una colonna, quella sottostante viene rivelata")
    print()
    print("Una volta posizionate tutte le carte nelle COLONNE FINALI, apparirà la schermata di VITTORIA!")
    print()
    print()
    print("Premi qualsiasi pulsante per tornare alla schermata principale: ")
    
    # Aspetta che l'utente prema qualsiasi pulsante
    getch_str()


# La schermata dei Comandi
def ComandiScreen():
    
    ClearScreen()
    
    print()
    print("Ecco i COMANDI DI GIOCO:")
    print()
    print()
    print("Per spostare una carta clicca il tasto '1'")
    print()
    print("Successivamente ti verrà chiesto di selezionare una colonna")
    print("Puoi selezionarla usando FRECCIA IN SU oppure FRECCIA IN GIU'")
    print()
    print("Per velocizzare la selezione puoi usare anche i tasti rapidi:")
    print("I TASTI da 1-7 selezioneranno le COLONNE da 1-7")
    print("Il tasto 'R' selezionerà la COLONNA DI RISERVA")
    print("Il tasto 'F' selezionerà la COLONNA FINALE 1")
    print()
    print("Se nella colonna selezionata c'è più di una carta spostabile")
    print("Puoi selezionare la carta di partenza utilizzando FRECCIA A DESTRA e FRECCIA A SINISTRA")
    print()
    print("Per confermare la selezione premi INVIO")
    print()
    print()
    print("Per pescare clicca il tasto '2'")
    print()
    print("Per visualizzare le regole del gioco clicca il tasto '3'")
    print()
    print("Per visualizzare di nuovo questa schermata clicca il tasto '4'")
    print()
    print("Per cambiare le impostazioni clicca il tasto '5'")
    print()
    print("Per uscire dal gioco clicca il tasto '6'")
    print()
    print()
    print("Premi qualsiasi pulsante per tornare alla schermata principale: ")

    # Aspetta che l'utente prema qualsiasi pulsante
    getch_str()

# Schermata d'uscita
def ExitScreen():
    
    ClearScreen()
    
    print()
    print("Sei sicuro di voler uscire?")
    print()
    print()
    print("\nComandi: 1: ANNULLA, 2: TORNA AL MENU, 3: ESCI")
    
    # Gestisce l'input dell'utente
    while True:
        x = getch_str()
        if x == '1':            # Se '1' annulla l'uscita dal gioco
            return False      
        elif x == '2':          # Se '2' torna al menu principale
            return True
        elif x == '3':          # Se '3' termina il programma
            exit()

# La schermata di Vittoria
def VictoryScreen():
    
    ClearScreen()
    
    print()
    print("COMPLIMENTI! HAI VINTO!")
    print()
    print()
    print("Grazie per aver giocato, vuoi fare un'altra partita?")
    print()
    print("\nComandi: 1: RIGIOCA, 2: ESCI")
    
    # Gestisce l'input dell'utente
    while True:
        x = getch_str()
        if x == '1':            # Se '1' allora ricomincia il gioco
            StartScreen()      
        elif x == '2':          # Se '2' termina il programma
            exit()

# Schermata delle impostazioni
def OptionsScreen():
    global isSimboliSelected, isHighContrast
    
    while True:
        ClearScreen()
        
        print()
        print("Qui puoi cambiare le impostazioni di gioco")
        print()
        print("Premi il numero affianco all'impostazione per cambiarla")
        print()
        print()
        print(f"1: Mostra simboli carte: {"ATTIVO" if isSimboliSelected else "DISATTIVO"}")
        print(f"2: Attiva Colori ad Alto Contrasto: {"ATTIVO" if isHighContrast else "DISATTIVO"}")
        print()
        print()
        print("Premi ENTER per tornare indietro")
        
        # Gestisce l'input dell'utente
        x = get_input()
        if x == '1':            # Se '1' cambia l'impostazione dei simboli
            isSimboliSelected = not isSimboliSelected      
        elif x == '2':          # Se '2' cambia l'impostazione del contrasto
            isHighContrast = not isHighContrast
        elif x == 'ENTER':          # Se 'ENTER' torna indietro
            break

# Gestisce le funzioni principali
def MainGame():
    deck = Generate_Deck()              # Crea un mazzo
    colonne = Crea_Colonne(deck)        # Crea le colonne dal mazzo appena creato
    
    while True:
        if Check_Win(colonne):          # Se Check_Win ritorna True allora mostra la schermata di vittoria
            VictoryScreen()
            break
        
        Stampa_Colonne(colonne)         # Stampa tutte le colonne di gioco
        
        print("\nComandi: 1: SPOSTA, 2: PESCA, 3: REGOLE, 4: COMANDI, 5: IMPOSTAZIONI, 6: ESCI")
        
        
        x = getch_str()                 # Gestisce l'input dell'utente
        if x == '1':                    # Se '1' allora Sposta
            Sposta(colonne)
        elif x == '2':                  # Se '2' allora Pesca
            Pesca(colonne)
        elif x == '3':                  # Se '3' mostra le regole
            RegoleScreen()
        elif x == '4':                  # Se '4' mostra i comandi
            ComandiScreen()
        elif x == '5':                  # Se '5' mostra le impostazioni
            OptionsScreen()
        elif x == '6':                  # Se '6' termina il programma
            if ExitScreen():
                StartScreen()
                break
            
            
 
# Schermata iniziale
def StartScreen():
    
    while(True):  
        ClearScreen()

        print()
        print("BENVENUTO A SOLITARIO!")

        print()
        print()

        print("Batti il gioco ordinando tutte le carte nelle colonne finali.")
        print("Se hai bisogno di aiuto per i comandi o per le regole del gioco")
        print()
        print("Clicca 2 per aprire la schermata delle regole")
        print("Clicca 3 per aprire la schermata dei comandi")
        print("Clicca 4 per aprire le impostazioni")
        print()
        print("Potrai cambiare la VISUALIZZAZIONE dei SEMI in SIMBOLI o TESTO")
        print("E potrai attivare i COLORI AD ALTO CONTRASTO")
        print()
        print()
        print("Per una migliore esperienza di gioco, ti consiglio di ingrandire il terminale a tutto schermo.")
        print()
        print("Mi raccomando DIVERTITI! Buona fortuna.")


        print("\n\nComandi: 1: GIOCA, 2: REGOLE, 3: COMANDI, 4: IMPOSTAZIONI, 5: ESCI")
    
    
        x = getch_str()             # Gestisce l'input dell'utente
        if x == '1':                # Se '1' avvia il gioco
            MainGame()
            break
        elif x == '2':              # Se '2' mostra le regole
            RegoleScreen()
        elif x == '3':              # Se '3' mostra i comandi
            ComandiScreen()
        elif x == '4':              # Se '4' mostra le impostazioni
            OptionsScreen()
        elif x == '5':              # Se '5' termina il programma
            exit()
     
            
# Mostra la schermata iniziale all'avvio del programma
StartScreen()