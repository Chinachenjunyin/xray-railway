# Xray VLESS+WS for Railway (prepared package)

Contents: Dockerfile + entrypoint.sh render config.json.template with the
UUID, WS_PATH and PORT environment variables, then run Xray.
External shape: VLESS + WS + TLS, port 443, host = your *.up.railway.app
domain (TLS is terminated by Railway's edge).

Upload:
1. Create a NEW private GitHub repository (do not add a README from GitHub).
2. Upload every file in this folder (including .gitignore) to that repo.
3. Back in Railway, on the service's Settings -> Source, tap Connect Repo
   and select that repository.
4. Add the variables from VARIABLES.md in the service's Variables tab
   BEFORE deploying, then generate a domain in Settings -> Networking.

Note: Railway's Fair Use Policy prohibits proxy/anonymization services;
the account owner deploys this at their own risk of removal.
