import streamlit as st
import requests
from datetime import datetime
# Import các hàm mới từ api_client
from api_client import signup, login, google_login, get_todos, create_todo, update_todo_status, delete_todo

st.set_page_config(page_title="To-do App", page_icon="✅")

# --- QUẢN LÝ TRẠNG THÁI ---
if "user" not in st.session_state:
    st.session_state.user = None

if "todos" not in st.session_state:
    st.session_state.todos = []

if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

if "show_login" not in st.session_state:
    st.session_state.show_login = True

# --- HÀM HỖ TRỢ ---
def load_todos():
    if not st.session_state.user:
        return
    try:
        # Gọi API lấy danh sách task
        todos = get_todos(st.session_state.user["idToken"])
        st.session_state.todos = todos
    except Exception as e:
        st.error(f"Không thể tải danh sách: {e}")

def clear_google_query_params():
    try:
        st.query_params.clear()
    except Exception:
        pass

# --- XỬ LÝ LOGIN ---
def handle_google_login_callback():
    if st.session_state.user: return
    params = st.query_params
    raw_token = params.get("id_token")
    if not raw_token: return
    id_token = raw_token[0] if isinstance(raw_token, list) else raw_token
    try:
        user = google_login(id_token)
        st.session_state.user = user
        load_todos()
        clear_google_query_params()
        st.rerun()
    except Exception as e:
        st.error(f"Lỗi Google login: {e}")
        clear_google_query_params()

# --- GIAO DIỆN ĐĂNG NHẬP/ĐĂNG KÝ ---
def login_form():
    st.subheader("Đăng nhập")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        if st.form_submit_button("Đăng nhập"):
            try:
                user = login(email, password)
                st.session_state.user = user
                load_todos()
                st.rerun()
            except Exception as e: st.error(f"Lỗi: {e}")
        if st.form_submit_button("Chưa có tài khoản? Đăng ký"):
            st.session_state.show_signup = True
            st.rerun()
    st.markdown("<br><h4 style='text-align: center;'>Hoặc</h4>", unsafe_allow_html=True)

    try:
        # Lấy URL từ secrets.toml
        google_login_url = st.secrets["google-login"]["google-url"]
        
        st.markdown(
            f'''
            <a href="{google_login_url}" target="_self" style="
                display: inline-block;
                width: 100%;
                text-align: center;
                padding: 0.6rem 1rem;
                background-color: white;
                color: black;
                text-decoration: none;
                border-radius: 0.5rem;
                border: 1px solid #ddd;
                font-weight: 600;
            ">
                🔵 Đăng nhập với Google
            </a>
            ''',
            unsafe_allow_html=True,
        )
    except Exception:
        st.info("Chưa cấu hình Google-login trong .streamlit/secrets.toml")

def signup_form():
    st.subheader("Đăng ký")
    with st.form("signup_form"):
        email = st.text_input("Email")
        password = st.text_input("Mật khẩu", type="password")
        if st.form_submit_button("Tạo tài khoản"):
            try:
                signup(email, password)
                st.success("Thành công! Hãy đăng nhập")
                st.session_state.show_signup = False
                st.rerun()
            except Exception as e: st.error(f"Lỗi: {e}")
        if st.form_submit_button("Quay lại Đăng nhập"):
            st.session_state.show_signup = False
            st.rerun()

# --- GIAO DIỆN CHÍNH ---
handle_google_login_callback()
st.title("✅ To-do List")

if st.session_state.user:
    col_user, col_logout = st.columns([0.8, 0.2])
    col_user.write(f"Chào, **{st.session_state.user['email']}**")
    if col_logout.button("Đăng xuất"):
        st.session_state.user = None
        st.session_state.todos = []
        st.rerun()

    st.divider()

    #THÊM TASK MỚI
    with st.expander("➕ Thêm công việc mới", expanded=True):
        with st.form("add_todo_form", clear_on_submit=True):
            title = st.text_input("Tên công việc", placeholder="Ví dụ: Làm bài Lab 2")
            desc = st.text_area("Mô tả chi tiết")
            deadline = st.date_input("Hạn chót")
            if st.form_submit_button("Lưu công việc"):
                if title:
                    create_todo(st.session_state.user["idToken"], title, desc, str(deadline))
                    load_todos()
                    st.rerun()
                else:
                    st.warning("Vui lòng nhập tiêu đề!")

    #HIỂN THỊ DANH SÁCH TASK
    st.subheader("Danh sách việc cần làm")
    if not st.session_state.todos:
        st.info("Bạn chưa có công việc nào. Hãy thêm ở trên!")
    else:
        for todo in st.session_state.todos:
            with st.container(border=True):
                c1, c2, c3 = st.columns([0.1, 0.7, 0.2])
                
                # Checkbox để đánh dấu hoàn thành
                is_done = c1.checkbox("", value=todo['is_completed'], key=f"check_{todo['id']}")
                if is_done != todo['is_completed']:
                    update_todo_status(st.session_state.user["idToken"], todo['id'], is_done)
                    load_todos()
                    st.rerun()

                # Hiển thị nội dung (gạch ngang nếu xong)
                display_title = f"~~{todo['title']}~~" if todo['is_completed'] else todo['title']
                c2.markdown(f"**{display_title}**")
                if todo['description']:
                    c2.caption(todo['description'])
                if todo['deadline']:
                    c2.caption(f"📅 Hạn chót: {todo['deadline']}")

                # Nút xóa
                if c3.button("🗑️ Xóa", key=f"del_{todo['id']}"):
                    delete_todo(st.session_state.user["idToken"], todo['id'])
                    load_todos()
                    st.rerun()

else:
    if st.session_state.show_signup:
        signup_form()
    else:
        login_form()