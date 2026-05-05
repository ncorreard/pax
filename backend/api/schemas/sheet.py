from datetime import datetime
from pydantic import BaseModel, field_validator
from .exercise import ExerciseResponse


# ── Feuille ──────────────────────────────────────────────────────────────────

class SheetCreate(BaseModel):
    title: str
    description: str | None = None
    author: str | None = None
    keywords: list[str] | None = None
    level: str | None = None
    domain: str | None = None
    status: int = 1
    open_at: datetime | None = None
    close_at: datetime | None = None

    @field_validator("status")
    @classmethod
    def status_valid(cls, v: int) -> int:
        if v not in (0, 1, 3):
            raise ValueError("status doit être 0 (caché), 1 (visible) ou 3 (testez-vous)")
        return v


class SheetResponse(BaseModel):
    id: int
    title: str
    description: str | None
    author: str | None
    keywords: list[str] | None
    level: str | None
    domain: str | None
    status: int
    open_at: datetime | None
    close_at: datetime | None
    created_at: datetime

    model_config = {"from_attributes": True}


class SheetUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    author: str | None = None
    keywords: list[str] | None = None
    level: str | None = None
    domain: str | None = None
    status: int | None = None
    open_at: datetime | None = None
    close_at: datetime | None = None

    @field_validator("status")
    @classmethod
    def status_valid(cls, v: int | None) -> int | None:
        if v is not None and v not in (0, 1, 3):
            raise ValueError("status doit être 0 (caché), 1 (visible) ou 3 (testez-vous)")
        return v


class SheetDetailResponse(SheetResponse):
    items: list["SheetItemResponse"]


# ── Exercice dans une feuille ─────────────────────────────────────────────────

class SheetExerciseAdd(BaseModel):
    exercise_id: str
    position: int = 0
    points: int = 10
    weight: float = 1.0
    multiplicity: float = 1.0
    prerequisite: str | None = None
    active: bool = True

    @field_validator("prerequisite")
    @classmethod
    def prerequisite_format(cls, v: str | None) -> str | None:
        """Valide le format "N:score" ou "N+M+...:score"."""
        if v is None:
            return v
        import re
        if not re.fullmatch(r"[\d+]+:\d+", v):
            raise ValueError('prerequisite doit être au format "N:score" ou "N+M:score"')
        return v


class SheetItemResponse(BaseModel):
    id: int
    position: int
    points: int
    weight: float
    multiplicity: float
    prerequisite: str | None
    active: bool
    exercise: ExerciseResponse

    model_config = {"from_attributes": True}
