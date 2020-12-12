from flask import Flask, render_template
from peewee import *
from db import *
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    titles = Post.select()
    return render_template('index.html', titles=titles)

def authorizify(id: int) -> str:
    authors = {
        -144705371: ["https://vk.com/ryukishi07", "ORIGINAL"],
        -81413361: ["https://vk.com/id70251320", "Алексей Кушелов"]
    }
    return authors[id]

@app.route('/post/<int:post_id>')
def get_post(post_id):
    query = Post.get(Post.vk_id==post_id)
    title = query.title
    body = query.text
    date = (datetime
            .utcfromtimestamp(query.date)
            .strftime('%Y-%m-%d %H:%M:%S'))
    author = authorizify(query.owner_id)
    tags = Tags.select().where(Tags.vk_id==post_id)
    att = Attachments.select().where(Attachments.vk_id==post_id)
    return render_template('post.html',
                           title=title,
                           date=date,
                           author=author,
                           body=body,
                           tags=tags,
                           att=att)

@app.route('/tag/<tag>')
def get_tag(tag):
    titles = (Tags
         .select(Tags, Post)
         .join(Post, on=(Post.vk_id == Tags.vk_id))
         .where(Tags.name==tag))
    return render_template('tag.html', titles=titles)

'''
SELECT tags.vk_id, post.title
FROM tags
inner join post on tags.vk_id = post.vk_id
where tags.name = "#Higurashi "
'''
