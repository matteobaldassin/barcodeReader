from flask import Flask, jsonify
from pyzbar.pyzbar import decode
import cv2
import numpy as np
import urllib.request
import os
app = Flask(__name__)

@app.route('/')
def comandi():
    comandi = "/getbarcode/<string:image> --> prende file da http://jmbooks.altervista.org/ISBNReader/barcodes/ + imageURL, scarica - decripta - ritorna ISBN <br>"
    comandi += "/getbarcode/decode/<string:image> --> prende file da cartella locale /barcodes/ + imageURL, decripta - ritorna ISBN"
    return comandi

@app.route('/getbarcode/<string:image>', methods=['GET'])
def get_from_barcode(image):
    urlDestinazione = "barcodes/"+image
    urllib.request.urlretrieve(
        "http://jmbooks.altervista.org/ISBNReader/barcodes/"+image, urlDestinazione)

    print("---- getting image from: " +
          "http://jmbooks.altervista.org/ISBNReader/barcodes/"+image)
    print("image placed in: "+urlDestinazione)
    
    img = cv2.imread(urlDestinazione)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray_img)
    #return jsonify({"result": "ciao"})
    #return jsonify({"barcodeLetto": barcodes[0].data})
    if len(barcodes) == 1:
        barcodeLetto = barcodes[0].data.decode("utf-8")
        return jsonify({"return": barcodeLetto})
    else:
        return jsonify({"error": "Barcode non trovato o letto erroneamente"})
    
    os.remove(urlDestinazione)



@app.route('/getbarcode/decode/<string:image>', methods=['GET'])
def get_from_barcode_decode(image):
    img = cv2.imread("barcodes/"+image)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    barcodes = decode(gray_img)
    #return jsonify({"result": "ciao"})
    #return jsonify({"barcodeLetto": barcodes[0].data})
    if len(barcodes) == 1:
        barcodeLetto = barcodes[0].data.decode("utf-8")
        return jsonify({"return": barcodeLetto})
    else:
        return jsonify({"error": "Barcode non trovato o letto erroneamente"})
    

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80) #per runnare su webservice lasciare solo ()
