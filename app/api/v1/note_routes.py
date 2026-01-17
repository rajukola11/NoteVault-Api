from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.note_schema import NoteCreate,NoteRead
from app.db.session import get_db
from app.models.note_model import NoteModel
from app.core.dependencies import get_current_user
from app.models.user_model import UserModel
from app.core.errors import not_found,forbidden

note_router=APIRouter(tags=["notes"])


@note_router.get("/notes",response_model=List[NoteRead])
def get_all_notes(db:Session=Depends(get_db),current_user:UserModel=Depends(get_current_user)):
    if current_user.role == "admin":
        return db.query(NoteModel).all()
    return db.query(NoteModel).filter(current_user.id == NoteModel.owner_id).all()

@note_router.post("/notes",status_code=status.HTTP_201_CREATED)
def create_a_note(note_data:NoteCreate,db:Session=Depends(get_db),current_user:UserModel=Depends(get_current_user)):
    new_note = NoteModel(**note_data.model_dump(),owner_id=current_user.id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@note_router.get("/notes/{note_id}",response_model=NoteRead)
def get_a_note(note_id:int,db:Session=Depends(get_db),current_user:UserModel=Depends(get_current_user)):
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not note:
        not_found("Note")
    if note.owner_id != current_user.id and current_user.role!="admin":
        forbidden("Not authorized")
    return note

@note_router.put("/notes/{note_id}",response_model=NoteRead)
def update_a_note(note_id:int,update_note_data:NoteCreate,db:Session=Depends(get_db),current_user:UserModel=Depends(get_current_user))->NoteRead:
    update_note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not update_note:
        not_found("Note")
    if update_note.owner_id!=current_user.id and current_user.role != "admin":
        forbidden("Not authorized to update this note")
        
    for key,value in update_note_data.model_dump(exclude_unset=True).items():
        setattr(update_note,key,value)
    db.commit()
    db.refresh(update_note)
    return update_note

@note_router.delete("/notes/{note_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_a_note(note_id:int,db:Session=Depends(get_db),current_user:UserModel=Depends(get_current_user)):
    delete_task=db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not delete_task:
        not_found("Note")
    if current_user.role != "admin":
        forbidden("Only admins can delete notes")

    db.delete(delete_task)
    db.commit()
    return