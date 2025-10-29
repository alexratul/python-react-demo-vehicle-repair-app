from sqlalchemy.orm import Session
from .models import Estimate, EstimateStatus


def seed(db: Session):
    if db.query(Estimate).count() == 0:
        samples = [
        Estimate(customer_name="Alice", vehicle="Toyota Corolla 2015", description="Front bumper replacement", amount=450.0, status=EstimateStatus.NEW),
        Estimate(customer_name="Bob", vehicle="Honda Civic 2018", description="Brake pads + rotors", amount=320.0, status=EstimateStatus.IN_PROGRESS),
        ]
    db.add_all(samples)
    db.commit()