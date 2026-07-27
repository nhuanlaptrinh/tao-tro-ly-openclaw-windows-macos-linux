# Checklist tạo OpenClaw member VPS

## Input
- [ ] Member name
- [ ] Email khách hàng dùng đăng nhập Token Codex
- [ ] Telegram account ID
- [ ] Telegram user ID
- [ ] Telegram Group ID
- [ ] requireMention true/false
- [ ] BotFather Privacy Mode

## Preflight
- [ ] Kiểm tra hiện trạng
- [ ] Backup cấu hình
- [ ] Automation dry-run
- [ ] Không lộ secret

## Token Codex trước VPS
- [ ] Đọc mục **Tạo Token Codex Trước Member VPS** trong skill chính
- [ ] Dry-run tài khoản theo email khách hàng
- [ ] Tạo user mặc định `alt123`, credit `250 USD`
- [ ] Tạo 1 API tên gắn với member
- [ ] Output/key lưu file quyền `600` dưới `/root/Data/private_accounts/token_codex/`
- [ ] Không in full API key vào chat hoặc log chung
- [ ] Truyền key qua `CUSTOM_PROVIDER_API_KEY`

## Telegram DM
- [ ] Global và account `dmPolicy` là `pairing`
- [ ] Global allowFrom có `6980864856`, `8342048167`
- [ ] Account allowFrom có `6980864856`, `8342048167`
- [ ] `TELEGRAM_CHAT_ID` được merge thêm nếu có
- [ ] Người ngoài allowFrom phải pairing

## Plugin approval
- [ ] `approvals.plugin.enabled` true
- [ ] Mode `targets`
- [ ] Agent filter chỉ `main`
- [ ] Target Telegram `6980864856` qua đúng account member
- [ ] Target Telegram `8342048167` qua đúng account member
- [ ] Hướng dẫn dùng Allow once hoặc `/approve <id> allow-once`
- [ ] Không dùng proposal ID thay approval ID

## Telegram group
- [ ] groupPolicy allowlist
- [ ] Group enabled
- [ ] Group allowFrom là `["*"]` ở top-level và account scope
- [ ] Không để group thiếu allowFrom vì sẽ fallback về DM owner allowlist
- [ ] requireMention mặc định false, trừ khi user yêu cầu true
- [ ] Binding riêng đúng account và group
- [ ] Không binding trùng

## Không cần mention
- [ ] requireMention false
- [ ] allowFrom `["*"]` cho đúng group
- [ ] BotFather /setprivacy Disable
- [ ] Test tin thường không mention
- [ ] Log có inbound đúng group
- [ ] Bot có outbound

## Runtime
- [ ] config validate
- [ ] Restart tmux
- [ ] gateway status OK
- [ ] channels probe OK

## Dashboard public
- [ ] Lấy đúng host web port map tới container port 80
- [ ] Lấy public IPv4 hoặc đặt `OPENCLAW_PUBLIC_IP`
- [ ] Nginx reverse proxy tới `127.0.0.1:18789` có WebSocket headers
- [ ] `allowedOrigins` đúng URL public
- [ ] `allowInsecureAuth` true
- [ ] `dangerouslyDisableDeviceAuth` true cho HTTP token-only
- [ ] Token lưu tại `/home/<name>/.openclaw_dashboard_token`, quyền 600
- [ ] UFW mở đúng web port
- [ ] Public URL trả HTTP 200
- [ ] Hướng dẫn nhập Token Gateway và để trống mật khẩu

## Hệ thống
- [ ] Token Codex provider dùng `https://codex.anhlaptrinh.vn/v1`
- [ ] API Token Codex đã cấu hình và model test thành công
- [ ] Audio/STT được bật mặc định: `tools.media.audio.enabled=true`, ngôn ngữ `vi`, model `gpt-4o-mini-transcribe` qua provider `openai`/9Router
- [ ] Provider audio có model khai báo `input: ["audio"]` và tái sử dụng credential 9Router hiện có mà không in secret
- [ ] Không tự cài `ffmpeg` chỉ để nghe voice; giữ nguyên nếu đã có, chỉ cài khi cần chuyển đổi định dạng riêng
- [ ] Gửi một voice tiếng Việt ngắn để xác nhận bot nhận `.ogg` và trả transcript
- [ ] DuckDuckGo
- [ ] Second AI Brain
- [ ] Proxy direct-first

## Hoàn tất
- [ ] Gửi email Token Codex cho khách
- [ ] Gửi mật khẩu Token Codex mặc định `alt123`
- [ ] Gửi link xem credit `https://codex.anhlaptrinh.vn/`
- [ ] Không gửi full API key
- [ ] Chưa test: chờ xác nhận thực tế
- [ ] Đã có inbound + outbound: hoàn tất hoàn toàn
