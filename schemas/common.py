"""
Common Pydantic schemas for structured extraction tasks.
"""
from __future__ import annotations
from typing import Literal, Optional
from pydantic import BaseModel, Field


class SentimentResult(BaseModel):
    label: Literal["positive", "negative", "neutral", "mixed"]
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence score 0-1")
    reasoning: str = Field(..., description="Brief explanation of the sentiment")
    key_phrases: list[str] = Field(default_factory=list, description="Phrases that drove the classification")


class EntityList(BaseModel):
    people: list[str] = Field(default_factory=list)
    organizations: list[str] = Field(default_factory=list)
    locations: list[str] = Field(default_factory=list)
    dates: list[str] = Field(default_factory=list)
    products: list[str] = Field(default_factory=list)


class MeetingNotes(BaseModel):
    title: str
    date: Optional[str] = None
    attendees: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    action_items: list[dict] = Field(default_factory=list, description="List of {owner, task, due_date}")
    open_questions: list[str] = Field(default_factory=list)
    next_meeting: Optional[str] = None


class ProductReview(BaseModel):
    product_name: str
    overall_rating: float = Field(..., ge=1.0, le=5.0)
    pros: list[str] = Field(default_factory=list)
    cons: list[str] = Field(default_factory=list)
    use_case: Optional[str] = None
    would_recommend: bool
    summary: str


class ResearchPaper(BaseModel):
    title: str
    authors: list[str]
    year: Optional[int] = None
    abstract_summary: str = Field(..., description="2-3 sentence summary of the abstract")
    key_contributions: list[str]
    methodology: str
    datasets_used: list[str] = Field(default_factory=list)
    main_results: str
