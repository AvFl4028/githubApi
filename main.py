from fastapi import FastAPI
from pydantic import BaseModel
from user import User

class UserInfo(BaseModel):
    user: str

app = FastAPI()
user = User()

@app.get("/")
def root():
    return {}

@app.post("/")
def userPost(req: UserInfo):
    if req.user == None or req.user == "":
        return {"status": False}
    user.setUser(req.user)
    # user.rq()
    return {"status": True}

@app.get("/repos")
def get_repositorys():
    return user.get_all_repositorys()

@app.get("/repos/{repo_title}")
def get_repository(repo_title):
    return user.search_repo(repo_title)
