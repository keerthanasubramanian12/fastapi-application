from fastapi import APIRouter, HTTPException, Depends
from app.models import Note
from app.utils.jwt import verify_access_token
from app.utils.database import db

router = APIRouter()

def get_current_user(token: str):
    payload = verify_access_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return payload["user_id"]

@router.post("/")
async def create_note(note: Note, user_id: str = Depends(get_current_user)):
    note.note_id = str(uuid4())
    note.user_id = user_id
    db["notes"].insert_one(note.dict())
    return {"message": "Note created successfully"}

@router.get("/")
async def get_notes(user_id: str = Depends(get_current_user)):
    notes = list(db["notes"].find({"user_id": user_id}, {"_id": 0}))
    return {"notes": notes}

@router.put("/{note_id}")
async def update_note(note_id: str, note: Note, user_id: str = Depends(get_current_user)):
    result = db["notes"].update_one(
        {"note_id": note_id, "user_id": user_id},
        {"$set": note.dict()}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Note not found or not authorized")
    return {"message": "Note updated successfully"}

@router.delete("/{note_id}")
async def delete_note(note_id: str, user_id: str = Depends(get_current_user)):
    result = db["notes"].delete_one({"note_id": note_id, "user_id": user_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found or not authorized")
    return {"message": "Note deleted successfully"}