P0: Fix chat history data leak risk (views.py)
Change history caching to user-scoped keys (chat_history:{conversation_id}:{user_id}), and always fetch/authorize the session before any cache read.

P0: Remove unsafe global caching on authenticated views (views.py, views.py, views.py)
Replace @cache_page on user/admin endpoints with manual per-user cache keys, or disable caching there entirely until keys are safe.

P0: Restore proper DB migration workflow (.gitignore, app migrations/, entrypoint.sh)
Stop ignoring migrations, commit all app migrations, and run python manage.py migrate during startup/deploy.

P1: Harden Celery error handling (tasks.py)
Guard exception blocks so they do not reference undefined message/session variables after lookup failures; fail gracefully and log context safely.

P1: Enforce passcode policy consistently (serializers.py, models.py)
Route passcode updates through model validation (set_passcode) instead of directly hashing arbitrary input.

P1: Fix event extraction field mismatch (tasks.py)
Align parsed fields (start_time_iso vs start_time) so detected events store valid schedule values.

P1: Strengthen OTP/auth abuse controls (utils.py, views.py, settings.py)
Increase OTP strength (length + expiry policy), add per-email+IP verification throttles, and use non-enumerating responses for resend/forgot flows.

P2: Make test suite CI-safe (tests_integration.py)
Move real OpenAI-call tests behind an explicit marker/env flag; default tests should be mocked and deterministic.

P2: Clean secret/config handling (utils.py, .env, demo.env)
Unify Firebase credential filename/path handling, keep secret files out of git, and add a startup config validation command.

P2: Add release guardrails (README/CI config)
Require check, makemigrations --check, migrate, and test pass in CI before deploy to prevent regressions.