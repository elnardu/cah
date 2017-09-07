from PIL import Image
import os

side = 390
border = 7
name = 0

f = os.listdir('raw_blackcards_pages')

print(f)
for file in f:
	print(file)

	im = Image.open('raw_blackcards_pages/' + file)
	im_w, im_h = im.size

	up = 107
	left = 56

	for x in range(0,5):
		for y in range(0,4):
			buff = im.crop((left, up, left+side, up+side))
			buff.load()
			buff.save('raw_blackcards/card_'+str(name)+'.png', 'PNG')
			print("Card " + str(name) + " saved")
			left += side
			left += border
			name += 1
		up += side
		up += border
		left = 56