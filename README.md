# CPU Stress Test GUI

Umfassende CPU Stress Test Tools mit grafischer Oberfläche und Monitoring.

## 📁 Dateien

### 🖥️ Hauptanwendung (EMPFOHLEN)
- **`cpu-stress-gui.py`** - Grafische GUI-Anwendung mit Fenster
  - Live CPU-Monitoring aller Kerne
  - Dropdown-Auswahl: Graph / bpytop / htop
  - Echtzeit-Graph der CPU-Auslastung
  - Embedded Terminal-Support
  - Start/Stop-Steuerung
  - Log-Ausgabe
  - **Start:** `python3 cpu-stress-gui.py`

### ⚙️ Installation & Setup
- **`install-dependencies.sh`** - Automatisches Installations-Skript
  - Installiert alle benötigten Pakete
  - Prüft vorhandene Abhängigkeiten
  - Interaktive Bestätigung
  - **Start:** `./install-dependencies.sh`

- **`start-gui.sh`** - Quick-Launcher für die GUI
  - Einfacher Start der Hauptanwendung
  - **Start:** `./start-gui.sh`

### 🔧 Terminal-basierte Tools
- **`cpu-stress-test.sh`** - Einfacher CLI-Stresstest
  - Erkennt automatisch CPU-Anzahl
  - Führt 60s Stresstest durch
  - **Start:** `./cpu-stress-test.sh`

- **`cpu-stress-test-gui-v2.sh`** - tmux Split-Screen Version
  - Geteilter Bildschirm mit bpytop + Stresstest
  - Erstellt tmux-Session
  - **Start:** `./cpu-stress-test-gui-v2.sh`
  - **Verbinden:** `tmux attach -t cpu-stress-test`

- **`cpu-stress-test-gui.sh`** - tmux Original-Version
  - Erste Version des Split-Screen Tools
  - **Start:** `./cpu-stress-test-gui.sh`

## 🚀 Schnellstart

### 1. Abhängigkeiten installieren
```bash
cd "cpu stress gui"
./install-dependencies.sh
```

Das Skript installiert automatisch:
- xterm (Terminal-Emulator)
- bpytop & htop (Monitoring-Tools)
- stress-ng (CPU-Stresstest)
- Python-Pakete (tkinter, psutil)
- tmux (Terminal-Multiplexer)

### 2. GUI-Anwendung starten (Empfohlen)
```bash
python3 cpu-stress-gui.py
# oder
./start-gui.sh
```

### Terminal Split-Screen
```bash
cd "cpu stress gui"
./cpu-stress-test-gui-v2.sh
tmux attach -t cpu-stress-test
```

### Einfacher CLI-Test
```bash
cd "cpu stress gui"
./cpu-stress-test.sh
```

## 📋 Systemanforderungen

- **Python 3** mit tkinter und psutil
- **stress-ng** für CPU-Tests
- **tmux** (optional, für Split-Screen)
- **bpytop** oder **htop** (optional, für Split-Screen Monitoring)

## 💡 Features

- ✅ Automatische Erkennung der CPU-Anzahl (16 Kerne)
- ✅ Live-Monitoring aller CPU-Kerne
- ✅ **Dropdown-Auswahl** für Monitoring-Ansicht:
  - 📊 **Graph** - CPU-Verlaufsdiagramm
  - 🖥️ **bpytop** - Integriertes bpytop-Terminal
  - 📈 **htop** - Integriertes htop-Terminal
- ✅ Grafische Verlaufsanzeige mit Echtzeit-Updates
- ✅ Anpassbare Test-Dauer
- ✅ Start/Stop-Steuerung
- ✅ Farbcodierte CPU-Auslastung (Grün/Orange/Rot)
- ✅ Live-Log-Ausgabe
- ✅ Embedded Terminal-Unterstützung

## 🎨 GUI Screenshot

Die GUI zeigt:
- **Links:** System-Info, Steuerung, CPU-Balken pro Kern
- **Rechts:** Verlaufs-Graph, Log-Output

---

**Erstellt:** 2025-12-28
**System:** 16 CPU-Kerne
