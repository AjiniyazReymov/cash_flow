from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from database import engine

from fastapi_jwt_auth import AuthJWT

from models import User, Debt
from schemas import DebtModel, DebtStatusModel
from database import session, engine
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends, status, Query

debt_router = APIRouter(
    prefix='/api'
)

session = session(bind=engine) # qaysi db ga baylanisiw kk ekenin korsetedi

@debt_router.post('/debt/to-me')
async def create_to_me(debt: DebtModel, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    # full_name = db.query(Debt)

    new_debt = Debt(
        first_name=debt.first_name,
        last_name=debt.last_name,
        debt_types=debt.debt_types,
        quantity=debt.quantity,
        valuta=debt.valuta,
        description=debt.description,
        data_incurred=debt.data_incurred,
        data_due=debt.data_due
    )
    new_debt.user = user
    session.add(new_debt)
    session.commit()
    data = {
        'success': True,
        'code': 200,
        'message': "Debt is created successfully",
        "data": {
            'id': new_debt.id,
            'full name': new_debt.full_name,
            'quantity': new_debt.quantity,
            'valuta': new_debt.valuta.value,
            'debt types': new_debt.debt_types.value,
            'description': new_debt.description,
            'data_incurred':  new_debt.data_incurred,
            'data_due': new_debt.data_due
        }
    }

    response = data

    return jsonable_encoder(response)

@debt_router.post('/debt/by-me')
async def create_by_me(debt: DebtModel, Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")

    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()

    new_debt = Debt(
        first_name=debt.first_name,
        last_name=debt.last_name,
        debt_types=debt.debt_types,
        quantity=-debt.quantity,
        valuta=debt.valuta,
        description=debt.description,
        data_incurred=debt.data_incurred,
        data_due=debt.data_due
    )
    new_debt.user = user
    session.add(new_debt)
    session.commit()
    data = {
        'success': True,
        'code': 200,
        'message': "Debt by_me is created successfully",
        "data": {
            'id': new_debt.id,
            'full name': new_debt.full_name,
            'debt types': new_debt.debt_types.value,
            'quantity': new_debt.quantity,
            'valuta': new_debt.valuta.value,
            'description': new_debt.description,
            'data_incurred':  new_debt.data_incurred,
            'data_due': new_debt.data_due
        }
    }

    response = data

    return jsonable_encoder(response)

@debt_router.put('/debt/{id}/update', status_code=status.HTTP_200_OK)
async def update_debt(id: int, debt: DebtModel, Authorize: AuthJWT=Depends()):
    # update
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    debt_to_update = session.query(Debt).filter(Debt.id == id).first()

    if debt_to_update:

        debt_to_update.first_name = debt.first_name,
        debt_to_update.last_name = debt.last_name,
        debt_to_update.debt_types = debt.debt_types,
        debt_to_update.quantity = debt.quantity,
        debt_to_update.valuta = debt.valuta,
        debt_to_update.description = debt.description,
        debt_to_update.data_incurred = debt.data_incurred,
        debt_to_update.data_due = debt.data_due
        session.commit()

        custom_response = {
            'success': True,
            'code': 200,
            'message': "Debt is updated successfully",
            "data": {
                'id': debt_to_update.id,
                'full name': debt_to_update.full_name,
                'debt types': debt_to_update.debt_types.value,
                'quantity': debt_to_update.quantity,
                'valuta': debt_to_update.valuta.value,
                'description': debt_to_update.description,
                'data_incurred': debt_to_update.data_incurred,
                'data_due': debt_to_update.data_due
            }
        }

        return jsonable_encoder(custom_response)


@debt_router.delete('/debt/{id}/delete', status_code=status.HTTP_204_NO_CONTENT)
async def delete_debt(id: int, Authorize: AuthJWT = Depends()):

    try:
        Authorize.jwt_required()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Enter valid access token"
        )


    debt_to_delete = session.query(Debt).filter(Debt.id == id).first()
    if not debt_to_delete:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Debt not found"
        )
    else:
        session.delete(debt_to_delete)
        session.commit()
        return None

@debt_router.get('/debt/list', status_code=status.HTTP_200_OK)
async def list_all_debt(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if user:
        debts = session.query(Debt).all()
        custom_data = [
            {
                'id': debt.id,
                'full name': debt.full_name,
                'debt types': debt.debt_types.value,
                'quantity': debt.quantity,
                'valuta': debt.valuta.value,
                'description': debt.description,
                'data_incurred': debt.data_incurred,
                'data_due': debt.data_due

            }
            for debt in debts
        ]
        return jsonable_encoder(custom_data)

@debt_router.get('/debt/list/to-me', status_code=status.HTTP_200_OK)
async def list_to_me_debt(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if user:
        debts = session.query(Debt).filter(Debt.debt_types == "OWED_TO")
        custom_data = [
            {
                'id': debt.id,
                'full name': debt.full_name,
                'debt types': debt.debt_types.value,
                'quantity': debt.quantity,
                'valuta': debt.valuta.value,
                'description': debt.description,
                'data_incurred': debt.data_incurred,
                'data_due': debt.data_due

            }
            for debt in debts
        ]
        return jsonable_encoder(custom_data)

@debt_router.get('/debt/list/by-me', status_code=status.HTTP_200_OK)
async def list_by_me_debt(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if user:
        debts = session.query(Debt).filter(Debt.debt_types == "OWED_BY")
        custom_data = [
            {
                'id': debt.id,
                'full name': debt.full_name,
                'debt types': debt.debt_types.value,
                'quantity': debt.quantity,
                'valuta': debt.valuta.value,
                'description': debt.description,
                'data_incurred': debt.data_incurred,
                'data_due': debt.data_due

            }
            for debt in debts
        ]
        return jsonable_encoder(custom_data)


@debt_router.get('/debt/list/individual', status_code=status.HTTP_200_OK)
async def list_individual_debt(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if user:
        debts = session.query(Debt).filter(Debt.debt_types == "INDIVIDUAL")
        custom_data = [
            {
                'id': debt.id,
                'full name': debt.full_name,
                'debt types': debt.debt_types.value,
                'quantity': debt.quantity,
                'valuta': debt.valuta.value,
                'description': debt.description,
                'data_incurred': debt.data_incurred,
                'data_due': debt.data_due

            }
            for debt in debts
        ]
        return jsonable_encoder(custom_data)


@debt_router.get('/debt/list/by-me', status_code=status.HTTP_200_OK)
async def list_by_me_debt(Authorize: AuthJWT=Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Enter valid access token")
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter(User.username == current_user).first()
    if user:
        debts = session.query(Debt).filter(Debt.debt_types == "OWED_BY")
        custom_data = [
            {
                'id': debt.id,
                'full name': debt.full_name,
                'debt types': debt.debt_types.value,
                'quantity': debt.quantity,
                'valuta': debt.valuta.value,
                'description': debt.description,
                'data_incurred': debt.data_incurred,
                'data_due': debt.data_due

            }
            for debt in debts
        ]
        return jsonable_encoder(custom_data)