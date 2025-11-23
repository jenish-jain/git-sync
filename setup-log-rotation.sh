#!/bin/bash
# Setup log rotation for Git Sync

echo "Setting up log rotation..."

# 1. Configure systemd journal rotation
echo "Configuring systemd journal..."
sudo mkdir -p /etc/systemd/journald.conf.d/

sudo tee /etc/systemd/journald.conf.d/git-sync.conf > /dev/null << 'EOF'
[Journal]
# Keep logs for maximum 7 days
MaxRetentionSec=7day

# Limit disk usage
SystemMaxUse=100M
SystemKeepFree=1G

# Limit per-service logs
MaxFileSec=1day
EOF

# 2. Restart journald to apply changes
echo "Restarting journald..."
sudo systemctl restart systemd-journald

# 3. Clean existing old logs
echo "Cleaning old logs..."
sudo journalctl --vacuum-time=7d
sudo journalctl --vacuum-size=100M

# 4. Verify settings
echo ""
echo "Current journal settings:"
sudo journalctl --disk-usage

echo ""
echo "✅ Log rotation configured!"
echo ""
echo "Settings:"
echo "  - Logs kept for: 7 days"
echo "  - Max disk usage: 100 MB"
echo "  - Rotate daily"
echo ""
echo "To manually clean logs:"
echo "  sudo journalctl --vacuum-time=7d"
echo "  sudo journalctl --vacuum-size=100M"
