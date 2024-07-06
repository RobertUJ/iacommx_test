from fastapi import APIRouter, status

# Import routers
from src.solicitudes.router import router as solicitudes_router

router = APIRouter()

# Include solicitudes router
router.include_router(
    solicitudes_router,
    prefix="/solicitudes",
    # dependencies=[Depends(auth.validate_token)],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not found"
        }
    },
    tags=["solicitudes"],  # tags are used to group endpoints in the docs
)
