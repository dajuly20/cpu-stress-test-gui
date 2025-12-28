#!/usr/bin/env python3
"""
CPU Stress Test GUI
Grafische Oberfläche für CPU-Stresstests mit Live-Monitoring
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import psutil
import subprocess
import threading
import time
from datetime import datetime
import os

class CPUStressGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Stress Test - Monitoring Dashboard")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1e1e1e')

        # Variablen
        self.cpu_count = psutil.cpu_count()
        self.is_running = False
        self.stress_process = None
        self.cpu_history = []
        self.max_history = 60
        self.monitor_process = None
        self.current_view = "graph"

        # GUI aufbauen
        self.create_widgets()

        # Update-Loop starten
        self.update_stats()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#2d2d2d', height=80)
        header_frame.pack(fill='x', padx=10, pady=10)
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="🖥️  CPU Stress Test Dashboard",
            font=('Arial', 24, 'bold'),
            bg='#2d2d2d',
            fg='#00ff00'
        )
        title_label.pack(pady=20)

        # Main Container
        main_container = tk.Frame(self.root, bg='#1e1e1e')
        main_container.pack(fill='both', expand=True, padx=10, pady=5)

        # Linke Seite - System Info & Steuerung
        left_frame = tk.Frame(main_container, bg='#2d2d2d', width=400)
        left_frame.pack(side='left', fill='both', padx=(0, 5), pady=0)

        # System Info
        info_frame = tk.LabelFrame(
            left_frame,
            text="System Information",
            font=('Arial', 12, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff',
            padx=10,
            pady=10
        )
        info_frame.pack(fill='x', padx=10, pady=10)

        self.info_text = tk.Label(
            info_frame,
            text=f"CPU Kerne: {self.cpu_count}\n"
                 f"Prozessor: {psutil.cpu_freq().current:.0f} MHz\n"
                 f"System: {os.uname().sysname} {os.uname().release}",
            font=('Courier', 11),
            bg='#2d2d2d',
            fg='#00ff00',
            justify='left'
        )
        self.info_text.pack(anchor='w')

        # Steuerung
        control_frame = tk.LabelFrame(
            left_frame,
            text="Stress Test Steuerung",
            font=('Arial', 12, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff',
            padx=10,
            pady=10
        )
        control_frame.pack(fill='x', padx=10, pady=10)

        # Dauer-Auswahl
        duration_frame = tk.Frame(control_frame, bg='#2d2d2d')
        duration_frame.pack(fill='x', pady=5)

        tk.Label(
            duration_frame,
            text="Test-Dauer (Sekunden):",
            font=('Arial', 10),
            bg='#2d2d2d',
            fg='#ffffff'
        ).pack(side='left')

        self.duration_var = tk.StringVar(value="60")
        duration_entry = tk.Entry(
            duration_frame,
            textvariable=self.duration_var,
            width=10,
            font=('Arial', 10)
        )
        duration_entry.pack(side='left', padx=10)

        # Start/Stop Buttons
        button_frame = tk.Frame(control_frame, bg='#2d2d2d')
        button_frame.pack(fill='x', pady=10)

        self.start_button = tk.Button(
            button_frame,
            text="▶ START TEST",
            command=self.start_stress_test,
            bg='#00aa00',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2'
        )
        self.start_button.pack(side='left', padx=5)

        self.stop_button = tk.Button(
            button_frame,
            text="⬛ STOP TEST",
            command=self.stop_stress_test,
            bg='#aa0000',
            fg='white',
            font=('Arial', 12, 'bold'),
            padx=20,
            pady=10,
            cursor='hand2',
            state='disabled'
        )
        self.stop_button.pack(side='left', padx=5)

        # Status
        self.status_label = tk.Label(
            control_frame,
            text="⚪ Bereit",
            font=('Arial', 11, 'bold'),
            bg='#2d2d2d',
            fg='#ffaa00'
        )
        self.status_label.pack(pady=10)

        # CPU Usage Bars
        bars_frame = tk.LabelFrame(
            left_frame,
            text="CPU Auslastung pro Kern",
            font=('Arial', 12, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff',
            padx=10,
            pady=10
        )
        bars_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Scrollbare CPU Bars
        canvas_frame = tk.Frame(bars_frame, bg='#2d2d2d')
        canvas_frame.pack(fill='both', expand=True)

        self.cpu_canvas = tk.Canvas(canvas_frame, bg='#2d2d2d', highlightthickness=0)
        scrollbar = ttk.Scrollbar(canvas_frame, orient='vertical', command=self.cpu_canvas.yview)

        self.cpu_bars_frame = tk.Frame(self.cpu_canvas, bg='#2d2d2d')
        self.cpu_bars_frame.bind(
            '<Configure>',
            lambda e: self.cpu_canvas.configure(scrollregion=self.cpu_canvas.bbox('all'))
        )

        self.cpu_canvas.create_window((0, 0), window=self.cpu_bars_frame, anchor='nw')
        self.cpu_canvas.configure(yscrollcommand=scrollbar.set)

        self.cpu_canvas.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # CPU Bars erstellen
        self.cpu_bars = []
        self.cpu_labels = []

        for i in range(self.cpu_count):
            core_frame = tk.Frame(self.cpu_bars_frame, bg='#2d2d2d')
            core_frame.pack(fill='x', pady=2)

            label = tk.Label(
                core_frame,
                text=f"CPU {i}:",
                font=('Courier', 9),
                bg='#2d2d2d',
                fg='#ffffff',
                width=8
            )
            label.pack(side='left')

            bar_bg = tk.Canvas(core_frame, height=20, bg='#1e1e1e', highlightthickness=1, highlightbackground='#444')
            bar_bg.pack(side='left', fill='x', expand=True, padx=5)

            bar = bar_bg.create_rectangle(0, 0, 0, 20, fill='#00ff00', outline='')
            self.cpu_bars.append((bar_bg, bar))

            percent_label = tk.Label(
                core_frame,
                text="0%",
                font=('Courier', 9),
                bg='#2d2d2d',
                fg='#00ff00',
                width=6
            )
            percent_label.pack(side='left')
            self.cpu_labels.append(percent_label)

        # Rechte Seite - Graph/Monitor & Log
        right_frame = tk.Frame(main_container, bg='#2d2d2d')
        right_frame.pack(side='right', fill='both', expand=True, padx=(5, 0), pady=0)

        # Monitor Selection Frame
        monitor_select_frame = tk.LabelFrame(
            right_frame,
            text="Monitoring Ansicht",
            font=('Arial', 12, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff',
            padx=10,
            pady=10
        )
        monitor_select_frame.pack(fill='x', padx=10, pady=10)

        select_container = tk.Frame(monitor_select_frame, bg='#2d2d2d')
        select_container.pack(fill='x')

        tk.Label(
            select_container,
            text="Ansicht:",
            font=('Arial', 10),
            bg='#2d2d2d',
            fg='#ffffff'
        ).pack(side='left', padx=(0, 10))

        self.view_var = tk.StringVar(value="graph")
        view_dropdown = ttk.Combobox(
            select_container,
            textvariable=self.view_var,
            values=["graph", "bpytop", "htop"],
            state='readonly',
            width=15,
            font=('Arial', 10)
        )
        view_dropdown.pack(side='left')
        view_dropdown.bind('<<ComboboxSelected>>', self.change_view)

        # Container für Graph/Monitor
        display_frame = tk.LabelFrame(
            right_frame,
            text="CPU Monitoring",
            font=('Arial', 12, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff',
            padx=10,
            pady=10
        )
        display_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Graph Canvas
        self.graph_canvas = tk.Canvas(
            display_frame,
            bg='#1e1e1e',
            highlightthickness=1,
            highlightbackground='#444'
        )
        self.graph_canvas.pack(fill='both', expand=True)

        # Terminal Frame (für bpytop/htop)
        self.terminal_frame = tk.Frame(display_frame, bg='#1e1e1e')

        # Log Output
        log_frame = tk.LabelFrame(
            right_frame,
            text="Test Output Log",
            font=('Arial', 12, 'bold'),
            bg='#2d2d2d',
            fg='#ffffff',
            padx=10,
            pady=10
        )
        log_frame.pack(fill='both', padx=10, pady=10)

        self.log_text = scrolledtext.ScrolledText(
            log_frame,
            height=8,
            bg='#1e1e1e',
            fg='#00ff00',
            font=('Courier', 9),
            insertbackground='white'
        )
        self.log_text.pack(fill='both', expand=True)
        self.log_text.insert('1.0', "Bereit für Stress Test...\n")

    def change_view(self, event=None):
        """Wechsle zwischen Graph und Terminal-Ansicht"""
        new_view = self.view_var.get()

        if new_view == self.current_view:
            return

        # Alte Ansicht beenden
        if self.current_view in ["bpytop", "htop"]:
            self.stop_monitor()
            self.terminal_frame.pack_forget()
            self.graph_canvas.pack(fill='both', expand=True)

        self.current_view = new_view

        # Neue Ansicht starten
        if new_view == "graph":
            self.log("📊 Wechsel zu Graph-Ansicht\n")
        elif new_view in ["bpytop", "htop"]:
            self.graph_canvas.pack_forget()
            self.terminal_frame.pack(fill='both', expand=True)
            self.start_monitor(new_view)

    def start_monitor(self, tool):
        """Starte bpytop oder htop in embedded terminal"""
        self.log(f"🖥️  Starte {tool}...\n")

        # Terminal Frame aktualisieren
        self.terminal_frame.update()

        # Window ID des Frames holen
        frame_id = self.terminal_frame.winfo_id()

        # Prüfen ob Tool verfügbar ist
        try:
            subprocess.run(['which', tool], check=True, capture_output=True)
        except subprocess.CalledProcessError:
            self.log(f"❌ {tool} ist nicht installiert!\n")
            self.view_var.set("graph")
            self.change_view()
            return

        # xterm mit embedded window starten
        try:
            self.monitor_process = subprocess.Popen([
                'xterm',
                '-into', str(frame_id),
                '-bg', 'black',
                '-fg', 'green',
                '-fa', 'Monospace',
                '-fs', '10',
                '-e', tool
            ])
            self.log(f"✅ {tool} gestartet\n")
        except FileNotFoundError:
            self.log("❌ xterm ist nicht installiert!\n")
            self.log("Installiere mit: sudo apt install xterm\n")
            self.view_var.set("graph")
            self.change_view()
        except Exception as e:
            self.log(f"❌ Fehler beim Starten: {str(e)}\n")
            self.view_var.set("graph")
            self.change_view()

    def stop_monitor(self):
        """Stoppe laufenden Monitor"""
        if self.monitor_process and self.monitor_process.poll() is None:
            self.monitor_process.terminate()
            try:
                self.monitor_process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                self.monitor_process.kill()
            self.monitor_process = None

    def update_stats(self):
        """Update CPU statistics"""
        # CPU Auslastung pro Kern
        cpu_percent = psutil.cpu_percent(interval=0.5, percpu=True)

        for i, percent in enumerate(cpu_percent):
            if i < len(self.cpu_bars):
                bar_bg, bar = self.cpu_bars[i]
                width = bar_bg.winfo_width()
                if width > 1:
                    new_width = int((percent / 100) * width)
                    bar_bg.coords(bar, 0, 0, new_width, 20)

                    # Farbe je nach Auslastung
                    if percent > 80:
                        color = '#ff0000'
                    elif percent > 50:
                        color = '#ffaa00'
                    else:
                        color = '#00ff00'
                    bar_bg.itemconfig(bar, fill=color)

                if i < len(self.cpu_labels):
                    self.cpu_labels[i].config(text=f"{percent:5.1f}%")

        # Gesamt CPU für Graph
        total_cpu = psutil.cpu_percent(interval=0.1)
        self.cpu_history.append(total_cpu)
        if len(self.cpu_history) > self.max_history:
            self.cpu_history.pop(0)

        if self.current_view == "graph":
            self.draw_graph()

        # Nächstes Update
        self.root.after(1000, self.update_stats)

    def draw_graph(self):
        """Zeichne CPU Verlaufsgraph"""
        self.graph_canvas.delete('all')

        width = self.graph_canvas.winfo_width()
        height = self.graph_canvas.winfo_height()

        if width < 2 or height < 2:
            return

        # Raster
        for i in range(0, 101, 25):
            y = height - (i / 100 * height)
            self.graph_canvas.create_line(0, y, width, y, fill='#333', dash=(2, 4))
            self.graph_canvas.create_text(5, y-10, text=f"{i}%", fill='#666', anchor='w', font=('Arial', 8))

        # Graph zeichnen
        if len(self.cpu_history) > 1:
            points = []
            step = width / max(1, self.max_history - 1)

            for i, value in enumerate(self.cpu_history):
                x = i * step
                y = height - (value / 100 * height)
                points.extend([x, y])

            if len(points) >= 4:
                self.graph_canvas.create_line(points, fill='#00ff00', width=2, smooth=True)

                # Aktuelle Auslastung anzeigen
                current = self.cpu_history[-1]
                self.graph_canvas.create_text(
                    width - 10,
                    20,
                    text=f"{current:.1f}%",
                    fill='#00ff00',
                    font=('Arial', 16, 'bold'),
                    anchor='e'
                )

    def start_stress_test(self):
        """Starte den Stress Test"""
        if self.is_running:
            return

        try:
            duration = int(self.duration_var.get())
        except ValueError:
            self.log("❌ Ungültige Dauer! Bitte eine Zahl eingeben.\n")
            return

        self.is_running = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.status_label.config(text="🟢 Test läuft...", fg='#00ff00')

        self.log(f"\n{'='*50}\n")
        self.log(f"🚀 Starte CPU Stress Test\n")
        self.log(f"CPU Kerne: {self.cpu_count}\n")
        self.log(f"Dauer: {duration} Sekunden\n")
        self.log(f"Start: {datetime.now().strftime('%H:%M:%S')}\n")
        self.log(f"{'='*50}\n\n")

        # Stress Test in separatem Thread
        thread = threading.Thread(target=self.run_stress_test, args=(duration,))
        thread.daemon = True
        thread.start()

    def run_stress_test(self, duration):
        """Führe Stress Test aus"""
        try:
            cmd = ['stress-ng', '--cpu', str(self.cpu_count), '--timeout', f'{duration}s', '--metrics-brief']

            self.stress_process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            # Output lesen
            for line in self.stress_process.stdout:
                self.log(line)

            self.stress_process.wait()

            if self.stress_process.returncode == 0:
                self.log(f"\n✅ Test erfolgreich abgeschlossen!\n")
                self.log(f"Ende: {datetime.now().strftime('%H:%M:%S')}\n")
            else:
                self.log(f"\n⚠️  Test mit Code {self.stress_process.returncode} beendet\n")

        except Exception as e:
            self.log(f"\n❌ Fehler: {str(e)}\n")
        finally:
            self.is_running = False
            self.root.after(0, self.reset_buttons)

    def stop_stress_test(self):
        """Stoppe den laufenden Test"""
        if self.stress_process and self.stress_process.poll() is None:
            self.log("\n⏹️  Stoppe Test...\n")
            self.stress_process.terminate()
            try:
                self.stress_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.stress_process.kill()

            self.is_running = False
            self.reset_buttons()

    def reset_buttons(self):
        """Setze Button-Status zurück"""
        self.start_button.config(state='normal')
        self.stop_button.config(state='disabled')
        self.status_label.config(text="⚪ Bereit", fg='#ffaa00')

    def log(self, message):
        """Füge Nachricht zum Log hinzu"""
        self.log_text.insert('end', message)
        self.log_text.see('end')

    def cleanup(self):
        """Cleanup beim Beenden"""
        self.stop_monitor()
        if self.stress_process and self.stress_process.poll() is None:
            self.stress_process.terminate()

def main():
    root = tk.Tk()
    app = CPUStressGUI(root)

    # Cleanup beim Schließen
    root.protocol("WM_DELETE_WINDOW", lambda: (app.cleanup(), root.destroy()))

    root.mainloop()

if __name__ == "__main__":
    main()
