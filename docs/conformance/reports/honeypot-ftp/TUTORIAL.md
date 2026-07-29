# Tutorial: grade alexbredo/honeypot-ftp (FTP)

Upstream needs external `common-modules`; this lab ships minimal `base`/`handler` stubs and `ftp_lab.py` (plain FTP).

```bash
docker build -f .local/labs/honeypot-ftp/Dockerfile.lab -t honeypot-ftp:uhbs-lab .local/labs/honeypot-ftp
docker run -d --name honeypot-ftp-lab --network uhbs-lab -p 127.0.0.1:19021:21 honeypot-ftp:uhbs-lab
```

Published: quick **42.71 / F**, full **42.6 / F**.
