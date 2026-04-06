#!/bin/bash
# =============================================================================
# SAFES - DigitalOcean Droplet Setup Script
# Run this ON the droplet after SSH-ing in:
#   ssh root@<DROPLET_IP>
#   bash setup_server.sh
# =============================================================================
set -e

echo "============================================="
echo " SAFES - Server Setup"
echo "============================================="

# 1. Update system
echo "[1/6] Updating system..."
apt-get update -qq && apt-get upgrade -y -qq

# 2. Install Docker
echo "[2/6] Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com | sh
    systemctl enable docker
    systemctl start docker
fi
docker --version

# 3. Install Docker Compose
echo "[3/6] Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    apt-get install -y -qq docker-compose-plugin 2>/dev/null || true
    # Fallback to standalone
    if ! docker compose version &> /dev/null; then
        curl -fsSL "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" \
            -o /usr/local/bin/docker-compose
        chmod +x /usr/local/bin/docker-compose
    fi
fi

# 4. Clone repo
echo "[4/6] Cloning SAFES repository..."
cd /root
if [ -d "safes" ]; then
    cd safes && git pull origin main
else
    git clone https://github.com/ShreyanshVaibhaw/SAFES-Source-Aware-Framework-for-Exam-Support-.git safes
    cd safes
fi

# 5. Create .env file
echo "[5/6] Setting up environment..."
if [ ! -f configs/.env ]; then
    cat > configs/.env << 'ENVEOF'
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-e3UeDbKrEftynAsl3YTtqfe9QOvWJXCB2UXaU47Gv7iN6SAibUTG0R14R6k6XyOl
OPENAI_BASE_URL=https://opencode.ai/zen/go/v1
LLM_MODEL=glm-5
ENVIRONMENT=production
LOG_LEVEL=INFO
ENVEOF
    echo "  .env created"
else
    echo "  .env already exists, skipping"
fi

# Export env vars for docker-compose
export $(grep -v '^#' configs/.env | xargs)

# 6. Build and start
echo "[6/6] Building and starting containers..."
docker compose up --build -d

echo ""
echo "============================================="
echo " SAFES is running!"
echo "============================================="
echo ""
DROPLET_IP=$(curl -s ifconfig.me 2>/dev/null || echo "<YOUR_DROPLET_IP>")
echo " Frontend:  http://${DROPLET_IP}"
echo " API:       http://${DROPLET_IP}:8000"
echo " API Docs:  http://${DROPLET_IP}:8000/docs"
echo " Health:    http://${DROPLET_IP}:8000/health"
echo ""
echo " View logs: docker compose logs -f"
echo " Stop:      docker compose down"
echo " Restart:   docker compose restart"
echo "============================================="
