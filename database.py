from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('postgresql://postgres:10032011@localhost/cash_flow',
                       echo=True) # (echo=True) - log fayl jaratadi

Base = declarative_base() #models.py da usi Base den paydalanamiz
session = sessionmaker() # CRUD operatsiyalardi orinlaw ushin sessionlardan paydalanamiz