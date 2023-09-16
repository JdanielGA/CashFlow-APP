# Desc: Import necessary libraries and modules to create the Cash Flow model.
from sqlalchemy import Column, Integer, String, Enum, ForeignKey, Float
from sqlalchemy.orm import relationship

# Desc: Import components from my own modules to create the Cash Flow model.
from config.database import Base
from enums.cash_flow import TaxCategories, DocumentType, Transactions, TransactionType, BanckEntities

# Desc: Create the Cash Flow model
class CashFlowModel(Base):

    __tablename__ = 'cash_flow'

    date = Column(String, nullable=False)
    city = Column(String, nullable=False)
    type = Column(Enum(TaxCategories), nullable=False)
    description = Column(String, nullable=False)
    document_type = Column(Enum(DocumentType), nullable=False)
    ref_number = Column(String, primary_key=True, nullable=False)
    tin = Column(Integer, ForeignKey('database.tin'), nullable=False)
    name = Column(String, nullable=False)
    transaction = Column(Enum(Transactions), nullable=False)
    transaction_type = Column(Enum(TransactionType), nullable=False)
    bank_entity = Column(Enum(BanckEntities), nullable=False)
    ciiu = Column(Integer, nullable=True)
    sub_total = Column(Float, nullable=False)
    special_st = Column(Float, nullable=True)
    withholding_tax = Column(Float)
    special_wt = Column(Float, nullable=True)
    ica_tax = Column(Float)
    special_it = Column(Float, nullable=True)
    iva_tax = Column(Float)
    iva_discount = Column(Float, nullable=True)
    total = Column(Float, nullable=False)

    database = relationship('DatabaseModel')


    # # Desc: Property to return the full name of the client according to the tin.
    # @property
    # def get_name(self):
    #     return self.database.name + ' ' + self.database.last_name
    
    # # Desc: Set the full name to the database model.
    # @get_name.setter
    # def get_name(self, value):
    #     self.database.name = value
