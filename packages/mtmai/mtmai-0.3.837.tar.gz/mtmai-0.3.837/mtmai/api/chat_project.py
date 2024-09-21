"""
博客系统api
"""

from fastapi import APIRouter

from mtmai.chainlit.types import GetThreadsRequest
from mtmai.crud import curd_chat
from mtmai.deps import AsyncSessionDep, CurrentUser

router = APIRouter()


@router.post("/threads")
async def get_user_threads(
    req: GetThreadsRequest,
    session: AsyncSessionDep,
    current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
):
    """Get the threads page by page."""
    # payload.filter.userId = current_user.id

    user_threads = await curd_chat.get_user_threads(
        session,
        current_user.id,
        # thread_id=req.filter.therad_id,
        limit=limit,
        skip=skip,
    )
    return user_threads
