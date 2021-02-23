from db.user_db import UserInDB
from db.user_db import update_user, get_user
from db.transaction_db import TransactionInDB
from db.transaction_db import save_transaction
from models.user_models import UserIn, UserOut
from models.transaction_models import TransactionIn,TransactionOut
import datetime
from fastapi import FastAPI #con esta línea decimos que vamos a crear un apirest con fastapi
from fastapi import HTTPException #Se utiliza para lanzar los errores

#nombre del api o de la aplicación back
api = FastAPI()

#método para autenticar usuario
#Esta anotación @api.post permite asociar la función al servicio web, es decir cada vez que hagan la petición a este url "/user/auth/ ingresa a esta función
@api.post("/user/auth/") 
async def auth_user(user_in: UserIn): #async: apenas llega la petición la ejecuta, es decir en paralelo con otras
    user_in_db = get_user(user_in.username)
    if user_in_db == None:
        raise HTTPException(status_code=404,
        detail="El usuario no existe")
    if user_in_db.password != user_in.password:
        return {"Autenticado": False}
    return {"Autenticado": True}

@api.get("/user/balance/{username}")#en este caso como es get se pasan parámetros por url
async def get_balance(username: str):
    user_in_db = get_user(username)
    if user_in_db == None:
        raise HTTPException(status_code=404,
                            detail="El usuario no existe")
    user_out = UserOut(**user_in_db.dict())#el doble asterisco mapea, es decir que le dice al "objeto" user_in_db que es de tipo UserIn que me traiga solo los campos de la clase UserOut
    return user_out

@api.put("/user/transaction/")
async def make_transaction(transaction_in: TransactionIn):
    user_in_db = get_user(transaction_in.username)
    if user_in_db == None:
        raise HTTPException(status_code=404,
                            detail="El usuario no existe")
    if user_in_db.balance < transaction_in.value:
        raise HTTPException(status_code=400,
                            detail="Sin fondos suficientes")
    user_in_db.balance = user_in_db.balance - transaction_in.value
    update_user(user_in_db)
    transaction_in_db = TransactionInDB(**transaction_in.dict(),
    actual_balance = user_in_db.balance)
    transaction_in_db = save_transaction(transaction_in_db)
    transaction_out = TransactionOut(**transaction_in_db.dict())
    return transaction_out