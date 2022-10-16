from fastapi import APIRouter

from . import directories


router = APIRouter()

router.include_router(directories.router)
