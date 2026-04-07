#!/bin/bash

# === CONFIGURATION ===
REPO_URL="https://github.com/DDorfm/raven_backup.git"
USER=$(whoami)
ICON_PATH="assets/raven_backup.png"

# === CHECKS ===

# Check Python 3.10+
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install it first."
    exit 1
fi
PYTHON_VERSION=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
if [[ "$PYTHON_VERSION" < "3.10" ]]; then
    echo "❌ Python 3.10 or higher is required. Current version: $PYTHON_VERSION"
    exit 1
fi
echo "✅ Python $PYTHON_VERSION detected."


# Chech tkinter
if python3 -c "import tkinter" &> /dev/null; then
    echo "✅ tkinter available"
else
    echo "❌ tkinter not available. Install it with: sudo apt install python3-tk"
    exit 1
fi


# Check venv module
if python3 -m venv --help &> /dev/null; then
    echo "✅ venv module available"
else
    echo "❌ venv module not available. Install it with: sudo apt install python3.10-venv"
    exit 1
fi


# Check git
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Install it with:"
    echo "   sudo apt install git"
    echo "   (or use your package manager: dnf, pacman, etc.)"
    exit 1
fi
echo "✅ Git is installed."


# Check rsync
if ! command -v rsync &> /dev/null; then
    echo "⚠️  rsync is not installed."
    echo "   You can install it with: sudo apt install rsync"
	exit 1
else
	echo "✅ rsync is installed."
fi


# === ASK FOR INSTALL LOCATION ===
echo ""
echo "📍 Where do you want to install Raven Backup?"
echo "1) ~/raven (local - no sudo RECOMMENDED)"
echo "2) /opt/raven (system-wide - requires sudo)"

read -p "Choose (1 or 2): " OPTION

case $OPTION in

    1)
        INSTALL_DIR="$HOME/raven_backup"
        echo "✅ Installing in ~/raven_backup..."
        mkdir -p "$INSTALL_DIR"
        ;;


    2)
        INSTALL_DIR="/opt/raven_backup"
        echo "✅ Installing in /opt/raven_backup..."
        sudo mkdir -p "$INSTALL_DIR" || { echo "❌ Error creating /opt/raven"; exit 1; }
        sudo chown "$USER":"$USER" "$INSTALL_DIR" || { echo "❌ Permission error"; exit 1; }
        ;;

    *)
        echo "❌ Invalid option. Exiting."
        exit 1
        ;;
esac

# === CLONE REPOSITORY ===
cd "$INSTALL_DIR" || { echo "❌ Cannot access $INSTALL_DIR"; exit 1; }
echo "📦 Cloning repository..."
git clone "$REPO_URL" . || { echo "❌ Error cloning repository"; exit 1; }


# === CREATE VIRTUAL ENVIRONMENT ===
echo "🐍 Creating virtual environment..."
python3 -m venv venv || { echo "❌ Error creating virtual environment"; exit 1; }


# Activate environment
source venv/bin/activate || { echo "❌ Error activating virtual environment"; exit 1; }

# === INSTALL DEPENDENCIES ===
if [ -f "requirements.txt" ]; then
    echo "📦 Installing dependencies..."
    pip install -r requirements.txt || { echo "❌ Error installing dependencies"; exit 1; }
fi


# === CREATE STARTUP SCRIPT ===
echo "📝 Creating startup script..."
cat > start.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
fi
python3 raven_backup.py
EOF

chmod +x start.sh


# === CREATE APPLICATION MENU ENTRY ===
echo "📌 Creating application menu entry..."
mkdir -p "$HOME/.local/share/applications"

cat > "$HOME/.local/share/applications/raven-backup.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Raven Backup
Comment=Automatic backup system
Exec=$INSTALL_DIR/start.sh
Icon=$INSTALL_DIR/$ICON_PATH
Categories=Utility;Backup;
Terminal=false
StartupNotify=true
EOF

chmod +x "$HOME/.local/share/applications/raven-backup.desktop"
update-desktop-database "$HOME/.local/share/applications" 2>/dev/null


# === FINAL MESSAGE ===
echo ""
echo "✅ Installation complete!"
echo "📁 Location: $INSTALL_DIR"
echo "🚀 Run: $INSTALL_DIR/start.sh"
echo "🖥️ Shortcut available in the application menu"
echo ""

# Warn if icon is missing
if [ ! -f "$INSTALL_DIR/$ICON_PATH" ]; then
    echo "⚠️  Icon not found at $ICON_PATH. Copy your icon there or edit the .desktop file."
fi
