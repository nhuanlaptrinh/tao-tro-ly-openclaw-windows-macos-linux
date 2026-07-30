---
name: tao-tro-ly-openclaw-windows-macos-linux
description: Skill tự chứa để cài đặt, tạo, cấu hình hoặc vận hành trợ lý OpenClaw trên Windows, macOS và Linux, gồm máy cá nhân, VPS chính và VPS thành viên chạy Docker. Bao gồm workflow Node.js/Python/OpenClaw local, Gateway, Codex login, DeepSeek tùy chọn, Token Codex, Telegram, Zalo QR/voice/reliability, kiểm tra openclaw.json, Custom Provider, proxy fallback, Second AI Brain, audio, web search và xử lý ảnh; không yêu cầu cài hay đọc skill phụ.
---

# Tạo Trợ Lý OpenClaw Trên Windows, macOS Và Linux

## Mục tiêu

Điều phối đúng quy trình cài đặt, tạo, cấu hình hoặc vận hành trợ lý OpenClaw trên Windows, macOS và Linux. Trên Linux phải phân biệt máy local/server, VPS chính và VPS thành viên chạy trong container Docker; không dùng lẫn script, config, token, port hoặc dữ liệu giữa các môi trường.

## Tính độc lập và cách chuyển VPS

- Đây là skill chính tự chứa; không yêu cầu cài, copy hoặc đọc bất kỳ skill phụ nào.
- Khi chuyển sang máy khác, copy nguyên folder skill, gồm `SKILL.md`, `agents/` và `references/`, vào thư mục skill của Codex/OpenClaw trên Windows, macOS hoặc Linux.
- Các project hoặc automation được nêu trong skill vẫn phải tồn tại nếu muốn dùng đúng lệnh tự động; nếu VPS đích chưa có, thực hiện workflow thủ công tương ứng trong skill thay vì gọi một skill khác.
- Không xóa các skill độc lập cũ trên VPS nguồn vì chúng có thể đang được workflow khác sử dụng; skill này chỉ loại bỏ sự phụ thuộc vào chúng.

## Chọn hệ điều hành và môi trường trước khi thao tác

1. Xác định hệ điều hành bằng PowerShell trên Windows hoặc `uname -s` trên macOS/Linux.
2. Xác định đây là máy cá nhân/lớp học, Linux server/VPS chính hay VPS thành viên Docker.
3. Trên Windows và macOS, mặc định cài local gateway chỉ bind loopback; không áp dụng script Docker member VPS.
4. Trên Linux VPS chính, kiểm tra runtime, service/container và workspace OpenClaw đang hoạt động; đường dẫn thường dùng trên VPS này là `/root/AI_Runtime/openclaw/.openclaw`.
5. Với VPS chính, không chạy `create_member_openclaw_assistant.sh` hoặc `manage-user.sh`; backup đúng file cấu hình sắp sửa và chỉ thay đổi runtime được yêu cầu.
6. Nếu là VPS thành viên, dùng toàn bộ workflow member trong skill này và automation `/root/Automation/openclaw_member_assistant`.
7. Nếu yêu cầu chưa nói rõ hệ điều hành hoặc môi trường, kiểm tra trước khi quyết định; không tự giả định Windows là WSL, Linux host là member container hoặc ngược lại.

## Cài đặt OpenClaw đa nền tảng

### Mặc định chung

- Luôn cài cố định `openclaw@2026.7.1-2`; không dùng `latest` và không tự đổi version. Sau khi cài phải xác nhận `openclaw --version` trả đúng `2026.7.1-2`.
- Cài Node.js LTS, npm, Python 3 và pip trước khi cài OpenClaw.
- Dashboard local mặc định: `http://127.0.0.1:18789/`.
- Gateway mặc định: mode `local`, bind `loopback`, port `18789`, auth `token`.
- Token `chatbot` chỉ được dùng cho máy local bind loopback; VPS/public/member phải dùng token ngẫu nhiên riêng.
- Chuẩn bị Codex CLI dùng đăng nhập tài khoản ChatGPT bằng `forced_login_method = "chatgpt"`; không tự chạy login và không copy auth cache.
- Chỉ bật DeepSeek khi biến `DEEPSEEK_API_KEY` đã tồn tại; không in hoặc ghi key vào skill/log.

### Windows

Chạy trong PowerShell. Ưu tiên `winget`; nếu có UAC thì yêu cầu người dùng xác nhận:

```powershell
winget install --id OpenJS.NodeJS.LTS --exact --accept-package-agreements --accept-source-agreements
winget install --id Python.Python.3.12 --exact --accept-package-agreements --accept-source-agreements
python -m ensurepip --upgrade
python -m pip install --upgrade pip
npm install -g openclaw@2026.7.1-2
openclaw onboard --non-interactive --accept-risk --mode local --auth-choice skip --skip-channels --skip-search --skip-skills --install-daemon --skip-health --gateway-bind loopback --gateway-auth token --gateway-port 18789 --gateway-token chatbot
openclaw config validate
openclaw gateway restart
openclaw gateway status
```

Nếu command chưa vào PATH sau khi cài, mở PowerShell mới rồi chạy lại phần kiểm tra. Không coi WSL là Windows native; nếu đang trong WSL thì dùng nhánh Linux.

### macOS

Kiểm tra Homebrew; nếu chưa có thì cài từ trang chính thức, sau đó:

```bash
brew install node python
python3 -m ensurepip --upgrade || true
python3 -m pip install --upgrade pip --break-system-packages || python3 -m pip install --upgrade pip
npm install -g openclaw@2026.7.1-2
openclaw onboard --non-interactive --accept-risk --mode local --auth-choice skip --skip-channels --skip-search --skip-skills --install-daemon --skip-health --gateway-bind loopback --gateway-auth token --gateway-port 18789 --gateway-token chatbot
openclaw config validate
openclaw gateway restart
openclaw gateway status
```

Hỗ trợ cả Apple Silicon (`/opt/homebrew`) và Intel (`/usr/local`). Không sửa LaunchAgent khác nếu task chỉ cài OpenClaw.

### Linux local hoặc server độc lập

Chọn package manager phù hợp (`apt`, `dnf`, `yum`, `pacman`) để cài Node.js, npm, Python và pip. Với Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y curl ca-certificates nodejs npm python3 python3-pip python3-venv
sudo npm install -g openclaw@2026.7.1-2
openclaw onboard --non-interactive --accept-risk --mode local --auth-choice skip --skip-channels --skip-search --skip-skills --install-daemon --skip-health --gateway-bind loopback --gateway-auth token --gateway-port 18789 --gateway-token chatbot
openclaw config validate
openclaw gateway restart
openclaw gateway status
```

Nếu là VPS cần truy cập từ ngoài, không tự đổi bind hoặc mở port. Chỉ cấu hình reverse proxy/firewall/domain sau khi người dùng yêu cầu rõ và phải dùng token ngẫu nhiên thay cho `chatbot`.

### Codex và DeepSeek

- Codex CLI: người dùng tự chạy `codex logout`, sau đó `codex login`; máy headless dùng `codex login --device-auth`.
- Ghi `forced_login_method = "chatgpt"` vào `~/.codex/config.toml` hoặc `%USERPROFILE%\.codex\config.toml`, giữ nguyên các cấu hình khác.
- Không tự cài, chạy login hoặc sao chép `auth.json`/credential store.
- Nếu có `DEEPSEEK_API_KEY`, có thể chạy lại `openclaw onboard` với `--auth-choice deepseek-api-key`; truyền key qua biến môi trường, không đặt trực tiếp trong tài liệu.

### Kiểm tra đa nền tảng

```bash
node -v
npm -v
python3 --version
python3 -m pip --version
openclaw --version
openclaw config validate
openclaw gateway status
openclaw models auth list
```

Trên Windows có thể thay `python3` bằng `python` hoặc `py -3`. Báo đúng dashboard local `http://127.0.0.1:18789/`; không quảng bá URL này là public.

## Quy trình an toàn cho VPS chính

1. Đọc tài liệu Second AI Brain, project note và `AGENTS.md` liên quan trước khi sửa.
2. Xác định chính xác runtime OpenClaw, user hệ thống, HOME, workspace, file `openclaw.json` và cách gateway đang được khởi chạy.
3. Backup file cấu hình cần sửa vào `/root/_Backups`; không sao chép secret vào backup công khai, skill, log hoặc câu trả lời.
4. Dùng đúng phần tích hợp trong skill này nếu task thuộc Telegram, Zalo, 9Router, STT, voice, proxy, Second AI Brain hoặc kiểm tra JSON.
5. Sau thay đổi, kiểm tra config, trạng thái gateway và đúng channel được yêu cầu; không chạy automation tạo container member.

## Mục tiêu cho VPS thành viên

Dùng automation `/root/Automation/openclaw_member_assistant` để tạo một container member VPS riêng, cài cố định `openclaw@2026.7.1-2`, cài Python và môi trường PDF/Excel dùng chung, sinh Gateway Token riêng, thêm Telegram account khi có bot token, đặt Telegram DM policy là `pairing`, giữ allowFrom quản trị mặc định, chuyển plugin approval tới Telegram, hỗ trợ Zalo Personal và chạy gateway bằng `tmux` trong container.

## Đường dẫn cho VPS thành viên

- Automation app: `/root/Automation/openclaw_member_assistant`
- Script chạy chính: `/root/Automation/openclaw_member_assistant/scripts/create_member_openclaw_assistant.sh`
- Bộ tạo member VPS: `/root/Apps/member_vps/docker-users/manage-user.sh`
- Log automation: `/root/Automation/openclaw_member_assistant/logs`
- Backup trước khi sửa workflow: `/root/_Backups`
- Nhật ký thay đổi: `/root/_Second_AI_Brain/06_Nhat_Ky_Thay_Doi.md`
- Checklist SVG/PNG và lỗi shell approvals path: `references/svg-png-shell-checklist.md`
- Fallback tạo ảnh local SVG/Python: `references/local-svg-python-image-fallback.md`
- Checklist rút gọn tạo member VPS và Telegram group: `references/member-vps-creation-checklist.md`
- Shared fallback proxy: thực hiện trực tiếp tại mục **Shared Fallback Proxy**.
- Second AI Brain: thực hiện trực tiếp tại mục **Second AI Brain Cho Member VPS Mới**.
- Tạo tài khoản/API Token Codex: thực hiện trực tiếp tại mục **Tạo Token Codex Trước Member VPS**.
- Đăng nhập Zalo Personal: thực hiện trực tiếp tại mục **Đăng nhập Zalo Personal/Zalo User**.

## Quy tắc mặc định cho VPS thành viên

- Tên container là `user-<name>`.
- Folder data member là `/root/Apps/member_vps/docker-users/data/<name>`.
- Mật khẩu SSH mặc định luôn là `<name>123`; ví dụ `nhuan` thành `nhuan123`. Không tự sinh mật khẩu ngẫu nhiên, trừ khi người dùng yêu cầu rõ mật khẩu khác.
- Trước khi tạo **OpenClaw member VPS đầy đủ**, bắt buộc có email khách hàng và tạo tài khoản Token Codex bằng command tích hợp trong skill này. Quy tắc này không áp dụng khi người dùng chỉ yêu cầu tạo VPS/container trống.
- Token Codex mặc định dùng mật khẩu `alt123`, credit `250 USD`, tạo 1 API và dùng API đó cho Custom Provider của member VPS.
- Khi bàn giao, gửi email Token Codex, mật khẩu và link `https://codex.anhlaptrinh.vn/` để khách xem credit/API usage còn lại; không gửi full API key.
- Port SSH/web do `manage-user.sh` tự lấy port cao nhất hiện có của các container `user-*` cộng `1`, rồi kiểm tra không trùng.

### Trường hợp chỉ tạo VPS thành viên

Khi người dùng nói rõ “chỉ tạo VPS thành viên”, “chỉ tạo container” hoặc “không cần cài mấy cái khác”:

1. Chỉ chạy `bash /root/Apps/member_vps/docker-users/manage-user.sh create <name>` và để script tự dùng mật khẩu `<name>123`.
2. Không chạy `create_member_openclaw_assistant.sh`; không tạo Token Codex và không cài OpenClaw, Telegram, Zalo, Nginx bổ sung, document tools, proxy hoặc Second AI Brain.
3. Xác minh container đang chạy, port SSH được map và đăng nhập SSH thành công.
4. Lưu thông tin đăng nhập trong file riêng quyền `600`; không ghi mật khẩu thật vào skill, README, nhật ký hoặc log chung.
5. Bàn giao IP, SSH port, username và vị trí file credential bảo mật cho người dùng.
- OpenClaw phải luôn cài cố định `openclaw@2026.7.1-2`; không dùng npm dist-tag `latest`, không nhận override version từ môi trường và không tự nâng cấp.
- Trước khi cài, đọc `engines.node` bằng `npm view openclaw@2026.7.1-2 engines --json`; version này yêu cầu Node `>=22.22.3 <23 || >=24.15.0 <25 || >=25.9.0`.
- Mọi member mới phải có `python3`, `python3-full`, `python3-venv`, `python3-pip`.
- Mọi member mới phải có Poppler (`pdfinfo`, `pdftotext`), `file`, `unzip`, `zip`.
- Mọi member mới phải có document venv tại `/home/<name>/.openclaw/tools/document-venv` với OpenPyXL, PyPDF, pdfplumber, PyMuPDF, Pillow, XlsxWriter và pandas.
- Pipeline tạo member phải gọi `/root/Automation/openclaw_member_assistant/scripts/setup_member_document_tools.sh`; không để người dùng phải cài thủ công sau khi tạo.
- Tạo symlink `document-python` và `document-pip`, đồng thời copy validator vào `/home/<name>/.openclaw/workspace/tools/validate_zalo_file.py`.
- Gateway URL trong container là `http://127.0.0.1:18789/`.
- Gateway Token phải được sinh ngẫu nhiên riêng cho từng member, trừ khi người dùng truyền `OPENCLAW_GATEWAY_TOKEN`; không dùng token cố định dùng chung.
- Mọi member mới phải có dashboard public tại `http://<PUBLIC_IP>:<web_port>/`, dùng đúng host web port mà `manage-user.sh` map tới port `80` của container.
- Pipeline phải tự cấu hình Nginx trong container reverse proxy port `80` tới `127.0.0.1:18789`, gồm WebSocket upgrade headers.
- Dashboard public HTTP mặc định chỉ yêu cầu Gateway Token: đặt `gateway.controlUi.allowedOrigins` đúng URL public, `gateway.controlUi.allowInsecureAuth = true`, và `gateway.controlUi.dangerouslyDisableDeviceAuth = true`.
- Lưu Gateway Token tại `/home/<name>/.openclaw_dashboard_token` với quyền `600`; khi đăng nhập nhập Token Gateway và để trống ô mật khẩu.
- Phải báo link public tương ứng web port sau khi tạo và xác minh URL trả HTTP `200`. Nếu không tự lấy được public IPv4, dùng `OPENCLAW_PUBLIC_IP`.
- Cấu hình HTTP token-only giảm bảo mật; khi có domain HTTPS phải ưu tiên HTTPS và tắt `dangerouslyDisableDeviceAuth`.
- Telegram DM mặc định phải dùng `dmPolicy: pairing` ở cả cấp chung và `channels.telegram.accounts.<account>`.
- Hai Telegram ID quản trị `6980864856` và `8342048167` luôn phải có trong `channels.telegram.allowFrom` và `channels.telegram.accounts.<account>.allowFrom`; các ID này được nhắn riêng không cần pairing.
- `TELEGRAM_CHAT_ID` nếu được truyền khi tạo member phải được merge thêm vào allowFrom, không thay thế hai ID quản trị mặc định.
- Người mới ngoài allowFrom phải pairing; dùng `openclaw pairing list telegram` để lấy request và chỉ approve đúng người đã xác minh.
- Mọi member mới phải bật `approvals.plugin.enabled = true`, mode `targets`, `agentFilter: ["main"]`; tạo hai target Telegram tới `6980864856` và `8342048167`, có `accountId` đúng bằng tên Telegram account/member.
- Cả hai ID quản trị mặc định có quyền nhận và xử lý approval bằng nút **Allow once** hoặc `/approve <id> allow-once`; phải dùng approval ID đang chờ, không dùng proposal ID của skill.
- Khi người dùng cung cấp Telegram Group ID lúc tạo nhân viên, mặc định cấu hình group allowlist với `enabled: true`, `requireMention: false`, `allowFrom: ["*"]` ở cả top-level và account scope, cùng binding riêng tới agent `main` trước khi restart gateway.
- Không được chỉ xóa `allowFrom` cấp group: OpenClaw hiện hành có thể fallback về DM/account `allowFrom` và tiếp tục chỉ cho chủ bot. Muốn mọi thành viên trong group được gọi bot, bắt buộc đặt wildcard `allowFrom: ["*"]` ngay trong đúng group.
- Giữ Telegram DM ở `pairing`; `allowFrom` chỉ chứa các ID đã duyệt/mặc định. Wildcard chỉ áp dụng cho group đã khai báo, không dùng wildcard để mở DM hoặc group khác.
- Khi cần Zalo Personal/Zalo User, cài `@openclaw/zalouser` đúng version OpenClaw, ưu tiên gửi QR trực tiếp tới Telegram ID đang có trong allowlist thay vì public QR trên web.
- Zalo mặc định giữ `dmPolicy: pairing` nếu user chưa yêu cầu policy. Nếu user yêu cầu DM allowlist, chỉ thêm sender đã xác minh qua pairing request vào `channels.zalouser.allowFrom`; không approve sender lạ.
- Khi user yêu cầu mở toàn bộ Zalo group, có thể đặt `channels.zalouser.groupPolicy: open`. Khi chỉ mở một hoặc vài group cụ thể và không cần mention, phải dùng `groupPolicy: allowlist`, khai báo `groups.<GROUP_ID>.enabled: true`, `groups.<GROUP_ID>.requireMention: false`, và `groupAllowFrom: ["*"]`; không dùng wildcard DM để mở group.
- Chạy gateway bằng home thật của member: `HOME=/home/<name> tmux new-session -d -s openclaw "HOME=/home/<name> openclaw gateway run"`.
- Không khởi chạy Gateway hoặc CLI OpenClaw với `HOME=/root` nếu `/root/.openclaw` là symlink tới `/home/<name>/.openclaw`; exec approvals sẽ từ chối traversal qua symlink.
- Mọi `docker exec ... openclaw` trong automation phải truyền `-e HOME=/home/<name>` hoặc chạy qua wrapper đã khóa `HOME`.
- **Cấu hình Custom Provider cho Token Codex (BẮT BUỘC KHI DÙNG VPS THÀNH VIÊN):** Tuyệt đối không trỏ nhầm URL sang 9Router. Khi cấu hình thủ công vào `openclaw.json`, bắt buộc dùng đúng nguyên mẫu JSON sau, không tự thêm thuộc tính lạ như `enabled`:
```json
"models": {
  "providers": {
    "token-codex": {
      "baseUrl": "https://codex.anhlaptrinh.vn/v1",
      "api": "openai-completions",
      "apiKey": "${TOKEN_CODEX_API_KEY}"
    }
  }
},
"agents": {
  "defaults": {
    "models": { "token-codex/GPT-5.6-sol": {} }
  }
}
```
- Nếu dùng 9Router (chỉ dùng khi không có Token Codex): Endpoint ID `9rt`, API Base URL `https://9router.anhlaptrinh.vn/v1`, Model ID `codex`, `api: openai-completions`.
- Mặc định cấu hình tạo ảnh giống member mẫu `anhlaptrinh`: `imageModel.primary` và `imageGenerationModel.primary` là `9rt/codex`, `agents.defaults.models` có cả `9r/codex` và `9rt/codex`, model `9rt/codex` có `input: ["text", "image"]`, `maxTokens: 4096`.
- Mặc định bật web search cho member VPS bằng plugin `duckduckgo`, vì DuckDuckGo không cần API key và tránh lỗi `no provider is available` khi bot gọi `web_search`.
- Khi tạo/cấu hình trợ lý mới, trong `/root/.openclaw/openclaw.json` của container member VPS phải có `plugins.entries.duckduckgo.enabled = true` và `tools.web.search.provider = "duckduckgo"`.
- Mặc định bật audio understanding/transcription cho mọi trợ lý member VPS: `tools.media.audio.enabled = true`, `language = "vi"`, `echoTranscript = true`, model `gpt-4o-mini-transcribe` qua provider `openai`.
- Luồng transcription mẫu `trolynhanvienao2` đọc trực tiếp file voice `.ogg` qua provider; không cài `ffmpeg` chỉ để bật tính năng nghe audio. VPS đã có `ffmpeg` thì giữ nguyên, VPS chưa có không cần cài nếu không có yêu cầu chuyển đổi định dạng riêng.
- Ngoại lệ Zalo Personal: plugin `zalouser` có thể chuyển voice thành URL `zdn.vn/*.aac`; endpoint STT không nhận AAC trực tiếp. Khi member bật Zalo Personal và cần nghe voice, cài `ffmpeg` riêng cho member đó rồi áp dụng workflow AAC tích hợp tại mục audio; không cài đại trà cho member chỉ dùng Telegram.
- Provider audio nên dùng `models.providers.openai` trỏ `baseUrl` về `https://9router.anhlaptrinh.vn/v1` khi chạy thực tế, có `apiKey` copy từ credential 9Router đang dùng trong provider `9rt`/custom provider; không in key ra màn hình.
- Chỉ dùng `http://localhost:20128/v1` cho audio nếu trong chính container/member VPS có 9Router local hoạt động; nếu gặp `SsrFBlockedError`, đổi sang domain 9Router HTTPS.
- Chỉ đặt model `input: ["text"]` nếu người dùng yêu cầu rõ không hỗ trợ ảnh input (`N`).
- Khi tạo VPS thành viên mới bằng pipeline này, mặc định public dashboard qua đúng web port Docker đã cấp; không mở thêm port gateway `18789` trực tiếp trên host.
- Mọi workflow tạo, cấu hình hoặc vận hành trợ lý member VPS phải áp dụng mục **Shared Fallback Proxy**; kết nối trực tiếp luôn là mặc định, proxy chỉ là fallback khi direct thất bại.
- Mỗi VPS thành viên mới phải được dry-run, bootstrap và kiểm tra theo mục **Second AI Brain Cho Member VPS Mới** bên trong đúng container `user-<ten_user>`.

## Shared Fallback Proxy

Mỗi khi tạo, cấu hình hoặc vận hành trợ lý OpenClaw trong member VPS, áp dụng trực tiếp quy trình sau; không gọi skill ngoài.

Quy tắc bắt buộc:

1. Luôn thử kết nối trực tiếp trước; proxy chỉ là fallback khi direct thất bại.
2. Không bật proxy toàn hệ thống; không sửa `/etc/environment`, shell rc, Docker daemon, systemd global environment hoặc luồng mạng mặc định.
3. Trong member VPS, lưu bí mật tại `/root/.config/openclaw/fallback-proxy.env`, owner `root`, quyền `600`.
4. Kiểm tra file hiện có trước; không ghi đè bí mật nếu chủ hệ thống chưa yêu cầu thay thế.
5. Truyền bí mật qua stdin hoặc kênh quản trị bảo mật; không để URL, username hoặc password proxy xuất hiện trong command line, log, Git, skill hoặc câu trả lời.
6. Kiểm tra riêng quyền file, direct mặc định và một HTTPS URL qua nhánh fallback; chỉ báo kết quả đã che credential.
7. Nếu chưa có proxy secret được chủ hệ thống cấp, bỏ qua riêng phần proxy và báo rõ; không tự suy đoán hoặc tìm credential trong file không liên quan.

## Second AI Brain Cho Member VPS Mới

Mỗi khi tạo VPS thành viên mới, thực hiện trực tiếp quy trình sau; không gọi skill ngoài.

Quy tắc triển khai bên trong đúng VPS/container thành viên:

1. Kiểm tra hiện trạng trước, không ghi đè file hoặc thư mục đã tồn tại.
2. Chạy bootstrap ở chế độ `--dry-run` trước, sau đó mới tạo thật khi kết quả an toàn.
3. Tạo hoặc bảo toàn `/root/_Second_AI_Brain`, `/root/Apps`, `/root/Automation`, `/root/Data`, `/root/AI_Runtime`, `/root/_Infra`, `/root/_Backups`, `/root/_Archive`.
4. Tạo hoặc bảo toàn `/root/AGENTS.md` làm entrypoint, yêu cầu AI đọc `_Second_AI_Brain` trước khi sửa project.
5. Bảo đảm đủ các file vận hành tối thiểu `START_HERE.md`, `01_Ban_Do_VPS.md`, `02_Danh_Sach_Project.md`, `03_Dich_Vu_Dang_Chay.md`, `04_Lenh_Van_Hanh.md`, `05_Canh_Bao_Bao_Mat.md`, `06_Nhat_Ky_Thay_Doi.md` và các thư mục `projects`, `services`, `templates`, `inventories`, `backups`, `checklists`.
6. Chỉ ghi thông tin thực tế đã làm sạch; không chép secret, token, cookie, password, private key hoặc credential.
7. Không đụng `/root/.ssh`, `/root/.codex`, `/root/.agents` hoặc provider credentials nếu người dùng không yêu cầu rõ.
8. Sau khi tạo, cập nhật `/root/_Second_AI_Brain/06_Nhat_Ky_Thay_Doi.md` bên trong member VPS và kiểm tra đủ cấu trúc.
9. Mọi đường dẫn `/root/...` trong phần này là đường dẫn bên trong container `user-<ten_user>`, không phải host chính.

Dry-run thủ công khi VPS đích không có bootstrap script:

```bash
for path in /root/_Second_AI_Brain /root/Apps /root/Automation /root/Data /root/AI_Runtime /root/_Infra /root/_Backups /root/_Archive /root/AGENTS.md; do
  if [ -e "$path" ]; then printf 'KEEP %s\n' "$path"; else printf 'CREATE %s\n' "$path"; fi
done
```

Chạy thật chỉ tạo phần còn thiếu bằng `mkdir -p`; các file Markdown mới phải là skeleton không chứa secret. Không ghi đè file hiện có bằng template chung.

## Workflow Tích Hợp Bắt Buộc

Khi tạo VPS thành viên mới, thực hiện theo đúng thứ tự:

1. Đọc mục Token Codex trong skill chính này; không gọi skill ngoài.
2. Yêu cầu email khách hàng; dry-run rồi tạo tài khoản Token Codex, credit và API trước khi tạo VPS.
3. Lưu output API một lần vào file quyền `600`, không đưa full key vào chat hoặc log chung.
4. Thực hiện hai mục tích hợp **Shared Fallback Proxy** và **Second AI Brain Cho Member VPS Mới** trong skill này.
5. Dry-run automation tạo member VPS.
6. Tạo OpenClaw member VPS với API vừa tạo truyền qua `CUSTOM_PROVIDER_API_KEY`.
7. Cấu hình dashboard public, Second AI Brain và shared fallback proxy.
8. Validate provider/model Token Codex, OpenClaw, public HTTP 200, gateway/channel, Second AI Brain và proxy fallback.
9. Bàn giao VPS cùng email/mật khẩu Token Codex và link `https://codex.anhlaptrinh.vn/` để xem credit.

## Tạo Token Codex Trước Member VPS

Đây là bước bắt buộc cho mọi member VPS mới. Phải có email khách hàng trước khi chạy automation VPS.

```bash
cd /root/Apps/9router_usage_dashboard
.venv/bin/python manage.py create_customer_account \
  --email '<email_khach_hang>' \
  --api-name 'member-<ten_user>' \
  --dry-run

umask 077
TOKEN_CODEX_OUTPUT='/root/Data/private_accounts/token_codex/<email_chuan_hoa>.txt'
.venv/bin/python manage.py create_customer_account \
  --email '<email_khach_hang>' \
  --api-name 'member-<ten_user>' \
  > "$TOKEN_CODEX_OUTPUT"
chmod 600 "$TOKEN_CODEX_OUTPUT"
```

- Mặc định tạo mật khẩu `alt123`, credit `250 USD` và một API.
- Full key nằm ở dòng cuối output và chỉ được đọc từ file bảo mật để nạp vào member VPS.
- Nếu tài khoản đã tồn tại, dừng và kiểm tra; không tự dùng `--update-existing` hoặc đổi mật khẩu/credit.
- Không chép full API key vào skill, README, nhật ký hoặc câu trả lời.

## Checklist hệ thống bắt buộc khi cần xuất ảnh

Nếu user báo lỗi không convert được SVG sang PNG/JPG, hoặc lỗi shell dạng `Refusing to traverse symlink in exec approvals path...`, đọc và làm theo `references/svg-png-shell-checklist.md`.

Với lỗi approvals path, kiểm tra `HOME` của tiến trình Gateway trước khi sửa quyền file. Kết quả bắt buộc là `/home/<name>`; không dùng `chmod 777` và không xóa symlink để chữa lỗi này.

Tóm tắt bắt buộc:

1. Kiểm tra đang ở đường dẫn thật bằng `readlink -f .`; tránh chạy trong symlink path.
2. Kiểm tra `/tmp` phải là `1777`; nếu sai thì chạy `chmod 1777 /tmp`.
3. Nếu thiếu tool, cài `imagemagick`, `librsvg2-bin`, `python3`.
4. Test bằng cả `convert` và `rsvg-convert` với SVG mẫu.
5. Nếu làm trong member VPS, chạy checklist bên trong container `user-<ten_user>`.

## Fallback tạo ảnh khi thiếu image provider key

Nếu user yêu cầu tạo ảnh/poster/banner và bot/OpenClaw báo thiếu API key cho OpenAI/Gemini/Fal/OpenRouter image provider, không dừng ngay. Đọc `references/local-svg-python-image-fallback.md` và ưu tiên tạo ảnh bằng SVG/Python local giống member mẫu `anhlaptrinh`.

Quy tắc:

1. Poster, banner, thumbnail, cover khóa học, ảnh chữ, infographic đơn giản: tạo bằng SVG/Python local.
2. Xuất PNG bằng `rsvg-convert`; fallback sang `convert`.
3. Lưu file trong `/root/.openclaw/workspace` của container member VPS.
4. Chỉ yêu cầu API key image provider nếu user cần ảnh photorealistic/AI-art phức tạp.
5. Khi thiếu provider key, nói rõ “em sẽ fallback sang SVG/Python local” rồi tạo file, không báo dừng.

## Chạy dry-run member VPS

Luôn chạy dry-run trước để xem thao tác và port dự kiến:

```bash
cd /root/Automation/openclaw_member_assistant
./scripts/create_member_openclaw_assistant.sh --name <ten_user> --dry-run
```

## Chạy thật member VPS

Nếu chưa có Telegram token, vẫn có thể tạo VPS và cài OpenClaw trước:

```bash
cd /root/Automation/openclaw_member_assistant
./scripts/create_member_openclaw_assistant.sh --name <ten_user>
```

Nếu đã có Telegram bot token, ưu tiên truyền qua biến môi trường tạm thời để tránh shell history lộ token trong tham số:

```bash
cd /root/Automation/openclaw_member_assistant
TELEGRAM_BOT_TOKEN='PASTE_TOKEN_TAM_THOI_O_DAY' TELEGRAM_CHAT_ID='CHAT_ID' ./scripts/create_member_openclaw_assistant.sh --name <ten_user>
```

Với member VPS mới, Custom Provider là bắt buộc và phải dùng API vừa tạo từ bước Token Codex. Đọc key từ file quyền `600`, không copy key vào chat hoặc tham số command:

```bash
cd /root/Automation/openclaw_member_assistant
TOKEN_CODEX_OUTPUT='/root/Data/private_accounts/token_codex/<email_chuan_hoa>.txt'
CUSTOM_PROVIDER_API_KEY="$(tail -n 1 "$TOKEN_CODEX_OUTPUT")" \
TELEGRAM_BOT_TOKEN='PASTE_TOKEN_TAM_THOI_O_DAY' \
TELEGRAM_CHAT_ID='CHAT_ID' \
./scripts/create_member_openclaw_assistant.sh --name <ten_user>
```

Env provider được app hỗ trợ:

- `CUSTOM_PROVIDER_API_KEY`: API key thật, chỉ ghi vào config container cần dùng, không in ra log.
- `CUSTOM_PROVIDER_ENDPOINT_ID`: mặc định `9rt`.
- `CUSTOM_PROVIDER_BASE_URL`: với member mới, đặt `https://codex.anhlaptrinh.vn/v1`.
- `CUSTOM_PROVIDER_MODEL_ID`: mặc định `codex`.
- `CUSTOM_PROVIDER_SUPPORTS_IMAGE_INPUT`: mặc định `Y` để giống member mẫu `anhlaptrinh`; khi `Y`, model input là `text+image`.
- `CUSTOM_PROVIDER_MAX_TOKENS`: mặc định `4096`, giống member mẫu `anhlaptrinh`.

Không ghi token thật vào skill, README, nhật ký, câu trả lời, Git, hoặc file dùng chung. Nếu script lưu Telegram settings, token/chat id chỉ nằm trong container tại `/root/.openclaw/telegram.env` với quyền riêng tư.

## Cấu hình Telegram allowlist thủ công

Nếu cần đổi một trợ lý đã tạo từ `pairing` sang `allowlist`, sửa đúng config trong container member VPS, không sửa OpenClaw host chính:

```bash
docker exec -i user-<ten_user> node <<'NODE'
const fs = require('fs');
const path = '/root/.openclaw/openclaw.json';
const accountId = '<ten_user>';
const chatId = '<telegram_chat_id>';
const config = JSON.parse(fs.readFileSync(path, 'utf8'));
config.channels ??= {};
config.channels.telegram ??= {};
  config.channels.telegram.dmPolicy = 'pairing';
config.channels.telegram.allowFrom = Array.isArray(config.channels.telegram.allowFrom) ? config.channels.telegram.allowFrom : [];
if (!config.channels.telegram.allowFrom.includes(chatId)) config.channels.telegram.allowFrom.push(chatId);
config.channels.telegram.accounts ??= {};
config.channels.telegram.accounts[accountId] ??= {};
const account = config.channels.telegram.accounts[accountId];
account.enabled = true;
account.dmPolicy = 'pairing';
account.allowFrom = Array.isArray(account.allowFrom) ? account.allowFrom : [];
if (!account.allowFrom.includes(chatId)) account.allowFrom.push(chatId);
fs.writeFileSync(path, JSON.stringify(config, null, 2) + '\n');
NODE
```

Không dùng key `allowlist` trong OpenClaw config vì `openclaw config validate` báo invalid; key đúng là `allowFrom`.

## Cấu hình Telegram Group ID khi tạo nhân viên

Khi người dùng cung cấp một hoặc nhiều Telegram Group ID lúc tạo nhân viên, coi đây là input bắt buộc của quy trình tạo và thực hiện toàn bộ các bước sau:

Trước khi thao tác, đọc `references/member-vps-creation-checklist.md` và dùng checklist đó để đối chiếu đầu vào, preflight, runtime và tiêu chí hoàn tất.

1. Thu thập tên member, Telegram `accountId`, user ID chủ bot dùng cho DM, và từng Group ID dạng string. Mặc định `requireMention: false`; chỉ đổi thành `true` khi người dùng yêu cầu. Nhận bot token và credential qua kênh bảo mật, không ghi vào checklist hoặc báo cáo.
2. Đặt `groupPolicy: "allowlist"` tại đúng cấp Telegram/account theo schema của phiên bản OpenClaw đang cài.
3. Thêm từng Group ID vào cả `channels.telegram.groups` và `channels.telegram.accounts.<accountId>.groups`; đặt `enabled: true`, `requireMention` theo yêu cầu và `allowFrom: ["*"]` để mọi thành viên trong đúng group được gọi bot.
4. Không bỏ trống group `allowFrom`: OpenClaw hiện hành có thể fallback về account/DM `allowFrom` và vô tình chỉ cho user chủ bot. Không đưa Telegram user ID chủ bot vào group `allowFrom` nếu mục tiêu là mở cho mọi thành viên.
5. Tạo binding từ đúng Telegram `accountId` tới agent `main` cho từng Group ID.
6. Mỗi binding group phải có `match.peer.kind: "group"` và `match.peer.id` là Group ID dạng string.
7. Tạo một binding riêng cho mỗi group; không gộp nhiều Group ID vào một binding.
8. Trước khi thêm, kiểm tra toàn bộ `bindings` và không tạo bản ghi trùng bộ khóa `agentId + channel + accountId + peer.kind + peer.id`.
9. Chạy `openclaw config validate` thành công trước khi restart gateway. Nếu validate lỗi, không restart và không báo cấu hình đã hoàn tất.
10. Kiểm tra BotFather `Group Privacy` đã tắt nếu group cần nhận tin nhắn thường không mention. Việc này cần người quản trị bot xác nhận hoặc thao tác bằng `/setprivacy` → chọn bot → `Disable`.
11. Sau restart, chạy `openclaw gateway status` và `openclaw channels status --probe`, rồi kiểm tra log có inbound từ đúng Group ID và outbound gửi thành công.
12. Không báo thành công hoàn toàn nếu mới chỉ validate/configure mà chưa thấy cả inbound và outbound thực tế.

Mẫu binding cho một group:

```json
{
  "agentId": "main",
  "match": {
    "channel": "telegram",
    "accountId": "<telegram_account_id>",
    "peer": {
      "kind": "group",
      "id": "<telegram_group_id>"
    }
  }
}
```

Thứ tự kiểm tra bắt buộc:

```bash
docker exec user-<ten_user> sh -lc 'openclaw config validate'
docker exec user-<ten_user> sh -lc 'tmux kill-session -t openclaw 2>/dev/null || true; tmux new-session -d -s openclaw "openclaw gateway"; sleep 8; openclaw gateway status'
docker exec user-<ten_user> sh -lc 'journalctl --user -u openclaw-gateway.service --since "10 minutes ago" --no-pager -o cat 2>/dev/null | rg -i "telegram:group|inbound|outbound send ok" || true'
```

Nếu gateway trong container không chạy bằng user systemd, đọc log của tmux/process hoặc log OpenClaw tương ứng. Yêu cầu người dùng gửi một tin nhắn thử trong từng group; nếu `requireMention: false`, phải thử tin nhắn không mention. Chỉ báo **hoàn tất cấu hình, chờ xác nhận thực tế** khi chưa có tin thử; chỉ báo **hoàn tất hoàn toàn** sau khi thấy inbound và outbound của đúng group.

Nếu không có inbound, kiểm tra lại Group ID hiện tại, binding, group allowlist, user `allowFrom` và BotFather Privacy Mode. Nếu có inbound nhưng không có phản hồi, kiểm tra routing tới `main`, provider/model và log gateway.

Khi phát hiện Group ID đổi do group chuyển thành supergroup hoặc cần kiểm tra JSON, dùng quy trình tích hợp sau:

1. Backup `openclaw.json` vào `/root/_Backups/openclaw/` trước khi sửa.
2. Xem log gateway trong 7 ngày gần nhất, tìm `Group migrated`, `Migrating group config` và `telegram:group:<id>` để xác định ID mới thật.
3. Giữ ID cũ, thêm ID mới vào `channels.telegram.groups` và `channels.telegram.accounts.<accountId>.groups`; group mới phải có `requireMention: false` nếu user muốn nhắn không mention.
4. Giữ wildcard `"*": {"requireMention": true}` để group chưa xác minh không tự mở.
5. Kiểm tra không trùng binding và chạy cả `python3 -m json.tool <config>` lẫn `openclaw config validate`; chỉ restart sau khi cả hai đều đạt.
6. Sau hot reload/restart, kiểm tra inbound và outbound của ID mới; không báo hoàn tất chỉ vì JSON hợp lệ.

Approve pairing nếu user đã nhắn bot và có pairing code:

```bash
docker exec user-<ten_user> openclaw pairing approve --channel telegram --account <ten_user> <PAIRING_CODE>
```

## Đăng nhập Zalo Personal/Zalo User và gửi QR qua Telegram

Áp dụng khi người dùng muốn OpenClaw trong member VPS dùng tài khoản Zalo cá nhân, đặc biệt khi QR hết hạn nhanh hoặc việc mở QR qua web mất thời gian. Workflow QR, backup, policy, cleanup và kiểm tra đều nằm trong các mục bên dưới; với member VPS đã có Telegram thì ưu tiên gửi ảnh QR trực tiếp tới Telegram allowlist.

### Đầu vào và preflight

1. Xác định đúng container `user-<ten_user>` và kiểm tra đang running.
2. Kiểm tra OpenClaw version; plugin Zalo phải dùng cùng version, không dùng `latest`.
3. Xác nhận Telegram account hiện có `enabled`, có `tokenFile` hoặc bot token, và có ít nhất một Telegram user ID dạng số trong `allowFrom`.
4. Không coi Telegram user ID là Zalo user ID; đây là hai hệ định danh khác nhau.
5. Không in bot token, cookie Zalo, QR raw payload hoặc nội dung credential ra terminal, log, skill hay câu trả lời.

Lệnh kiểm tra:

```bash
docker ps -a --filter name='^/user-<ten_user>$'
docker exec user-<ten_user> openclaw --version
docker exec user-<ten_user> openclaw channels status --probe
```

### Backup bắt buộc

Backup config và credential Zalo nếu đã tồn tại trước khi cài plugin, login lại hoặc đổi policy:

```bash
TS=$(date -u '+%Y%m%dT%H%M%SZ')
BACKUP_DIR="/root/_Backups/<ten_user>_zalouser_$TS"
install -d -m 700 "$BACKUP_DIR"
docker exec user-<ten_user> sh -lc \
  'tar -C /root/.openclaw -czf - openclaw.json $(test -d credentials/zalouser && printf credentials/zalouser || true)' \
  > "$BACKUP_DIR/openclaw_before.tar.gz"
chmod 600 "$BACKUP_DIR/openclaw_before.tar.gz"
```

### Cài plugin Zalo đúng version

Với OpenClaw bản mới nhất:

```bash
docker exec user-<ten_user> \
  openclaw plugins install --pin '@openclaw/zalouser@2026.7.1'
docker exec user-<ten_user> openclaw config validate
```

Trước khi cài plugin, chạy `npm view @openclaw/zalouser@2026.7.1 peerDependencies --json` và xác nhận core `2026.7.1-2` đáp ứng peer dependency `openclaw >=2026.7.1`.

### Gửi QR mới trực tiếp vào Telegram allowlist

Tạo một watcher tạm trong `/tmp` bên trong container trước khi chạy login. Watcher phải:

- Đọc `/root/.openclaw/openclaw.json` để tìm Telegram account đang enabled.
- Đọc bot token từ `tokenFile` bên trong process; không truyền token trong command line và không ghi token vào log.
- Lấy Telegram recipient từ `channels.telegram.accounts.<account>.allowFrom`, fallback về `channels.telegram.allowFrom`; chỉ nhận ID dạng số.
- Theo dõi `/tmp/openclaw/openclaw-zalouser-qr-default.png` và các file khớp `*zalouser*qr*.png`.
- Ghi nhận checksum của file có sẵn khi watcher bắt đầu để không gửi QR cũ.
- Poll khoảng `0.25` đến `1` giây; khi checksum thay đổi, gọi Telegram Bot API `sendPhoto` ngay.
- Nếu có QR mới thay QR cũ, gửi ảnh mới trước rồi mới xóa tin nhắn QR cũ nếu có `message_id`.
- Log chỉ ghi bot username, số recipient, tên file và trạng thái gửi; không ghi token, Telegram ID hoặc QR payload.
- Chỉ chạy trong thời gian login; phải dừng và xóa watcher sau khi thành công hoặc hủy.

Caption nên ngắn và rõ: `QR đăng nhập Zalo Personal mới của OpenClaw <ten_user>. Hãy quét ngay vì QR có thời hạn ngắn.`

Nếu Telegram chưa sẵn sàng, fallback sang web QR theo thứ tự: copy QR mới từ `/tmp/openclaw/openclaw-zalouser-qr-default.png` tới file public `/var/www/html/openclaw-qr.png`, đặt quyền đọc phù hợp, kiểm tra URL `https://<domain>/openclaw-qr.png`, rồi xóa QR sau khi đăng nhập thành công. Không mở URL public nếu đã gửi Telegram được; không ghi QR raw payload, cookie hoặc token vào log.

### Tạo QR và chờ đăng nhập

Ưu tiên lệnh login riêng thay vì chạy toàn bộ `openclaw onboard`:

```bash
docker exec -it user-<ten_user> \
  openclaw channels login --channel zalouser --verbose
```

Khi terminal báo:

```text
Scan QR image: /tmp/openclaw/openclaw-zalouser-qr-default.png
```

watcher phải gửi ảnh tới Telegram allowlist gần như ngay lập tức. Giữ phiên PTY mở cho tới khi OpenClaw báo `Login successful`. Nếu QR hết hạn, tạo QR mới; watcher tự nhận checksum mới và gửi lại.

Sau login, credential thường nằm tại:

```text
/root/.openclaw/credentials/zalouser/credentials.json
```

Không đọc/in cookie thật. Chỉ kiểm tra file tồn tại và quyền truy cập phù hợp.

### Chọn policy Zalo

Nếu user chưa yêu cầu, giữ DM `pairing`. Nếu user yêu cầu DM allowlist và group open, làm đúng thứ tự sau:

1. Yêu cầu người dùng nhắn Zalo Personal bot một tin để tạo pairing request.
2. Chạy `openclaw pairing list zalouser`.
3. Đối chiếu tên người gửi với user; không approve request khác dù xuất hiện cùng lúc.
4. Approve đúng pairing code.
5. Lấy đúng `userId` của sender vừa approve và ghi rõ vào `channels.zalouser.allowFrom`.
6. Đặt `channels.zalouser.dmPolicy: allowlist` và `channels.zalouser.groupPolicy: open`.

Lệnh mẫu:

```bash
docker exec user-<ten_user> openclaw pairing list zalouser
docker exec user-<ten_user> \
  openclaw pairing approve zalouser <PAIRING_CODE>
docker exec user-<ten_user> \
  openclaw config set channels.zalouser.dmPolicy allowlist
docker exec user-<ten_user> \
  openclaw config set channels.zalouser.allowFrom '["<ZALO_USER_ID>"]' --strict-json
docker exec user-<ten_user> \
  openclaw config set channels.zalouser.groupPolicy open
```

Lưu ý với OpenClaw hiện hành: `pairing approve` có thể ghi sender vào file credential `zalouser-default-allowFrom.json`, nhưng `openclaw config validate` vẫn có thể cảnh báo nếu `channels.zalouser.allowFrom` rỗng. Vì vậy, khi dùng `dmPolicy: allowlist`, bắt buộc đồng bộ sender ID vào `channels.zalouser.allowFrom`; không chỉ approve pairing rồi dừng.

Không dùng `allowFrom: ["*"]` cho Zalo DM. Wildcard DM sẽ mở tin nhắn riêng ngoài ý muốn.

### Chỉ mở một Zalo group và không cần mention

Khi user yêu cầu bot chỉ phản hồi trong một group Zalo cụ thể mà thành viên không cần mention, không dùng `groupPolicy: open` vì giá trị đó mở tất cả group mà tài khoản Zalo tham gia.

Trigger bắt buộc dùng phần này gồm các cách nói như: `Zalo group không cần mention`, `không cần tag bot vẫn trả lời`, `chỉ áp dụng group này`, `thêm Zalo Group ID`, `add group Zalo`, `requireMention false`, hoặc yêu cầu tương đương về việc bot đọc tin nhắn thường trong một group Zalo cụ thể.

1. Lấy Group ID thật bằng directory API; ưu tiên ID số, không dùng tên nếu không cần:

```bash
docker exec user-<ten_user> \
  openclaw directory groups list --channel zalouser --json
```

Output có thể trả `id: "group:<GROUP_ID>"`; key trong `channels.zalouser.groups` dùng phần số `<GROUP_ID>`.

2. Cấu hình route allowlist cho đúng group, cho mọi sender trong group đó và tắt mention:

```bash
docker exec user-<ten_user> \
  openclaw config set channels.zalouser.groupPolicy allowlist
docker exec user-<ten_user> \
  openclaw config set channels.zalouser.groupAllowFrom '["*"]' --strict-json
docker exec user-<ten_user> \
  openclaw config set 'channels.zalouser.groups["<GROUP_ID>"]' \
  '{"enabled":true,"requireMention":false}' --strict-json
```

Ý nghĩa và phạm vi:

- `groupPolicy: allowlist` chặn mọi group không có trong `channels.zalouser.groups`.
- `groups.<GROUP_ID>.enabled: true` chỉ mở đúng group đã chọn.
- `groups.<GROUP_ID>.requireMention: false` cho phép tin nhắn thường kích hoạt bot.
- `groupAllowFrom: ["*"]` cho phép mọi thành viên gửi tin trong các group đã route-allowlist; không mở DM và không mở group ngoài danh sách.
- Không bỏ `groupAllowFrom` khi `groupPolicy: allowlist`: OpenClaw hiện hành có thể chặn toàn bộ sender group vì group sender allowlist rỗng.
- Nếu chỉ có một group trong `groups`, wildcard sender vẫn chỉ có hiệu lực trong group đó do route policy chạy trước sender policy.

3. Validate, restart và kiểm tra:

```bash
docker exec user-<ten_user> openclaw config validate
docker exec user-<ten_user> sh -lc \
  'tmux kill-session -t openclaw 2>/dev/null || true; sleep 1; tmux new-session -d -s openclaw "openclaw gateway"; sleep 8'
docker exec user-<ten_user> openclaw channels status --probe
```

Yêu cầu user gửi một tin nhắn chữ bình thường trong group, không mention và không reply bot. Chỉ báo **cấu hình hoàn tất, chờ test thực tế** nếu chưa thấy inbound/outbound; chỉ báo **hoàn tất hoàn toàn** sau khi bot phản hồi tin không mention trong đúng group. Đồng thời thử một group Zalo khác nếu có để xác nhận group ngoài allowlist bị chặn.

### Restart, kiểm tra và dọn dẹp

```bash
docker exec user-<ten_user> openclaw config validate
docker exec user-<ten_user> sh -lc \
  'tmux kill-session -t openclaw 2>/dev/null || true; sleep 1; tmux new-session -d -s openclaw "openclaw gateway"; sleep 8'
docker exec user-<ten_user> openclaw channels status --probe
```

Tiêu chí hoàn tất:

- Zalo Personal: `enabled`, `configured`, `running`, `works`.
- Nếu DM allowlist: probe hiển thị `dm:allowlist` và config có ít nhất một `allowFrom` đã xác minh.
- Nếu group open: `channels.zalouser.groupPolicy` là `open`.
- Telegram account cũ vẫn `running`, `works`, `audit ok`; trạng thái `disconnected` ngay sau restart có thể là tạm thời, chờ vài giây rồi probe lại.
- Không còn watcher tạm hoặc file `*zalouser*qr*.png` trong `/tmp/openclaw`.
- Pairing request của sender lạ không được approve.

Dọn file/process tạm sau thành công:

```bash
docker exec user-<ten_user> sh -lc '
  test -f /tmp/<ten_user>_zalo_qr_sender.pid && \
    kill "$(cat /tmp/<ten_user>_zalo_qr_sender.pid)" 2>/dev/null || true
  rm -f /tmp/<ten_user>_zalo_qr_sender.py \
        /tmp/<ten_user>_zalo_qr_sender.pid \
        /tmp/<ten_user>_zalo_qr_sender.log \
        /tmp/openclaw/openclaw-zalouser-qr-default.png
'
```

Sau thay đổi, cập nhật `/root/_Second_AI_Brain/06_Nhat_Ky_Thay_Doi.md`, nhưng không ghi bot token, Telegram/Zalo user ID thật, cookie hoặc QR payload.

## Chạy gateway bằng tmux trong member VPS

Trong container member VPS, cài tmux và chạy gateway theo yêu cầu chuẩn:

```bash
docker exec user-<ten_user> sh -lc 'apt update && apt install tmux -y'
docker exec user-<ten_user> sh -lc 'tmux kill-session -t openclaw 2>/dev/null || true; tmux new-session -d -s openclaw "openclaw gateway"'
```

Kiểm tra:

```bash
docker exec user-<ten_user> sh -lc 'tmux ls && openclaw gateway status && openclaw channels status --probe'
```

## Cấu hình Custom Provider 9Router

Tham khảo schema từ member mẫu `/root/Apps/member_vps/docker-users/data/anhlaptrinhthu/.openclaw/openclaw.json`. Member mẫu này giữ home nội bộ `/home/anhlaptrinh`. Khi cấu hình trong member VPS mới, sửa config bên trong container `user-<ten_user>` tại `/root/.openclaw/openclaw.json`.

Không ghi API key thật vào skill, README, nhật ký hoặc câu trả lời. Với member mới, lấy key từ output bảo mật của command Token Codex tích hợp ở trên và ghi trực tiếp vào config container cần dùng.

Mẫu script cấu hình, thay `<API_KEY>` bằng key thật chỉ khi chạy thực tế:

```bash
docker exec -i user-<ten_user> node <<'NODE'
const fs = require('fs');
const path = '/root/.openclaw/openclaw.json';
const config = JSON.parse(fs.readFileSync(path, 'utf8'));
config.agents ??= {};
config.agents.defaults ??= {};
config.agents.defaults.model = { primary: '9rt/codex' };
config.agents.defaults.imageModel = { primary: '9rt/codex' };
config.agents.defaults.imageGenerationModel = { primary: '9rt/codex' };
config.agents.defaults.models ??= {};
config.agents.defaults.models['9rt/codex'] = config.agents.defaults.models['9rt/codex'] || {};
config.models ??= {};
config.models.mode = 'merge';
config.models.providers ??= {};
config.models.providers['9rt'] = {
  baseUrl: 'https://9router.anhlaptrinh.vn/v1',
  api: 'openai-completions',
  apiKey: '<API_KEY>',
  models: [{
    id: 'codex',
    name: 'codex (Custom Provider)',
    contextWindow: 128000,
    maxTokens: 4096,
    input: ['text', 'image'],
    cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
    reasoning: false
  }]
};
fs.writeFileSync(path, JSON.stringify(config, null, 2) + '\n');
NODE
```

Sau khi cấu hình provider, validate và restart gateway tmux:

```bash
docker exec user-<ten_user> sh -lc 'openclaw config validate'
docker exec user-<ten_user> sh -lc 'tmux kill-session -t openclaw 2>/dev/null || true; tmux new-session -d -s openclaw "openclaw gateway"; sleep 8; openclaw gateway status; openclaw models list | head'
```

## Bật audio understanding cho member VPS

Khi tạo mọi trợ lý OpenClaw member VPS, luôn bật audio transcription để bot đọc được voice/audio từ Telegram/Zalo. Đây là cấu hình mặc định bắt buộc, không chờ người dùng yêu cầu riêng. Chuẩn dùng model `gpt-4o-mini-transcribe`, ngôn ngữ `vi`, và provider `openai` đi qua 9Router. Không tự cài `ffmpeg` cho chức năng này; chỉ cài khi có yêu cầu chuyển đổi định dạng audio riêng.

Config cần có trong container `user-<ten_user>` tại `/root/.openclaw/openclaw.json`:

```json
{
  "tools": {
    "media": {
      "audio": {
        "enabled": true,
        "language": "vi",
        "timeoutSeconds": 60,
        "echoTranscript": true,
        "echoFormat": "📝 \"{transcript}\"",
        "models": [
          {
            "provider": "openai",
            "type": "provider",
            "model": "gpt-4o-mini-transcribe",
            "capabilities": ["audio"],
            "language": "vi"
          }
        ]
      }
    }
  },
  "models": {
    "providers": {
      "openai": {
        "baseUrl": "https://9router.anhlaptrinh.vn/v1",
        "apiKey": "DUNG_API_KEY_9ROUTER_DANG_CO",
        "request": {
          "allowPrivateNetwork": true
        },
        "models": [
          {
            "id": "gpt-4o-mini-transcribe",
            "name": "gpt-4o-mini-transcribe",
            "input": ["audio"],
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            }
          }
        ]
      }
    }
  }
}
```

Lệnh vá an toàn cho member VPS đã tạo, tự copy `apiKey` từ provider `9rt` sang provider `openai` nếu có. Không in key ra màn hình:

```bash
docker exec -i user-<ten_user> node <<'NODE'
const fs = require('fs');
const path = '/root/.openclaw/openclaw.json';
const config = JSON.parse(fs.readFileSync(path, 'utf8'));
config.tools ??= {};
config.tools.media ??= {};
config.tools.media.audio = {
  enabled: true,
  language: 'vi',
  echoTranscript: true,
  models: [{
    type: 'provider',
    provider: 'openai',
    model: 'gpt-4o-mini-transcribe',
    capabilities: ['audio'],
    language: 'vi'
  }]
};
config.models ??= {};
config.models.mode = config.models.mode || 'merge';
config.models.providers ??= {};
const existingKey = config.models.providers['openai']?.apiKey || config.models.providers['9rt']?.apiKey || config.models.providers['9r']?.apiKey;
config.models.providers['openai'] = {
  baseUrl: 'https://9router.anhlaptrinh.vn/v1',
  apiKey: existingKey || 'DUNG_API_KEY_9ROUTER_DANG_CO',
  request: { allowPrivateNetwork: true },
  models: [{
    id: 'gpt-4o-mini-transcribe',
    name: 'gpt-4o-mini-transcribe',
    input: ['audio'],
    cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 }
  }]
};
fs.writeFileSync(path, JSON.stringify(config, null, 2) + '\n');
NODE
```

Validate và restart gateway bằng tmux vì member VPS không dùng systemd user service cho OpenClaw:

```bash
docker exec user-<ten_user> sh -lc 'openclaw config validate'
docker exec user-<ten_user> sh -lc 'tmux kill-session -t openclaw 2>/dev/null || true; tmux new-session -d -s openclaw "openclaw gateway"; sleep 8; openclaw gateway status; openclaw channels status --probe'
```

Nếu voice/audio vẫn chưa đọc được, điều tra theo thứ tự:

1. Xem log để xác nhận OpenClaw đã nhận file `.ogg`/audio chưa.
2. Nếu lỗi `SsrFBlockedError`, thường do `baseUrl` còn là `http://localhost:20128/v1`; đổi sang `https://9router.anhlaptrinh.vn/v1`.
3. Nếu lỗi `ProviderAuthError`, provider `openai` đang thiếu `apiKey`; copy credential đang dùng ở provider `9rt`/custom provider sang provider `openai`, không in key ra màn hình.
4. Test API models không lộ key:
   ```bash
   docker exec user-<ten_user> sh -lc 'node -e "const c=require(\"/root/.openclaw/openclaw.json\"); const k=c.models?.providers?.openai?.apiKey; fetch(\"https://9router.anhlaptrinh.vn/v1/models\", {headers:{Authorization:\"Bearer \"+k}}).then(r=>console.log(r.status)).catch(e=>console.error(e.message))"'
   ```
5. Có thể test transcription trực tiếp bằng file `.ogg` mới nhất trong cache OpenClaw, nhưng không gửi/in nội dung audio riêng tư nếu chưa được user cho phép.

Kết luận thường gặp: nếu đổi từ local 9Router sang domain 9Router mà voice vẫn lỗi, nguyên nhân hay là provider `openai` thiếu auth; thêm/copy đúng `apiKey` là audio transcription chạy được.

### Xử lý voice Zalo dạng AAC URL

Khi plugin `zalouser` chỉ trả URL `https://*.zdn.vn/*.aac`, không đưa URL đó trực tiếp vào endpoint STT. Chỉ chấp nhận HTTPS trên `zdn.vn` hoặc subdomain, giới hạn file tải xuống tối đa `25 MB`, dùng thư mục tạm và xóa file sau khi hoàn tất:

1. Cài `ffmpeg` trong đúng VPS/container có Zalo Personal; không cài cho member chỉ dùng Telegram.
2. Tải URL vào file tạm, chuyển bằng `ffmpeg` sang MP3 mono `16 kHz`.
3. Đọc API key từ provider `openai`, `9rt` hoặc `9r` trong `openclaw.json`, không in key.
4. Gọi `https://9router.anhlaptrinh.vn/v1/audio/transcriptions` với model `gpt-4o-mini-transcribe`, language `vi`, rồi chỉ trả transcript.
5. Xóa AAC/MP3 tạm ngay cả khi request lỗi; không ghi audio, URL riêng tư hoặc transcript vào log.

Nếu cần tự động hóa bước này, viết script ngay trong project member theo quy tắc trên; không cài hoặc gọi một skill voice riêng.

## Bật web search DuckDuckGo cho member VPS

Khi tạo trợ lý OpenClaw trong member VPS, luôn cấu hình DuckDuckGo làm search provider mặc định để bot trả lời được các câu hỏi cần tra cứu web tổng quát. Không dùng provider cần API key nếu người dùng chưa cung cấp rõ.

Triệu chứng cần áp dụng/sửa:

- Bot báo lỗi `web_search` hoặc `no provider is available`.
- `tools.web.search.enabled` đã bật nhưng `plugins.entries` chưa có search plugin khả dụng.
- `plugins.entries` chỉ bật Telegram/Zalo hoặc các plugin không phải search provider.

Cấu hình cần có trong container `user-<ten_user>` tại `/root/.openclaw/openclaw.json`:

```json
{
  "plugins": {
    "entries": {
      "duckduckgo": {
        "enabled": true
      }
    }
  },
  "tools": {
    "profile": "full",
    "web": {
      "search": {
        "enabled": true,
        "provider": "duckduckgo",
        "openaiCodex": {
          "enabled": true
        }
      }
    }
  }
}
```

Lệnh vá an toàn cho member VPS đã tạo:

```bash
docker exec -i user-<ten_user> node <<'NODE'
const fs = require('fs');
const path = '/root/.openclaw/openclaw.json';
const config = JSON.parse(fs.readFileSync(path, 'utf8'));
config.plugins ??= {};
config.plugins.entries ??= {};
config.plugins.entries.duckduckgo = { enabled: true };
config.tools ??= {};
config.tools.profile = 'full';
config.tools.web ??= {};
config.tools.web.search ??= {};
config.tools.web.search.enabled = true;
config.tools.web.search.provider = 'duckduckgo';
config.tools.web.search.openaiCodex ??= {};
config.tools.web.search.openaiCodex.enabled = true;
fs.writeFileSync(path, JSON.stringify(config, null, 2) + '\n');
NODE
```

Sau khi vá DuckDuckGo, validate và restart gateway trong container:

```bash
docker exec user-<ten_user> sh -lc 'openclaw config validate'
docker exec user-<ten_user> sh -lc 'tmux kill-session -t openclaw 2>/dev/null || true; tmux new-session -d -s openclaw "openclaw gateway"; sleep 8; openclaw gateway status'
```

Khi báo kết quả cho user, hướng dẫn test bằng câu hỏi cần tra cứu web, ví dụ hỏi tin mới hoặc thông tin thị trường hiện tại. Không tự gửi tin Telegram thật nếu chưa được user cho phép.

## Kiểm tra sau khi chạy

```bash
cd /root/Apps/member_vps/docker-users
bash manage-user.sh show <ten_user>
docker exec user-<ten_user> sh -lc 'openclaw --version && openclaw gateway status && openclaw channels status --probe'
docker exec user-<ten_user> sh -lc 'python3 --version && document-python --version && command -v pdfinfo && command -v pdftotext'
docker exec user-<ten_user> sh -lc '/home/<ten_user>/.openclaw/tools/document-venv/bin/python -c "import openpyxl,pypdf,pdfplumber,fitz,PIL,xlsxwriter,pandas; print(\"document_modules=OK\")"'
```

## Chuẩn độ ổn định Zalo cho member đang chạy

Khi member dùng Zalo để xử lý PDF/Excel/ảnh/video hoặc từng có hiện tượng Zalo im trong khi Telegram vẫn chạy:

1. Bật watchdog `member_anhlaptrinh_zalouser` theo mẫu shared center, kiểm tra cả `channels status --probe` và sự kiện listener cuối cùng trong log.
2. Cài bộ công cụ tài liệu bằng `/root/Automation/openclaw_member_assistant/scripts/setup_member_document_tools.sh`.
3. Ghi các quy tắc reliability trực tiếp vào workspace/AGENTS của member: phản hồi sớm nếu tác vụ quá 20 giây, cập nhật sau khoảng 120 giây, tách tác vụ nặng thành worker khi có thể, kiểm tra file trước khi gửi, không gửi file rỗng/hỏng, tạo bản nhẹ nếu file vượt 8 MB và chỉ báo đã gửi sau khi kiểm tra thành công.
4. Đặt `tools.sessions.visibility: agent` khi session chính cần theo dõi worker cùng agent; không đặt `all` nếu không cần cross-agent.
5. Đặt giới hạn context và session maintenance; compact session vượt ngưỡng bằng `/root/Automation/openclaw_member_assistant/scripts/audit_member_sessions.sh` sau khi backup.
6. Không xóa transcript cũ hoặc tự logout Zalo; nếu phục hồi thất bại, yêu cầu quét QR lại.

Báo cho người dùng:

- Container: `user-<ten_user>`
- Mật khẩu: `<ten_user>123`
- Port SSH/web lấy từ output của `manage-user.sh show <ten_user>` hoặc lúc tạo
- Dashboard nội bộ: `http://127.0.0.1:18789/`
- Dashboard public: `http://<PUBLIC_IP>:<web_port>/`; đăng nhập bằng token trong `/home/<ten_user>/.openclaw_dashboard_token`, để trống mật khẩu
- Token Codex email: `<email_khach_hang>`
- Token Codex mật khẩu mặc định: `alt123`, trừ khi người dùng yêu cầu mật khẩu khác
- Link đăng nhập xem credit/API usage còn lại: `https://codex.anhlaptrinh.vn/`
- Xác nhận API Token Codex đã được cấu hình vào member VPS và provider/model đã test thành công; không nêu full API key
- Nếu có Telegram group: báo `accountId`, Group ID, user ID allowlist, `requireMention`, trạng thái Privacy Mode, validate, gateway, inbound và outbound; không nêu bot token hoặc API key.

## Tích hợp Fanpage và CSKH (On-Demand)

Skill này chứa sẵn toàn bộ mã nguồn để tự động hóa đăng bài và nhắn tin CSKH qua Fanpage Facebook, được lưu trữ tại thư mục con `resources/post-fanpage-fb/`. Khi người dùng yêu cầu cài đặt Auto Post Facebook hoặc Auto Nhắn tin CSKH, hãy thực hiện cài đặt trực tiếp từ thư mục này.

**Tuyệt đối tuân thủ 6 nguyên tắc (Checklist) sau nếu phải thiết lập tích hợp này:**
1. **Kiểm tra đúng tên file JSON:** File Service Account của Google Sheets **BẮT BUỘC** phải được đổi tên thành `googlesheetcn.json` và nằm ở thư mục gốc của dự án.
2. **Đầy đủ Token trong `.env`:** Phải có file `.env` ở thư mục gốc, chứa đủ `SPREADSHEET_ID`, `FB_PAGE_ID`, `FB_PAGE_ACCESS_TOKEN`, `MESSENGER_TOKEN`.
3. **Quyền truy cập Google Sheet:** Bắt buộc phải Share quyền **Editor** của bảng tính cho địa chỉ email service account bên trong file `googlesheetcn.json`.
4. **Thư mục chứa ảnh:** Đảm bảo có thư mục `images/` nằm ở thư mục gốc.
5. **Cài đặt Cronjob chuẩn ALT:** KHÔNG chèn trực tiếp lệnh `python` vào `crontab`. Bắt buộc dùng file bash wrapper `run_fanpage_cron.sh` hoặc `run_cskh_cron.sh` (có chứa lệnh cd và gọi venv).
6. **Cấp quyền thực thi:** File bash chạy cron bắt buộc phải được cấp quyền `chmod +x`.
7. **Tích hợp OpenClaw Workspace & Prompt (BẮT BUỘC):** Copy `SKILL.md` vào `~/.openclaw/workspace/skills/post-fanpage-fb/SKILL.md` và khai báo cấu hình vai trò (`IDENTITY.md`) + ánh xạ lệnh chạy bash script (`AGENTS.md`) để OpenClaw Telegram Bot tự biết thực thi script Python trên VPS thay vì trả lời lý thuyết chung chung.

### Phân luồng Hướng dẫn 

**Luồng 1: Nếu người dùng yêu cầu "Cài auto post Facebook" hoặc "Đăng bài Fanpage"**
- Chỉ tập trung hướng dẫn người dùng cấu hình tab "Fanpage" trên Google Sheet.
- Mặc định thiết lập chạy mỗi 4 giờ (`0 */4 * * *`) bằng file `run_fanpage_cron.sh`. Nếu có yêu cầu khác thì đổi lịch tương ứng.

**Luồng 2: Nếu người dùng yêu cầu "Cài tự động CSKH" hoặc "Cài auto nhắn tin"**
- Chỉ tập trung hướng dẫn người dùng cấu hình tab "Chăm Sóc Khách Hàng" trên Google Sheet.
- Mặc định thiết lập chạy mỗi 5 phút (`*/5 * * * *`) bằng file `run_cskh_cron.sh`.

Không cài mặc định hoặc lôi kéo người dùng cài đặt tính năng này trừ khi được yêu cầu rõ ràng.

## Quy trình sửa/nâng cấp workflow

1. Đọc `/root/_Second_AI_Brain/START_HERE.md`, bản đồ VPS, registry project, và checklist production nếu sửa script đang chạy.
2. Backup file sắp sửa vào `/root/_Backups`.
3. Sửa automation tại `/root/Automation/openclaw_member_assistant`.
4. Cập nhật skill này nếu đổi input/output, đường dẫn, version OpenClaw, token mặc định, logic port, hoặc cách chạy Telegram.
5. Chạy `bash -n` cho script shell và ít nhất một lệnh `--dry-run`.
6. Quét không để lộ secret thật.
7. Ghi `/root/_Second_AI_Brain/06_Nhat_Ky_Thay_Doi.md`.

## An toàn

- Không in Telegram bot token hoặc API key trong câu trả lời.
- Được gửi email, mật khẩu đăng nhập Token Codex và link `https://codex.anhlaptrinh.vn/` cho đúng khách hàng; không gửi full API key.
- Không sửa `.env`, credential, Chrome/Selenium profile nếu task không yêu cầu.
- Không xóa container/data folder khi chưa được yêu cầu rõ.
- Không mở port public ngoài SSH/web member VPS nếu chưa có yêu cầu rõ.
- Không tự gửi tin Telegram thật ngoài bước test được người dùng cho phép.
