#!/bin/bash

# Installation Script für CPU Stress Test GUI
# Installiert alle benötigten Abhängigkeiten

set -e  # Bei Fehler abbrechen

# Farben für Output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}CPU Stress Test GUI - Dependency Installer${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# Prüfen ob als root/sudo ausgeführt wird
if [ "$EUID" -ne 0 ]; then
    echo -e "${YELLOW}Hinweis: Dieses Skript benötigt sudo-Rechte.${NC}"
    echo -e "${YELLOW}Bitte geben Sie Ihr Passwort ein, wenn gefragt.${NC}"
    echo ""
fi

# Funktion zum Prüfen ob Paket installiert ist
check_installed() {
    if dpkg -l | grep -q "^ii  $1 "; then
        echo -e "${GREEN}✓${NC} $1 ist bereits installiert"
        return 0
    else
        echo -e "${YELLOW}✗${NC} $1 ist nicht installiert"
        return 1
    fi
}

# Funktion zum Prüfen ob Befehl verfügbar ist
check_command() {
    if command -v "$1" &> /dev/null; then
        echo -e "${GREEN}✓${NC} $1 ist verfügbar"
        return 0
    else
        echo -e "${YELLOW}✗${NC} $1 ist nicht verfügbar"
        return 1
    fi
}

echo -e "${BLUE}Schritt 1: Überprüfe installierte Pakete${NC}"
echo "----------------------------------------"

NEED_INSTALL=()

# Liste der benötigten Pakete
PACKAGES=(
    "xterm:Terminal-Emulator für bpytop/htop Integration"
    "bpytop:Modernes System-Monitoring Tool"
    "htop:Klassisches System-Monitoring Tool"
    "stress-ng:CPU Stress-Test Tool"
    "python3:Python 3 Interpreter"
    "python3-tk:Python Tkinter GUI-Bibliothek"
    "python3-pip:Python Package Manager"
    "tmux:Terminal-Multiplexer für Split-Screen"
)

for pkg_info in "${PACKAGES[@]}"; do
    pkg="${pkg_info%%:*}"
    desc="${pkg_info#*:}"

    echo -n "  "
    if ! check_installed "$pkg"; then
        NEED_INSTALL+=("$pkg")
    fi
done

echo ""

# Python-Pakete prüfen
echo -e "${BLUE}Schritt 2: Überprüfe Python-Pakete${NC}"
echo "----------------------------------------"

PYTHON_PACKAGES=(
    "psutil:CPU/System-Monitoring für Python"
)

NEED_PIP_INSTALL=()

for pkg_info in "${PYTHON_PACKAGES[@]}"; do
    pkg="${pkg_info%%:*}"
    desc="${pkg_info#*:}"

    echo -n "  "
    if python3 -c "import $pkg" 2>/dev/null; then
        echo -e "${GREEN}✓${NC} Python-Paket '$pkg' ist installiert"
    else
        echo -e "${YELLOW}✗${NC} Python-Paket '$pkg' ist nicht installiert"
        NEED_PIP_INSTALL+=("$pkg")
    fi
done

echo ""

# Installation durchführen
if [ ${#NEED_INSTALL[@]} -eq 0 ] && [ ${#NEED_PIP_INSTALL[@]} -eq 0 ]; then
    echo -e "${GREEN}================================================${NC}"
    echo -e "${GREEN}Alle Abhängigkeiten sind bereits installiert!${NC}"
    echo -e "${GREEN}================================================${NC}"
    exit 0
fi

echo -e "${YELLOW}Folgende Pakete müssen installiert werden:${NC}"
for pkg in "${NEED_INSTALL[@]}"; do
    echo -e "  - $pkg"
done
for pkg in "${NEED_PIP_INSTALL[@]}"; do
    echo -e "  - python3-$pkg (via pip)"
done
echo ""

# Benutzer um Bestätigung fragen
read -p "Installation starten? (j/N) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[JjYy]$ ]]; then
    echo -e "${RED}Installation abgebrochen.${NC}"
    exit 1
fi

echo ""

# APT-Pakete installieren
if [ ${#NEED_INSTALL[@]} -gt 0 ]; then
    echo -e "${BLUE}Schritt 3: Aktualisiere Paket-Liste${NC}"
    echo "----------------------------------------"
    sudo apt update

    echo ""
    echo -e "${BLUE}Schritt 4: Installiere System-Pakete${NC}"
    echo "----------------------------------------"
    sudo apt install -y "${NEED_INSTALL[@]}"
fi

# Python-Pakete installieren
if [ ${#NEED_PIP_INSTALL[@]} -gt 0 ]; then
    echo ""
    echo -e "${BLUE}Schritt 5: Installiere Python-Pakete${NC}"
    echo "----------------------------------------"
    sudo pip3 install "${NEED_PIP_INSTALL[@]}"
fi

echo ""
echo -e "${GREEN}================================================${NC}"
echo -e "${GREEN}Installation erfolgreich abgeschlossen!${NC}"
echo -e "${GREEN}================================================${NC}"
echo ""

# Zusammenfassung
echo -e "${BLUE}Installierte Tools:${NC}"
check_command "xterm" && echo "  ✓ xterm"
check_command "bpytop" && echo "  ✓ bpytop"
check_command "htop" && echo "  ✓ htop"
check_command "stress-ng" && echo "  ✓ stress-ng"
check_command "python3" && echo "  ✓ python3"
check_command "tmux" && echo "  ✓ tmux"

echo ""
echo -e "${GREEN}Sie können jetzt die GUI starten mit:${NC}"
echo -e "  ${YELLOW}python3 cpu-stress-gui.py${NC}"
echo -e "  oder"
echo -e "  ${YELLOW}./start-gui.sh${NC}"
echo ""
