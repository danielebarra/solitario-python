from random import shuffle
import os
from termcolor import colored
import sys
is_Windows = sys.platform.startswith('win')

try:
    from msvcrt import getch
except ImportError:
    from getch import getch # type: ignore

def getch_str():
    c = getch()
    if isinstance(c, bytes):
        return c.decode(errors="ignore")
    return c

red = 'red'
black = (65, 105, 225)

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
        if seme in ["Cuore", "Diamante"]:
            self.colore = "rosso"
        else:
            self.colore = "nero"
        
        # Definisce se la carta è visibile o no
        self.scoperta = False
        
        
    def __repr__(self):
        return self.altvalore + " di " + self.seme


# Genera il mazzo di carte
def Generate_Deck():

    # Definisce i colori del mazzo di carte
    semi = ['Cuore', 'Diamante', 'Picche', 'Fiore']

    # Crea il mazzo di carte
    deck = [Carta(valore, seme) for valore in range (1, 14) for seme in semi]
    
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

    for i in range(7):
        for j in range(i + 1):
            deck[n].scoperta = (j == i)
            colonne[i].append(deck[n])
            n += 1
    
    for i in range (28, 52):
        colonne[7].append(deck[i])
        deck[i].scoperta = True
        
    return colonne


def Check_Win(colonne):
    for i in range(9, 13):
        n = 0

        for j in colonne[i]:
            n += 1

        if n != 13:
            return False
    return True


def Stampa_Colonne(colonne):
    os.system('cls||clear')

    print()
    print()

    print("Mazzo di Riserva: ")

    print("CR: ", end="")
    if len(colonne[8]) != 0:
        carta = colonne[8][0]
        if carta.colore == "rosso":
            print(colored(carta, red), end="")
        else:
            print(colored(carta, black), end="")
    
    print()
    print()
    print("Mazzi Finali:")
    
    for i in range(9, 13):
        print(f"CF{i - 8}: ", end="")
        if len(colonne[i]) == 0:
            print("VUOTA", end="")
        else:
            for j in range(len(colonne[i])):
                carta = colonne[i][j]

                if carta.colore == "rosso":
                    print(colored(carta, red), end="")
                else:
                    print(colored(carta, black), end="")

                if j < len(colonne[i]) - 1:
                    print(" | ", end="")
        print()
    
    print()
    print("Colonne di gioco:")
    
    for i in range(len(colonne) - 6):
        print("C", i + 1, ": ", sep="", end="")
        
        for j in range(len(colonne[i])):
            carta = colonne[i][j]
            if carta.scoperta:
                if carta.colore == "rosso":
                    print(colored(carta, red), end="")
                else:
                    print(colored(carta, black), end="")
            else:
                print("NASCOSTA", end="")

            if j < len(colonne[i]) - 1:
                print(" | ", end="")
                
        print("")


def Pesca(colonne):

    if len(colonne[7]) != 0:
        carta = colonne[7][0]
        colonne[8].insert(0, carta)
        del colonne[7][0]
    else:
        if len(colonne[8]) != 0:
            colonne[7].extend(colonne[8])
            colonne[8].clear()
            shuffle(colonne[7])

        
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
    
    if y >= 9 and y <= 12:
        if index != -1 and x != 8:
            seme_colonna = set()

            for i in colonne[x]:
                seme_colonna.add(i.seme)
            
            if len(seme_colonna) > 1:
                print("L'intera sequenza deve avere lo stesso seme")
                return False

        if len(colonne[y]) != 0:
            carta_y = colonne[y][-1]
            if carta_x.seme == carta_y.seme:
                if carta_x.valore == carta_y.valore + 1:
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


    if len(colonne[y]) != 0: 
        carta_y = colonne[y][-1]
    else:
        if carta_x.valore == 13:
            return True
        else:
            print("Puoi spostare solo i RE nelle caselle vuote")
            return False

    if carta_x.valore == carta_y.valore - 1:
        if carta_x.colore != carta_y.colore:
            return True
        else:
            print("Devi spostarla ad una col colore opposto")
    else:
        print("Devi spostarla ad una col valore immediatamente inferiore")
        
    return False
            
            
def get_input():
    x = getch_str()
    if is_Windows:
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
        if x == '\r':
            return 'ENTER'
    else:
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
        elif x == '\n':
            return 'ENTER'
    return x         
            

def Sposta_Colonna(colonna):
    spostabili = []

    for i in colonna:
        if i.scoperta:
            spostabili.append(i)
    
    print("Da quale carta vuoi iniziare a spostare? (FRECCE e INVIO per selezionare)")


    LINE_CLEAR = '\x1b[2K' # <-- ANSI sequence
    index = 0

    print(spostabili[index], end='\r')

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
            
        elif x == 'ENTER':
            print(end=LINE_CLEAR)
            break

    print(spostabili[index])
    
    removeIndex = index - len(spostabili)

    return removeIndex


def GetSpostaInput():
    
    LINE_CLEAR = '\x1b[2K' # <-- ANSI sequence
    index = 0

    print(selezionabili[index], end='\r')

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
            if x == 'ENTER':
                return index
            elif x in ['F', 'f']:
                index = 9
            elif x in ['R', 'r']:
                index = 8
            elif x in ['1','2','3','4','5','6','7']:
                index = int(x) - 1

        print(end=LINE_CLEAR)
        print(selezionabili[index], end='\r')
         

def Sposta(colonne):
    
    Stampa_Colonne(colonne)
    
    while True:
        print("\nChe colonna vuoi spostare?")

        x = GetSpostaInput()

        if x == 13:
            return None

        print("Hai scelto la colonna", selezionabili[x])

        if x == 8:
            removeIndex = 0 - len(colonne[8])
        else:
            j = 0
            for i in colonne[x]:
                if i.scoperta:
                    j += 1
                if j > 1:
                    removeIndex = Sposta_Colonna(colonne[x])
                    break
                else:
                    removeIndex = -1
        

        print("\nIn che colonna la vuoi spostare?")

        y = GetSpostaInput()

        if y == 13:
            return None
            
        print("Hai scelto la colonna", selezionabili[y], end="\n\n")


        if Check_Sposta(x, y, removeIndex, colonne):
            for i in range(removeIndex, 0):
                colonne[y].append(colonne[x][i])
                colonne[x].pop(i)

            if len(colonne[x]) != 0:
                    colonne[x][-1].scoperta = True
                    
            break 
              
                
def RegoleScreen():
    
    os.system('cls||clear')
    
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
    
    getch_str()



def ComandiScreen():
    
    os.system('cls||clear')
    
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
    print()
    print("Per pescare clicca il tasto '2'")
    print()
    print()
    print("Per visualizzare le regole del gioco clicca il tasto '3'")
    print()
    print()
    print("Per visualizzare di nuovo questa schermata clicca il tasto '4'")
    print()
    print()
    print("Per uscire dal gioco clicca il tasto '5'")
    print()
    print()
    print("Premi qualsiasi pulsante per tornare alla schermata principale: ")

    getch_str()



def VictoryScreen():
    
    os.system('cls||clear')
    
    print()
    print("COMPLIMENTI! HAI VINTO!")
    print()
    print()
    print("Grazie per aver giocato, vuoi fare un'altra partita?")
    print()
    print("\nComandi: 1: RIGIOCA, 2: ESCI")
    
    while True:
        x = getch_str()
        if x == '1':
            StartScreen()
        elif x == '2':
            exit()

 
def MainGame():
    deck = Generate_Deck()
    colonne = Crea_Colonne(deck)
    
    while True:
        if Check_Win(colonne):
            VictoryScreen()
            break
        
        Stampa_Colonne(colonne)
        
        print("\nComandi: 1: SPOSTA, 2: PESCA, 3: REGOLE, 4: COMANDI, 5: ESCI")
            
        x = getch_str()
        if x == '1':
            Sposta(colonne)
        elif x == '2':
            Pesca(colonne)
        elif x == '3':
            RegoleScreen()
        elif x == '4':
            ComandiScreen()
        elif x == '5':
            exit()
 
        
def StartScreen():
    
    while(True):  
        os.system('cls||clear')

        print()
        print("BENVENUTO A SOLITARIO!")

        print()
        print()

        print("Batti il gioco ordinando tutte le carte nelle colonne finali.")
        print("Se hai bisogno di aiuto per i comandi o per le regole del gioco")
        print()
        print("Clicca 2 per aprire la schermata delle regole")
        print("Clicca 3 per aprire la schermata dei comandi")

        print()
        print()
        print("Mi raccomando DIVERTITI! Buona fortuna.")


        print("\n\nComandi: 1: GIOCA, 2: REGOLE, 3: COMANDI, 4: ESCI")
    
    
        x = getch_str()
        if x == '1':
            MainGame()
            break
        elif x == '2':
            RegoleScreen()
        elif x == '3':
            ComandiScreen()
        elif x == '4':
            exit()
            

StartScreen()