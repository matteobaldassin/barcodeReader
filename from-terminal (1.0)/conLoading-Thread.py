from pyzbar.pyzbar import decode
import cv2
import os
import itertools
import threading
import time
import sys

filename=""
def carica():
    soloNomeFile = os.path.basename(filename)
    print("Decodifico il file "+soloNomeFile)
    img = cv2.imread(filename)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray_img)
    if len(barcodes) == 1:
        print("BARCODE TROVATO: " + barcodes[0].data.decode("utf-8"))
    else:
        print("BARCODE NON TROVATO")


def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)

print("BENVENUTO NEL SISTEMA DI DECODIFICA")
print("Inserisci [0] per uscire, oppure")

while(filename!="0"):

    filename = input("Inserisci l'URL del file da scannerizzare: ")

    t = threading.Thread(name="carica e decripta file", target=carica)
    t.start()

    while t.isAlive():
        animate()

##ERRORE: continua a loopare anche dopo aver trovato il file
        


