---
name: post-fanpage-fb
description: Tự động hóa đăng bài viết lên Facebook Fanpage và gửi tin nhắn Chăm Sóc Khách Hàng (CSKH) qua Facebook Graph API
---

# Skill: Tự động hóa đăng bài Fanpage & gửi tin nhắn CSKH Messenger qua Facebook API

Bộ skill này hướng dẫn cách cài đặt và vận hành công cụ tự động hóa **đăng bài viết (kèm ảnh)** lên Facebook Fanpage và **gửi tin nhắn Chăm Sóc Khách Hàng (CSKH)** từ Google Sheets thông qua Facebook Graph API chính thức bằng Python.

---

## 1. Mục đích và Các Khái Niệm Quan Trọng

- **Tính Năng**: Bot tự động quét dữ liệu từ Google Sheets (danh sách bài đăng có nội dung, hình ảnh), sử dụng Facebook Graph API để đăng bài lên Fanpage, sau đó tự động cập nhật trạng thái đã đăng thành công/thất bại vào lại Google Sheets.
- **Sử Dụng API Chính Chủ**: Việc dùng Facebook Graph API có ưu điểm tuyệt đối so với giả lập trình duyệt (Selenium): Tốc độ cực nhanh, không qua màn hình, hoạt động ngầm hoàn toàn và không lo bị khóa tài khoản do hành vi chuột.

---

## 2. Triển Khai Trên Máy Mới (Từ A đến Z)

### Bước 0: Clone repo về máy
Nếu **chưa có** thư mục dự án trên máy:
```powershell
git clone https://github.com/quocdat16061990/POST_FANPAGE_FB.git
cd POST_FANPAGE_FB
```

### Bước 1: BẮT BUỘC - Chuẩn bị file JSON Service Account (Google)

> ⚠️ **KHÔNG CÓ FILE NÀY THÌ BOT KHÔNG ĐỌC ĐƯỢC SHEET!**

File JSON này là chìa khóa để Bot đọc/ghi dữ liệu ở Google Sheets:
1. Vào [Google Cloud Console](https://console.cloud.google.com/), tạo **Service Account** với quyền quản lý Google Sheets API.
2. Tạo và tải xuống file **JSON key** cho Service Account đó.
3. **Copy file JSON vào thư mục gốc** của dự án.
4. **Share Google Sheet cho email của Service Account**: Mở bảng tính Google Web, nhấn nút Share và paste địa chỉ email `client_email` lấy từ file JSON (VD: `bot-abc@project-xyz.iam.gserviceaccount.com`) vào, cấp quyền **Editor**.

### Bước 1.1: BẮT BUỘC - Chuẩn bị Page Access Token của Facebook Fanpage

> ⚠️ **CẦN KẾT NỐI FACEBOOK GRAPH API ĐỂ ĐĂNG BÀI:**

1. Vào [Facebook Developers](https://developers.facebook.com/), tạo/cấp quyền App và tạo **Page Access Token** vĩnh viễn (hoặc dài hạn) của Fanpage bạn muốn bot tự đăng.
2. Lấy **Page ID** của Fanpage.
3. Đặt các khóa này vào file môi trường (`.env`) hoặc khai báo biến. Ví dụ:
   ```env
   PAGE_ACCESS_TOKEN=token_cua_ban_o_day
   PAGE_ID=id_fanpage_cua_ban
   ```

### Bước 2: Cài đặt Python và tạo môi trường ảo

```powershell
# 1. Kiểm tra Python đã cài chưa
python --version

# 2. Tạo môi trường ảo (chỉ làm 1 lần)
py -m venv venv

# 3. Kích hoạt môi trường ảo
.\venv\Scripts\Activate.ps1
# Hoặc dùng CMD: .\venv\Scripts\activate.bat

# 4. Cài toàn bộ thư viện cần thiết
pip install --upgrade pip
pip install requests gspread pandas oauth2client pyinstaller python-dotenv
```
*(Ghi chú: Thư viện `requests` dùng để gọi Facebook API, còn lại là xử lý Sheet).*

### Bước 3: Chuẩn bị thư mục images

- **Thư mục images**: Tạo một thư mục `images/` ở ngay gốc dự án. Mọi file ảnh cần đăng sẽ để vào đây. Tên ảnh cần khớp với khai báo trên Sheet (vd khai `anh-san-pham` trên Sheet thì phải có file `anh-san-pham.png` hoặc `.jpg` trong thư mục này).

---

## 3. Cách Khởi Chạy (Run Chương Trình)

### Option A: Chạy Auto Đăng Bài Fanpage
```powershell
.\venv\Scripts\python.exe scripts\Facebook_Post_Bai_Fanpage.py
```

### Option B: Chạy Auto Gửi Tin Nhắn CSKH
```powershell
.\venv\Scripts\python.exe scripts\Facebook_Message_CSKH.py
```

### Option C: Build file .exe chạy thực tế

Build một lần, click đúp file `.exe` sử dụng độc lập (không cần cài Python):

```powershell
.\venv\Scripts\pyinstaller.exe --onefile --distpath . scripts\Facebook_Post_Bai_Fanpage.py
```

> ⚠️ **Lưu ý quan trọng khi dùng file .exe**:
> - File `.exe` phải đặt **cùng cấp** với file JSON credentials, thư mục `images/` và file `.env`.
> - Thư mục `build/` sinh ra sau build có thể xóa.

---

## 4. Cấu Hình Google Sheet Quản Lý

### 4.1 Tab "Fanpage" (Dành cho Auto Đăng Bài)
Sheet quản lý (Worksheet dự kiến) cần có các cột:

| Cột | Mô tả |
|-----|-------|
| `Tiêu Đề` | Tiêu đề của bài viết (có thể dùng để nhận diện nhanh trong file hoặc làm dòng đầu tiên) |
| `Mô Tả` | Nội dung văn bản (Caption) sẽ đăng lên Fanpage. Có thể chứa emoji hoặc xuống dòng |
| `Images` | Tên tệp ảnh đại diện cần tải lên (Ví dụ: `khung_anh_1` => tìm trong `/images/khung_anh_1.jpg`) |
| `Status` | Trạng thái xử lý: `PENDING` hoặc `UNAPPROVED` (chờ gửi), `APPROVED` (đã đăng), `ERROR` (lỗi up api) |

> Bot quét Google Sheet lọc các dòng `Status = UNAPPROVED` (hoặc `PENDING`). Gửi Graph API báo kết quả về. Tùy HTTP Status Code sẽ cập nhật giá trị vào `Status`.

### 4.2 Tab "Chăm Sóc Khách Hàng" (Dành cho Auto Gửi Tin Nhắn)
Sheet quản lý cần có các cột:

| Cột | Mô tả |
|-----|-------|
| `ID` | Bắt buộc là PSID (Page-Scoped ID) của khách hàng trên Facebook Messenger. |
| `Tên Khách Hàng` | Tên khách hàng (để theo dõi, không bắt buộc dùng trong API). |
| `Tin Nhắn` | Nội dung tin nhắn cần gửi cho khách hàng. |
| `Trạng Thái` | Trạng thái xử lý: `UNAPPROVED` (chờ gửi), `APPROVED` (đã gửi thành công), `ERROR` (lỗi API). |

---

## 5. API Logic - Các Endpoints Cơ Bản Cần Tham Khảo

Sử dụng thư viện `requests` để tương tác:

- **Đăng trạng thái chỉ có text**:
  ```http
  POST https://graph.facebook.com/v19.0/{PAGE_ID}/feed
  ```
  Truyền tham số `message=<Nội Dung>` và `access_token=<PAGE_ACCESS_TOKEN>`

- **Đăng bài kèm ảnh**:
  ```http
  POST https://graph.facebook.com/v19.0/{PAGE_ID}/photos
  ```
  Thông thường cần truyền `message=<Caption>` và đính kèm `source` ở dạng tập tin (multipart file stream), và tất nhiên `access_token`.

- **Gửi tin nhắn (CSKH)**:
  ```http
  POST https://graph.facebook.com/v19.0/me/messages
  ```
  Truyền tham số `access_token=<PAGE_ACCESS_TOKEN>` và JSON body chứa `recipient.id` (PSID) và `message.text`. Lưu ý luật 24h của Messenger (có thể cần `messaging_type="MESSAGE_TAG"`).

---

## 6. Gitignore Khuyến Nghị

```gitignore
# PyInstaller
build/
dist/
*.spec
*.exe

# Keys & Auth (Tuyệt đối không đẩy lên repo public!)
*.json
.env

# Virtual Environment
venv/
__pycache__/
```

---

## 7. Tích Hợp Tự Động Vào OpenClaw Assistant Workspace

Để trợ lý OpenClaw nhận diện và biết cách tự động thực thi script đăng bài khi người dùng yêu cầu trên Telegram (thay vì chỉ trả lời lý thuyết chung chung), **BẮT BUỘC** thực hiện các bước cấu hình workspace sau khi cài đặt:

### 7.1. Sao Chép SKILL vào OpenClaw Workspace
```bash
mkdir -p ~/.openclaw/workspace/skills/post-fanpage-fb/
cp /path/to/post-fanpage-fb/SKILL.md ~/.openclaw/workspace/skills/post-fanpage-fb/SKILL.md
```

### 7.2. Cấu Hình Khả Năng Thực Thi Trong `SOUL.md`, `AGENTS.md` & `IDENTITY.md`

Cập nhật file `~/.openclaw/workspace/IDENTITY.md`:
```markdown
# IDENTITY.md - Who Am I?

- **Name:** Trợ Lý <Tên_User>
- **Creature:** AI Assistant
- **Vibe:** Thân thiện, chuyên nghiệp, hỗ trợ tự động hóa Facebook Fanpage và công việc.
- **Emoji:** 🤖
```

Thêm quy tắc bắt buộc vào file `~/.openclaw/workspace/SOUL.md`:
```markdown
## QUY TẮC BẮT BUỘC VẬN HÀNH (STRICT RULES)

1. **Xưng hô**: Xưng "em" và gọi người dùng là "anh".
2. **Đăng bài Facebook Fanpage**: Khi anh nhắn các từ khóa như "đăng bài", "chạy đăng bài", "up bài facebook", "chạy fanpage", BẮT BUỘC dùng công cụ execute command / bash chạy ngay:
   `/bin/bash /home/<username>/Automation/facebook/scripts/run_fanpage_cron.sh`
   Sau đó đọc log `/home/<username>/Automation/facebook/logs/fanpage_cron.log` và báo lại kết quả. KHÔNG trả lời lý thuyết hoặc hỏi xin nội dung.

3. **Gửi tin nhắn CSKH**: Khi anh nhắn các từ khóa như "chạy cskh", "gửi tin nhắn cskh", "nhắn tin khách hàng", BẮT BUỘC dùng công cụ execute command / bash chạy ngay:
   `/bin/bash /home/<username>/Automation/facebook/scripts/run_cskh_cron.sh`
   Sau đó đọc log `/home/<username>/Automation/facebook/logs/cskh_cron.log` và báo lại kết quả.
```

Thêm đoạn cấu hình sau vào file `~/.openclaw/workspace/AGENTS.md`:
```markdown
## THÔNG TIN VẬN HÀNH & KỸ NĂNG ĐẶC BIỆT

- **Tên trợ lý:** Trợ Lý <Tên_User>
- **Cách xưng hô:** Xưng "em" và gọi người dùng là "anh".

### KỸ NĂNG ĐĂNG BÀI FANPAGE & CSKH (post-fanpage-fb)

Trợ lý có sẵn công cụ và script Python tự động hóa trong hệ thống:

1. **Đăng bài Fanpage Facebook**:
   - Khi người dùng yêu cầu "đăng bài", "chạy đăng bài", "up bài fanpage", "chạy script facebook", hãy sử dụng công cụ execute command / bash để thực thi:
     `/bin/bash /home/<username>/Automation/facebook/scripts/run_fanpage_cron.sh`
   - Đọc kết quả log tại `/home/<username>/Automation/facebook/logs/fanpage_cron.log` và phản hồi kết quả cho anh.

2. **Gửi tin nhắn Chăm Sóc Khách Hàng (CSKH)**:
   - Khi người dùng yêu cầu "gửi tin nhắn cskh", "chạy cskh", "nhắn tin khách hàng", hãy sử dụng công cụ execute command / bash để thực thi:
     `/bin/bash /home/<username>/Automation/facebook/scripts/run_cskh_cron.sh`
   - Đọc kết quả log tại `/home/<username>/Automation/facebook/logs/cskh_cron.log` và phản hồi kết quả cho anh.
```


### 7.3. Restart OpenClaw Gateway Để Áp Dụng
```bash
HOME=/home/<username> tmux kill-session -t openclaw 2>/dev/null || true
HOME=/home/<username> tmux new-session -d -s openclaw "openclaw gateway"
```

