from fastapi import HTTPException , status

def not_found(resource:str="Resource"):
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{resource} not found"
    )

def forbidden(message:str="Not authorized"):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=message
    )

def unauthorized():
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )

def conflict(message: str = "Conflict"):
    raise HTTPException(
        status_code=status.HTTP_409_CONFLICT,
        detail=message
    )