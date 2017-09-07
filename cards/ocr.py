import os, json
from PIL import Image
import pytesseract

f = os.listdir('blackcards')
list = []
for i in f:
	im = Image.open('blackcards/'+i)
	im = im.crop((0, 0, 390, 325))
	im.load()
	a = pytesseract.image_to_string(im, lang='rus+eng')
	print(a)
	list.append(a)



f = open("black_cards.json", "w")
f.write(json.dumps(list))
f.close()
