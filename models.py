from database import Base
from sqlalchemy import Column, Integer, Boolean, Text, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship, Relationship
from sqlalchemy_utils.types import ChoiceType

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(70), unique=True)
    password = Column(Text, nullable=True)  #nullable=True - parol majbur emes


    def __repr__(self):
        return f"<user {self.username}"

class Debt(Base):
    CURENCY_STATUSES = (
        ("EUR", 'evro'),
        ('USD', 'dollar'),
        ('RUB', 'ruble'),
        ('UZS', 'som')
    )
    DEBT_TYPES = (
        ("OWED_TO", "owed_to"),
        ("OWED_BY", "owed_by"),
        ("INDIVIDUAL", "individual")
    )

    __tablename__ = 'debt'
    id = Column(Integer, primary_key=True)
    debt_types = Column(ChoiceType(choices=DEBT_TYPES), default = 'OWED_TO')
    first_name = Column(String(50))
    last_name = Column(String(50))
    quantity = Column(Integer)
    valuta = Column(ChoiceType(choices=CURENCY_STATUSES), default='UZS')
    description = Column(String(200), nullable=True)
    data_incurred = Column(DateTime)
    data_due = Column(DateTime)

    def __repr__(self):
        return f"<debt {self.debt_types}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"