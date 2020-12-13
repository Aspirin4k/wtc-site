import json
import sqlite3
import re
from peewee import *
from db import *

def convert_json_to_sqlite(posts):
    "Перевод данных из JSON, который получен из vk, в SQLite."
    # Создаем переменную, куда будем класть очищенные данные
    clean_posts = []

    # Прогоняем все посты по циклу, где будем унифицировать их
    # и очищать от ненужной информации
    for post in posts:
        if is_reposted(post):
            post = nativify(post)

        clean_post = clearify(post)
        clean_posts.append(clean_post)

    save_data(clean_posts)
    return clean_posts

def is_reposted(post: dict) -> bool:
    "Проверка, явлется ли пост репостом."
    return 'copy_history' in post


def nativify(post: dict) -> dict:
    "Делаем из репоста обычный пост."
    return post['copy_history'][0]


def clearify(post: dict) -> dict:
    junky_rows = (
        'comments',
        'from_id',
        'is_favorite',
        'is_pinned',
        'likes',
        'marked_as_ads',
        'post_source',
        'reposts',
        'views',
        'post_type'
    )
    att = []
    for junky_row in junky_rows:
        if junky_row in post:
            post.pop(junky_row)
        if 'attachments' in post:
            attachs = post.pop('attachments')
            for attach in attachs:
                if 'photo' in attach:
                    photo = attach['photo']
                    sizes = photo['sizes']
                    img = select_best(sizes)
                    att.append(img['url'])
    post['attachments'] = att
    return post

def select_best(sizes: list) -> str:
    types =  ['w', 'z', 'y', 'x', 's', 'r', 'q', 'p', 'o', 'm']
    sizes.reverse()
    for size in sizes:
        for i in range(len(types)):
            if size['type'] == types[i]:
                return size

def title_maker(text: str) -> str:
    title = re.sub(tag_regex, "", text)
    if len(title) > 60:
        title = title[:60]
        title += "..."
    return title

def save_data(posts):
    for post in posts:
        posty = Post(
            owner_id=post['owner_id'],
            vk_id=post['id'],
            date=post['date'],
            title=title_maker(post['text']),
            text=post['text'])
        posty.save()
        for tag in re.findall(tag_regex, post['text']):
            tag = re.sub("#", "", tag).strip()
            taggy = Tags(vk_id=post['id'], name=tag)
            taggy.save()
        if post['attachments'] != []:
            for at in post['attachments']:
                att = Attachments(vk_id=post['id'], type="photo", url=at)
                att.save()


if __name__ == "__main__":
    tag_regex = r"#\w+\s"
    database.connect()
    database.create_tables([Post, Attachments, Tags])
    ## Подготавливаем данные

    # Читаем json
    with open("dest_file.json") as f:
        dirty_posts = json.load(f)

    # Получает только посты
    posts = dirty_posts['items']
    convert_json_to_sqlite(posts)
