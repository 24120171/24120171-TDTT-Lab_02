from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List

from backend.app.dependencies.auth import get_current_user
from backend.app.schemas.todo import TodoCreate, TodoResponse 
from backend.app.services.firestore_service import (
    create_todo, 
    get_user_todos, 
    update_todo_status,
    delete_todo
)

router = APIRouter(prefix="/todos", tags=["todo"])

#Lấy danh sách công việc
@router.get("", response_model=List[TodoResponse])
def get_todos(user=Depends(get_current_user)):
    try:
        todos = get_user_todos(user["uid"])
        return todos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Thêm một công việc mới
@router.post("", response_model=TodoResponse)
def add_todo(payload: TodoCreate, user=Depends(get_current_user)):
    try:
        #Gọi service để lưu vào Firestore
        todo_id = create_todo(user["uid"], payload)
        return {**payload.dict(), "id": todo_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Cập nhật trạng thái hoàn thành (Check/Uncheck)
@router.patch("/{todo_id}")
def toggle_todo(todo_id: str, is_completed: bool, user=Depends(get_current_user)):
    try:
        success = update_todo_status(user["uid"], todo_id, is_completed)
        if not success:
            raise HTTPException(status_code=404, detail="Không tìm thấy task")
        return {"status": "updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

#Xóa một công việc
@router.delete("/{todo_id}")
def remove_todo(todo_id: str, user=Depends(get_current_user)):
    try:
        success = delete_todo(user["uid"], todo_id)
        if not success:
            raise HTTPException(status_code=404, detail="Không tìm thấy task")
        return {"status": "deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))