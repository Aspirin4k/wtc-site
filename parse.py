import json
import sqlite3
import re
from peewee import *

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

db = SqliteDatabase('posts.db')

class BaseModel(Model):
    class Meta:
        database = db

class Post(BaseModel):
    id = AutoField(unique=True)
    date = DateField()
    owner_id = IntegerField()
    vk_id = IntegerField()
    title = CharField()
    text = TextField()

class Attachments(BaseModel):
    id = AutoField(unique=True)
    post_id = ForeignKeyField(Post, backref='attachments')
    type = CharField()
    url = CharField()

def title_maker(text: str) -> str:
    title = re.sub(r"#\w+\s", "", text)
    if len(title) > 30:
        title = title[:30]
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
        if post['attachments'] != []:
            for at in post['attachments']:
                att = Attachments(post_id=post['id'], type="photo", url=at)
                att.save()


if __name__ == "__main__":
    db.connect()
    db.create_tables([Post, Attachments])
    ## Подготавливаем данные
    
    # Читаем json
    with open("dest_file.json") as f:
        dirty_posts = json.load(f)
        
    # Получает только посты
    posts = dirty_posts['items']
    a = convert_json_to_sqlite(posts)
    save_data(a)

        
