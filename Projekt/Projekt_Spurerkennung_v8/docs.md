# Digitale Bildverarbeitung - Spurerkennung 

Diese Schritte beziehen sich auf das Jupyter Notebook "Projekt_Spurerkennung_Dokumentation".

# 1. Schritt: Kalibrierung der Kamera
Kalibrierung der Kamera und entzerren der Udacity-Testbilder. 
Es werden sowohl die Schachbrettbilder als auch die Udacity-Testbilder entzerrt und beispielhaft angezeigt.
Vor dem Anzeigen werden die Bilder zugeschnitten, sodass der schwarze Rand entfernt wird.
Die entzerrten Bilder werden in dem Array `undistorted_images` gespeichert.

# 2. Schritt: Zuschneiden der Bilder
Die zugeschnittenen Bilder werden in dem Array `cropped_images` gespeichert.
Es werden nur die für die Spurerkennung relevanten Bildbereiche ausgeschnitten.

# 3. Schritt: Perspektivtransformation
Die Bilder werden perspektivisch transformiert, sodass die Spurmarkierungen
von oben betrachtet werden können.
Die Bilder werden in dem Array `warpped_images` gespeichert.

# 4. Schritt: Farbfilter
Es werden die Farbfilter für die Farben weiß und gelb definiert, 
sodass die Spurmarkierungen in den Bildern hervorgehoben werden.
Die Bilder werden in dem Array `filtered_images` gespeichert.

# 5. Schritt: Thresholding
Auf die gefilterten Bilder wird ein Thresholding angewendet, 
um die Spurmarkierungen besser hervorzuheben. 
Die Bilder werden in dem Array `thresh_images` gespeichert.


# 6. Schritt: Curve fitting und Radiusberechnung
Es wird eine Kurve durch die Spurmarkierungen gelegt und der Radius der Kurve berechnet.
Die Bilder werden in dem Array `curve_images` gespeichert.
