from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=100)
    icon: Optional[str] = None
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: str  
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True
        
    @classmethod
    def from_orm(cls, obj):
        data = {
            "id": str(obj.id),
            "name": obj.name,
            "slug": obj.slug,
            "icon": obj.icon,
            "description": obj.description,
            "user_id": obj.user_id,
            "created_at": obj.created_at
        }
        return cls(**data)