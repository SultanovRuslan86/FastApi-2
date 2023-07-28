from fastapi import FastAPI, status, HTTPException
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



@app.get('/articles/{id}', status_code=status.HTTP_200_OK, response_model=MyArticleSchema)
def get_articles_by_pk(id: int, db: Session = Depends(get_db)):
    # my_article = db.query(models.Article).filter(models.Article.id == id).first()
    my_article = db.query(models.Article).get(id)
    if my_article:
        return my_article

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='The Article with this id not exist!')



@app.post('/articles', status_code=status.HTTP_201_CREATED)
def add_article(article: ArticleSchema, db:Session = Depends(get_db)):
    new_article = models.Article(title=article.title, description=article.description)
    db.add(new_article)
    db.commit()
    db.refresh(new_article)
    return new_article



@app.put('/update_article/{id}', status_code=status.HTTP_202_ACCEPTED)
def update_article(id, article: ArticleSchema, db: Session = Depends(get_db)):
    db.query(models.Article).filter(models.Article.id == id).update({'title': article.title, 'description': article.description})
    db.commit()

    return {'message': 'the datas is updated!'}



@app.delete(f'/article_delete/{id}', status_code=status.HTTP_202_ACCEPTED)
def delete_article(id: int, db: Session = Depends(get_db)):
    db.query(models.Article).filter(models.Article.id == id).delete(synchronize_session=False)
    db.commit()

    return {f'Article with {id} deleted'}
