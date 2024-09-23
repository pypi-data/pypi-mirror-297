"""
Informatikunterricht - Bildverarbeitungsmodul

Dieses Modul bietet Funktionen für die sehr einfache erarbeitung und Analyse von Bildern.
Es ermöglicht das Laden, Speichern und Anzeigen von Bildern, sowie die Berechnung von
Farbtiefen und die Transformation von palettenbasierten Bildern in RGB.

Autor:
- Henning Mattes

Lizenz:
- MIT License mit Zusatz: Siehe LICENSE-Datei im Repository

Abhängigkeiten:
- numpy
- matplotlib
- pillow

Beispielverwendung:

    # Bild laden und Farbtiefe berechnen
    bild, farbmodus, farbtiefe, palette = lade_bild('pfad/zum/bild.png')
    print(f"Farbtiefe: {farbtiefe} Bit")

    # Bild anzeigen
    zeige(bild)

    # Bild speichern
    speichere_bild('pfad/zum/ausgabebild.png', bild, palette)

"""

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import matplotlib.cm as cm
from matplotlib.cm import ScalarMappable
from matplotlib.colors import Normalize

def numpy_array(bild):
    original_farbmodus = bild.mode
    return (np.array(bild), original_farbmodus)

# Funktion zur Berechnung der Farbtiefe
def berechne_farbtiefe(bild):
    farbmodus = bild.mode
    if farbmodus == '1':  # Binärmodus
        return 1
    elif farbmodus == 'L':  # 8-Bit-Graustufen
        return 8
    elif farbmodus == 'RGB':  # 24-Bit-Farbe
        return 24
    elif farbmodus == 'RGBA':  # 32-Bit-Farbe mit Alpha
        return 32
    elif farbmodus == 'P':  # Palette
        palette = bild.getpalette()
        anzahl_farben = len({tuple(palette[i:i+3]) for i in range(0, len(palette), 3)})
        if anzahl_farben <= 16:
            return 4  # 4 Bits für 16 Farben
        else:
            return 8  # 8 Bits für mehr als 16 Farben
    else:
        return 'Unbekannt'

def transformiere_palettenbild_zu_rgb(np_array_bild, palette):
    # Erstellen eines leeren Bildes mit der gleichen Größe wie das Eingabebild
    bild = np.zeros((np_array_bild.shape[0], np_array_bild.shape[1], 3), dtype=np.uint8)
    
    # Ersetzen der Farbwerte durch die Werte aus der Palette
    for i in range(np_array_bild.shape[0]):
        for j in range(np_array_bild.shape[1]):
            bild[i, j] = palette[np_array_bild[i, j]]
    
    return bild

def lade_bild(pfad_und_dateiname):
    pil_bild = Image.open(pfad_und_dateiname)
    bild, farbmodus = numpy_array(pil_bild)
    if farbmodus == 'P':  # Palette
        palette = pil_bild.getpalette()
        # Umwandeln der flachen Palette in ein 2D-NumPy-Array (N x 3), wobei N die Anzahl der Farben ist
        palette_array = np.array(palette).reshape((-1, 3))
    else:
        palette_array = None
    return bild, farbmodus, berechne_farbtiefe(pil_bild), palette_array

def pillow_bild(numpy_array, palette=None):
    # Bestimmen des Farbmodus basierend auf der Form und der Palette
    if palette is not None:
        farbmodus = 'P'
        image = Image.fromarray(numpy_array.astype('uint8'), 'P')
        flat_palette = palette.flatten().tolist()
        image.putpalette(flat_palette)
    elif numpy_array.ndim == 2:
        farbmodus = 'L'
        image = Image.fromarray(numpy_array, 'L')
    elif numpy_array.shape[2] == 3:
        farbmodus = 'RGB'
        image = Image.fromarray(numpy_array, 'RGB')
    elif numpy_array.shape[2] == 4:
        farbmodus = 'RGBA'
        image = Image.fromarray(numpy_array, 'RGBA')
    else:
        raise ValueError("Unbekanntes Format oder Farbmodus kann nicht bestimmt werden")

    return image

def speichere_bild(pfad, np_array_bild, palette=None):
    # Erstellen des Pillow-Bildes, jetzt mit möglicher Palette
    pillow_image = pillow_bild(np_array_bild, palette)
    # Speichern des Bildes
    pillow_image.save(pfad)

def transformiere_palettenbild_zu_rgb(np_array_bild, palette):
    # Erstellen eines leeren Bildes mit der gleichen Größe wie das Eingabebild
    bild = np.zeros((np_array_bild.shape[0], np_array_bild.shape[1], 3), dtype=np.uint8)
    
    # Ersetzen der Farbwerte durch die Werte aus der Palette
    for i in range(np_array_bild.shape[0]):
        for j in range(np_array_bild.shape[1]):
            bild[i, j] = palette[np_array_bild[i, j]]
    
    return bild

def zeige(bilddaten, zeige_achsen=True, beschriftungsdaten=None, palettendaten=None, zeige_grid=False, grid_color='black', tickanzahl=None, spaltenanzahl=1, figsize=None):
    if not isinstance(bilddaten, list):
        bilddaten = [bilddaten]  # Einzelbild in Liste umwandeln für einheitliche Verarbeitung

    def parameter_liste_vorbereiten(param, name, length):
        if isinstance(param, list):
            if len(param) != length:
                raise ValueError(f"Wenn für bilddaten eine Liste übergeben wird, kann (muss aber nicht) auch für '{name}' eine"
                                 + f"Liste übergeben werden. In diesem Falls muss die Länge der Liste '{name}' muss der Länge der"
                                 + f" Liste bilddaten übereinstimmen.")
        else:
            param = [param] * length
        return param

    palettendaten = parameter_liste_vorbereiten(palettendaten, 'palettendaten', len(bilddaten))
    beschriftungsdaten = parameter_liste_vorbereiten(beschriftungsdaten, 'beschriftungsdaten', len(bilddaten))
    zeige_grid = parameter_liste_vorbereiten(zeige_grid, 'zeige_grid', len(bilddaten))
    grid_color = parameter_liste_vorbereiten(grid_color, 'grid_color', len(bilddaten))
    tickanzahl = parameter_liste_vorbereiten(tickanzahl, 'tickanzahl', len(bilddaten))

    anzahl_bilder = len(bilddaten)
    zeilenanzahl = np.ceil(anzahl_bilder / spaltenanzahl).astype(int)

    # Erstelle Subplots
    if figsize is None:
        figsize = (spaltenanzahl * 5, zeilenanzahl * 5)
    fig, axs = plt.subplots(zeilenanzahl, spaltenanzahl, figsize=figsize)
    axs = np.ravel([axs])

    for idx, bild in enumerate(bilddaten):
        ax = axs[idx]
        if beschriftungsdaten[idx] is not None:
            ax.set_title(beschriftungsdaten[idx])

        current_palette = palettendaten[idx]
        if isinstance(current_palette, np.ndarray):
            bild = transformiere_palettenbild_zu_rgb(bild, current_palette)
            ax.imshow(bild)
        else:
            cmap = current_palette if current_palette is not None else 'gray'
            ax.imshow(bild, cmap=cmap)

        if zeige_achsen:
            ax.axis('on')
            if tickanzahl[idx] is not None:
                ticks_x = np.linspace(0, bild.shape[1] - 1, num=tickanzahl[idx], dtype=int)
                ticks_y = np.linspace(0, bild.shape[0] - 1, num=tickanzahl[idx], dtype=int)
                ax.set_xticks(ticks_x)
                ax.set_yticks(ticks_y)
                ax.set_xticklabels(ticks_x)
                ax.set_yticklabels(ticks_y)
        else:
            ax.axis('off')

        if zeige_grid[idx]:
            ax.set_xticks(np.arange(-.5, bild.shape[1], 1), minor=True)
            ax.set_yticks(np.arange(-.5, bild.shape[0], 1), minor=True)
            ax.grid(which="minor", color=grid_color[idx], linestyle='-', linewidth=1)
            ax.tick_params(which="minor", size=0)
        else:
            ax.grid(False)

    plt.tight_layout()
    plt.show()

def plot_histogramm(histogramm, palette='inferno'):
    fig, ax = plt.subplots(1, 1, figsize=(10, 5))
    # Min und Max für die Normalisierung finden
    # Ignoriere 0 Werte für Min-Bestimmung
    non_zero_values = histogramm[np.nonzero(histogramm)]
    if non_zero_values.size == 0:  # Fall, wenn das Histogramm nur Nullen enthält
        min_val = 0
    else:
        min_val = non_zero_values.min()
    max_val = histogramm.max()

    # Normalisierungsobjekt erstellen
    norm = Normalize(vmin=min_val, vmax=max_val)
    cmap = plt.get_cmap(palette)
    
    # ScalarMappable für die Colorbar
    mappable = ScalarMappable(norm=norm, cmap=cmap)

    # Balken zeichnen mit Farben basierend auf der Höhe des Balkens
    # Alle Balken, auch die mit Wert 0, zeichnen, um Farbe 0 zu nutzen
    for i in range(256):
        color = cmap(0) if histogramm[i] == 0 else cmap(norm(histogramm[i]))
        ax.bar(i, histogramm[i], color=color, width=1)

    ax.set_title('Histogramm')
    ax.set_xlabel('Helligkeit/Luminanzwerte (0-255)')
    ax.set_ylabel('Anzahl der Pixel')

    ax.set_xlim(0, 255)
    ax.set_ylim(0, max(histogramm) + max(histogramm) * 0.05)

    ax.set_xticks(range(0, 256, 50))
    y_ticks_max = max(histogramm) + 1
    ax.set_yticks(np.linspace(0, y_ticks_max, num=5, endpoint=True))
    ax.tick_params(axis='both', which='major', labelsize=8)

    # Colorbar hinzufügen
    fig = ax.figure
    cbar = fig.colorbar(mappable, ax=ax)
    cbar.set_label('Anzahl der Pixel')
    plt.show()
