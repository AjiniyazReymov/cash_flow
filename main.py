from fastapi import FastAPI
from auth_routes import auth_router
from fastapi_jwt_auth import AuthJWT

from schemas import Settings, LoginModel
from debt_routes import debt_router

app = FastAPI()

@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth_router)
app.include_router(debt_router)

@app.get('/')
async def root():
    return {'message': "Cash Flow project"}