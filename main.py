import vk
import yadisk
import settings
import json

vk_api = vk.API(access_token = settings.vk_token, v = '5.199')

vk_id = input("Введите ID пользователя, для копирования фото: ")

albums = vk_api.photos.getAlbums(owner_id=vk_id)
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
    vk_photos_info.append({"file_name": f"{vk_photo['likes']['count']}.{format}","size": vk_photo['sizes'][-1]['type'],"url": vk_photo['sizes'][-1]['url']})

vk_photos_for_json = []
for vk_photo in vk_photos_info:
    vk_photos_for_json.append({k: v for k, v in vk_photo.items() if k != 'url'})

with open(f'results/{vk_id}_{vk_album_id}.json','w') as f:
    json.dump(vk_photos_for_json, f)

ya_token = input("Введите токен Яндекс.Диск'а для сохранения фото: ")
yadisk_api = yadisk.Client(token=ya_token)

dir_to_photos = f'/user_{vk_id}_album_{vk_album_id}'
with yadisk_api:
    try:
        yadisk_api.mkdir(dir_to_photos)
    except Exception as e:
        print(e)
    for photo in vk_photos_info:
        try:
            print(f"Скачивание в Яндекс.Диск - {photo['file_name']}")
            yadisk_api.upload_url(photo['url'], f"{dir_to_photos}/{photo['file_name']}")
            print(f"Завершено скачивание для - {photo['file_name']}")
        except Exception as e:
            print(e)
print(f"Завершено скачивание для - {dir_to_photos}")