from typing import List
from fastapi import APIRouter, status, HTTPException, Response
import sqlalchemy as sa
from app import models, schemas
from app.database import SessionDep

router = APIRouter(
    prefix="/posts", 
    tags=["Posts"]
)

@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(response: Response, session: SessionDep):
    response.status_code = status.HTTP_200_OK
    # with psycopg2.connect(DUP) as conn:
    #     with conn.cursor(cursor_factory=RealDictCursor) as cur:
    #         cur.execute(""" 
    #                     SELECT * 
    #                     FROM posts; 
    #                     """)
    #         data = cur.fetchall()


    stmt = sa.select(models.Post)
    posts = session.scalars(stmt).all()

    return posts



@router.get("//{id}", response_model=schemas.PostResponse)
def get_post_by_id(id: int, response: Response, session: SessionDep):
    # with psycopg2.connect(DUP) as conn:
    #     with conn.cursor(cursor_factory=RealDictCursor) as cur:
    #         cur.execute(""" 
    #                     SELECT * 
    #                     FROM posts 
    #                     WHERE id = %s; 
    #                     """, (id,))
    #         post = cur.fetchone()


    stmt = sa.select(models.Post).where(models.Post.id == id)
    try:
        post = session.scalars(stmt).one()
    except sa.exc.NoResultFound:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail = f"post with id {id} not found")

    # dict_post = schemas.Post.model_validate(post).model_dump()

    response.status_code = status.HTTP_200_OK
    return post


@router.post("/", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, response: Response, session: SessionDep):   
    # with psycopg2.connect(DUP) as conn:
    #     with conn.cursor(cursor_factory=RealDictCursor) as cur:
    #         cur.execute(""" 
    #                     INSERT INTO posts (title, content, published)
    #                     VALUES (%s, %s, %s) 
    #                     RETURNING *; 
    #                     """, (new_post.title, new_post.content, new_post.published))
    #         post = cur.fetchone()


    new_post = models.Post(**post.model_dump())
    session.add(new_post)
    session.commit()
    session.refresh(new_post)   
        

    response.status_code = status.HTTP_201_CREATED
    return new_post


@router.delete("/{id}")
def delete_post(id: int, session: SessionDep):
    # with psycopg2.connect(DUP) as conn:
    #     with conn.cursor(cursor_factory=RealDictCursor) as cur:
    #         cur.execute(""" 
    #                     DELETE 
    #                     FROM posts 
    #                     WHERE id = %s 
    #                     RETURNING *
    #                     """, (id,))
    #         post = cur.fetchone()

    post = session.get(models.Post, id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} not found")

    session.delete(post)
    session.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
    

@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, new_post: schemas.PostCreate, response: Response, session: SessionDep):

    # with psycopg2.connect(DUP) as conn:
    #     with conn.cursor(cursor_factory=RealDictCursor) as cur:
    #         cur.execute(""" 
    #                     UPDATE posts
    #                     SET title = %s,
    #                         content = %s,
    #                         published = %s
    #                     WHERE id = %s
    #                     RETURNING *
    #                     """, (new_post.title, new_post.content, new_post.published, id))
    #         post = cur.fetchone()

    post = session.get(models.Post, id)

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"post with id {id} not found")
    
    stmt = (
        sa.update(models.Post)
        .where(models.Post.id == id)
        .values(new_post.model_dump())
        .returning(models.Post)
        .execution_options(synchronize_session=False)
    )
    post = session.scalars(stmt).one()
    session.commit()

    
    response.status_code = status.HTTP_200_OK
    return post
