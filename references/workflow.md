# Workflow Summary

1. Require a secure Token Codex API key, or verify that a real provisioning backend exists before attempting account creation; an email is only required when creating a dashboard account.
2. If a new key is generated, create `/root/Data/private_accounts/token_codex/` with mode `700`, save the one-time output there with mode `600`, and never print the full key in chat or shared logs.
3. Preflight the actual container manager, image, SSH port, web port, volumes and existing container name; do not assume a dry-run flag exists.
4. Create/configure the member with the key passed through `TOKEN_CODEX_API_KEY` or `CUSTOM_PROVIDER_API_KEY`, plus Telegram env vars when available.
5. Resolve the assigned host web port mapped to container port `80` and the public IPv4 using Docker inspection.
6. Store the key in `/home/<name>/.openclaw/token-codex.env` with mode `600`; keep only `${TOKEN_CODEX_API_KEY}` in `openclaw.json` and source the env file before every Gateway start.
7. Configure Nginx, Gateway Token, Telegram policy, Second AI Brain and shared fallback proxy only when each component is present and validated.
8. Verify base URL `https://codex.anhlaptrinh.vn/v1`, API `openai-completions`, and exact models `GPT-5.6-sol`, `GPT-5.6-terra`, `GPT-5.6-luna`; do not restore an old provider or append `/v1` twice.
9. Verify public dashboard HTTP `200`, Gateway and channel status.
10. Report member VPS access plus Token Codex dashboard credentials only when an account was actually created, and `https://codex.anhlaptrinh.vn/` for remaining credit; never disclose the full API key.
