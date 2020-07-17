# Will contain all the login that will address the db
from fastapi import HTTPException
from sqlalchemy.orm import Session

# import the model
from models import ArticleModel

# import the schema
from schema import ArticleCreate, Article

class ArticleService:

    # method to get all articles
    @staticmethod
    def get_articles(db:Session):
        """Get all articles from the database"""
        return db.query(ArticleModel).all()

    # get an article
    @staticmethod
    def get_article(db:Session, article_id:int):
        """Return an article that matches the id"""
        return db.query(ArticleModel).filter(ArticleModel.id==article_id).first()

    # create a new article
    @staticmethod
    def create_new_article(db:Session, article:ArticleCreate):
        """Insert an article"""
        the_article = ArticleModel(**article.dict())
        db.add(the_article)
        db.commit()
        return the_article

    # update an article
    @staticmethod
    def update_article(db:Session, article_id:int, article: ArticleCreate):
        """Update an existing article"""
        the_article:Article = db.query(ArticleModel).filter(ArticleModel.id==article_id).first()

        if the_article is None:
            raise HTTPException(status_code=404, detail="The article does not exist")

        the_article.title = article.title
        the_article.description = article.description
        the_article.author = article.author
        db.commit()
        return the_article

    # delete an article
    @staticmethod
    def delete_article(article_id:int, db:Session):
        """Delete an article"""
        the_article:Article = db.query(ArticleModel).filter(ArticleModel.id==article_id).first()

        if the_article is None:
            raise HTTPException(status_code=404, detail="The article does not exist")

        db.delete(the_article)
        db.commit()

        return {"message" : "Article deleted successfully"}
