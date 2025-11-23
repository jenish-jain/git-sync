#!/bin/bash
# Git Sync - One-Line Installer
# Usage: curl -fsSL https://raw.githubusercontent.com/jenish-jain/git-sync/main/install.sh | bash

set -e

echo "=================================="
echo "Git Sync Installer"
echo "=================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install git first:"
    echo "   sudo apt-get update && sudo apt-get install -y git"
    exit 1
fi

# Check if python3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install python3 first:"
    echo "   sudo apt-get update && sudo apt-get install -y python3"
    exit 1
fi

echo "✅ Prerequisites met (git, python3)"
echo ""

# Clone the repository
INSTALL_DIR="$HOME/git-sync-setup"
echo "📦 Downloading Git Sync..."

if [ -d "$INSTALL_DIR" ]; then
    echo "   Removing existing installation..."
    rm -rf "$INSTALL_DIR"
fi

git clone https://github.com/jenish-jain/git-sync.git "$INSTALL_DIR"
cd "$INSTALL_DIR"

echo "✅ Downloaded successfully"
echo ""

# Install sync script
echo "📂 Installing sync script..."
sudo mkdir -p /opt/git-sync
sudo cp sync.py /opt/git-sync/
sudo chmod +x /opt/git-sync/sync.py
echo "✅ Installed to /opt/git-sync/sync.py"
echo ""

# Setup log rotation
echo "📝 Setting up log rotation..."
chmod +x setup-log-rotation.sh
./setup-log-rotation.sh
echo ""

# Create repository config if it doesn't exist
if [ ! -f "$HOME/sync-repos.json" ]; then
    echo "📋 Creating repository configuration..."
    cat > "$HOME/sync-repos.json" << 'EOF'
[
  {"name": "example-repo"}
]
EOF
    echo "✅ Created $HOME/sync-repos.json"
    echo "   ⚠️  Edit this file to add your repositories!"
    echo ""
fi

# Get GitHub username
echo "🔧 Configuration needed:"
echo ""
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -n "$GITHUB_USERNAME" ]; then
    sudo sed -i "s/YOUR_GITHUB_USERNAME/$GITHUB_USERNAME/g" /opt/git-sync/sync.py
    echo "✅ GitHub username set to: $GITHUB_USERNAME"
else
    echo "⚠️  Skipped username configuration"
    echo "   Edit /opt/git-sync/sync.py and change line 24"
fi
echo ""

# Get GitHub token
read -p "Enter your GitHub Personal Access Token (or press Enter to skip): " GITHUB_TOKEN

if [ -n "$GITHUB_TOKEN" ]; then
    echo "🔑 Setting up GitHub token..."
    sudo bash -c "cat > /etc/systemd/system/git-sync.env" << EOF
GITHUB_TOKEN=$GITHUB_TOKEN
EOF
    sudo chmod 600 /etc/systemd/system/git-sync.env
    echo "✅ Token saved securely"
else
    echo "⚠️  Skipped token setup"
    echo "   You'll need to create /etc/systemd/system/git-sync.env manually"
fi
echo ""

# Create systemd service
echo "⚙️  Creating systemd service..."
sudo tee /etc/systemd/system/git-sync.service > /dev/null << EOF
[Unit]
Description=Git Sync Service
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
User=$USER
EnvironmentFile=/etc/systemd/system/git-sync.env
ExecStart=/usr/bin/python3 /opt/git-sync/sync.py
TimeoutStartSec=600

[Install]
WantedBy=multi-user.target
EOF

echo "✅ Service file created"

# Create systemd timer
echo "⏰ Creating systemd timer..."
sudo tee /etc/systemd/system/git-sync.timer > /dev/null << 'EOF'
[Unit]
Description=Git Sync Timer
Requires=git-sync.service

[Timer]
OnBootSec=5min
OnUnitActiveSec=1h
Unit=git-sync.service

[Install]
WantedBy=timers.target
EOF

echo "✅ Timer file created (runs every hour)"
echo ""

# Reload systemd
sudo systemctl daemon-reload

# Ask if user wants to enable and start
read -p "Enable and start the service now? (y/n): " START_SERVICE

if [ "$START_SERVICE" = "y" ] || [ "$START_SERVICE" = "Y" ]; then
    echo "🚀 Starting service..."
    sudo systemctl enable git-sync.timer
    sudo systemctl start git-sync.timer
    echo "✅ Timer started and enabled (syncs every hour)"
    echo ""
    echo "🔄 Running initial sync in background..."
    sudo systemctl start --no-block git-sync.service
    echo "   Check status with: sudo systemctl status git-sync.service"
    echo "   View logs with: sudo journalctl -u git-sync.service -f"
else
    echo "⚠️  Service not started"
    echo "   To start later, run:"
    echo "   sudo systemctl enable git-sync.timer"
    echo "   sudo systemctl start git-sync.timer"
fi

echo ""
echo "=================================="
echo "✅ Installation Complete!"
echo "=================================="
echo ""
echo "📝 Next Steps:"
echo ""
echo "1. Edit repository list:"
echo "   nano $HOME/sync-repos.json"
echo ""
echo "2. Update GitHub username (if skipped):"
echo "   sudo nano /opt/git-sync/sync.py"
echo "   Change line 24: \"github_username\": \"$GITHUB_USERNAME\""
echo ""
echo "3. Add GitHub token (if skipped):"
echo "   echo 'GITHUB_TOKEN=your_token' | sudo tee /etc/systemd/system/git-sync.env"
echo "   sudo chmod 600 /etc/systemd/system/git-sync.env"
echo ""
echo "4. Test the sync:"
echo "   sudo systemctl start --no-block git-sync.service  # runs in background"
echo ""
echo "5. View logs:"
echo "   sudo journalctl -u git-sync.service -f"
echo ""
echo "6. Check sync status:"
echo "   sudo systemctl status git-sync.service"
echo ""
echo "📚 Full documentation:"
echo "   $INSTALL_DIR/README.md"
echo ""
echo "🎉 Happy syncing!"
