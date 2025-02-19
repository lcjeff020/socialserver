from typing import List, Optional
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app import crud, models, schemas

class TaskService:
    def create_task(
        self, 
        db: Session,
        task_in: schemas.TaskCreate,
        user: models.User
    ) -> models.Task:
        """Create a new task."""
        # Check if account belongs to user
        account = crud.account.get(db, id=task_in.account_id)
        if not account or account.user_id != user.id:
            raise HTTPException(
                status_code=404,
                detail="Account not found or does not belong to user"
            )
            
        task = crud.task.create_with_owner(
            db=db,
            obj_in=task_in,
            owner_id=user.id
        )
        return task

    def get_user_tasks(
        self,
        db: Session,
        user: models.User,
        skip: int = 0,
        limit: int = 100
    ) -> List[models.Task]:
        """Get all tasks for a user."""
        return crud.task.get_multi_by_owner(
            db=db,
            owner_id=user.id,
            skip=skip,
            limit=limit
        ) 