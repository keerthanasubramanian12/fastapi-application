from fastapi import FastAPI
from app.routes import auth, users, notes
from app.utils.database import connect_to_mongo

app = FastAPI()

@app.on_event("startup")
def startup():
    connect_to_mongo()

# Include Routes
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(notes.router, prefix="/notes", tags=["Notes"])
