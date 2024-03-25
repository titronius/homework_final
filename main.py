import vk
import yadisk
import settings
import json
from progress.bar import IncrementalBar

vk_api = vk.API(access_token = settings.vk_token, v = '5.199')

class vk_downloaded_photos:
    def __init__(self,vk_id,vk_album_id,vk_photos_info):
        self.id = vk_id
        self.album_id = vk_album_id
        self.info = vk_photos_info

def vk_get_photos(vk_id):
    albums = vk_api.photos.getAlbums(owner_id = vk_id)
    user_info = vk_api.users.get(user_ids = vk_id)
    user_name = user_info[0]['first_name']
    user_surname = user_info[0]['last_name']

    print(f'Альбомы пользователя "{user_name} {user_surname}":')
    for album in albums['items']:
        print(f'Название: {album["title"]} ID: {album["id"]}')
    print('Название: Фотографии профиля ID: profile')

    vk_album_id = input("Введите ID альбома, из которого надо скопировать фото: ")

    vk_photos = vk_api.photos.get(owner_id = vk_id, album_id = vk_album_id, extended = 1)['items']
    print(f'Количество фото у пользователя в этом альбоме: {len(vk_photos)}')
    vk_photos_info = []
    for vk_photo in vk_photos:
        format = (vk_photo['sizes'][-1]['url'].split('?')[0]).split('.')[-1]
        vk_photos_info.append({"file_name": f"{vk_photo['likes']['count']}_{vk_photo['date']}.{format}","size": vk_photo['sizes'][-1]['type'],"url": vk_photo['sizes'][-1]['url']})

    vk_photos_for_json = []
    for vk_photo in vk_photos_info:
        vk_photos_for_json.append({k: v for k, v in vk_photo.items() if k != 'url'})

    with open(f'results/{vk_id}_{vk_album_id}.json','w') as f:
        json.dump(vk_photos_for_json, f)

    result = vk_downloaded_photos(vk_id,vk_album_id,vk_photos_info)

    return result

def ya_disk_save_photos(ya_token,vk_photos):
    yadisk_api = yadisk.Client(token = ya_token)

    dir_to_photos = f'/user_{vk_photos.id}_album_{vk_photos.album_id}'
    with yadisk_api:
        try:
            yadisk_api.mkdir(dir_to_photos)
        except Exception as e:
            print(e)
        bar = IncrementalBar('Скачиваем фото:', max = len(vk_photos.info))
        for photo in vk_photos.info:
            bar.next()
            try:
                yadisk_api.upload_url(photo['url'], f"{dir_to_photos}/{photo['file_name']}")
            except Exception as e:
                print(e)
    bar.finish()

vk_id = input("Введите ID пользователя, для копирования фото: ")
vk_photos = vk_get_photos(vk_id)

ya_token = input("Введите токен Яндекс.Диск'а для сохранения фото: ")
ya_disk_save_photos(ya_token,vk_photos)