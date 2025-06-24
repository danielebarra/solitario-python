import msvcrt

while True:
    x = msvcrt.getch()

    if x == b'\xe0':
        x = msvcrt.getch()

        if x == b'H':   # Freccette in alto
            print("Sopra")
        elif x == b'P': # Freccette in basso
            print("Sotto")