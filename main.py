import json
import os
import customtkinter as ctk
import requests

# Dastur mavzusi
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

API_BASE_URL = "http://127.0.0.1:8000/api"
TOKEN_FILE = "tokens.json"


# ==========================================
# HELPER FUNCTIONS (TOKEN MANAGEMENT)
# ==========================================
def save_tokens(access, refresh):
    with open(TOKEN_FILE, "w") as f:
        json.dump({"access": access, "refresh": refresh}, f)

def load_tokens():
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return None
    return None

def clear_tokens():
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)


# ==========================================
# 1. LOGIN PAGE
# ==========================================
class LoginPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Tizimga Kirish", font=("Arial", 22, "bold"))
        label.pack(pady=(40, 20))

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username", width=280)
        self.username_entry.pack(pady=10)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Parol", show="*", width=280)
        self.password_entry.pack(pady=10)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=5)

        login_btn = ctk.CTkButton(self, text="Kirish", width=280, command=self.login)
        login_btn.pack(pady=10)

        reg_btn = ctk.CTkButton(self, text="Ro'yxatdan o'tish", width=280, fg_color="transparent", border_width=1,
                                command=lambda: controller.show_frame("RegisterPage"))
        reg_btn.pack(pady=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.error_label.configure(text="Barcha maydonlarni to'ldiring!")
            return

        try:
            response = requests.post(f"{API_BASE_URL}/token/", json={"username": username, "password": password})
            if response.status_code == 200:
                data = response.json()
                save_tokens(data["access"], data["refresh"])
                self.error_label.configure(text="")
                self.username_entry.delete(0, 'end')
                self.password_entry.delete(0, 'end')
                self.controller.show_frame("MainPage")
            else:
                self.error_label.configure(text="Username yoki parol xato!")
        except Exception as e:
            self.error_label.configure(text="Serverga ulanib bo'lmadi!")


# ==========================================
# 2. REGISTER PAGE
# ==========================================
class RegisterPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Ro'yxatdan O'tish", font=("Arial", 22, "bold"))
        label.pack(pady=(30, 15))

        self.username_entry = ctk.CTkEntry(self, placeholder_text="Username", width=280)
        self.username_entry.pack(pady=8)

        self.email_entry = ctk.CTkEntry(self, placeholder_text="Email", width=280)
        self.email_entry.pack(pady=8)

        self.password_entry = ctk.CTkEntry(self, placeholder_text="Parol", show="*", width=280)
        self.password_entry.pack(pady=8)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=5)

        register_btn = ctk.CTkButton(self, text="Hisob Yaratish", width=280, command=self.do_register)
        register_btn.pack(pady=10)

        back_btn = ctk.CTkButton(self, text="Orqaga (Login)", width=280, fg_color="transparent", border_width=1,
                                 command=lambda: controller.show_frame("LoginPage"))
        back_btn.pack(pady=5)

    def do_register(self):
        username = self.username_entry.get()
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.error_label.configure(text="Username va parolni kiriting!")
            return

        try:
            response = requests.post(f"{API_BASE_URL}/register/", json={
                "username": username, "email": email, "password": password
            })
            if response.status_code in [200, 201]:
                self.error_label.configure(text="")
                self.controller.show_frame("LoginPage")
            else:
                self.error_label.configure(text="Xatolik! Ma'lumotlarni tekshiring.")
        except Exception:
            self.error_label.configure(text="Server bilan aloqa yo'q!")


# ==========================================
# 3. MAIN PAGE (TASKS)
# ==========================================
class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Navigation Header
        header = ctk.CTkFrame(self, height=50)
        header.pack(fill="x", padx=10, pady=5)  # padx va pady deb o'zgartiring

        title = ctk.CTkLabel(header, text="Mening Topshiriqlarim", font=("Arial", 18, "bold"))
        title.pack(side="left", padx=15)

        profile_btn = ctk.CTkButton(header, text="Profil 👤", width=80, command=lambda: controller.show_frame("ProfilePage"))
        profile_btn.pack(side="right", padx=10, pady=5)

        # Input Area (Bitta katta text area yoki input)
        self.task_entry = ctk.CTkEntry(self, placeholder_text="Yangi topshiriq yozing...", width=450)
        self.task_entry.pack(pady=15, side="top")

        add_btn = ctk.CTkButton(self, text="Qo'shish", width=100, command=self.add_task)
        add_btn.pack(pady=5)

        # Tasks Scrollable List
        self.scroll_frame = ctk.CTkScrollableFrame(self, width=600, height=350)
        self.scroll_frame.pack(pady=15, fill="both", expand=True)

    def on_show(self):
        """Sahifaga o'tganda avtomatik ma'lumotlarni yuklaydi"""
        self.load_tasks()

    def load_tasks(self):
        tokens = load_tokens()
        if not tokens:
            self.controller.show_frame("LoginPage")
            return

        # Pylance uchun kafolat beramiz:
        assert tokens is not None

        # Endi bu qatorda (195-qator) Pylance umuman xato bermaydi:
        headers = {"Authorization": f"Bearer {tokens['access']}"}

    def add_task(self):
        title = self.task_entry.get()
        if not title:
            return
        tokens = load_tokens()
        if tokens and "access" in tokens:
            headers = {"Authorization": f"Bearer {tokens['access']}"}
            requests.post(f"{API_BASE_URL}/tasks/", json={"title": title}, headers=headers)
            self.task_entry.delete(0, 'end')
            self.load_tasks()


# ==========================================
# 4. PROFILE PAGE
# ==========================================
class ProfilePage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        label = ctk.CTkLabel(self, text="Foydalanuvchi Profili", font=("Arial", 22, "bold"))
        label.pack(pady=20)

        self.info_label = ctk.CTkLabel(self, text="Yuklanmoqda...", font=("Arial", 14), justify="left")
        self.info_label.pack(pady=20)

        back_btn = ctk.CTkButton(self, text="Asosiy Sahifaga Qaytish", command=lambda: controller.show_frame("MainPage"))
        back_btn.pack(pady=10)

        logout_btn = ctk.CTkButton(self, text="Chiqish (Logout)", fg_color="red", hover_color="darkred", command=self.logout)
        logout_btn.pack(pady=10)

    def on_show(self):
        self.load_profile()

    def load_profile(self):
        tokens = load_tokens()
        if not tokens:
            self.controller.show_frame("LoginPage")
            return

        headers = {"Authorization": f"Bearer {tokens['access']}"}
        try:
            res = requests.get(f"{API_BASE_URL}/profile/", headers=headers)
            if res.status_code == 200:
                data = res.json()
                text = (
                    f"Username: {data.get('username')}\n\n"
                    f"Email: {data.get('email')}\n\n"
                    f"Yosh: {data.get('age', 'Kiritilmagan')}\n\n"
                    f"Manzil: {data.get('location', 'Kiritilmagan')}\n\n"
                    f"Jami Topshiriqlar: {data.get('tasks_count', 0)}"
                )
                self.info_label.configure(text=text)
        except Exception:
            self.info_label.configure(text="Profil ma'lumotlarini olib bo'lmadi.")

    def logout(self):
        clear_tokens()
        self.controller.show_frame("LoginPage")


# ==========================================
# MAIN APP ROUTER (CONTAINER)
# ==========================================
class WeeklyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Weekly Planner - Desktop")
        self.geometry("700x550")
        self.minsize(600, 500)

        # Container (barcha sahifalar joylashadigan asosiy ramka)
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        # Sahifalarni ro'yxatdan o'tkazamiz
        for PageClass in (LoginPage, RegisterPage, MainPage, ProfilePage):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Ishga tushganda token bormi-yo'qligini tekshirish
        if load_tokens():
            self.show_frame("MainPage")
        else:
            self.show_frame("LoginPage")

    def show_frame(self, page_name):
        """Sahifalarni almashtirish funksiyasi"""
        frame = self.frames[page_name]
        frame.tkraise()
        # Agar sahifada on_show metodi bo'lsa, uni chaqiramiz (ma'lumotlarni yangilash uchun)
        if hasattr(frame, "on_show"):
            frame.on_show()


if __name__ == "__main__":
    app = WeeklyApp()
    app.mainloop()