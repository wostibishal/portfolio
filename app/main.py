from fastapi import FastAPI # type: ignore
from sqlmodel import SQLModel
from backend.app.db.database import engine
from backend.app.routers import auths_router, products_router

app = FastAPI()

@app.on_event("startup")
async def startup_event():
   print('startup event triggered')
   SQLModel.metadata.create_all(engine)
   print('database tables created')

app.include_router(auths_router.router, prefix="/auth")
app.include_router(products_router.router, prefix="/product")
#app.include_router(users.router, prefix="/users", tags=["users"])