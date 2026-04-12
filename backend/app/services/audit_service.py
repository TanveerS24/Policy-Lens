from datetime import datetime
from typing import Optional, Dict, Any
from bson import ObjectId

from app.database.client import get_db


class AuditService:
    """Service for logging audit trails"""
    
    async def log_action(
        self,
        actor_type: str,
        actor_id: str,
        action: str,
        entity_type: str,
        entity_id: Optional[str] = None,
        before_json: Optional[Dict[str, Any]] = None,
        after_json: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ):
        """
        Log an action to the audit log
        
        Args:
            actor_type: Type of actor (patient, admin, system)
            actor_id: ID of the actor
            action: Action performed
            entity_type: Type of entity affected
            entity_id: ID of entity affected
            before_json: State before change
            after_json: State after change
            ip_address: IP address of request
            user_agent: User agent string
        """
        db = get_db()
        
        await db["audit_logs"].insert_one({
            "actor_type": actor_type,
            "actor_id": actor_id,
            "action": action,
            "entity_type": entity_type,
            "entity_id": entity_id,
            "before_json": before_json,
            "after_json": after_json,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "created_at": datetime.utcnow()
        })
    
    async def get_audit_logs(
        self,
        actor_type: Optional[str] = None,
        actor_id: Optional[str] = None,
        entity_type: Optional[str] = None,
        entity_id: Optional[str] = None,
        limit: int = 50,
        skip: int = 0
    ):
        """
        Get audit logs with filters
        
        Args:
            actor_type: Filter by actor type
            actor_id: Filter by actor ID
            entity_type: Filter by entity type
            entity_id: Filter by entity ID
            limit: Max results
            skip: Skip results
        
        Returns:
            List of audit logs
        """
        db = get_db()
        
        query: dict = {}
        if actor_type:
            query["actor_type"] = actor_type
        if actor_id:
            query["actor_id"] = actor_id
        if entity_type:
            query["entity_type"] = entity_type
        if entity_id:
            query["entity_id"] = entity_id
        
        cursor = db["audit_logs"].find(query).sort([("created_at", -1)]).skip(skip).limit(limit)
        return [log async for log in cursor]
    
    async def get_entity_history(self, entity_type: str, entity_id: str, limit: int = 20):
        """
        Get full history of changes for an entity
        
        Args:
            entity_type: Type of entity
            entity_id: ID of entity
            limit: Max results
        
        Returns:
            List of audit logs for the entity
        """
        return await self.get_audit_logs(
            entity_type=entity_type,
            entity_id=entity_id,
            limit=limit
        )


audit_service = AuditService()
