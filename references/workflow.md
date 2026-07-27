# Workflow Summary

1. Require the customer's email, then use the integrated Token Codex command in the main `SKILL.md` to dry-run and create the account with default password `alt123`, credit `250 USD`, and one member-named API.
2. Save the one-time API output in `/root/Data/private_accounts/token_codex/` with mode `600`; never print the full key in chat or shared logs.
3. Run member automation dry-run with `--name <user>`.
4. Run real automation with the saved key passed through `CUSTOM_PROVIDER_API_KEY`, plus Telegram env vars when available.
5. Resolve the assigned host web port mapped to container port `80` and the public IPv4.
6. Configure Nginx, Gateway Token, Telegram policy, Second AI Brain and shared fallback proxy.
7. Verify Token Codex provider/model, public dashboard HTTP `200`, gateway and channel status.
8. Report member VPS access plus Token Codex email, password, and `https://codex.anhlaptrinh.vn/` for remaining credit; never disclose the full API key.
