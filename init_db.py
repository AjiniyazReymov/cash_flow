from database import engine, Base
from models import User, Debt

Base.metadata.create_all(bind=engine) # db mn baylanistiriw ushin
