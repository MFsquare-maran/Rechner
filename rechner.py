# -*- coding: utf-8 -*-
"""
Created on Tue May 19 14:13:14 2026

@author: FMA
"""

import tkinter as tk

# --------------------------------------------------------------------
# Farben & Schriften
# --------------------------------------------------------------------
FARBEN = {
    "hintergrund":  "#1a1a2e",
    "display_bg":   "#16213e",
    "taste_zahl":   "#0f3460",
    "taste_op":     "#e94560",
    "taste_gleich": "#e94560",
    "taste_clear":  "#533483",
    "taste_spez":   "#1a1a2e",
    "text_hell":    "#eaeaea",
    "text_op":      "#ffffff",
    "hover_zahl":   "#1a4a8a",
    "hover_op":     "#c73652",
    "hover_clear":  "#6a42a8",
    "rand":         "#0a0a1a",
}

SCHRIFT_DISPLAY  = ("Courier New", 32, "bold")
SCHRIFT_KLEIN    = ("Courier New", 12)
SCHRIFT_TASTE    = ("Courier New", 18, "bold")
SCHRIFT_TASTE_SM = ("Courier New", 14, "bold")


# --------------------------------------------------------------------
# Rechner-Logik
# --------------------------------------------------------------------
class Rechner:
    def __init__(self):
        self.ausdruck   = ""   # was gerade eingegeben wird
        self.vorherig   = ""   # vorheriger Ausdruck (Verlauf)
        self.ergebnis   = "0"
        self.neu_zahl   = True # nach "=" neue Zahl starten

    def zahl_eingeben(self, wert):
        if self.neu_zahl and wert not in ("+", "-", "*", "/", "%"):
            self.ausdruck = ""
            self.neu_zahl = False
        self.ausdruck += wert

    def berechnen(self):
        try:
            self.vorherig = self.ausdruck + " ="
            ergebnis = eval(self.ausdruck)
            # Ganze Zahlen ohne Dezimalpunkt anzeigen
            if ergebnis == int(ergebnis):
                self.ergebnis = str(int(ergebnis))
            else:
                self.ergebnis = str(round(ergebnis, 10))
            self.ausdruck = self.ergebnis
            self.neu_zahl = True
        except:
            self.ergebnis = "Fehler"
            self.ausdruck = ""
            self.neu_zahl = True

    def loeschen(self):
        self.ausdruck = ""
        self.vorherig = ""
        self.ergebnis = "0"
        self.neu_zahl = True

    def backspace(self):
        self.ausdruck = self.ausdruck[:-1]
        self.neu_zahl = False

    def plusminus(self):
        if self.ausdruck.startswith("-"):
            self.ausdruck = self.ausdruck[1:]
        elif self.ausdruck:
            self.ausdruck = "-" + self.ausdruck

    def komma(self):
        # Nur ein Komma pro Zahl erlauben
        teile = self.ausdruck.replace("*", "+").replace("/", "+").replace("-", "+").split("+")
        letzte = teile[-1] if teile else ""
        if "." not in letzte:
            if not self.ausdruck or self.ausdruck[-1] in "+-*/":
                self.ausdruck += "0."
            else:
                self.ausdruck += "."
        self.neu_zahl = False


# --------------------------------------------------------------------
# GUI
# --------------------------------------------------------------------
class RechnerGUI:
    def __init__(self, root):
        self.root   = root
        self.logik  = Rechner()

        root.title("Rechner")
        root.resizable(False, False)
        root.configure(bg=FARBEN["rand"])

        self._aufbau()
        self._anzeige_aktualisieren()

    # ----------------------------------------------------------------
    # Display
    # ----------------------------------------------------------------
    def _aufbau(self):
        # Äusserer Rahmen
        rahmen = tk.Frame(self.root, bg=FARBEN["rand"], padx=2, pady=2)
        rahmen.pack()

        haupt = tk.Frame(rahmen, bg=FARBEN["hintergrund"], padx=12, pady=12)
        haupt.pack()

        # Display-Bereich
        display_rahmen = tk.Frame(haupt, bg=FARBEN["display_bg"],
                                  padx=16, pady=12)
        display_rahmen.grid(row=0, column=0, columnspan=4,
                            sticky="ew", pady=(0, 12))

        self.vorherig_var = tk.StringVar()
        self.anzeige_var  = tk.StringVar()

        tk.Label(
            display_rahmen,
            textvariable=self.vorherig_var,
            font=SCHRIFT_KLEIN,
            bg=FARBEN["display_bg"],
            fg="#666688",
            anchor="e",
        ).pack(fill="x")

        tk.Label(
            display_rahmen,
            textvariable=self.anzeige_var,
            font=SCHRIFT_DISPLAY,
            bg=FARBEN["display_bg"],
            fg=FARBEN["text_hell"],
            anchor="e",
        ).pack(fill="x")

        # Tastenlayout definieren
        # (Text, Zeile, Spalte, Colspan, Typ)
        tasten = [
            ("AC",  1, 0, 1, "clear"),
            ("+/-", 1, 1, 1, "spez"),
            ("%",   1, 2, 1, "spez"),
            ("÷",   1, 3, 1, "op"),

            ("7",   2, 0, 1, "zahl"),
            ("8",   2, 1, 1, "zahl"),
            ("9",   2, 2, 1, "zahl"),
            ("×",   2, 3, 1, "op"),

            ("4",   3, 0, 1, "zahl"),
            ("5",   3, 1, 1, "zahl"),
            ("6",   3, 2, 1, "zahl"),
            ("−",   3, 3, 1, "op"),

            ("1",   4, 0, 1, "zahl"),
            ("2",   4, 1, 1, "zahl"),
            ("3",   4, 2, 1, "zahl"),
            ("+",   4, 3, 1, "op"),

            ("⌫",   5, 0, 1, "spez"),
            ("0",   5, 1, 1, "zahl"),
            (",",   5, 2, 1, "zahl"),
            ("=",   5, 3, 1, "gleich"),
        ]

        farb_map = {
            "zahl":   (FARBEN["taste_zahl"],  FARBEN["hover_zahl"],  FARBEN["text_hell"]),
            "op":     (FARBEN["taste_op"],    FARBEN["hover_op"],    FARBEN["text_op"]),
            "clear":  (FARBEN["taste_clear"], FARBEN["hover_clear"], FARBEN["text_hell"]),
            "spez":   (FARBEN["taste_spez"],  "#2a2a4e",             FARBEN["text_hell"]),
            "gleich": (FARBEN["taste_gleich"],FARBEN["hover_op"],    FARBEN["text_op"]),
        }

        TASTE_W = 72
        TASTE_H = 56

        for (text, zeile, spalte, span, typ) in tasten:
            bg, hover, fg = farb_map[typ]
            schrift = SCHRIFT_TASTE if len(text) == 1 else SCHRIFT_TASTE_SM

            btn = tk.Button(
                haupt,
                text=text,
                font=schrift,
                bg=bg,
                fg=fg,
                activebackground=hover,
                activeforeground=fg,
                relief="flat",
                bd=0,
                width=int(TASTE_W * span / 10),
                cursor="hand2",
                command=lambda t=text: self._taste_gedrueckt(t),
            )
            btn.grid(
                row=zeile, column=spalte,
                columnspan=span,
                padx=4, pady=4,
                ipadx=14, ipady=10,
                sticky="nsew",
            )

            # Hover-Effekt
            btn.bind("<Enter>", lambda e, b=btn, h=hover: b.config(bg=h))
            btn.bind("<Leave>", lambda e, b=btn, n=bg:    b.config(bg=n))

        # Tastatur-Shortcuts
        self.root.bind("<Key>", self._tastatur)

    # ----------------------------------------------------------------
    # Anzeige aktualisieren
    # ----------------------------------------------------------------
    def _anzeige_aktualisieren(self):
        anzeige = self.logik.ausdruck if self.logik.ausdruck else self.logik.ergebnis
        # Operatoren leserlich darstellen
        anzeige = anzeige.replace("*", "×").replace("/", "÷").replace("-", "−")
        self.anzeige_var.set(anzeige)
        self.vorherig_var.set(self.logik.vorherig)

    # ----------------------------------------------------------------
    # Taste gedrückt
    # ----------------------------------------------------------------
    def _taste_gedrueckt(self, taste):
        l = self.logik
        if   taste == "AC":   l.loeschen()
        elif taste == "+/-":  l.plusminus()
        elif taste == "%":    l.zahl_eingeben("%")
        elif taste == "÷":    l.zahl_eingeben("/")
        elif taste == "×":    l.zahl_eingeben("*")
        elif taste == "−":    l.zahl_eingeben("-")
        elif taste == "+":    l.zahl_eingeben("+")
        elif taste == "=":    l.berechnen()
        elif taste == ",":    l.komma()
        elif taste == "⌫":    l.backspace()
        else:                 l.zahl_eingeben(taste)
        self._anzeige_aktualisieren()

    # ----------------------------------------------------------------
    # Tastatur-Shortcuts
    # ----------------------------------------------------------------
    def _tastatur(self, event):
        taste = event.char
        keysym = event.keysym
        if taste in "0123456789":   self._taste_gedrueckt(taste)
        elif taste == "+":          self._taste_gedrueckt("+")
        elif taste in ("-", "−"):   self._taste_gedrueckt("−")
        elif taste == "*":          self._taste_gedrueckt("×")
        elif taste == "/":          self._taste_gedrueckt("÷")
        elif taste in ("=", "\r"):  self._taste_gedrueckt("=")
        elif taste in (",", "."):   self._taste_gedrueckt(",")
        elif taste == "%":          self._taste_gedrueckt("%")
        elif keysym == "BackSpace": self._taste_gedrueckt("⌫")
        elif keysym == "Escape":    self._taste_gedrueckt("AC")


# --------------------------------------------------------------------
# Start
# --------------------------------------------------------------------
root = tk.Tk()
app  = RechnerGUI(root)
root.mainloop()