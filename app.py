from flask import Flask, render_template, make_response, request
from urllib.parse import urljoin
from feedgen.feed import FeedGenerator
from peewee import *
from db import *
from datetime import datetime
import pytz
from math import ceil

app = Flask(__name__)

@app.route('/')
def index():
    return pager(0)

@app.route('/page/<int:page>')
def pager(page):
    titles = Post.select()
    displayed_titles = Post.select().limit(30).offset(page*30)
    return render_template('index.html',
                           number_of_pages=ceil(len(titles)/30),
                           displayed_titles=displayed_titles)

@app.route('/feed.xml')
def rss():
    fg = FeedGenerator()
    fg.title('Посты в th07-expansion.ru')
    fg.description('Посты в th07-expansion.ru')
    fg.link(href=request.url)
    cte = Post.select().order_by(Post.date.desc()).limit(20).cte('qq')
    q = Post.select(Post.alias('qq')).order_by(cte.c.date.asc()).with_cte(cte).from_(cte)
    for article in q:
        att = Attachments.select().where(Attachments.vk_id==article.vk_id)
        res = ""
        for img in att:
            res += f"<img src={img.url}>"
        fe = fg.add_entry()
        fe.title(article.title)
        fe.link(href=f"https://www.whentheycry.xyz/post/{article.vk_id}")
        fe.content(article.text + " " + res)
        fe.description("Описание")
        fe.guid(str(article.vk_id), permalink=False) # Or: fe.guid(article.url, permalink=True)
        fe.author(name=authorizify(article.owner_id))
        fe.pubDate(datetime.fromtimestamp(int(article.date)).replace(tzinfo=pytz.UTC))

    response = make_response(fg.rss_str())
    response.headers.set('Content-Type', 'application/rss+xml')

    return response

def get_abs_url(url):
    return urljoin(request.url_root, url)

def authorizify(id: int) -> str:
    authors = {
        -144705371: ["https://vk.com/ryukishi07", "ORIGINAL"],
        -81413361: ["https://vk.com/id70251320", "Алексей Кулешов"],
        -89327841: ["https://vk.com/xx_gensokyo_xx", "EXTREME RUSSIAN FANDOM FOR TOUHOU"],
        -192241227:["https://vk.com/clocktowerzines", "Clock Tower Zines | TYPE-MOON zine | WTCZINE"]
    }
    if id in authors:
        return authors[id]
    else:
        return ["https://vk.com/ryukishi07", "АВТОР ПОКА НЕ НАЙДЕН"]

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
