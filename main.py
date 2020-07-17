from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session

# database import 
from database import SessionLocal, engine, Base
from models import ArticleModel
Base.metadata.create_all(bind=engine)

# service imports
from service import ArticleService

app = FastAPI(
    title="Articles API",
    description="CRUD operations for a articles application",
    version="1.0.0"
)

# import the schemas
from schema import ArticleCreate, Article

# Setup the dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/')
def home():
    return {"message":"Hello world"}


@app.get('/articles', tags=["Article"], summary="Get all the articles" ,response_description="A list of all articles")
async def get_articles(db: Session = Depends(get_db)):
    all_articles = ArticleService.get_articles(db=db)
    return all_articles

@app.get('/articles/{article_id}', tags=["Article"], summary="Get an article by ID", response_description="An article")
async def get_post(article_id:int, db: Session = Depends(get_db)):
    the_article = ArticleService.get_article(db=db, article_id=article_id)
    if the_article is None:
        raise HTTPException(status_code=404, detail="The article does not exist!")
    return the_article

@app.post('/articles', tags=["Article"], summary="Create an article")
async def create_article(article:ArticleCreate, db: Session = Depends(get_db)):
    new_article = ArticleService.create_new_article(db=db, article=article)
    return new_article

@app.put('/articles/{article_id}', tags=["Article"], summary="Update and article by ID", response_description="The created article")
async def update_article(article_id:int, article: ArticleCreate, db: Session = Depends(get_db)):
    return ArticleService.update_article(article_id=article_id, article=article, db=db)
    
    
@app.delete('/articles/{article_id}', tags=["Article"],summary="Delete an article by ID")
async def delete_article(article_id:int, db: Session = Depends(get_db)):
    return ArticleService.delete_article(article_id=article_id, db=db)
    

