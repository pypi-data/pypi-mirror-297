from typing import Any

from fastapi import APIRouter
from sqlmodel import SQLModel, func, select

from mtmai.deps import CurrentUser, SessionDep
from mtmai.models.models import (
    Item,
)
from mtmai.models.site import Site, SiteBase

router = APIRouter()


class SiteItemPublic(SiteBase):
    id: str
    # owner_id: str


class ListSiteResponse(SQLModel):
    data: list[SiteItemPublic]
    count: int


@router.get("/", response_model=ListSiteResponse)
def list_sites(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve site items.
    """

    count_statement = (
        select(func.count()).select_from(Site).where(Item.owner_id == current_user.id)
    )
    count = session.exec(count_statement).one()
    statement = (
        select(Site).where(Site.owner_id == current_user.id).offset(skip).limit(limit)
    )
    items = session.exec(statement).all()

    return ListSiteResponse(data=items, count=count)


class SiteCreate(SiteBase):
    pass


@router.post("/", response_model=SiteItemPublic)
def create_Site(
    *, session: SessionDep, current_user: CurrentUser, item_in: SiteCreate
) -> Any:
    """
    Create new site.
    """
    item = Site.model_validate(item_in, update={"owner_id": current_user.id})
    session.add(item)
    session.commit()
    session.refresh(item)
    return item
