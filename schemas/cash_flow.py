# Desc: Import necessary libraries and modules to create the Cash Flow schema.
from pydantic import BaseModel, Field
from typing import Optional

# Desc: Import components from my own modules to create the Cash Flow schema.
from enums.cash_flow import *

# Desc: Create the Cash Flow schema using the BaseModel class.
class CashFlowSchema(BaseModel):

    date: str = Field(..., alias='date')
    city: str = Field(..., alias='city')
    type: TaxCategories = Field(..., alias='type')
    description: str = Field(..., alias='description')
    document_type: DocumentType = Field(..., alias='document_type')
    ref_number: str = Field(..., alias='ref_number')
    tin: int = Field(..., alias='tin')
    name: str = Field(..., alias='name')
    transaction: Transactions = Field(..., alias='transaction')
    transaction_type: TransactionType = Field(..., alias='transaction_type')
    bank_entity: BanckEntities = Field(..., alias='bank_entity')
    ciiu: Optional[int] = Field(None, alias='ciiu')
    sub_total: float = Field(..., alias='sub_total')
    special_st: Optional[float] = Field(None, alias='special_st')
    withholding_tax: Optional[float] = Field(None, alias='withholding_tax')
    special_wt: Optional[float] = Field(None, alias='special_wt')
    ica_tax: Optional[float] = Field(None, alias='ica_tax')
    special_it: Optional[float] = Field(None, alias='special_it')
    iva_tax: Optional[float] = Field(None, alias='iva_tax')
    iva_discount: Optional[float] = Field(None, alias='iva_discount')
    total: float = Field(..., alias='total')

    class Config:
        # Desc: Allow the ORM mode.
        orm_mode = True