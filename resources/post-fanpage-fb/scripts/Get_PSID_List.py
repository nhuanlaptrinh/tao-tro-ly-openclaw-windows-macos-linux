import os
import requests
from dotenv import load_dotenv

load_dotenv()

FB_PAGE_ACCESS_TOKEN = os.getenv("FB_PAGE_ACCESS_TOKEN", "")

def get_recent_psids():
    if not FB_PAGE_ACCESS_TOKEN or FB_PAGE_ACCESS_TOKEN == "Nhap_API_Cua_Ban":
        print("❌ Lỗi: Bạn chưa cấu hình FB_PAGE_ACCESS_TOKEN trong file .env")
        return

    print("Đang quét danh sách khách hàng đã nhắn tin cho Fanpage...\n")
    url = "https://graph.facebook.com/v19.0/me/conversations"
    params = {
        "fields": "participants",
        "access_token": FB_PAGE_ACCESS_TOKEN,
        "limit": 50  # Lấy 50 cuộc hội thoại gần nhất
    }

    try:
        response = requests.get(url, params=params, timeout=30)
        data = response.json()

        if not response.ok:
            print(f"❌ Lỗi Graph API: {data}")
            return

        conversations = data.get("data", [])
        if not conversations:
            print("Không tìm thấy cuộc hội thoại nào.")
            return

        print(f"{'TÊN KHÁCH HÀNG':<30} | {'MÃ PSID (Copy vào Google Sheet)'}")
        print("-" * 65)

        for conv in conversations:
            participants = conv.get("participants", {}).get("data", [])
            # Lọc ra participant không phải là Fanpage (thường Fanpage không có email/name rõ ràng như user hoặc có ID trùng với Page ID)
            # Tuy nhiên đơn giản nhất là in ra hết tên
            for p in participants:
                name = p.get("name", "Unknown")
                psid = p.get("id", "")
                print(f"{name:<30} | {psid}")
                
        print("-" * 65)
        print("💡 Lưu ý: Hãy loại trừ tên của chính Fanpage ra nhé!")
        
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")

if __name__ == "__main__":
    get_recent_psids()
