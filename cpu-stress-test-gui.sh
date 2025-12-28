#!/bin/bash

# CPU-Stresstest mit geteiltem Bildschirm (GUI)
# Zeigt bpytop auf der linken Seite und den Stresstest rechts

# Farben für bessere Ausgabe
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Session-Name für tmux
SESSION_NAME="cpu-stress-test"

# Prüfen ob tmux verfügbar ist
if ! command -v /usr/bin/tmux &> /dev/null; then
    echo "Fehler: tmux ist nicht installiert!"
    exit 1
fi

# Prüfen ob bpytop verfügbar ist, sonst htop verwenden
if command -v bpytop &> /dev/null; then
    MONITOR_TOOL="bpytop"
elif command -v htop &> /dev/null; then
    MONITOR_TOOL="htop"
else
    echo "Fehler: Weder bpytop noch htop sind installiert!"
    exit 1
fi

# CPU-Kerne ermitteln
CPU_CORES=$(nproc)

echo -e "${BLUE}======================================"
echo -e "CPU-Stresstest mit Monitoring-GUI"
echo -e "======================================${NC}"
echo -e "${GREEN}Erkannte CPU-Kerne: ${CPU_CORES}${NC}"
echo -e "${GREEN}Monitoring-Tool: ${MONITOR_TOOL}${NC}"
echo -e "${YELLOW}Testdauer: 60 Sekunden${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""
echo "Starte geteilte Ansicht..."
echo "Drücken Sie Ctrl+B dann D zum Beenden der Ansicht"
echo ""
sleep 2

# Alte Session beenden falls vorhanden
/usr/bin/tmux kill-session -t $SESSION_NAME 2>/dev/null

# Neue tmux Session starten
/usr/bin/tmux new-session -d -s $SESSION_NAME

# Fenster vertikal teilen
/usr/bin/tmux split-window -h -t $SESSION_NAME

# Im linken Pane: bpytop/htop starten
/usr/bin/tmux send-keys -t $SESSION_NAME:0.0 "$MONITOR_TOOL" C-m

# Im rechten Pane: Stresstest vorbereiten und starten
/usr/bin/tmux send-keys -t $SESSION_NAME:0.1 "clear" C-m
/usr/bin/tmux send-keys -t $SESSION_NAME:0.1 "echo '======================================'" C-m
/usr/bin/tmux send-keys -t $SESSION_NAME:0.1 "echo 'CPU-Stresstest läuft...'" C-m
/usr/bin/tmux send-keys -t $SESSION_NAME:0.1 "echo 'CPU-Kerne: $CPU_CORES'" C-m
/usr/bin/tmux send-keys -t $SESSION_NAME:0.1 "echo 'Dauer: 60 Sekunden'" C-m
/usr/bin/tmux send-keys -t $SESSION_NAME:0.1 "echo '======================================'" C-m
/usr/bin/tmux send-keys -t $SESSION_NAME:0.1 "echo ''" C-m
/usr/bin/tmux send-keys -t $SESSION_NAME:0.1 "sleep 2" C-m
/usr/bin/tmux send-keys -t $SESSION_NAME:0.1 "stress-ng --cpu $CPU_CORES --timeout 60s --metrics-brief" C-m

# Nach dem Stresstest: Erfolgsmeldung anzeigen und Session offen lassen
/usr/bin/tmux send-keys -t $SESSION_NAME:0.1 "echo ''" C-m
/usr/bin/tmux send-keys -t $SESSION_NAME:0.1 "echo '======================================'" C-m
/usr/bin/tmux send-keys -t $SESSION_NAME:0.1 "echo 'Stresstest abgeschlossen!'" C-m
/usr/bin/tmux send-keys -t $SESSION_NAME:0.1 "echo 'Drücke ENTER zum Beenden oder Ctrl+B dann D zum Detach'" C-m
/usr/bin/tmux send-keys -t $SESSION_NAME:0.1 "echo '======================================'" C-m

# An die Session anhängen
/usr/bin/tmux attach-session -t $SESSION_NAME
