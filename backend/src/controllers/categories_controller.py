from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..config.database import get_db
from ..models.model import User, Category
from ..schemas.category import CategoryCreate, CategoryResponse
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/categories", tags=["Categories"])

@router.get("", response_model=List[CategoryResponse])
def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    categories = db.query(Category).filter(
        Category.user_id == current_user.id
    ).all()
    
    return [
        CategoryResponse(
            id=str(cat.id),
            name=cat.name,
            slug=cat.slug,
            icon=cat.icon,
            description=cat.description,
            user_id=cat.user_id,
            created_at=cat.created_at
        )
        for cat in categories
    ]


@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    existing = db.query(Category).filter(
        Category.user_id == current_user.id,
        Category.slug == category_data.slug
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Categoria com este slug já existe"
        )
    
    new_category = Category(
        name=category_data.name,
        slug=category_data.slug,
        icon=category_data.icon,
        description=category_data.description,
        user_id=current_user.id
    )
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return CategoryResponse(
        id=str(new_category.id),
        name=new_category.name,
        slug=new_category.slug,
        icon=new_category.icon,
        description=new_category.description,
        user_id=new_category.user_id,
        created_at=new_category.created_at
    )


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada"
        )
    
    return CategoryResponse(
        id=str(category.id),
        name=category.name,
        slug=category.slug,
        icon=category.icon,
        description=category.description,
        user_id=category.user_id,
        created_at=category.created_at
    )


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    category_data: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada"
        )
    
    category.name = category_data.name
    category.slug = category_data.slug
    category.icon = category_data.icon
    category.description = category_data.description
    
    db.commit()
    db.refresh(category)
    
    return CategoryResponse(
        id=str(category.id),
        name=category.name,
        slug=category.slug,
        icon=category.icon,
        description=category.description,
        user_id=category.user_id,
        created_at=category.created_at
    )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = db.query(Category).filter(
        Category.id == category_id,
        Category.user_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada"
        )
    
    db.delete(category)
    db.commit()
    
    return None