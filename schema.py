from pydantic import BaseModel

# Article Model
class Article(BaseModel):
    title: str
    description: str
    author: str

# create a class that will extend the base class
class ArticleCreate(Article):
    pass

# create a class that 
class Article_two(Article):
    id: int

    class Config:
        orm_mode = True
