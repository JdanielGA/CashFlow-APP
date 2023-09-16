# Desc: Import the necessary libraries and modules to create roles.
from enum import Enum

# Desc: Create the transaction categories list class.
class TaxCategories(Enum):
    PINVOICE = 'Purchase Invoice'
    SINVOICE = 'Sale Invoice'
    OTHER = 'Other'

# Desc: Create the type of documents list class.
class DocumentType(Enum):
    EBILL = 'E-bill'
    CBILL = 'C-bill'
    ECREDITNOTE = 'E-credit note'
    NOTAPPLY = 'Not apply'

# Desc: Create the transaction types list class.
class Transactions(Enum):
    CREDIT = 'Credit'
    DEBIT = 'Debit'
    WITHDRAWAL = 'Withdrawal'
    DEPOSIT = 'Deposit'

# Desc: Create the type of transaction list class.
class TransactionType(Enum):
    PRODUCT = 'Product'
    SERVICE = 'Service'
    TRANSPORT = 'Transport'
    SEVERAL = 'Several'
    AIU = 'AIU'
    NOT_IVA = 'Not IVA'

# Desc: Create the bank entities list class.
class BanckEntities(Enum):
    DAVIVIENDA = 'Davivienda'
    BANCOLOMBIA = 'Bancolombia'
    CAJA_MENOR = 'Caja Menor'