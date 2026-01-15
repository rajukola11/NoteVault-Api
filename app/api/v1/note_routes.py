from fastapi import APIRouter,Depends,status,HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas.note_schema import NoteCreate,NoteRead
from app.db.session import get_db
from app.models.note_model import NoteModel

note_router=APIRouter()


@note_router.get("/notes",response_model=List[NoteRead])
def get_all_notes(db:Session=Depends(get_db))->List[NoteRead]:
    notes=db.query(NoteModel).all()
    return notes

@note_router.post("/notes",status_code=status.HTTP_201_CREATED)
def create_a_note(note_data:NoteCreate,db:Session=Depends(get_db)):
    new_note = NoteModel(**note_data.model_dump())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@note_router.get("/notes/{note_id}",response_model=NoteRead)
def get_a_note(note_id:int,db:Session=Depends(get_db)):
    note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    return note

@note_router.put("/notes/{note_id}",response_model=NoteRead)
def update_a_note(note_id:int,update_note_data:NoteCreate,db:Session=Depends(get_db))->NoteRead:
    update_note = db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not update_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    for key,value in update_note_data.model_dump(exclude_unset=True).items():
        setattr(update_note,key,value)
    db.add(update_note)
    db.commit()
    db.refresh(update_note)
    return update_note

@note_router.delete("/notes/{note_id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_a_note(note_id:int,db:Session=Depends(get_db)):
    delete_task=db.query(NoteModel).filter(NoteModel.id == note_id).first()
    if not delete_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )
    db.delete(delete_task)
    db.commit()
    return