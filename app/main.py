from fastapi import FastAPI

from .db.setup import session
from .db.models.user import User

app = FastAPI()


@app.get("/")
async def root():
    user: User = session.query(User).filter_by(username="test").first()
    return {"message": f"Hi, {user.email}"}
