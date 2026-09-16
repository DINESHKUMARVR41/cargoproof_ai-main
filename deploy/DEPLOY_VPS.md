# CargoProof deployment (no Docker)

This deployment keeps the application architecture intact. The only application change is that the frontend uses the same-origin API in production while preserving the existing localhost:4021 behavior for local development on port 5173.

## 1. Server
Use an Ubuntu 24.04 VPS with a public IP. Recommended minimum for the hackathon demo: 2 vCPU, 4 GB RAM, 20 GB disk.

Install:
```bash
sudo apt update
sudo apt install -y nginx git curl python3 python3-venv python3-pip
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
```

## 2. Copy project
```bash
sudo mkdir -p /opt/cargoproof
sudo cp -R . /opt/cargoproof/
sudo useradd --system --home /opt/cargoproof --shell /usr/sbin/nologin cargoproof || true
sudo chown -R cargoproof:cargoproof /opt/cargoproof
```

## 3. Node dependencies
```bash
cd /opt/cargoproof
sudo -u cargoproof npm ci
```

## 4. Python environment
```bash
cd /opt/cargoproof
sudo -u cargoproof python3 -m venv .venv
sudo -u cargoproof .venv/bin/pip install -r requirements.txt
sudo -u cargoproof .venv/bin/pip install -r verification_engine_service/requirements.txt
```

## 5. Environment
Create `/opt/cargoproof/.env` from `.env.example`.

For the first public demo, keep:
```env
PORT=4021
DEMO_MODE=true
VERIFICATION_ENGINE_URL=http://127.0.0.1:8001
EVIDENCE_API_URL=http://127.0.0.1:8000
```

Keep Algorand Testnet settings as supplied by the project. Only add funded wallet/payment variables when you intentionally want live x402 payment behavior.

## 6. Start the three application services
```bash
sudo cp deploy/systemd/cargoproof-api.service /etc/systemd/system/
sudo cp deploy/systemd/cargoproof-evidence.service /etc/systemd/system/
sudo cp deploy/systemd/cargoproof-verification.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now cargoproof-evidence
sudo systemctl enable --now cargoproof-verification
sudo systemctl enable --now cargoproof-api
```

Check:
```bash
systemctl status cargoproof-evidence --no-pager
systemctl status cargoproof-verification --no-pager
systemctl status cargoproof-api --no-pager
```

## 7. Expose the frontend + API
```bash
sudo cp deploy/nginx-cargoproof.conf /etc/nginx/sites-available/cargoproof
sudo ln -sf /etc/nginx/sites-available/cargoproof /etc/nginx/sites-enabled/cargoproof
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
```

Open `http://YOUR_SERVER_IP/`.

## 8. HTTPS
Point a domain to the VPS, then use Certbot:
```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.example
```

## 9. Smoke tests
```bash
curl http://127.0.0.1:4021/api/state
curl http://127.0.0.1:8000/api/v1/health
curl http://127.0.0.1:8001/api/v1/health
curl http://YOUR_SERVER_IP/api/state
```

The browser should load the frontend from the same host and the frontend API calls will automatically use `/api/...` in production.
