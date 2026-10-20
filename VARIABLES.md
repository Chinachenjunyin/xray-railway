# Railway Variables — set these in the service, do NOT commit them

In Railway: open the service -> Variables tab -> add:

- UUID — a fresh UUID v4 (generate locally, keep private)
- WS_PATH — a random path starting with / (e.g. / + 16 random chars)

Railway provides PORT automatically. TLS is terminated by Railway at the
*.up.railway.app domain, so no certificate files are needed in the repo.

The same UUID and WS_PATH are what the FlClash/Shadowrocket generators
need locally (in a params.env that stays out of Git) after you have the
real Railway domain.
