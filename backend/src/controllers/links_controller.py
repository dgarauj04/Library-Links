from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..config.database import get_db
from ..models.model import User, Link, Category
from ..schemas.link import LinkCreate, LinkResponse
from ..utils.auth import get_current_user

router = APIRouter(prefix="/api/links", tags=["Links"])

def link_to_response(link: Link) -> dict:
    return {
        "id": str(link.id),
        "title": link.title,
        "url": link.url,
        "description": link.description,
        "favicon_url": link.favicon_url,
        "faviconUrl": link.favicon_url,
        "tags": link.tags or [],
        "categoryId": str(link.category_id),
        "user_id": link.user_id,
        "created_at": link.created_at,
        "updated_at": link.updated_at
    }

@router.get("", response_model=List[LinkResponse])
def get_links(
    category_id: int = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Link).filter(Link.user_id == current_user.id)
    
    if category_id:
        query = query.filter(Link.category_id == category_id)
    
    links = query.all()
    
    return [
        LinkResponse(**link_to_response(link))
        for link in links
    ]


@router.post("", response_model=LinkResponse, status_code=status.HTTP_201_CREATED)
def create_link(
    link_data: LinkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = db.query(Category).filter(
        Category.id == link_data.category_id,
        Category.user_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada"
        )
    
    new_link = Link(
        title=link_data.title,
        url=link_data.url,
        description=link_data.description,
        favicon_url=link_data.favicon_url,
        tags=link_data.tags,
        category_id=link_data.category_id,
        user_id=current_user.id
    )
    
    db.add(new_link)
    db.commit()
    db.refresh(new_link)
    
    return LinkResponse(**link_to_response(new_link))


@router.get("/{link_id}", response_model=LinkResponse)
def get_link(
    link_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    link = db.query(Link).filter(
        Link.id == link_id,
        Link.user_id == current_user.id
    ).first()
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link não encontrado"
        )
    
    return LinkResponse(**link_to_response(link))


@router.put("/{link_id}", response_model=LinkResponse)
def update_link(
    link_id: int,
    link_data: LinkCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    link = db.query(Link).filter(
        Link.id == link_id,
        Link.user_id == current_user.id
    ).first()
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link não encontrado"
        )
    
    category = db.query(Category).filter(
        Category.id == link_data.category_id,
        Category.user_id == current_user.id
    ).first()
    
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoria não encontrada"
        )
    
    link.title = link_data.title
    link.url = link_data.url
    link.description = link_data.description
    link.favicon_url = link_data.favicon_url
    link.tags = link_data.tags
    link.category_id = link_data.category_id
    
    db.commit()
    db.refresh(link)
    
    return LinkResponse(**link_to_response(link))


@router.delete("/{link_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_link(
    link_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    link = db.query(Link).filter(
        Link.id == link_id,
        Link.user_id == current_user.id
    ).first()
    
    if not link:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Link não encontrado"
        )
    
    db.delete(link)
    db.commit()
    
    return None