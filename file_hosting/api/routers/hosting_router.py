from fastapi import APIRouter

from . import directories
from . import auth


router = APIRouter()

router.include_router(directories.router)
router.include_router(auth.router)
