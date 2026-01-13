from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime

class LinkBase(BaseModel):
    title: str = Field(..., max_length=200)
    url: str
    description: Optional[str] = None
    favicon_url: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    category_id: str  
    
    @field_validator('category_id', mode='before')
    @classmethod
    def convert_category_id(cls, v):
        return str(v)

class LinkCreate(LinkBase):
    pass

class LinkResponse(BaseModel):
    id: str 
    title: str
    url: str
    description: Optional[str] = None
    favicon_url: Optional[str] = Field(None, alias="favicon_url")
    tags: List[str]
    categoryId: str 
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True
        
    @classmethod
    def from_orm(cls, obj):
        data = {
            "id": str(obj.id),
            "title": obj.title,
            "url": obj.url,
            "description": obj.description,
            "favicon_url": obj.favicon_url,
            "tags": obj.tags or [],
            "categoryId": str(obj.category_id),  
            "user_id": obj.user_id,
            "created_at": obj.created_at,
            "updated_at": obj.updated_at
        }
        return cls(**data)