"""Bill model classes for representing and managing bill data in the application."""

from datetime import datetime

date_now = datetime.now()

class BillStatus:
    """Enum representing the status of a bill."""
    Paid = 1
    Unpaid = 2
    Overdue = 3
    Cancelled = 4
    Refunded = 5
    PartiallyPaid = 6

class BillCategory:
    """Enum representing the category of a bill."""
    Food = "Comida"
    Protein = "Comida / Proteina"
    Transport = "Transporte"
    Clothes = "Ropa"
    Technology = "Tecnologia"
    Housing = "Vivienda"
    Education = "Educacion"
    Debt = "Deuda"
    Savings = "Ahorro"
    Ants = "Gastos Hormiga"
    Investment = "Inversion"
    Salary = "Sueldo"
    Unknown = "Unknown"

class BillMedium:
    """Enum representing the medium of a bill."""
    CreditCard = "Credit Card"
    Debit = "Debit"
    Loan = "Loan"
    Deel = "Deel"
    Binance = "Binance"
    Cash = "Cash"
    Unknown = "Unknown"

class Bill:
    """Class representing a bill."""
    id: int
    created_at: str = date_now.strftime("%Y-%m-%d %H:%M:%S")
    created_by: str = "Lambda Function"
    date: str | None
    category: BillCategory | None
    medium: BillMedium | None
    amount: float
    status: BillStatus = BillStatus.Unpaid
    notes: str | None
    updated_at: str | None
    updated_by: str | None
    deleted_at: str | None
    deleted_by: str | None

    def __init__(self, date: str | None, category: BillCategory | None, medium: BillMedium | None, amount: float, status: BillStatus, notes: str | None) -> None:
        self.date = date
        self.category = category
        self.medium = medium
        self.amount = amount
        self.status = status
        self.notes = notes
    def to_json_db(self) -> dict:
        """Convert the Bill object to a dictionary representation for database insertion."""
        return {
          "created_at": self.created_at,
          "created_by": self.created_by,
          "date": self.date,
          "category": self.category,
          "medium": self.medium,
          "amount": self.amount,
          "status": self.status,
          "notes": self.notes
        }
