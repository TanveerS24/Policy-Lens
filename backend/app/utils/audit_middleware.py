from fastapi import Request
from typing import Callable
from app.services.audit_service import audit_service


async def audit_middleware(request: Request, call_next: Callable):
    """
    Middleware to log audit trails for write operations
    
    This middleware logs all POST, PUT, PATCH, DELETE requests
    """
    # Get client info
    ip_address = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")
    
    # Process request
    response = await call_next(request)
    
    # Log audit trail for write operations
    if request.method in ["POST", "PUT", "PATCH", "DELETE"]:
        # Try to extract user info from token if available
        actor_id = "anonymous"
        actor_type = "system"
        
        auth_header = request.headers.get("authorization")
        if auth_header and auth_header.startswith("Bearer "):
            try:
                from app.utils.security import decode_token
                token = auth_header.split(" ")[1]
                payload = decode_token(token)
                if payload:
                    actor_id = payload.get("sub", actor_id)
                    # Determine actor type based on path
                    if "/admin/" in request.url.path:
                        actor_type = "admin"
                    elif "/patients/" in request.url.path:
                        actor_type = "patient"
            except:
                pass
        
        # Determine entity type from path
        path_parts = request.url.path.strip("/").split("/")
        entity_type = path_parts[-1] if path_parts else "unknown"
        
        # Log the action
        await audit_service.log_action(
            actor_type=actor_type,
            actor_id=actor_id,
            action=request.method.lower(),
            entity_type=entity_type,
            entity_id=None,  # Would need to extract from response body for specific entity ID
            ip_address=ip_address,
            user_agent=user_agent
        )
    
    return response
