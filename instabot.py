import time
import urllib.request as req
from InstagramAPI import InstagramAPI
from Instahandler import get_image_path
from image_access import image_aspect_change

print("Starting")
InstagramAPI = InstagramAPI('culver_loons','jibneh82')
InstagramAPI.login()
my_id = InstagramAPI.username_id


def post_image(item_id,pic_info,posted_list,notseen_file):
    gate2 = pic_info['item_type']
    if item_id not in posted_list:
        notseen_file.write(item_id+'\n')
        if gate2 == 'media':
            photo_url = pic_info['media']['image_versions2']['candidates'][0]['url']
            image_handle(photo_url,"image_name.jpg")
        if gate2 == 'raven_media':
            photo_url = pic_info['visual_media']['media']['image_versions2']['candidates'][0]['url']
            image_handle(photo_url,"image_name.jpg")
        if gate2 == 'media_share':
            print('In Media Share Gate')
            try:
                photo_url = pic_info['direct_media_share']['media']['image_versions2']['candidates'][0]['url']
                print('try',photo_url)
                image_handle(photo_url,"image_name.jpg")
            except:
                photo_url = pic_info['media_share']['image_versions2']['candidates'][0]['url']
                print('except',photo_url)
                image_handle(photo_url,"image_name.jpg")


def inbox():
    '''Goes through messages and posts photos'''
    def image_handle(photo_url, photo):
        '''nested helper function for image resizing and posting'''
        req.urlretrieve(photo_url, photo)
        image_aspect_change(photo)
        InstagramAPI.uploadPhoto(photo)
        time.sleep(5)

    seen_file = open('seenit.txt','r+')
    InstagramAPI.getv2Inbox()
    num_messages = InstagramAPI.LastJson['inbox']['threads']
    threads_to_check = [thread['thread_id'] for thread in num_messages]
    posted_list = [line.replace('\n','') for line in seen_file.readlines()]
    seen_file.close()

    notseen_file = open('seenit.txt','a+')

    for thread_id in threads_to_check:
        InstagramAPI.getv2Threads(thread_id)
        thread_content = InstagramAPI.LastJson
        pictures = thread_content['thread']['items'] #gives back 8 dictionaries with images
        for picture_info in pictures:
            item_id = picture_info['item_id']
            gate2 = picture_info['item_type']
            if item_id not in posted_list:
                notseen_file.write(item_id+'\n')
                if gate2 == 'media':
                    photo_url = picture_info['media']['image_versions2']['candidates'][0]['url']
                    image_handle(photo_url,"image_name.jpg")
                if gate2 == 'raven_media':
                    photo_url = picture_info['visual_media']['media']['image_versions2']['candidates'][0]['url']
                    image_handle(photo_url,"image_name.jpg")
                if gate2 == 'media_share':
                    print('In Media Share Gate')
                    try:
                        photo_url = picture_info['direct_media_share']['media']['image_versions2']['candidates'][0]['url']
                        print('try',photo_url)
                        image_handle(photo_url,"image_name.jpg")
                    except:
                        photo_url = picture_info['media_share']['image_versions2']['candidates'][0]['url']
                        print('except',photo_url)
                        image_handle(photo_url,"image_name.jpg")

    notseen_file.close()
    print('file closed')





if __name__ == '''__main__''':
    print("Starting")
    while True:
        inbox()
        print('Sleeping')
        time.sleep(25)
        print('Awake')
