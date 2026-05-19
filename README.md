# 🧮 Rechner

Ein einfacher Taschenrechner mit grafischer Benutzeroberfläche, gebaut mit Python und Tkinter.

---

## Vorschau

```
┌─────────────────────────┐
│         125 + 37 =      │  ← Verlaufszeile
│              162         │  ← Ergebnis
├──────┬──────┬──────┬────┤
│  AC  │  +/- │  %   │  ÷ │
│   7  │   8  │   9  │  × │
│   4  │   5  │   6  │  − │
│   1  │   2  │   3  │  + │
│  ⌫   │   0  │   ,  │  = │
└──────┴──────┴──────┴────┘
```

---

## Features

- Grundrechenarten: `+` `−` `×` `÷`
- Prozentrechnung `%`
- Vorzeichen wechseln `+/-`
- Komma-Eingabe `,`
- Einzelnes Zeichen löschen `⌫`
- Verlaufszeile zeigt den vorherigen Ausdruck
- Hover-Effekte auf allen Tasten
- Tastatur-Shortcuts (siehe unten)

---

## Tastatur-Shortcuts

| Taste               | Funktion          |
|---------------------|-------------------|
| `0` – `9`           | Zahl eingeben     |
| `+` `-` `*` `/`     | Rechenoperation   |
| `Enter` oder `=`    | Berechnen         |
| `,` oder `.`        | Komma             |
| `%`                 | Prozent           |
| `Backspace`         | Zeichen löschen   |
| `Escape`            | Alles löschen (AC)|

---

## Voraussetzungen

- Python 3.x
- Tkinter (ist standardmässig in Python enthalten)

---

## Starten

```bash
python rechner.py
```

---

## Als EXE erstellen (Windows)

PyInstaller installieren:

```bash
pip install pyinstaller
```

EXE bauen:

```bash
pyinstaller --onefile --windowed --name Rechner rechner.py
```

Die fertige `.exe` befindet sich danach im Ordner `dist\`.

---

## Lizenz

Dieses Projekt ist frei verwendbar.