# 學生修課分數系統 (Django 範例)

簡單的 Django 專案，示範學生、課程、任課老師與修課（Enrollment）功能。包含：

- 首頁：列出目前學生的修課與分數
- 課程明細：課名、課號、任課老師、修課學生與期中分數
- 新增課程：可從現有老師下拉選擇或輸入新增老師
- 加選 / 退選：以登入的 Student（或資料庫中的第一個 Student）為當前學生

快速上手

1. 建議在 virtualenv 中執行：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. 建立資料庫並套用 migrations：

```powershell
python manage.py makemigrations
python manage.py migrate
```

3. 建立樣本資料（會建立學生「莊閎翔」與三門課）：

```powershell
python manage.py populate_sample
```

4. 建立 superuser（進入 admin）：

```powershell
python manage.py createsuperuser
```

5. 啟動開發伺服器：

```powershell
python manage.py runserver
```

6. 前往 http://127.0.0.1:8000/ 查看網站，前往 /admin/ 管理資料。

備註
- 系統會自動為新註冊的 Django User 建立對應的 `Student` 實例（名稱預設為 username）。
- 須登入（或將 User 與 Student 在 admin 中關聯）才能以該登入帳號做加選/退選/新增課程的操作。
