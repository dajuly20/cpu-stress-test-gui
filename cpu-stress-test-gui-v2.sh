#!/bin/bash

# CPU-Stresstest mit geteiltem Bildschirm (GUI)
# Diese Version erstellt eine tmux-Session im Hintergrund

# Farben
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

SESSION_NAME="cpu-stress-test"
CPU_CORES=$(nproc)

# Prüfen ob in einer interaktiven Shell
if [ -t 0 ]; then
    # Interaktiv - direkt tmux starten
    echo -e "${BLUE}======================================"
    echo -e "CPU-Stresstest mit Monitoring-GUI"
    echo -e "======================================${NC}"
    echo -e "${GREEN}Erkannte CPU-Kerne: ${CPU_CORES}${NC}"
    echo -e "${GREEN}Monitoring-Tool: bpytop${NC}"
    echo -e "${YELLOW}Testdauer: 60 Sekunden${NC}"
    echo -e "${BLUE}======================================${NC}"
    echo ""
    echo "Starte geteilte Ansicht..."
    echo ""
    sleep 1

    # Alte Session beenden
    /usr/bin/tmux kill-session -t $SESSION_NAME 2>/dev/null

    # Neue tmux Session starten und direkt anhängen
    /usr/bin/tmux new-session -s $SESSION_NAME \; \
        split-window -h \; \
        send-keys -t 0 'bpytop' C-m \; \
        send-keys -t 1 "echo '======================================'" C-m \; \
        send-keys -t 1 "echo 'CPU-Stresstest läuft...'" C-m \; \
        send-keys -t 1 "echo 'CPU-Kerne: $CPU_CORES'" C-m \; \
        send-keys -t 1 "echo 'Dauer: 60 Sekunden'" C-m \; \
        send-keys -t 1 "echo '======================================'" C-m \; \
        send-keys -t 1 "echo ''" C-m \; \
        send-keys -t 1 "sleep 2 && stress-ng --cpu $CPU_CORES --timeout 60s --metrics-brief && echo '' && echo 'Test abgeschlossen! Drücke ENTER zum Beenden.'" C-m \; \
        select-pane -t 1
else
    # Nicht-interaktiv - Session im Hintergrund erstellen
    echo "Session wird im Hintergrund erstellt..."

    /usr/bin/tmux kill-session -t $SESSION_NAME 2>/dev/null

    /usr/bin/tmux new-session -d -s $SESSION_NAME \; \
        split-window -h \; \
        send-keys -t 0 'bpytop' C-m \; \
        send-keys -t 1 "echo '======================================'" C-m \; \
        send-keys -t 1 "echo 'CPU-Stresstest läuft...'" C-m \; \
        send-keys -t 1 "echo 'CPU-Kerne: $CPU_CORES'" C-m \; \
        send-keys -t 1 "echo 'Dauer: 60 Sekunden'" C-m \; \
        send-keys -t 1 "echo '======================================'" C-m \; \
        send-keys -t 1 "echo ''" C-m \; \
        send-keys -t 1 "stress-ng --cpu $CPU_CORES --timeout 60s --metrics-brief" C-m

    echo ""
    echo -e "${GREEN}✓ tmux-Session '$SESSION_NAME' wurde erstellt!${NC}"
    echo ""
    echo "Zum Verbinden mit der Session führen Sie aus:"
    echo -e "${YELLOW}    tmux attach -t $SESSION_NAME${NC}"
    echo ""
    echo "Zum Beenden der Session:"
    echo "    Ctrl+B dann D (detach)"
    echo "    oder Ctrl+C im Stresstest-Fenster"
fi
