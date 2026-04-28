from datetime import datetime, timezone
from backend.app.core.firebase_config import get_firestore
from firebase_admin import firestore
from backend.app.schemas.todo import TodoCreate

db = get_firestore()

#Thêm một task mới
def create_todo(uid: str, todo: TodoCreate):
    doc_data = {
        "title": todo.title,
        "description": todo.description,
        "is_completed": todo.is_completed,
        "deadline": todo.deadline,
        "created_at": datetime.now(timezone.utc)
    }
    _, doc_ref = db.collection("users").document(uid).collection("todos").add(doc_data)
    return doc_ref.id

#Lấy danh sách tất cả task của người dùng
def get_user_todos(uid: str):
    todos_ref = (
        db.collection("users")
        .document(uid)
        .collection("todos")
        .order_by("created_at", direction=firestore.Query.DESCENDING)
    )
    
    docs = todos_ref.stream()
    
    result = []
    for d in docs:
        data = d.to_dict()
        result.append({
            "id": d.id,
            "title": data.get("title", ""),
            "description": data.get("description", ""),
            "is_completed": data.get("is_completed", False),
            "deadline": data.get("deadline")
        })
    return result

#Cập nhật trạng thái (Hoàn thành / Chưa hoàn thành)
def update_todo_status(uid: str, todo_id: str, is_completed: bool):
    try:
        doc_ref = db.collection("users").document(uid).collection("todos").document(todo_id)
        doc_ref.update({
            "is_completed": is_completed
        })
        return True
    except Exception:
        return False

#Xóa một task
def delete_todo(uid: str, todo_id: str):
    try:
        db.collection("users").document(uid).collection("todos").document(todo_id).delete()
        return True
    except Exception:
        return False