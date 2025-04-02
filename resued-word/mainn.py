from fastapi import FastAPI, Response, HTTPException , status
from fastapi.params import Body
from pydantic import BaseModel 
from typing import Optional
from random import randrange
import time
import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()



class Post(BaseModel):
    title  : str
    content : str
    published : bool = True
    # rating : Optional[int] = None

while True:
    try:
        conn = psycopg2.connect(host = "localhost" , database = "fastapi", user = "postgres", 
                                password = "sumay", cursor_factory = RealDictCursor)

        cursor = conn.cursor()
        print("Database connnection is succefull")
        break
    except Exception as error:
        print("Connecting to database is failed")
        print("Eroor : ", error)
        time.sleep(2)


my_post = [
    {
        "title": "sumay_title",
        "content": "new_abc",
        "id" : 2
    }
    ]

def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p
        

def find_index_post(id: int):
    for i , p in enumerate(my_post):
        if int(p['id']) == id:
            return i
    return None


@app.get("/posts")
def get_posts():
    cursor.execute("""select * from posts""")
    posts = cursor.fetchall()
    # print(posts)
    return {"data" : posts }

@app.post("/posts" , status_code = status.HTTP_201_CREATED)
def post(post: Post):
    cursor.execute(""" insert into posts 
                   (title, content, published) 
                   values (%s , %s, %s) returning * """ , 
                   (post.title, post.content, post.published))
    new_posts = cursor.fetchone()
    conn.commit()
    return {"data" : new_posts}


@app.get("/posts/{id}" , status_code = status.HTTP_201_CREATED)
async def get_post(id: int):
    
    cursor.execute(""" select * from posts where id = %s """, (str(id), ))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                             detail = f"post with id: {id} was not found")
        
    return {"post_details": post }


@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    
    cursor.execute( """ delete from posts where id = %s returning * """, (str(id),) )
    delete_post = cursor.fetchone()
    conn.commit()

    if delete_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id: {id} doesn't exist")

    # my_post.pop(index)
    return Response( status_code = status.HTTP_204_NO_CONTENT)
  


@app.get("/")
async def root():
    return {"message": "Hello world"}

@app.post("/create")
def create_post(new_post : Post):
    print(new_post)
    print(new_post.dict())
    return {"data" : new_post}

# @app.post("/posts" , status_code = status.HTTP_201_CREATED)
# def post(post: Post):
#     post_dict = post.dict()
#     post_dict["id"] = randrange(0,100)
#     my_post.append(post_dict)
#     return {"data" : post_dict}


# @app.get("/posts/{id}")
# def get_post(id: int, response: Response):
#     post = find_post(id)
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail= f"posst with id: {id} was not found")
#     return {"data" : post}


@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # delete post
    # find the index in the array 
    # my_post.pop(index)

    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail = f"Post with id: {id} doesn't exist")

    my_post.pop(index)
    return 
    # return Response (status_code = status.HTTP_204_NO_CONTENT)

# Update -> Put : Here we have to pass all the field
@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    print(post)
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            details = f"Post with id: {id} do not exists...")

    # my_post.pop(index)
    post_dict = post.__dict__
    post_dict["id"] = id
    my_post[index] = post_dict 
    return {"data": post_dict}




# @app.get("/posts/{id}")
# def get_post(id: int):
#    # post = find_post(int(id))
#     post = find_post(id)
#     return {"data" : post}


# @app.post("/create")
# def create_post(payload: dict = Body(...)):
#     print(payload)
#     return {"message" : "Succesfully createdd posst"}