from fastapi import FastAPI, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError

from models.database import Base, get_db, engine
from models.user import User


from schemas.collection import CollectionCreate, CollectionOut
from schemas.user import UserCreate, UserOut
from schemas.token import Token

from controllers.collection import create_collection, list_collections, get_collection, add_vinyl_to_collection, remove_vinyl_from_collection
from controllers.user import create_user, authenticate, get_user

from routes.vinyls_routes import vinyl_router


from utils.jwt import create_access_token, decode_access_token


app = FastAPI()
Base.metadata.create_all(bind=engine)  # crée les tables dans la BDD, la structure de la BDD.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

app.include_router(vinyl_router)


# ROUTE D'ACCUEIL
@app.get("/")
def read_root():
    return {"Hello": "World"}


# ==================
# == UTILISATEURS ==
# ==================

# AJOUTER UN UTILISATEUR
@app.post('/users/register', response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = create_user(user, db)
        return new_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
        
# ACCÉDER À l'UTILISATEUR COURANT
@app.get('/users/me', response_model=UserOut)
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = decode_access_token(token)
        username = payload.get("username")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No username"
            )
        user = get_user(db, username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="No user"
            )
        return user
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is wrong"
        )




# =====================
# == AUTEHTIFICATION ==
# =====================

@app.post('/token')
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    token = create_access_token({"username": user.username, "email": user.email})   # Le JWT est créé ici
    return Token(access_token = token, token_type = "bearer")




# =================
# == COLLECTIONS ==
# =================


# LISTER TOUTES LES COLLECTIONS
@app.get("/collections", response_model = list[CollectionOut])
def list_collections_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return list_collections(skip, limit, db)


# RÉCUPÉRER UNE SEULE COLLECTION
@app.get("/collection/{collection_id}", response_model = CollectionOut)
def get_collection_route(collection_id:int, db: Session = Depends(get_db)):
    try: 
        collection = get_collection(collection_id, db)
    except Exception as e:  # on récupère l'Exception qu'on a créer dans le controller
        raise HTTPException(status_code=404, detail=str(e)) # La route décide comment le communiquer au client (except + HTTPException).
                                                            # e --> message d'erreur dans le controller
    return collection


# CRÉER UNE COLLECTION
@app.post("/collection/", response_model = CollectionOut, status_code = status.HTTP_201_CREATED)

def create_collection_route(
    collections: CollectionCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)): # FastAPI orchestre le cycle de vie de get_db (injection + fermeture) ;
                                    # SQLAlchemy crée la session BDD                                  
    return create_collection(collections, current_user, db)


# AJOUTER UN VINYL À UNE COLLECTION
@app.post("/collections/{collection_id}/vinyls/{vinyl_id}", response_model = CollectionOut)
def add_vinyl_to_collection_route(
    collection_id: int,
    vinyl_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)):
    return add_vinyl_to_collection(collection_id, vinyl_id, current_user, db)



# SUPPRIMER UN VINYL D'UNE COLLECTION
@app.delete("/collections/{collection_id}/vinyls/{vinyl_id}")
def remove_vinyl_from_collection_route(
    collection_id: int,
    vinyl_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return remove_vinyl_from_collection(collection_id, vinyl_id, current_user, db)


