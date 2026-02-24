"""
MIDAS: Minimax-based Interactive Dynamic Assessment Simulation (v23.7)
Author: Joseph D. Arico
Description: Modular engine with externalized Intelligence Database and Resilience Analytics.
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import sys, random, os, datetime, json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MidasIntelligenceSuite(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MIDAS v23.7 - Joseph D. Arico Strategic Suite")
        self.geometry("1200x850")
        self.configure(bg="#121212")

        # Load Intelligence Database
        self.scenarios = self._load_intelligence()
        
        # UI State Variables
        if self.scenarios:
            self.scenario_var = tk.StringVar(value=list(self.scenarios.keys())[0])
        else:
            self.scenario_var = tk.StringVar(value="")
            
        self.personality_var = tk.StringVar(value="STANDARD")
        self.black_swan_var = tk.BooleanVar(value=True)
        self.current_report = ""

        self._build_ui()
        if self.scenarios:
            self.update_briefing()
            
        sys.stdout = TextRedirector(self.report_window)

    def _load_intelligence(self):
        """Attempts to load scenario data from external JSON."""
        json_path = 'scenarios.json'
        try:
            if not os.path.exists(json_path):
                raise FileNotFoundError
            with open(json_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Critical Error", f"Intelligence Database Not Found!\nEnsure 'scenarios.json' is in the root folder.\nError: {e}")
            return {}

    def _build_ui(self):
        # --- Sidebar ---
        sidebar = tk.Frame(self, width=320, bg="#1e1e1e", padx=15, pady=15)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(sidebar, text="COMMAND PANEL", fg="#00ff00", bg="#1e1e1e", font=("Impact", 20)).pack(pady=10)

        # Scenario Selection
        tk.Label(sidebar, text="SELECT FLASHPOINT:", fg="#aaaaaa", bg="#1e1e1e", font=("Arial", 9, "bold")).pack(anchor="w")
        if self.scenarios:
            scen_menu = ttk.OptionMenu(sidebar, self.scenario_var, list(self.scenarios.keys())[0], *self.scenarios.keys(), command=self.update_briefing)
            scen_menu.pack(fill=tk.X, pady=5)

        # Intelligence Briefing
        tk.Label(sidebar, text="INTELLIGENCE BRIEFING:", fg="#aaaaaa", bg="#1e1e1e", font=("Arial", 9, "bold")).pack(anchor="w", pady=(15, 0))
        self.brief_box = tk.Label(sidebar, text="Awaiting selection...", fg="white", bg="#252525", wraplength=270, justify="left", font=("Arial", 9), padx=10, pady=10)
        self.brief_box.pack(fill=tk.X, pady=5)

        # Risk Doctrine
        tk.Label(sidebar, text="DOCTRINE & RISK:", fg="#aaaaaa", bg="#1e1e1e", font=("Arial", 9, "bold")).pack(anchor="w", pady=(15, 0))
        ttk.OptionMenu(sidebar, self.personality_var, "STANDARD", "STANDARD", "AGGRESSIVE", "CAUTIOUS").pack(fill=tk.X, pady=5)
        
        tk.Checkbutton(sidebar, text="Enable Black Swan Events", variable=self.black_swan_var, bg="#1e1e1e", fg="#00ff00", selectcolor="#121212", activebackground="#1e1e1e").pack(anchor="w", pady=10)

        # Buttons
        self.run_btn = tk.Button(sidebar, text="EXECUTE SIMULATION", bg="#b91d1d", fg="white", command=self.run_simulation, font=("Arial", 11, "bold"), cursor="hand2")
        self.run_btn.pack(fill=tk.X, pady=10)

        self.save_btn = tk.Button(sidebar, text="SAVE BRIEFING REPORT", bg="#2e7d32", fg="white", command=self.save_report, font=("Arial", 10), cursor="hand2", state="disabled")
        self.save_btn.pack(fill=tk.X, pady=5)

        # --- Main Visualization ---
        main_panel = tk.Frame(self, bg="#121212")
        main_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(7, 4), facecolor="#121212")
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.report_window = scrolledtext.ScrolledText(main_panel, height=18, bg="#0a0a0a", fg="#00ff00", font=("Consolas", 10), borderwidth=0)
        self.report_window.pack(fill=tk.X, padx=20, pady=(0, 20))

    def update_briefing(self, *args):
        if not self.scenario_var.get(): return
        intel = self.scenarios[self.scenario_var.get()]
        brief = f"NAME: {intel['name']}\n\nCENTER OF GRAVITY:\n{intel['cog']}\n\nCONTEXT:\n{intel['desc']}"
        self.brief_box.config(text=brief)

    def run_simulation(self):
        if not self.scenario_var.get(): return
        self.ax.clear()
        self.ax.set_facecolor("#181818")
        self.ax.tick_params(colors='white')
        
        key = self.scenario_var.get()
        intel = self.scenarios[key]
        pers = self.personality_var.get()
        
        # Strategic Decay Logic
        hists = {'t': [], 'a1': [], 'a2': []}
        i1, i2 = 1.0, 1.0
        swan_triggered = False
        swan_data = None

        for t in range(intel['turns']):
            i1 -= random.uniform(0.01, 0.07) * intel['friction']
            i2 -= random.uniform(0.01, 0.07) * intel['friction']
            
            # Sawtooth Logic (Attrition Scenarios)
            if "ATTR" in key and t % 10 == 0: i2 = min(1.0, i2 + 0.15)
            
            # Black Swan Resilience Test
            if self.black_swan_var.get() and not swan_triggered and t > 5 and random.random() < 0.08:
                target = intel['a1'] if random.random() < 0.5 else intel['a2']
                shock = random.uniform(0.25, 0.45)
                if target == intel['a1']: i1 -= shock
                else: i2 -= shock
                swan_triggered = True
                swan_data = (t, target, round(shock*100, 1))

            hists['t'].append(t); hists['a1'].append(i1); hists['a2'].append(i2)
            if i1 <= 0.1 or i2 <= 0.1: break

        # Render Visualization
        self.ax.plot(hists['t'], hists['a1'], '#ff3333', label=intel['a1'], linewidth=2, marker='o', markersize=4)
        self.ax.plot(hists['t'], hists['a2'], '#3399ff', label=intel['a2'], linewidth=2, marker='x', markersize=4)
        
        if swan_triggered:
            self.ax.annotate('BLACK SWAN', xy=(swan_data[0], 0.5), xytext=(swan_data[0], 0.8),
                             arrowprops=dict(facecolor='yellow', shrink=0.05), color='yellow', fontweight='bold')

        self.ax.axhline(0.1, color='white', linestyle='--', alpha=0.3)
        self.ax.set_title(f"LIVE FEED: {intel['name']}", color="white", fontdict={'weight': 'bold'})
        self.ax.legend(facecolor="#1e1e1e", labelcolor="white")
        self.canvas.draw()

        # Generate Reporting
        winner = intel['a1'] if i1 > i2 else intel['a2']
        status = "OPTIMAL" if pers == intel['best_pers'] else f"SUB-OPTIMAL (Suggested: {intel['best_pers']})"
        
        report_header = f"{'='*70}\n[POST-ACTION BRIEFING] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n{'='*70}"
        report_body = (f"\nSCENARIO: {intel['name']}\nDOCTRINE: {pers} | ALIGNMENT: {status}\n"
                       f"WINNER: {winner} | FINAL INTEGRITY: {max(i1,i2):.2f}\n")
        
        if swan_triggered:
            report_body += f"EVENT: Black Swan shock of {swan_data[2]}% hit {swan_data[1]} at Turn {swan_data[0]}.\n"
        
        report_body += f"\nTHE 'WHY':\n{intel['why']}\n"
        
        self.current_report = report_header + report_body + "="*70
        print(self.current_report)
        self.save_btn.config(state="normal")

    def save_report(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")],
                                                initialfile=f"MIDAS_Report_{self.scenario_var.get()}.txt")
        if filename:
            with open(filename, "w") as f: f.write(self.current_report)
            messagebox.showinfo("Report Saved", "Success: Briefing report exported.")

class TextRedirector:
    def __init__(self, widget): self.widget = widget
    def write(self, s): self.widget.insert(tk.END, s); self.widget.see(tk.END)
    def flush(self): pass

if __name__ == "__main__":
    MidasIntelligenceSuite().mainloop()
