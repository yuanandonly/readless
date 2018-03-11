#!/usr/bin/env python3
import requests
import json

import cgi
import cgitb
import sys
from googletrans import Translator 
from matplotlib.patches import Rectangle
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

def main(arg=None):
    output = 'output'
    subscription_key = "b93fdefa52ba49d48a0efb7b89efd4e3" 
    vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v1.0/"
    image_url = arg if arg and len(arg) > 2 else "http://braziliangringo.com/wp-content/uploads/2015/05/caminho.png" 
    headers  = {'Ocp-Apim-Subscription-Key': subscription_key }
    params   = {'language' : 'unk'} #{'visualFeatures': 'Categories,Description,Color', 'language' : 'unk', 'detectOrientation' : 'true', 'handwriting' : True}
    data     = {'url': image_url}

    ocr_url = vision_base_url + "ocr"
    text_url = vision_base_url + "RecognizeText"
    response = requests.post(ocr_url, headers=headers, params=params, json=data)
    response.raise_for_status()
    analysis = response.json()
    line_infos = [region["lines"] for region in analysis["regions"]]
    word_infos = []
    for line in line_infos:
        for word_metadata in line:
            for word_info in word_metadata["words"]:
                word_infos.append(word_info)
#word_infos
    plt.figure(figsize=(5,5))
    image  = Image.open(BytesIO(requests.get(image_url).content))
    ax     = plt.imshow(image, alpha=0.5)
    hah = ""
    for word in word_infos:
        bbox = [int(num) for num in word["boundingBox"].split(",")]
        text = word["text"]
        if text == "11m":
            text = "I'm"
        hah += text.strip() + ' '
        if len(hah) > 5 and hah[-2] == '.' and hah[-3].lower() in "qwertyuiopasdfghjklzxcvbnm":
            hah += '\n'
    #translator = Translator()
    #finaltext = translator.translate(hah, dest='en').text
    print(hah)

    """
    print("Content-Type: text/html")
    print()
    print("<HTML> <body>")
    print("<title>Output</title>")
    print("<h1>Text</h1>")
    print('<p>'+finaltext.strip()+'</p>')
    print("</body> </HTML>")
    """
if __name__ == "__main__":
    main(sys.argv[1])
