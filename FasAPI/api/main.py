from fastapi import FastAPI, status
from fastapi.params import Depends
from sqlalchemy.orm import Session
from . import models
from .database import engine, sessionlocal, Base
from .schemas import ArticleSchema, MyArticleSchema
from .models import Article
from typing import List

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
async def index():
    return {'message': 'Hello'}


@app.get('/articles/', response_model=List[MyArticleSchema])
def get_articles(db:Session = Depends(get_db)):
    my_articles = db.query(models.Article).all()
    return my_articles


@app.post('/articles', status_code=status.HTTP_201_CREATED)
def add_article(article: ArticleSchema, db:Session = Depends(get_db)):
    new_article = models.Article(title=article.title, description=article.description)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article



