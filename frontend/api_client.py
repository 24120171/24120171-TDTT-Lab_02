import requests

API_BASE = "http://localhost:8000"

def signup(email: str, password: str):
    r = requests.post(f"{API_BASE}/auth/signup", json={
        "email": email,
        "password": password
    })
    r.raise_for_status()
    return r.json()

def login(email: str, password: str):
    r = requests.post(f"{API_BASE}/auth/login", json={
        "email": email,
        "password": password
    })
    r.raise_for_status()
    return r.json()

def google_login(id_token: str):
    r = requests.post(f"{API_BASE}/auth/google", json={
        "id_token": id_token
    })
    r.raise_for_status()
    return r.json()

#Lấy danh sách task
def get_todos(id_token: str):
    r = requests.get(
        f"{API_BASE}/todos",
        headers={"Authorization": f"Bearer {id_token}"}
    )
    r.raise_for_status()
    return r.json()

#Tạo một task mới
def create_todo(id_token: str, title: str, description: str = None, deadline: str = None):
    payload = {
        "title": title,
        "description": description,
        "deadline": deadline,
        "is_completed": False
    }
    r = requests.post(
        f"{API_BASE}/todos",
        json=payload,
        headers={"Authorization": f"Bearer {id_token}"}
    )
    r.raise_for_status()
    return r.json()

#Cập nhật trạng thái (để tích chọn hoàn thành)
def update_todo_status(id_token: str, todo_id: str, is_completed: bool):
    r = requests.patch(
        f"{API_BASE}/todos/{todo_id}",
        params={"is_completed": is_completed},
        headers={"Authorization": f"Bearer {id_token}"}
    )
    r.raise_for_status()
    return r.json()

#Xóa task
def delete_todo(id_token: str, todo_id: str):
    r = requests.delete(
        f"{API_BASE}/todos/{todo_id}",
        headers={"Authorization": f"Bearer {id_token}"}
    )
    r.raise_for_status()
    return r.json()