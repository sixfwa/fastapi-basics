from typing import List
import fastapi as _fastapi
import sqlalchemy.orm as _orm
import services as _services, schemas as _schemas

app = _fastapi.FastAPI()

_services.create_database()


@app.post("/users/", response_model=_schemas.User)
def create_user(
    user: _schemas.UserCreate, db: _orm.Session = _fastapi.Depends(_services.get_db)
):
    db_user = _services.get_user_by_email(db=db, email=user.email)
    if db_user:
        raise _fastapi.HTTPException(
            status_code=400, detail="woops the email is in use"
        )
    return _services.create_user(db=db, user=user)


@app.get("/users/", response_model=List[_schemas.User])
def read_users(
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    users = _services.get_users(db=db, skip=skip, limit=limit)
    return users


@app.get("/users/{user_id}", response_model=_schemas.User)
def read_user(user_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this user does not exist"
        )
    return db_user


@app.post("/users/{user_id}/posts/", response_model=_schemas.Post)
def create_post(
    user_id: int,
    post: _schemas.PostCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    db_user = _services.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this user does not exist"
        )
    return _services.create_post(db=db, post=post, user_id=user_id)


@app.get("/posts/", response_model=List[_schemas.Post])
def read_posts(
    skip: int = 0,
    limit: int = 10,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    posts = _services.get_posts(db=db, skip=skip, limit=limit)
    return posts


@app.get("/posts/{post_id}", response_model=_schemas.Post)
def read_post(post_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    post = _services.get_post(db=db, post_id=post_id)
    if post is None:
        raise _fastapi.HTTPException(
            status_code=404, detail="sorry this post does not exist"
        )

    return post


@app.delete("/posts/{post_id}")
def delete_post(post_id: int, db: _orm.Session = _fastapi.Depends(_services.get_db)):
    _services.delete_post(db=db, post_id=post_id)
    return {"message": f"successfully deleted post with id: {post_id}"}


@app.put("/posts/{post_id}", response_model=_schemas.Post)
def update_post(
    post_id: int,
    post: _schemas.PostCreate,
    db: _orm.Session = _fastapi.Depends(_services.get_db),
):
    return _services.update_post(db=db, post=post, post_id=post_id)