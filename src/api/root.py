from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/")
def home():
    return Response(content="Welcome to the awesome API for ia.com.mx Test!")
