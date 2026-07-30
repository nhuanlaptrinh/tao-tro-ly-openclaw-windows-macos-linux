import os
import requests
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================
# CẤU HÌNH GOOGLE SHEET
# ==========================================
SHEET_ID = os.getenv("SPREADSHEET_ID")
WORKSHEET_NAME = os.getenv("WORKSHEET_CSKH", "Chăm Sóc Khách Hàng")
CREDENTIALS_FILE = os.path.join(os.path.dirname(BASE_DIR), "googlesheetcn.json")
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# ==========================================
# CẤU HÌNH FACEBOOK FANPAGE
# ==========================================
FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN", "Nhap_API_Cua_Ban")


def send_facebook_message(psid: str, message: str) -> dict:
    """Gửi tin nhắn chăm sóc khách hàng tới một PSID qua Facebook Graph API."""
    if not FB_PAGE_ACCESS_TOKEN or FB_PAGE_ACCESS_TOKEN == "Nhap_API_Cua_Ban":
        raise ValueError("Chưa cấu hình FB_PAGE_ACCESS_TOKEN trong file .env")
        
    url = "https://graph.facebook.com/v19.0/me/messages"
    params = {"access_token": FB_PAGE_ACCESS_TOKEN}
    data = {
        "recipient": {"id": psid},
        "message": {"text": message},
        "messaging_type": "RESPONSE"
    }
    
    print(f"[Facebook] Đang gửi tin nhắn tới PSID '{psid}'...")
    response = requests.post(url, params=params, json=data, timeout=60)
        
    if not response.ok:
        raise RuntimeError(f"Lỗi khi gọi Fanpage API: {response.text}")
        
    return response.json()


def main():
    print("========================================")
    print("VẬN HÀNH AUTO GỬI TIN NHẮN CHĂM SÓC KHÁCH HÀNG")
    print("========================================")
    
    print("Đang kết nối tới Google Sheet...")
    try:
        credentials = Credentials.from_service_account_file(CREDENTIALS_FILE, scopes=SCOPES)
        gc = gspread.authorize(credentials)
        workbook = gc.open_by_key(SHEET_ID)
        
        try:
            worksheet = workbook.worksheet(WORKSHEET_NAME)
        except Exception as e:
            print(f"Không tìm thấy tab '{WORKSHEET_NAME}', lỗi: {e}")
            return
            
        records = worksheet.get_all_records()
        headers = worksheet.row_values(1)
        
        if 'Trạng Thái' not in headers:
            status_col = len(headers) + 1
            worksheet.update_cell(1, status_col, 'Trạng Thái')
            headers = worksheet.row_values(1)
            
        status_col_index = headers.index('Trạng Thái') + 1

        print(f"Đã tải {len(records)} dòng khách hàng từ Google Sheet.")
        
        for idx, row in enumerate(records):
            row_num = idx + 2
            
            psid = str(row.get('ID', '')).strip()
            ten_khach_hang = str(row.get('Tên Khách Hàng', '')).strip()
            tin_nhan = str(row.get('Tin Nhắn', '')).strip()
            status = str(row.get('Trạng Thái', '')).strip()
            
            if psid.lower() == 'nan': psid = ""
            if tin_nhan.lower() == 'nan': tin_nhan = ""
            
            # Chỉ xử lý các dòng có trạng thái UNAPPROVED và có đủ ID (PSID) + Tin Nhắn
            if status == 'UNAPPROVED' and psid and tin_nhan:
                print(f"\n=> Đang xử lý Gửi tin nhắn UNAPPROVED ở dòng {row_num} (Khách hàng: {ten_khach_hang})")
                
                try:
                    fb_result = send_facebook_message(psid, tin_nhan)
                    message_id = fb_result.get('message_id')
                    print(f"✅ Gửi tin nhắn thành công! Message ID: {message_id}")
                    
                    # Update lại Google Sheet
                    worksheet.update_cell(row_num, status_col_index, 'APPROVED')
                    print(f"✅ Đã cập nhật trạng thái 'APPROVED' trên dòng {row_num}.")
                    
                    # Mỗi lần chạy chỉ gửi 1 người rồi thoát (giống cơ chế đăng Fanpage cũ)
                    print("\n--- HOÀN TẤT GỬI TIN NHẮN CHO 1 KHÁCH HÀNG ---")
                    break
                    
                except Exception as e:
                    print(f"❌ Lỗi khi gửi tin nhắn (dòng {row_num}): {e}")
                    # Update trạng thái ERROR
                    worksheet.update_cell(row_num, status_col_index, 'ERROR')
                    
    except Exception as e:
        print(f"❌ Lỗi cấu hình tải Sheet/API hệ thống: {e}")

if __name__ == "__main__":
    main()
