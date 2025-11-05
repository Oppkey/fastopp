"""
Flexible template context processor for authentication state
Can be used across different FastAPI applications with different auth systems
"""
import logging
from typing import Any, Callable, Dict, Optional

from fastapi import Request

logger = logging.getLogger(__name__)


class TemplateContextProvider:
    """
    Flexible template context provider that can be configured for different auth systems
    """
    
    def __init__(
        self,
        auth_cookie_name: str = "access_token",
        session_token_key: str = "token",
        user_attributes: Optional[Dict[str, str]] = None
    ):
        """
        Initialize the template context provider
        
        Args:
            auth_cookie_name: Name of the authentication cookie
            session_token_key: Key for session token storage
            user_attributes: Mapping of session keys to user attributes
        """
        self.auth_cookie_name = auth_cookie_name
        self.session_token_key = session_token_key
        self.user_attributes = user_attributes or {
            "is_superuser": "is_superuser",
            "is_staff": "is_staff", 
            "user_email": "user_email",
            "user_group": "group"
        }
    
    def get_template_context(self, request: Request, **kwargs) -> Dict[str, Any]:
        """
        Get template context with authentication state
        
        Args:
            request: FastAPI request object
            **kwargs: Additional context to merge
            
        Returns:
            Dictionary with authentication context
        """
        # Check for authentication cookie
        has_auth_cookie = bool(request.cookies.get(self.auth_cookie_name))
        
        # Check for session token
        has_session_token = bool(request.session.get(self.session_token_key))
        
        # Basic authentication state
        auth_state = {
            "is_authenticated": has_auth_cookie or has_session_token,
            f"has_{self.auth_cookie_name}": has_auth_cookie,
            "has_session_token": has_session_token,
            "current_user": None,
        }
        
        # Add user attributes from session if available
        if has_session_token:
            for attr_name, session_key in self.user_attributes.items():
                auth_state[attr_name] = request.session.get(session_key, False if attr_name.startswith('is_') else None)
        
        # Merge with any additional context
        auth_state.update(kwargs)
        
        return auth_state


# Default instance for backward compatibility
_default_provider = TemplateContextProvider()


def get_template_context(request: Request, **kwargs) -> Dict[str, Any]:
    """
    Default template context function for backward compatibility
    
    Args:
        request: FastAPI request object
        **kwargs: Additional context to merge
        
    Returns:
        Dictionary with authentication context
    """
    return _default_provider.get_template_context(request, **kwargs)


def create_template_context_provider(
    auth_cookie_name: str = "access_token",
    session_token_key: str = "token", 
    user_attributes: Optional[Dict[str, str]] = None
) -> TemplateContextProvider:
    """
    Create a custom template context provider for different auth systems
    
    Args:
        auth_cookie_name: Name of the authentication cookie
        session_token_key: Key for session token storage
        user_attributes: Mapping of session keys to user attributes
        
    Returns:
        Configured TemplateContextProvider instance
        
    Example:
        # For a different auth system
        provider = create_template_context_provider(
            auth_cookie_name="jwt_token",
            session_token_key="auth_token",
            user_attributes={
                "is_admin": "admin",
                "user_name": "username",
                "user_role": "role"
            }
        )
    """
    return TemplateContextProvider(
        auth_cookie_name=auth_cookie_name,
        session_token_key=session_token_key,
        user_attributes=user_attributes
    )
