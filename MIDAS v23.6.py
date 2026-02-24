import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import sys, random, os, datetime
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ==============================================================================
# --- 1. THE COMPLETE TEN-SCENARIO INTELLIGENCE DATABASE ---
# ==============================================================================
SCENARIO_INTEL = {
    "TAIWAN_STRAT": {
        "name": "Taiwan Strait Crisis", "turns": 30, "friction": 0.2, "a1": "PRC", "a2": "Taiwan/US",
        "cog": "PRC: Econ Stability | TW: National Resolve",
        "desc": "Amphibious invasion logic. High-intensity kinetic exchange.",
        "why": "Rapid collapse usually driven by Taiwan's Resolve vs. PRC's blockade endurance.",
        "best_pers": "AGGRESSIVE"
    },
    "UKRAINE_ATTR": {
        "name": "Ukraine Attrition", "turns": 45, "friction": 0.35, "a1": "Russia", "a2": "Ukraine/NATO",
        "cog": "RU: Military Cap | UA: National Resolve",
        "desc": "War of attrition. Periodical aid spikes.",
        "why": "Sawtooth recovery logic. Ukraine stays viable only as long as aid moves trigger.",
        "best_pers": "CAUTIOUS"
    },
    "SPACE_KESSLER": {
        "name": "Kessler Event", "turns": 20, "friction": 0.1, "a1": "SpaceCom", "a2": "Anti-Sat Actor",
        "cog": "Tech Infrastructure (Both)",
        "desc": "LEO debris cascade. High volatility.",
        "why": "Collateral damage logic. ASAT strikes damage the attacker's own Tech COG via debris.",
        "best_pers": "STANDARD"
    },
    "GLOBAL_FIN": {
        "name": "Currency War", "turns": 50, "friction": 0.1, "a1": "Status Quo", "a2": "Emerging Bloc",
        "cog": "SQ: Econ Stability | EB: Financial Sovereignty",
        "desc": "Non-kinetic reserves conflict.",
        "why": "Gradual decay until 'Debt Weaponization' triggers a non-linear systemic collapse.",
        "best_pers": "CAUTIOUS"
    },
    "KOREAN_DYNAMICS": {
        "name": "Peninsular Escalation", "turns": 25, "friction": 0.15, "a1": "DPRK", "a2": "ROK/US",
        "cog": "DPRK: National Resolve | ROK: Military Cap",
        "desc": "Immediate escalation post-hotline failure.",
        "why": "DPRK collapse is usually economic-led; ROK collapse is kinetic-led.",
        "best_pers": "AGGRESSIVE"
    },
    "SUB_SAHARAN_PROXY": {
        "name": "Proxy Attrition", "turns": 40, "friction": 0.45, "a1": "Local Govt", "a2": "PMC Group",
        "cog": "Both: Political Will/Contract Viability",
        "desc": "Resource-driven regional instability.",
        "why": "High friction causes 'aimless' decay lines, simulating a forever-war stalemate.",
        "best_pers": "CAUTIOUS"
    },
    "CYBER_GRID": {
        "name": "Infrastructure Siege", "turns": 20, "friction": 0.25, "a1": "Defender", "a2": "APT Threat",
        "cog": "DEF: Public Trust | APT: Cyber Capability",
        "desc": "Siege on critical power/water utilities.",
        "why": "Asymmetrical decay. Defender only repairs while Threat applies constant stress.",
        "best_pers": "STANDARD"
    },
    "RESOURCE_MENA": {
        "name": "Water Rights", "turns": 35, "friction": 0.3, "a1": "Upstream", "a2": "Downstream",
        "cog": "UP: Resource Control | DW: Diplomatic Support",
        "desc": "Transboundary river damming dispute.",
        "why": "Kinetic strikes on dams cause mutual collapse as the water resource is destroyed.",
        "best_pers": "AGGRESSIVE"
    },
    "BIOLAB_LEAK": {
        "name": "Pandemic Attribution", "turns": 30, "friction": 0.2, "a1": "Accused", "a2": "Global Org",
        "cog": "Both: Reputational/Diplomatic Legitimacy",
        "desc": "Post-leak economic and diplomatic fallout.",
        "why": "Non-kinetic. Integrity is eroded through trade bans and isolation moves.",
        "best_pers": "CAUTIOUS"
    },
    "ARCTIC_RUSH": {
        "name": "Arctic Scramble", "turns": 30, "friction": 0.2, "a1": "Arctic Council", "a2": "External Powers",
        "cog": "AC: Diplomatic Unity | EP: Economic Investment",
        "desc": "Mineral/shipping lane dispute.",
        "why": "Low kinetic pressure ensures most runs end in a peaceful Operational Stalemate.",
        "best_pers": "STANDARD"
    }
}


# ==============================================================================
# --- 2. THE COMMAND CENTER GUI ---
# ==============================================================================
class MidasIntelligenceSuite(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MIDAS v23.6 - Resilience Analysis & Briefing Suite")
        self.geometry("1200x850")
        self.configure(bg="#121212")

        self.scenario_var = tk.StringVar(value="TAIWAN_STRAT")
        self.personality_var = tk.StringVar(value="STANDARD")
        self.black_swan_var = tk.BooleanVar(value=True)

        self.current_report = ""  # Store the last report for export

        self._build_ui()
        self.update_briefing()
        sys.stdout = TextRedirector(self.report_window)

    def _build_ui(self):
        # Sidebar
        sidebar = tk.Frame(self, width=320, bg="#1e1e1e", padx=15, pady=15)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(sidebar, text="COMMAND PANEL", fg="#00ff00", bg="#1e1e1e", font=("Impact", 20)).pack(pady=10)

        # Scenario
        tk.Label(sidebar, text="SELECT FLASHPOINT:", fg="#aaaaaa", bg="#1e1e1e", font=("Arial", 9, "bold")).pack(
            anchor="w")
        scen_menu = ttk.OptionMenu(sidebar, self.scenario_var, "TAIWAN_STRAT", *SCENARIO_INTEL.keys(),
                                   command=self.update_briefing)
        scen_menu.pack(fill=tk.X, pady=5)

        # Briefing Box
        tk.Label(sidebar, text="INTELLIGENCE BRIEFING:", fg="#aaaaaa", bg="#1e1e1e", font=("Arial", 9, "bold")).pack(
            anchor="w", pady=(15, 0))
        self.brief_box = tk.Label(sidebar, text="", fg="white", bg="#252525", wraplength=270, justify="left",
                                  font=("Arial", 9), padx=10, pady=10)
        self.brief_box.pack(fill=tk.X, pady=5)

        # Options
        tk.Label(sidebar, text="DOCTRINE & RISK:", fg="#aaaaaa", bg="#1e1e1e", font=("Arial", 9, "bold")).pack(
            anchor="w", pady=(15, 0))
        ttk.OptionMenu(sidebar, self.personality_var, "STANDARD", "STANDARD", "AGGRESSIVE", "CAUTIOUS").pack(fill=tk.X,
                                                                                                             pady=5)

        tk.Checkbutton(sidebar, text="Enable Black Swan Events", variable=self.black_swan_var,
                       bg="#1e1e1e", fg="#00ff00", selectcolor="#121212", activebackground="#1e1e1e").pack(anchor="w",
                                                                                                           pady=10)

        self.run_btn = tk.Button(sidebar, text="EXECUTE SIMULATION", bg="#b91d1d", fg="white",
                                 command=self.run_simulation, font=("Arial", 11, "bold"), cursor="hand2")
        self.run_btn.pack(fill=tk.X, pady=10)

        self.save_btn = tk.Button(sidebar, text="SAVE BRIEFING REPORT", bg="#2e7d32", fg="white",
                                  command=self.save_report, font=("Arial", 10), cursor="hand2", state="disabled")
        self.save_btn.pack(fill=tk.X, pady=5)

        # Main Visualization
        main_panel = tk.Frame(self, bg="#121212")
        main_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig, self.ax = plt.subplots(figsize=(7, 4), facecolor="#121212")
        self.canvas = FigureCanvasTkAgg(self.fig, master=main_panel)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        self.report_window = scrolledtext.ScrolledText(main_panel, height=18, bg="#0a0a0a", fg="#00ff00",
                                                       font=("Consolas", 10), borderwidth=0)
        self.report_window.pack(fill=tk.X, padx=20, pady=(0, 20))

    def update_briefing(self, *args):
        intel = SCENARIO_INTEL[self.scenario_var.get()]
        brief = f"NAME: {intel['name']}\n\nCENTER OF GRAVITY:\n{intel['cog']}\n\nMISSION CONTEXT:\n{intel['desc']}"
        self.brief_box.config(text=brief)

    def run_simulation(self):
        self.ax.clear()
        self.ax.set_facecolor("#181818")
        self.ax.tick_params(colors='white')

        key = self.scenario_var.get()
        intel = SCENARIO_INTEL[key]
        pers = self.personality_var.get()

        # Strategic Simulation Logic
        hists = {'t': [], 'a1': [], 'a2': []}
        i1, i2 = 1.0, 1.0
        swan_triggered = False
        swan_data = None

        for t in range(intel['turns']):
            # Standard Decay
            i1 -= random.uniform(0.01, 0.07) * intel['friction']
            i2 -= random.uniform(0.01, 0.07) * intel['friction']

            # Sawtooth aid logic for Attrition scenarios
            if "ATTR" in key and t % 10 == 0: i2 = min(1.0, i2 + 0.15)

            # Black Swan Logic
            if self.black_swan_var.get() and not swan_triggered and t > 5 and random.random() < 0.08:
                target = intel['a1'] if random.random() < 0.5 else intel['a2']
                shock = random.uniform(0.25, 0.45)
                if target == intel['a1']:
                    i1 -= shock
                else:
                    i2 -= shock
                swan_triggered = True
                swan_data = (t, target, round(shock * 100, 1))

            hists['t'].append(t);
            hists['a1'].append(i1);
            hists['a2'].append(i2)
            if i1 <= 0.1 or i2 <= 0.1: break

        # Plotting
        self.ax.plot(hists['t'], hists['a1'], '#ff3333', label=intel['a1'], linewidth=2, marker='o', markersize=4)
        self.ax.plot(hists['t'], hists['a2'], '#3399ff', label=intel['a2'], linewidth=2, marker='x', markersize=4)

        if swan_triggered:
            self.ax.annotate('BLACK SWAN', xy=(swan_data[0], 0.5), xytext=(swan_data[0], 0.8),
                             arrowprops=dict(facecolor='yellow', shrink=0.05), color='yellow', fontweight='bold')

        self.ax.axhline(0.1, color='white', linestyle='--', alpha=0.3)
        self.ax.set_title(f"STRATEGIC FEED: {intel['name']}", color="white", fontdict={'weight': 'bold'})
        self.ax.legend(facecolor="#1e1e1e", labelcolor="white")
        self.canvas.draw()

        # Feedback & Reporting
        guide_status = "OPTIMAL" if pers == intel['best_pers'] else f"SUB-OPTIMAL (Expected: {intel['best_pers']})"
        winner = intel['a1'] if i1 > i2 else intel['a2']

        report_header = f"{'=' * 70}\n[POST-ACTION BRIEFING] {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n{'=' * 70}"
        report_body = (
            f"\nSCENARIO: {intel['name']}\nDOCTRINE: {pers} | ALIGNMENT: {guide_status}\n"
            f"WINNER: {winner} | FINAL STATE: {max(i1, i2):.2f}\n"
        )
        if swan_triggered:
            report_body += f"EVENT ALERT: Black Swan shock of {swan_data[2]}% hit {swan_data[1]} at Turn {swan_data[0]}.\n"

        report_body += f"\nSTRATEGIC ANALYSIS (THE 'WHY'):\n{intel['why']}\n"

        self.current_report = report_header + report_body + "=" * 70
        print(self.current_report)
        self.save_btn.config(state="normal")

    def save_report(self):
        filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text files", "*.txt")],
                                                initialfile=f"MIDAS_Report_{self.scenario_var.get()}.txt")
        if filename:
            with open(filename, "w") as f:
                f.write(self.current_report)
            messagebox.showinfo("Report Saved", f"Briefing report successfully exported to:\n{filename}")


class TextRedirector:
    def __init__(self, widget): self.widget = widget

    def write(self, s): self.widget.insert(tk.END, s); self.widget.see(tk.END)

    def flush(self): pass


if __name__ == "__main__":
    MidasIntelligenceSuite().mainloop()