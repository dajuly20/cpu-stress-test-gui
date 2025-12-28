#!/bin/bash

# Automatischer CPU-Stresstest
# Ermittelt die Anzahl der CPU-Kerne und führt einen Stresstest durch

# Anzahl der CPU-Kerne ermitteln
CPU_CORES=$(nproc)

echo "======================================"
echo "CPU-Stresstest"
echo "======================================"
echo "Erkannte CPU-Kerne: $CPU_CORES"
echo "Testdauer: 60 Sekunden"
echo "======================================"
echo ""
echo "Starte Stresstest..."
echo ""

# Stresstest mit allen verfügbaren Kernen durchführen
stress-ng --cpu "$CPU_CORES" --timeout 60s --metrics-brief

echo ""
echo "======================================"
echo "Stresstest abgeschlossen!"
echo "======================================"
