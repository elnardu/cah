import requests, json, logging, random

logger = logging.getLogger(__name__)

token = 'ae89845120c3acf3c7377941b55e5b35bbd24093fadda655dffed67c2a1e65147d33d7d83cf8290a73686'

def searchMusic(query):
    req = "https://api.vk.com/method/audio.search"
    data = {
        'access_token': token,
        'q': query,
        'auto_complete': 1,
        'sort': 2,
        'count': 5,
        'v':'5.44'
       }
    resp = requests.get(req, params = data)
    data = resp.json()['response']['items']
    attachment = ''
    for song in data:
        string = 'audio' + str(song['owner_id']) + '_' + str(song['id']) + ','
        attachment = attachment + string
    return attachment


def searchVideo(query):
    req = "https://api.vk.com/method/video.search"
    data = {
        'access_token': token,
        'q': query,
        'adult': 1,
        'sort': 2,
        'count': 3,
        'v':'5.44'
       }
    resp = requests.get(req, params = data)
    data = resp.json()['response']['items']
    attachment = ''
    for song in data:
        string = 'video' + str(song['owner_id']) + '_' + str(song['id']) + ','
        attachment = attachment + string
    return attachment


def getRandomUserMusic(userId):
    req = "https://api.vk.com/method/audio.get"
    data = {
        'access_token': token,
        'owner_id': userId,
        'auto_complete': 1,
        'count': 400,
        'v':'5.44'
       }
    resp = requests.get(req, params = data)
    try:
        data = resp.json()['response']['items']
        data.pop(1)
        randomMusic = []
        attachment = ""
        for x in range(1,5):
            randomMusic.append(random.choice(data))
        for song in randomMusic:
            string = 'audio' + str(song['owner_id']) + '_' + str(song['id']) + ','
            attachment = attachment + string
        return attachment
    except KeyError:
        logger.warn('Access denied: Access to users audio is denied')
        return None


def sendImgToChat(chatId, location, text = None, forward = None, isChat = True):
    req = 'https://api.vk.com/method/photos.getMessagesUploadServer?v=5.50&access_token=' + token
    resp = requests.post(req)

    uploadUrl = resp.json()['response']['upload_url']
    img = [('photo', ('pic.jpg', open(location, 'rb')))]
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
        'Connection': 'keep-alive',
        'Accept': 'application/json'
        }

    resp1 = requests.post(uploadUrl, files=img, headers=headers)
    
    req2 = 'https://api.vk.com/method/photos.saveMessagesPhoto?v=5.50&access_token=' + token
    
    try:
        data = resp1.json()
    except ValueError:
        logger.warn(resp1.text) 
        logger.warn(resp1.headers)
        logger.warn(uploadUrl)    
        return
    resp2 = requests.get(req2, params = data)
    
    image = resp2.json()['response'][0]
    sendMessage(chatId, isChat, message = text, attachment = 'photo' + str(image['owner_id']) + '_' + str(image['id']), forward = forward)

    f = open(location, "w")
    f.write("Nothing")
    f.close()


def uploadImage(location):
    req = 'https://api.vk.com/method/photos.getMessagesUploadServer?v=5.50&access_token=' + token
    resp = requests.post(req)

    uploadUrl = resp.json()['response']['upload_url']
    img = [('photo', ('pic.png', open(location, 'rb')))]

    resp1 = requests.post(uploadUrl, files=img)
    
    req2 = 'https://api.vk.com/method/photos.saveMessagesPhoto?v=5.50&access_token=' + token
    
    try:
        data = resp1.json()
    except ValueError:
        logger.warn(resp1.text) 
        logger.warn(resp1.headers)
        logger.warn(uploadUrl)    
        return
    resp2 = requests.get(req2, params = data)
    
    image = resp2.json()['response'][0]

    return  'photo' + str(image['owner_id']) + '_' + str(image['id'])



def getUser(userId):
    req = "https://api.vk.com/method/users.get"
    data = {
        'user_ids': userId,
        'v':'5.42'
       }
    resp = requests.get(req, params = data)
    data = resp.json()['response'][0]
    array = [data['first_name'], data['last_name'], {}, {}]
    return array


def searchUsers():
    req = "https://api.vk.com/method/users.search"
    data = {
        'access_token': token,
        'city': 204,
        'age_from': 0,
        'age_to': 20,
        'sort': 0,
        'status': 6,
        'fields': 'screen_name,can_write_private_message,online,followers_count',
        'count': 300,
        'v':'5.44'
       }
    resp = requests.get(req, params = data)
    
    data = resp.json()['response']['items']
    
    i = 0
    for x in range(0, len(data) - 1):
        if data[i]['can_write_private_message'] == 0 or data[i]['online'] == 0 or data[i]['followers_count'] > 300:
            data.pop(i)
        else:
            i = i + 1

    return data


def getMessages(count = None, lastMessageId = None):
    req = "https://api.vk.com/method/messages.get"
    data = {
        'access_token': token,
        'last_message_id': lastMessageId,
        'count': count,
        'v':'5.44'
       }
    try:
        resp = requests.get(req, params = data)
        messages = resp.json()['response']['items']
        return messages
    except requests.exceptions.ConnectionError:
        logger.error('Connection error')
        return None
    except ValueError:
        logger.warn('Decoding JSON has failed')
        logger.warn(resp.text)
    except Exception as e:
        logger.error('Error: ' + str(e))
        logger.error(resp.text)


def sendMessage(chatId, isChat, message = None, forward = None, attachment = None, lat = None, long = None):
    req = "https://api.vk.com/method/messages.send"
    if isChat:
        data = {
            'access_token': token,
            'chat_id': chatId,
            'v':'5.42',
            'forward_messages': forward,
            'message': message,
            'attachment': attachment,
            'lat': lat,
            'long': long
           }
    else:
        data = {
            'access_token': token,
            'user_id': chatId,
            'v':'5.42',
            'forward_messages': forward,
            'message': message,
            'attachment': attachment,
            'lat': lat,
            'long': long
           }
    resp = requests.get(req, params = data)
    # print(resp.text)
    # print(resp.status_code)
    # if message:
    #     sendDataToFrontend("Milena", message, "text-success")


def setOnline():
    req = "https://api.vk.com/method/account.setOnline"
    data = {
        'access_token': token,
        'v':'5.50'
       }
    resp = requests.get(req, params = data)


def setOffline():
    req = "https://api.vk.com/method/account.setOffline"
    data = {
        'access_token': token,
        'v':'5.50'
       }
    resp = requests.get(req, params = data)
    vkapi.sendMessage(1, True, "Мила оффлайн.")