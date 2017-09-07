import vkapi
import os, json, logging, time

logger = logging.getLogger(__name__)
import coloredlogs
coloredlogs.DEFAULT_LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
# coloredlogs.install(level="DEBUG")
coloredlogs.install()
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

white_cards = {}

f = open("white_cards.json", "r")
white_cards = json.loads(f.read())
f.close()

f = os.listdir('raw_whitecards')

def main():
	for image in f:
		if white_cards.get(image):
			logger.info('Skipping '+image)
			continue
		logger.info('Uploading image ' + image)
		path = 'raw_whitecards/' + image
		a = vkapi.uploadImage(path)
		logger.info('Image uploaded')
		vkapi.sendMessage(111543942, False, attachment = a)
		white_cards[image] = a
		time.sleep(1)


try:
    if __name__ == '__main__':
        main()
except KeyboardInterrupt:
	f = open("white_cards.json", "w")
	f.write(json.dumps(white_cards))
	f.close()

