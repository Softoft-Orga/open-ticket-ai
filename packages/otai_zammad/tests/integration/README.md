# otai_zammad Integration Tests

These tests exercise a live Zammad instance and are disabled by default. To run them:

1. Obtain an API access token from the shared integration Zammad environment.
   - Visit `http://18.156.167.59/#profile/tokens` and create a personal access token with permission to read and write tickets.
   - Copy the generated token value.
2. Export the credentials before running pytest:
   ```bash
   export OTAI_ZAMMAD_TEST_TOKEN="<your-token>"
   export OTAI_ZAMMAD_TEST_URL="http://18.156.167.59/"  # optional; defaults to this value
   ```
3. Run the integration suite explicitly:
   ```bash
   uv run -m pytest packages/otai_zammad/tests/integration -m integration
   ```

The tests create tickets and notes as part of their validation. They rely on being able to create, update, and search tickets using the configured credentials.
