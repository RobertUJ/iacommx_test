""" Module for health check method """
from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/_healthcheck")
def health_check():
    return Response(content="OK")
