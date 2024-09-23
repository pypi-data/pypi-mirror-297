"""
Informatikunterricht - Visualisierung von Verteilungen

Dieses Modul bietet Funktionen zur Visualisierung von zwei Verteilungen, die typischerweise
im Rahmen des Informatikunterrichts verwendet werden können. Es verwendet Matplotlib, um 
zwei Verteilungen nebeneinander als Linien- oder Balkendiagramme darzustellen. 

Funktionen:
- zeige_verteilungen(verteilung1, verteilung2, titel1="", titel2="", modus="Linien", figsize=(10, 10)):
    Visualisiert zwei Verteilungen als Linien- oder Balkendiagramme.

Parameter:
- verteilung1: Eine Liste oder ein Array, das die erste Verteilung darstellt.
- verteilung2: Eine Liste oder ein Array, das die zweite Verteilung darstellt.
- titel1: Titel für das erste Diagramm (Standard: leer).
- titel2: Titel für das zweite Diagramm (Standard: leer).
- modus: Modus der Darstellung, entweder "Linien" (Standard) oder "Balken".
- figsize: Höhe und Breite der Gesamtdarstellung.

Beispielverwendung:
    verteilung1 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
    verteilung2 = [26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
    zeige_verteilungen(verteilung1, verteilung2, "Verteilung 1", "Verteilung 2", "Balken")

Hinweis:
Dieses Modul wurde speziell für den Einsatz im Informatikunterricht entwickelt und bietet 
eine einfache Möglichkeit, grundlegende Datenvisualisierungen durchzuführen. Es kann in 
anderen Projekten wiederverwendet werden, die ähnliche Anforderungen an die Visualisierung 
stellen.

Autor:
- Henning Mattes

Lizenz:
- MIT License mit Zusatz: Siehe LICENSE-Datei im Repository

Abhängigkeiten:
- matplotlib

"""

import matplotlib.pyplot as plt

def zeige_verteilungen(verteilung1, verteilung2, titel1 = "", titel2 = "", modus = "Linien", figsize=(10, 10)):
    
    def zeichen(code26zahl):
        return chr(code26zahl + ord("A"))
    
    fig, axs = plt.subplots(2, 1, figsize=figsize)
    ticks = range(1, 27)
    beschriftungen = [zeichen(i-1) for i in ticks]
    for ax, verteilung, titel, color in zip(axs, [verteilung1, verteilung2], [titel1, titel2], ["red", "blue"]):
        if modus.upper() == "BALKEN":
            ax.bar(ticks, verteilung, align = 'center', color = color)
        else:
            ax.plot(ticks, verteilung, marker = "x", color = color)
        ax.grid()
        ax.set_xticks(ticks)
        ax.set_xticklabels(beschriftungen)
        ax.set_title(titel)
    plt.show()
