from fastapi import APIRouter

from . import directories
from . import auth
from . import user
from . import files
from . import upload


router = APIRouter()

router.include_router(directories.router)
router.include_router(auth.router)
router.include_router(user.router)
router.include_router(files.router)
router.include_router(upload.router)
