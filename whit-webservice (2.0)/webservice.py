from flask import Flask, jsonify
from pyzbar.pyzbar import decode
import cv2
import numpy as np
import urllib.request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({"about": "Hello, world"})

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
@app.route('/getbarcode/openwebcam', methods=['GET'])
def open_webcam():
    cap = cv2.VideoCapture(0)
 
# Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
#out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
    count=0
    while(cap.isOpened()):
 
        ret, frame = cap.read()
        if ret==True:
            count +=1
        #frame = cv2.flip(frame,0)
        # write the flipped frame
            cv2.imshow('frame webcam',frame)
            gray_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
       # out.write(frame)
            barcodes = decode(gray_img)
            if len(barcodes) ==1:
                barcodeLetto=barcodes[0].data.decode("utf-8")
                print("trovato: "+barcodeLetto)
                return "trovato"
                break
            else:
                print("Codice non trovato")

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
 
    # Release everything if job is finished
    cap.release()
    #out.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
