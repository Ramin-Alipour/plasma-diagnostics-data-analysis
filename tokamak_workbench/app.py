"""Desktop starter shell for Tokamak Workbench (Tkinter + Matplotlib)."""
from __future__ import annotations
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import pandas as pd
from .catalog import CATALOG, FAMILIES
from .io import load_table, quality_report

class WorkbenchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tokamak Workbench — Plasma Diagnostics Analysis")
        self.root.geometry("1180x760")
        self.frame = ttk.Frame(root, padding=10)
        self.frame.pack(fill="both", expand=True)
        header = ttk.Frame(self.frame)
        header.pack(fill="x")
        ttk.Label(header, text="TOKAMAK WORKBENCH", font=("TkDefaultFont", 16, "bold")).pack(side="left")
        ttk.Button(header, text="Import data…", command=self.open_data).pack(side="right")
        ttk.Label(self.frame, text="New analysis workspace. The existing publication workflows remain preserved.", foreground="#555").pack(anchor="w", pady=(2,8))
        panes = ttk.Panedwindow(self.frame, orient="horizontal")
        panes.pack(fill="both", expand=True)
        left = ttk.Frame(panes, padding=6)
        right = ttk.Frame(panes, padding=6)
        panes.add(left, weight=1); panes.add(right, weight=2)
        ttk.Label(left, text="Diagnostic / observable catalog", font=("TkDefaultFont", 11, "bold")).pack(anchor="w")
        self.search = tk.StringVar()
        search = ttk.Entry(left, textvariable=self.search)
        search.pack(fill="x", pady=5); search.bind("<KeyRelease>", lambda _e: self.refresh_catalog())
        self.family = tk.StringVar(value="All families")
        family_box = ttk.Combobox(left, textvariable=self.family, values=["All families"] + FAMILIES, state="readonly")
        family_box.pack(fill="x", pady=(0,5)); family_box.bind("<<ComboboxSelected>>", lambda _e: self.refresh_catalog())
        self.catalog_tree = ttk.Treeview(left, columns=("family","status"), show="tree headings", height=20)
        self.catalog_tree.heading("#0", text="Observable")
        self.catalog_tree.heading("family", text="Family")
        self.catalog_tree.heading("status", text="Output type")
        self.catalog_tree.column("#0", width=220); self.catalog_tree.column("family", width=130); self.catalog_tree.column("status", width=120)
        self.catalog_tree.pack(fill="both", expand=True)
        self.catalog_tree.bind("<<TreeviewSelect>>", self.show_parameter)
        ttk.Label(right, text="Workspace", font=("TkDefaultFont", 11, "bold")).pack(anchor="w")
        self.status = tk.StringVar(value="No data imported. Choose Import data… to load CSV, TSV, TXT or Excel.")
        ttk.Label(right, textvariable=self.status, wraplength=650).pack(anchor="w", pady=4)
        self.detail = tk.Text(right, height=13, wrap="word")
        self.detail.pack(fill="x", pady=5)
        self.detail.insert("1.0", "Select an observable from the catalog to inspect its methods, equation, inputs and limitations.\n\nCatalog formulas are not all implemented as executable algorithms; each result must be checked against calibration, units, geometry and the instrument response.")
        self.detail.configure(state="disabled")
        ttk.Label(right, text="Imported table preview", font=("TkDefaultFont", 10, "bold")).pack(anchor="w", pady=(8,2))
        table_wrap = ttk.Frame(right); table_wrap.pack(fill="both", expand=True)
        self.table = ttk.Treeview(table_wrap, show="headings")
        ybar = ttk.Scrollbar(table_wrap, orient="vertical", command=self.table.yview)
        xbar = ttk.Scrollbar(table_wrap, orient="horizontal", command=self.table.xview)
        self.table.configure(yscrollcommand=ybar.set, xscrollcommand=xbar.set)
        self.table.grid(row=0,column=0,sticky="nsew"); ybar.grid(row=0,column=1,sticky="ns"); xbar.grid(row=1,column=0,sticky="ew")
        table_wrap.rowconfigure(0,weight=1); table_wrap.columnconfigure(0,weight=1)
        self.data = None
        self.refresh_catalog()

    def refresh_catalog(self):
        for node in self.catalog_tree.get_children(): self.catalog_tree.delete(node)
        q = self.search.get().strip().lower()
        fam = self.family.get()
        for p in CATALOG:
            if fam != "All families" and p["family"] != fam: continue
            hay = " ".join(str(p.get(k,"")) for k in ("name","symbol","methods","formula","id")).lower()
            if q and q not in hay: continue
            self.catalog_tree.insert("", "end", iid=p["id"], text=p["name"], values=(p["family"],p["status"]))

    def show_parameter(self, _event=None):
        selected = self.catalog_tree.selection()
        if not selected: return
        p = next((x for x in CATALOG if x["id"] == selected[0]), None)
        if not p: return
        lines = [p["name"], f"ID: {p['id']} | Symbol: {p['symbol']} | Unit: {p['unit']}", f"Family: {p['family']} | Classification: {p['status']}", "", "Methods:", ", ".join(p.get("methods",[])), "", "Formula / principle:", p["formula"], "", "Required inputs:", ", ".join(p.get("inputs",[])), "", "Limitations:", p["limitations"]]
        self.detail.configure(state="normal"); self.detail.delete("1.0","end"); self.detail.insert("1.0","\n".join(lines)); self.detail.configure(state="disabled")

    def open_data(self):
        path = filedialog.askopenfilename(title="Import diagnostic data", filetypes=[("Data tables","*.csv *.tsv *.txt *.xlsx *.xls"),("All files","*.*")])
        if not path: return
        try:
            frame = load_table(path)
        except Exception as exc:
            messagebox.showerror("Import failed", str(exc)); return
        self.data = frame
        self.status.set(f"Loaded {Path(path).name}: {len(frame)} rows × {len(frame.columns)} columns. Quality report: {quality_report(frame)['duplicate_rows']} duplicate rows; {sum(frame.isna().sum())} missing cells. Source values have not been modified.")
        self.show_table(frame)

    def show_table(self, frame):
        self.table.delete(*self.table.get_children())
        cols = [str(c) for c in frame.columns]
        self.table["columns"] = cols
        for c in cols:
            self.table.heading(c,text=c); self.table.column(c,width=110,stretch=True)
        for _, row in frame.head(200).iterrows():
            values = ["" if pd.isna(v) else str(v) for v in row.tolist()]
            self.table.insert("","end",values=values)

def main():
    root = tk.Tk()
    WorkbenchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
