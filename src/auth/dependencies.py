""" Module for dependencies permission on routes.  """
from fastapi import Depends, HTTPException, status


def check_token_is_valid(token: str):
    """ Check if token is valid """
    return token == "valid_token"


def check_user_has_permission(token: str = Depends(check_token_is_valid)):
    """ Check if user has permission 
    Args:
        token (str): Token to check
    """
    if not token:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User has no permission",
        ) 
    
    return token
