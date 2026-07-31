# Checklist tạo OpenClaw member VPS

## Input
- [ ] Member name
- [ ] Email khách hàng nếu cần tạo tài khoản dashboard Token Codex
- [ ] Token Codex API key nhận qua kênh bảo mật nếu đã có sẵn
- [ ] Telegram account ID
- [ ] Telegram user ID
- [ ] Telegram Group ID
- [ ] requireMention true/false
- [ ] BotFather Privacy Mode

## Preflight
- [ ] Kiểm tra hiện trạng
- [ ] Backup cấu hình
- [ ] Kiểm tra manager/image/container/SSH port/web port/volume thực tế; không giả định có dry-run
- [ ] Không lộ secret

## Token Codex trước VPS
- [ ] Đọc mục **Chuẩn bị Token Codex trước member VPS** trong skill chính
- [ ] `/models` trả HTTP `200` và có đủ `GPT-5.6-sol`, `GPT-5.6-terra`, `GPT-5.6-luna`
- [ ] Nếu tạo tài khoản mới: provisioning backend đã được xác minh và dry-run thực sự tồn tại
- [ ] Nếu sinh key mới: thư mục `/root/Data/private_accounts/token_codex/` quyền `700`, file output quyền `600`
- [ ] Không in full API key vào chat hoặc log chung
- [ ] Truyền key qua `TOKEN_CODEX_API_KEY`; chỉ dùng `CUSTOM_PROVIDER_API_KEY` để tương thích workflow cũ
- [ ] Lưu `/home/<name>/.openclaw/token-codex.env` quyền `600`; `openclaw.json` chỉ chứa `${TOKEN_CODEX_API_KEY}`

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
- [ ] Restart tmux sau khi source `token-codex.env`
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
- [ ] Không thêm `/v1` lần thứ hai; API là `openai-completions`
- [ ] API Token Codex đã cấu hình và cả ba model chat test thành công
- [ ] Không còn provider/model cũ trong config hoặc cache model của member
- [ ] Gọi Token Codex `/models` không lộ secret và kiểm tra chính xác model `gpt-4o-mini-transcribe`
- [ ] Chỉ bật audio/STT qua provider `token-codex` khi model được công bố; nếu không có hoặc kiểm tra lỗi, đặt `tools.media.audio.enabled=false`
- [ ] Xóa provider audio `openai` cũ; không tự thay model hoặc fallback sang provider khác
- [ ] Không tự cài `ffmpeg` chỉ để nghe voice; giữ nguyên nếu đã có, chỉ cài khi cần chuyển đổi định dạng riêng
- [ ] Chỉ gửi voice tiếng Việt để kiểm tra khi STT đã được xác nhận khả dụng và người dùng cho phép
- [ ] DuckDuckGo
- [ ] Second AI Brain
- [ ] Proxy direct-first

## Hoàn tất
- [ ] Chỉ gửi email/mật khẩu Token Codex khi tài khoản thực tế đã được tạo
- [ ] Gửi link xem credit `https://codex.anhlaptrinh.vn/`
- [ ] Không gửi full API key
- [ ] Chưa test: chờ xác nhận thực tế
- [ ] Đã có inbound + outbound: hoàn tất hoàn toàn
