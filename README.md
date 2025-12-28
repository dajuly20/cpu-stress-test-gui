# CPU Stress Test GUI

Eine professionelle grafische Oberfläche für CPU-Stresstests mit Echtzeit-Monitoring und flexiblen Anzeigeoptionen.

## Features

- **Live CPU-Monitoring** - Echtzeit-Überwachung aller CPU-Kerne mit farbcodierten Balken
- **Flexible Anzeigeoptionen** - Wechsel zwischen Graph, bpytop und htop per Dropdown
- **Embedded Terminal** - Integrierte Terminal-Ansicht für bpytop/htop direkt in der GUI
- **Interaktive Steuerung** - Start/Stop-Buttons mit konfigurierbarer Testdauer
- **Verlaufsdiagramm** - Grafische Darstellung der CPU-Auslastung über Zeit
- **Live-Logging** - Echtzeit-Ausgabe des Stress-Test-Outputs
- **Auto-Detection** - Automatische Erkennung der CPU-Kernanzahl
- **Dark Theme** - Moderne dunkle Benutzeroberfläche

## Schnellstart

### 1. Installation der Abhängigkeiten
```bash
./install-dependencies.sh
```

Das Skript installiert automatisch:
- `xterm` - Terminal-Emulator für embedded Terminals
- `bpytop` & `htop` - System-Monitoring-Tools
- `stress-ng` - CPU-Stresstest-Tool
- `python3-tk` & `python3-psutil` - Python-Pakete
- `tmux` - Terminal-Multiplexer (für Shell-Versionen)

### 2. GUI starten
```bash
python3 cpu-stress-gui.py
```
oder
```bash
./start-gui.sh
```

## Projektstruktur

### Hauptanwendung (Empfohlen)
**[cpu-stress-gui.py](cpu-stress-gui.py)** - Grafische GUI-Anwendung
- Tkinter-basierte Benutzeroberfläche
- 3 Monitoring-Ansichten: Graph / bpytop / htop
- Live-Updates alle 1 Sekunde
- Prozess-Management für Stress-Tests
- Embedded xterm-Integration

### Installation & Launcher
- **[install-dependencies.sh](install-dependencies.sh)** - Installiert alle benötigten Pakete mit interaktiver Bestätigung
- **[start-gui.sh](start-gui.sh)** - Quick-Launcher für die Python-GUI

### Terminal-basierte Tools
- **[cpu-stress-test.sh](cpu-stress-test.sh)** - Einfacher CLI-Stresstest (60s)
- **[cpu-stress-test-gui-v2.sh](cpu-stress-test-gui-v2.sh)** - tmux Split-Screen mit bpytop
- **[cpu-stress-test-gui.sh](cpu-stress-test-gui.sh)** - tmux Original-Version
- **[test-bpytop-integration.sh](test-bpytop-integration.sh)** - Test-Skript für bpytop-Integration

## Benutzung

### GUI-Anwendung

1. **Starte die Anwendung**
   ```bash
   python3 cpu-stress-gui.py
   ```

2. **Wähle die Monitoring-Ansicht**
   - **Graph** - Zeigt CPU-Verlaufsdiagramm mit Echtzeit-Updates
   - **bpytop** - Embedded bpytop-Terminal mit detaillierten Systeminfos
   - **htop** - Embedded htop-Terminal mit Prozessliste

3. **Konfiguriere den Test**
   - Setze die Test-Dauer in Sekunden (Standard: 60)
   - Klicke auf "START TEST"

4. **Überwache die Auslastung**
   - Linke Seite: Einzelne CPU-Kern-Balken mit Prozentanzeige
   - Rechte Seite: Graph/Terminal-Ansicht
   - Log-Bereich: Ausgabe von stress-ng

5. **Stoppe bei Bedarf**
   - Klicke auf "STOP TEST" um den laufenden Test zu beenden

### Terminal-Versionen

#### Einfacher CLI-Test
```bash
./cpu-stress-test.sh
```
Führt einen 60-Sekunden-Stresstest aus und zeigt die Ausgabe direkt im Terminal.

#### tmux Split-Screen
```bash
./cpu-stress-test-gui-v2.sh
```
Erstellt eine tmux-Session mit geteiltem Bildschirm:
- Links: bpytop Monitoring
- Rechts: stress-ng Ausgabe

Zum Verbinden:
```bash
tmux attach -t cpu-stress-test
```

Zum Beenden: `Ctrl+B` dann `X` dann `Y`

## GUI-Übersicht

```
┌─────────────────────────────────────────────────────────────────┐
│              CPU Stress Test Dashboard                          │
├───────────────────────┬─────────────────────────────────────────┤
│  System Information   │      Monitoring Ansicht                 │
│  ─────────────────    │      Ansicht: [Graph ▼]                 │
│  CPU Kerne: 16        │                                          │
│  Prozessor: 3600 MHz  │  ┌────────────────────────────────────┐ │
│  System: Linux 6.x    │  │                              100%   │ │
│                       │  │         ___                         │ │
│  Stress Test Steuerung│  │      __/   \___       CPU Graph    │ │
│  ─────────────────    │  │   __/          \___                │ │
│  Dauer: [60] Sekunden │  │                                0%  │ │
│                       │  └────────────────────────────────────┘ │
│  [▶ START] [⬛ STOP]  │                                          │
│  ⚪ Bereit             │  Test Output Log                        │
│                       │  ┌────────────────────────────────────┐ │
│  CPU Auslastung       │  │ Bereit für Stress Test...          │ │
│  ─────────────────    │  │ 🚀 Starte CPU Stress Test          │ │
│  CPU 0:  [████░░] 45% │  │ CPU Kerne: 16                      │ │
│  CPU 1:  [████░░] 43% │  │ Dauer: 60 Sekunden                 │ │
│  CPU 2:  [███░░░] 38% │  │ ...                                │ │
│  ...                  │  └────────────────────────────────────┘ │
└───────────────────────┴─────────────────────────────────────────┘
```

### Monitoring-Ansichten

#### Graph-Ansicht
- Echtzeit-Verlaufsdiagramm der CPU-Gesamtauslastung
- 60 Datenpunkte Historie (1 Minute)
- Farbcodiert: Grün (normal), Orange (mittel), Rot (hoch)
- Prozentanzeige in Echtzeit

#### bpytop-Ansicht
- Vollständige bpytop-Integration in embedded Terminal
- CPU, Memory, Disk, Network Monitoring
- Prozessliste mit Details
- Interaktive Navigation

#### htop-Ansicht
- Klassisches htop in embedded Terminal
- Prozess-basierte Überwachung
- CPU-Kern-Auslastung
- Sortier- und Filterfunktionen

## Systemanforderungen

### Erforderlich
- **Python 3.6+** mit tkinter
- **stress-ng** - CPU-Stresstest-Tool
- **psutil** - Python System-Monitoring

### Optional (für erweiterte Features)
- **xterm** - Für embedded Terminal-Ansichten (bpytop/htop)
- **bpytop** - Für bpytop-Monitoring-Ansicht
- **htop** - Für htop-Monitoring-Ansicht
- **tmux** - Für Terminal-basierte Split-Screen-Versionen

### Installation auf Debian/Ubuntu
```bash
sudo apt update
sudo apt install python3 python3-tk python3-psutil stress-ng xterm bpytop htop tmux
```

Oder nutze das Installations-Skript:
```bash
./install-dependencies.sh
```

## Technische Details

### Python-GUI ([cpu-stress-gui.py](cpu-stress-gui.py))
- **Framework**: Tkinter (Standard Python GUI-Library)
- **System-Monitoring**: psutil für CPU-Statistiken
- **Prozess-Management**: subprocess für stress-ng und xterm
- **Threading**: Separate Threads für Stress-Tests
- **Update-Rate**: 1 Sekunde für CPU-Statistiken

### Embedded Terminal
- Verwendet `xterm -into <window_id>` für Terminal-Embedding
- Startet bpytop/htop als Subprocess in xterm
- Automatisches Cleanup beim View-Wechsel

### CPU-Monitoring
- Per-Core Monitoring mit psutil.cpu_percent(percpu=True)
- Dynamische Farbcodierung basierend auf Auslastung:
  - Grün: 0-50%
  - Orange: 50-80%
  - Rot: 80-100%

## Fehlerbehebung

### "xterm ist nicht installiert"
```bash
sudo apt install xterm
```

### "bpytop ist nicht installiert"
```bash
sudo apt install bpytop
```
Oder verwende die Graph-Ansicht als Alternative.

### "stress-ng: command not found"
```bash
sudo apt install stress-ng
```

### GUI startet nicht
Prüfe ob alle Python-Abhängigkeiten installiert sind:
```bash
python3 -c "import tkinter; import psutil; print('OK')"
```

Falls Fehler auftreten:
```bash
sudo apt install python3-tk python3-psutil
```

## Bekannte Limitierungen

- Embedded Terminals (bpytop/htop) benötigen X11 (funktioniert nicht in reinem Wayland ohne XWayland)
- xterm muss installiert sein für Terminal-Embedding
- tmux-Versionen funktionieren nur in Terminal-Umgebungen, nicht in der GUI

## Lizenz & Credits

- **Erstellt**: 2025-12-28
- **Getestet auf**: Linux (Fedora/Ubuntu), 16 CPU-Kerne
- **Dependencies**: stress-ng, psutil, tkinter, bpytop, htop, xterm

## Weitere Informationen

### stress-ng
CPU-Stresstest-Tool mit vielen Optionen. Das Projekt nutzt:
```bash
stress-ng --cpu <cores> --timeout <duration>s --metrics-brief
```

Weitere Optionen siehe: `man stress-ng`

### psutil
Python-Library für System-Monitoring:
- `cpu_count()` - Anzahl CPU-Kerne
- `cpu_percent(percpu=True)` - Per-Core Auslastung
- `cpu_freq()` - CPU-Frequenz

Dokumentation: https://psutil.readthedocs.io/

---

**Happy Stress-Testing!** 🚀
