from pyzbar.pyzbar import decode
import cv2
import os

filename = input("Inserisci l'URL del file da scannerizzare: ")


def carica():
    soloNomeFile = os.path.basename(filename)
    print("Decodifico il file "+soloNomeFile)

    img = cv2.imread(filename)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    barcodes = decode(gray_img)
    if len(barcodes) == 1:
        print("BARCODE TROVATO: "+ barcodes[0].data.decode("utf-8"))
    else: 
        print("BARCODE NON TROVATO")
        #
