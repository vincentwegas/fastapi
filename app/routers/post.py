from fastapi.routing import APIRouter
from sqlalchemy.sql.functions import func
from starlette.status import HTTP_403_FORBIDDEN


from .. import models, schemas, oauth2
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from .. database import engine, get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/posts", tags=['Posts'])



@router.get('/', response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    

    
    
    #cursor.execute(""" SELECT * from posts""")
    #cursor.execute('''Select * from posts''')
    #posts = cursor.fetchall()

    #print(limit)
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    

    
    #Will only provide the users own posts
    #posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
   

    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # #Execute SQL Command
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # #Fetch result 
    # new_post = cursor.fetchone()
    # print(new_post)
    # conn.commit()

    posts = db.query(models.Post).all()

    #new_post = models.Post(title=post.title, content=post.content, published=post.published)
    #print(current_user.email)
    #print(current_user.id)
    new_post = models.Post(owner_id = current_user.id , **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post

#@router.get('/posts/latest')
#def get_latest_post():
#    post = my_posts[-1]
#    return {"details" : post}

@router.get('/{id}', response_model=schemas.PostOut)
def get_posts(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    #post = cursor.fetchone()

    #post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()

    #If no Post with Specific Nbr then retrun statuscode 404 with failure text
    if not post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id: {id} was not found")
    return post

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):


    #cursor.execute("""DELETE FROM posts WHERE id = %s Returning *""", (str(id),))
    #deleted_post = cursor.fetchone()
    #conn.commit()

    #Query SQL -> returning data frpm sql if match
    post_query = db.query(models.Post).filter(models.Post.id == id)
    #print(post_query)

    post = post_query.first()

    if post  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID: {id} doesn't exists")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perfrom requested action!") 

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put('/{id}',response_model=schemas.Post)
def update_post(id: int, updated_post:schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s returning * """, (post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()


    if post  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with ID: {id} doesn't exists")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail= "Not authorized to perfrom requested action!") 

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()