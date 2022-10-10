from fastapi import APIRouter, Query, Body, Path
from pydantic import BaseModel
from typing import Optional, List, Dict

router = APIRouter(
    prefix='/blog',
    tags=['blog']
)

class Image(BaseModel):
    url: str
    alias: str

class BlogModel(BaseModel):
    title: str
    content: str
    nb_comments: int
    published: Optional[bool]
    tags: List[str] = [] #zamiast listy można dodać List, set, dict, tuple
    metadata: Dict[str, str] = {'key': 'value'}
    image: Optional[Image] = None

@router.post('/new/{id}')
def create_blog(blog: BlogModel, id: int, version: int =1):
    return {
        'id': id,
        'version': version,
        'data': blog
    }


@router.post('/new/{id}/comment')
def create_comment(
        blog: BlogModel,
        id: int,
        comment_title: int = Query(
            None,
            #metadata:
            title='Id of the comment',
            description='Some description for comment_id',
            alias='commentId',
            deprecated=True
        ),
        #validator:
        content: str = Body(...,
                            min_length=10,
                            max_length=20,
                            regex='^[a-z\s]*$' ),
        # Body("hi how are you")  parametr opcjonalny
        # aby nie był opcjonalny trzeba użyć trzech kropek -> Body(...)
        v: Optional[List[str]] = Query(['1.0', '1.1', '1.4']),
        #number validator
        comment_id: int = Path(None,
                               gt=5,
                               le=10)

):
    return {
        'blog': blog,
        'id': id,
        'comment_title': comment_title,
        'comment_id': comment_id,
        'content': content,
        'version': v
    }
