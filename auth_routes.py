import datetime

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

from fastapi import APIRouter, status, Depends

from models import User, Debt
from schemas import SignUpModel, LoginModel  # LoginModel
from database import session, engine  #db ga baylanisiw ushin
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from sqlalchemy import or_

auth_router = APIRouter(
    prefix='/api'
)

session = session(bind=engine) #sessiyani qosiw ushin (from database import engine) magliwmatlari kk boladi kk boladi

@auth_router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User with this email already exist")
    db_username = session.query(User).filter(User.username==user.username).first()
    if db_username is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                             detail="User with this email already exist")
    new_user = User(
        username=user.username,
        email=user.email,
        password= generate_password_hash(user.password)
    )

    session.add(new_user)
    session.commit()
    data = {
        'id': new_user.id,
        'username': new_user.username,
        'email': new_user.email
    }

    response_model = {
        'success': True,
        'code': 201,
        'message': 'user created successfully',
        'data': data
    }

    return response_model

@auth_router.post('/login', status_code=200)
async def login(user: LoginModel, Authorize: AuthJWT=Depends()): #AuthJwt di obekt esabinda jiberiwdi bildiredi

    db_user = session.query(User).filter(
        or_(
            User.username == user.username_or_email,
            User.email == user.username_or_email
        )
    ).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_lifetime = datetime.timedelta(minutes=60)
        refresh_lifetime = datetime.timedelta(days=3)
        access_token = Authorize.create_access_token(subject=db_user.username, expires_time=access_lifetime)
        refresh_token = Authorize.create_refresh_token(subject=db_user.username, expires_time=refresh_lifetime)

        token = {
            'access': access_token,
            'refresh_token': refresh_token
        }

        response = {
            'success': True,
            'code': 200,
            'message': 'user successfully login',
            'data': token
        }

        return jsonable_encoder(response)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="invalid username or password")

@auth_router.get('/login/refresh')
async def refresh_token(Authorize: AuthJWT=Depends()):

    try:
        access_lifetime = datetime.timedelta(minutes=60)
        Authorize.jwt_refresh_token_required() # valid access tokendi talap etedi
        current_user = Authorize.get_jwt_subject() # access tokennen usernamedi ajiratip aladi

        #     db dan userdi filter qilip tabamiz
        db_user = session.query(User).filter(User.username == current_user).first() # bir obekt esabinda alamiz
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
        #  access token jaratamiz
        new_access_token = Authorize.create_access_token(subject=db_user.username, expires_time=access_lifetime)
        response_model = {
            'success': True,
            'code': 200,
            'message': 'new access token is created',
            'data': {
                'access token': new_access_token
            }
        }
        return response_model
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid refresh token')


@auth_router.put('/settings/update/{user_id}', status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: SignUpModel):
    existing_user = session.query(User).filter(User.id == user_id).first()
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User not found")

    if user.email != existing_user.email:
        db_email = session.query(User).filter(User.email == user.email).first()
        if db_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Email is already in use")

    if user.username != existing_user.username:
        db_username = session.query(User).filter(User.username == user.username).first()
        if db_username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="Username is already in use")

    existing_user.username = user.username
    existing_user.email = user.email
    if user.password:
        existing_user.password = generate_password_hash(user.password)

    session.commit()


    response_model = {
        'success': True,
        'code': 200,
        'message': 'User updated successfully',
        'data': {
                'id': existing_user.id,
                'username': existing_user.username,
                'email': existing_user.email
        }
    }

    return jsonable_encoder(response_model)