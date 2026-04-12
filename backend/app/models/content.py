from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class FAQBase(BaseModel):
    question: str = Field(..., min_length=10, max_length=500)
    answer: str = Field(..., min_length=10, max_length=2000)
    category: str = Field(..., max_length=100, description="Category for grouping FAQs")
    display_order: int = Field(default=0, ge=0, description="Order for display")
    active: bool = Field(default=True)


class FAQCreate(FAQBase):
    pass


class FAQUpdate(BaseModel):
    question: Optional[str] = Field(None, min_length=10, max_length=500)
    answer: Optional[str] = Field(None, min_length=10, max_length=2000)
    category: Optional[str] = Field(None, max_length=100)
    display_order: Optional[int] = Field(None, ge=0)
    active: Optional[bool] = None


class FAQInDB(FAQBase):
    id: str = Field(..., alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class FAQPublic(FAQInDB):
    pass


class BannerBase(BaseModel):
    title: str = Field(..., min_length=5, max_length=200)
    description: str = Field(..., max_length=500)
    image_url: Optional[str] = Field(None, max_length=500)
    link_url: Optional[str] = Field(None, max_length=500)
    display_order: int = Field(default=0, ge=0)
    active: bool = Field(default=True)
    start_date: Optional[datetime] = Field(None)
    end_date: Optional[datetime] = Field(None)


class BannerCreate(BannerBase):
    pass


class BannerUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=200)
    description: Optional[str] = Field(None, max_length=500)
    image_url: Optional[str] = Field(None, max_length=500)
    link_url: Optional[str] = Field(None, max_length=500)
    display_order: Optional[int] = Field(None, ge=0)
    active: Optional[bool] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None


class BannerInDB(BannerBase):
    id: str = Field(..., alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        json_encoders = {datetime: lambda v: v.isoformat()}


class BannerPublic(BannerInDB):
    pass
