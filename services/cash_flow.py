# Desc: Import the necesary libraries and modules to create the Cash Flow services.
from sqlalchemy import not_

# Desc: Import components from my own modules to create the Cash Flow services.
from schemas.cash_flow import CashFlowSchema
from models.cash_flow import CashFlowModel

# Desc: Cash Flow services class.
class CashFlowServices:
    def __init__(self, db):
        self.db = db

    # Desc: Function to get all the Cash Flow records.
    def get_all(self):
        records = self.db.query(CashFlowModel).all()
        return records