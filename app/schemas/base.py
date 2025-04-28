from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt

TIME_EXAMPLE = "2025-01-01T00:00:00"


class AbstractBaseSchema(BaseModel):
    """Базовая схема с основными полями для проектов и пожертвований."""
    full_amount: PositiveInt
    invested_amount: int = 0
    fully_invested: bool
    create_date: datetime = Field(..., example=TIME_EXAMPLE)
    close_date: Optional[datetime] = Field(None, example=TIME_EXAMPLE)
