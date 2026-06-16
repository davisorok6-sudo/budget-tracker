# gui_main.py
# Main GUI for the Budget Tracker Application
# University Project - Budget Tracker
# Run this file to launch the app: python gui_main.py

import tkinter as tk
from tkinter import ttk, messagebox
from budget_manager import BudgetManager

# ── Colour Palette ────────────────────────────────────────────────────────────
BG_DARK      = "#0D1B2A"   # deep navy  – window background
BG_CARD      = "#1B2E45"   # dark blue  – card / panel background
BG_INPUT     = "#243B55"   # mid blue   – entry / listbox background
ACCENT       = "#1E90FF"   # dodger blue – primary accent
ACCENT_HOVER = "#3AA8FF"   # lighter blue for hover
SUCCESS      = "#2ECC71"   # green for income / positive balance
DANGER       = "#E74C3C"   # red for expenses / negative balance
TEXT_MAIN    = "#E8F4FD"   # near-white
TEXT_SUB     = "#7EB8D4"   # muted blue-white
BORDER       = "#2A4870"   # subtle border

FONT_TITLE  = ("Segoe UI", 22, "bold")
FONT_HEAD   = ("Segoe UI", 13, "bold")
FONT_BODY   = ("Segoe UI", 10)
FONT_SMALL  = ("Segoe UI", 9)
FONT_MONO   = ("Consolas", 10)
FONT_BIG    = ("Segoe UI", 20, "bold")


class BudgetApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.manager = BudgetManager()
        self.title("Budget Tracker  •  University Project")
        self.geometry("980x720")
        self.minsize(900, 650)
        self.configure(bg=BG_DARK)
        self._configure_styles()
        self._build_ui()

    # ── ttk style setup ───────────────────────────────────────────────────────
    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TFrame", background=BG_DARK)
        style.configure("Card.TFrame", background=BG_CARD)

        style.configure("TLabel",
                        background=BG_DARK, foreground=TEXT_MAIN,
                        font=FONT_BODY)
        style.configure("Card.TLabel",
                        background=BG_CARD, foreground=TEXT_MAIN,
                        font=FONT_BODY)
        style.configure("Sub.TLabel",
                        background=BG_CARD, foreground=TEXT_SUB,
                        font=FONT_SMALL)
        style.configure("Head.TLabel",
                        background=BG_CARD, foreground=TEXT_MAIN,
                        font=FONT_HEAD)

        # Notebook (tabs)
        style.configure("TNotebook",
                        background=BG_DARK, borderwidth=0)
        style.configure("TNotebook.Tab",
                        background=BG_CARD, foreground=TEXT_SUB,
                        font=FONT_BODY, padding=[18, 8])
        style.map("TNotebook.Tab",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", TEXT_MAIN)])

        # Combobox
        style.configure("TCombobox",
                        fieldbackground=BG_INPUT,
                        background=BG_INPUT,
                        foreground=TEXT_MAIN,
                        selectbackground=ACCENT,
                        font=FONT_BODY)
        style.map("TCombobox",
                  fieldbackground=[("readonly", BG_INPUT)],
                  foreground=[("readonly", TEXT_MAIN)])

        # Scrollbar
        style.configure("Vertical.TScrollbar",
                        background=BG_CARD, troughcolor=BG_INPUT,
                        arrowcolor=TEXT_SUB, borderwidth=0)

    # ── Root layout ───────────────────────────────────────────────────────────
    def _build_ui(self):
        # Header bar
        header = tk.Frame(self, bg=BG_CARD, height=64)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(header, text="💰  Budget Tracker",
                 bg=BG_CARD, fg=ACCENT,
                 font=FONT_TITLE).pack(side="left", padx=24, pady=14)

        tk.Label(header, text="University Project",
                 bg=BG_CARD, fg=TEXT_SUB,
                 font=FONT_SMALL).pack(side="left", pady=20)

        # Refresh button (top right)
        self._make_btn(header, "⟳  Refresh / Clear All",
                       self._confirm_reset,
                       bg=DANGER, fg=TEXT_MAIN,
                       padx=16, pady=6).pack(side="right", padx=20, pady=14)

        # Summary bar
        self._summary_frame = tk.Frame(self, bg=BG_DARK, pady=12)
        self._summary_frame.pack(fill="x", padx=20)
        self._build_summary_bar()

        # Divider
        tk.Frame(self, bg=BORDER, height=1).pack(fill="x", padx=20)

        # Main content: notebook
        nb = ttk.Notebook(self)
        nb.pack(fill="both", expand=True, padx=20, pady=16)

        # Tab 1 – Add Transaction
        tab_add = ttk.Frame(nb, style="TFrame")
        nb.add(tab_add, text="  ➕  Add Transaction  ")
        self._build_add_tab(tab_add)

        # Tab 2 – Income History
        tab_income = ttk.Frame(nb, style="TFrame")
        nb.add(tab_income, text="  📈  Income  ")
        self._income_list_frame = tab_income
        self._build_list_tab(tab_income, "income")

        # Tab 3 – Expenses History
        tab_exp = ttk.Frame(nb, style="TFrame")
        nb.add(tab_exp, text="  📉  Expenses  ")
        self._expense_list_frame = tab_exp
        self._build_list_tab(tab_exp, "expense")

    # ── Summary bar ───────────────────────────────────────────────────────────
    def _build_summary_bar(self):
        for w in self._summary_frame.winfo_children():
            w.destroy()

        summary = self.manager.get_summary()
        items = [
            ("Total Income",   f"₦{summary['income']:,.2f}",   SUCCESS),
            ("Total Expenses", f"₦{summary['expenses']:,.2f}", DANGER),
            ("Balance Left",   f"₦{summary['balance']:,.2f}",
             SUCCESS if summary['balance'] >= 0 else DANGER),
        ]

        for label, value, color in items:
            card = tk.Frame(self._summary_frame, bg=BG_CARD,
                            padx=28, pady=14)
            card.pack(side="left", expand=True, fill="both",
                      padx=8, ipadx=8)
            self._add_card_border(card, color)
            tk.Label(card, text=label,
                     bg=BG_CARD, fg=TEXT_SUB,
                     font=FONT_SMALL).pack(anchor="w")
            tk.Label(card, text=value,
                     bg=BG_CARD, fg=color,
                     font=FONT_BIG).pack(anchor="w", pady=(2, 0))

    def _add_card_border(self, frame, color):
        """Add a thin left-side coloured border to a card."""
        bar = tk.Frame(frame, bg=color, width=4)
        bar.place(x=0, y=0, relheight=1)

    # ── Add Transaction tab ───────────────────────────────────────────────────
    def _build_add_tab(self, parent):
        parent.columnconfigure(0, weight=1)
        parent.columnconfigure(1, weight=1)

        # -- Income panel (left) --
        inc_card = self._card(parent, "📈  Add Income")
        inc_card.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=8)
        self._inc_title_var   = tk.StringVar()
        self._inc_amount_var  = tk.StringVar()
        self._inc_cat_var     = tk.StringVar(value="Salary")
        income_cats = ["Salary", "Freelance", "Allowance",
                       "Business", "Gift", "Other"]
        self._build_form(inc_card,
                         title_var=self._inc_title_var,
                         amount_var=self._inc_amount_var,
                         cat_var=self._inc_cat_var,
                         categories=income_cats,
                         btn_text="Add Income",
                         btn_color=SUCCESS,
                         command=self._add_income)

        # -- Expense panel (right) --
        exp_card = self._card(parent, "📉  Add Expense")
        exp_card.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=8)
        self._exp_title_var  = tk.StringVar()
        self._exp_amount_var = tk.StringVar()
        self._exp_cat_var    = tk.StringVar(value="Food")
        expense_cats = ["Food", "Transport", "Housing", "Utilities",
                        "Education", "Health", "Entertainment",
                        "Clothing", "Other"]
        self._build_form(exp_card,
                         title_var=self._exp_title_var,
                         amount_var=self._exp_amount_var,
                         cat_var=self._exp_cat_var,
                         categories=expense_cats,
                         btn_text="Add Expense",
                         btn_color=DANGER,
                         command=self._add_expense)

        # -- Status label --
        self._status_var = tk.StringVar(value="")
        tk.Label(parent, textvariable=self._status_var,
                 bg=BG_DARK, fg=SUCCESS,
                 font=FONT_BODY).grid(row=1, column=0, columnspan=2,
                                      pady=(0, 4))

    def _card(self, parent, title: str) -> tk.Frame:
        """Create and return a styled card frame with a heading."""
        outer = tk.Frame(parent, bg=BORDER, padx=1, pady=1)
        inner = tk.Frame(outer, bg=BG_CARD, padx=24, pady=20)
        inner.pack(fill="both", expand=True)
        tk.Label(inner, text=title,
                 bg=BG_CARD, fg=TEXT_MAIN,
                 font=FONT_HEAD).pack(anchor="w", pady=(0, 14))
        outer.inner = inner
        return outer

    def _build_form(self, card_outer, title_var, amount_var,
                    cat_var, categories, btn_text, btn_color, command):
        f = card_outer.inner

        tk.Label(f, text="Description", bg=BG_CARD,
                 fg=TEXT_SUB, font=FONT_SMALL).pack(anchor="w")
        self._styled_entry(f, title_var).pack(fill="x", pady=(2, 10))

        tk.Label(f, text="Amount (₦)", bg=BG_CARD,
                 fg=TEXT_SUB, font=FONT_SMALL).pack(anchor="w")
        self._styled_entry(f, amount_var).pack(fill="x", pady=(2, 10))

        tk.Label(f, text="Category", bg=BG_CARD,
                 fg=TEXT_SUB, font=FONT_SMALL).pack(anchor="w")
        cb = ttk.Combobox(f, textvariable=cat_var,
                          values=categories, state="readonly",
                          font=FONT_BODY)
        cb.pack(fill="x", pady=(2, 16))

        self._make_btn(f, btn_text, command,
                       bg=btn_color, fg=TEXT_MAIN,
                       padx=0, pady=8,
                       fill=True).pack(fill="x")

    def _styled_entry(self, parent, textvariable) -> tk.Entry:
        e = tk.Entry(parent, textvariable=textvariable,
                     bg=BG_INPUT, fg=TEXT_MAIN,
                     insertbackground=ACCENT,
                     relief="flat", font=FONT_BODY,
                     highlightthickness=1,
                     highlightbackground=BORDER,
                     highlightcolor=ACCENT)
        e.configure(disabledbackground=BG_INPUT)
        return e

    # ── History list tab ──────────────────────────────────────────────────────
    def _build_list_tab(self, parent, kind: str):
        parent.columnconfigure(0, weight=1)
        parent.rowconfigure(1, weight=1)

        # Column headers
        hdr = tk.Frame(parent, bg=BG_CARD, padx=12, pady=8)
        hdr.grid(row=0, column=0, sticky="ew", pady=(8, 0))
        cols = [("#", 4), ("Description", 30), ("Category", 18),
                ("Date", 14), ("Amount (₦)", 14)]
        for col_name, width in cols:
            tk.Label(hdr, text=col_name, bg=BG_CARD, fg=TEXT_SUB,
                     font=FONT_SMALL, width=width,
                     anchor="w").pack(side="left", padx=4)

        # Listbox + scrollbar
        list_frame = tk.Frame(parent, bg=BG_DARK)
        list_frame.grid(row=1, column=0, sticky="nsew", pady=(2, 8))
        list_frame.rowconfigure(0, weight=1)
        list_frame.columnconfigure(0, weight=1)

        sb = ttk.Scrollbar(list_frame, orient="vertical")
        lb = tk.Listbox(list_frame,
                        bg=BG_INPUT, fg=TEXT_MAIN,
                        selectbackground=ACCENT,
                        activestyle="none",
                        font=FONT_MONO,
                        relief="flat",
                        bd=0,
                        yscrollcommand=sb.set)
        sb.config(command=lb.yview)
        lb.grid(row=0, column=0, sticky="nsew")
        sb.grid(row=0, column=1, sticky="ns")

        if kind == "income":
            self._income_lb = lb
        else:
            self._expense_lb = lb

    # ── Helpers ───────────────────────────────────────────────────────────────
    def _make_btn(self, parent, text, command,
                  bg=ACCENT, fg=TEXT_MAIN,
                  padx=12, pady=6, fill=False):
        btn = tk.Button(parent, text=text, command=command,
                        bg=bg, fg=fg, activebackground=ACCENT_HOVER,
                        activeforeground=TEXT_MAIN,
                        relief="flat", cursor="hand2",
                        font=("Segoe UI", 10, "bold"),
                        padx=padx, pady=pady, bd=0)
        btn.bind("<Enter>", lambda e: btn.config(bg=ACCENT_HOVER))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    # ── Actions ───────────────────────────────────────────────────────────────
    def _add_income(self):
        try:
            msg = self.manager.add_income(
                self._inc_title_var.get(),
                self._inc_amount_var.get(),
                self._inc_cat_var.get()
            )
            self._status_var.set("✔  " + msg)
            self._inc_title_var.set("")
            self._inc_amount_var.set("")
            self._refresh_all()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def _add_expense(self):
        try:
            msg = self.manager.add_expense(
                self._exp_title_var.get(),
                self._exp_amount_var.get(),
                self._exp_cat_var.get()
            )
            self._status_var.set("✔  " + msg)
            self._exp_title_var.set("")
            self._exp_amount_var.set("")
            self._refresh_all()
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def _confirm_reset(self):
        if messagebox.askyesno(
                "Clear All Data",
                "Are you sure you want to clear ALL transactions?\n"
                "This cannot be undone."):
            self.manager.reset()
            self._status_var.set("")
            self._refresh_all()

    def _refresh_all(self):
        """Rebuild summary and refresh both history lists."""
        self._build_summary_bar()
        self._refresh_list(self._income_lb,  self.manager.get_all_income())
        self._refresh_list(self._expense_lb, self.manager.get_all_expenses())

    def _refresh_list(self, listbox: tk.Listbox, transactions):
        listbox.delete(0, tk.END)
        if not transactions:
            listbox.insert(tk.END, "   No records yet.")
            return
        for i, t in enumerate(transactions, start=1):
            row = (f"  {i:<4} "
                   f"{t.title:<30} "
                   f"{t.category:<18} "
                   f"{t.date:<14} "
                   f"₦{t.amount:>12,.2f}")
            listbox.insert(tk.END, row)
            # Alternate row shading
            if i % 2 == 0:
                listbox.itemconfig(i - 1, bg="#1E3350", fg=TEXT_MAIN)
            else:
                listbox.itemconfig(i - 1, bg=BG_INPUT, fg=TEXT_MAIN)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    app = BudgetApp()
    app.mainloop()
