# Digitale Bildverarbeitung - Spurerkennung

## Setup
**Project runs on Python 3.12**, other Python Verisons have not been tested. 

1. Istallieren der Requirements aus `requirements.txt`.
2. Die Videos und Bilder müssen in den Ordnern `img\Udacity` für die Kalibration (`\calib\ `), die
   Mindestanforderung (`project_video.mp4`) und erste Zusatzleistung (`challenge_video.mp4`) sein. Die Daten der zweite
   Zusatzleistung (Anwendung der Spurerkennung auf dem Kitti-Datensatz) müssen in dem Ordner (`img\KITTI`) sein. Falls
   sich ein Pfad ändert, so müssen die Pfade auch im jeweiligen Programm angepasst werden.
3. Das Jupyter Notebook `Projekt_Spurerkennung_Dokumentation.ipynb` muss zuerst ausgeführt werden, damit die
   Datei `calibration_parameters.npz` erstellt wird und die Python Programme die Parameter importieren können.
4. Das Programm mit den Mindestanforderungen ist `lane_detection.py`.

***

# Mindestanforderungen

## Dokumentation: Jupyter Notebook `Projekt_Spurerkennung_Dokumentation.ipynb`

Diese Schritte beziehen sich auf das Jupyter Notebook `Projekt_Spurerkennung_Dokumentation.ipynb`.
In diesem Notebook sind alle Schritte der Spurerkennung dokumentiert.
Darunter befinden sich auch die Schritte, die nicht in der Pipeline verwendet werden.
Die Schritte wurde jedoch nicht aus dem Notebook entfernt,
um die Entwicklung der Pipeline nachvollziehen zu können.

Teile des Notebooks sind in den Python Programmen übernommen und leicht abgeändert worden.
Die Kalibrierung der Kamera wird nur in dem Notebook durchgeführt,
da die Kamerakalibrierung nur einmal durchgeführt werden muss.
Die Parameter der Kamerakalibrierung werden in der Datei `calibration_parameters.npz` gespeichert
und in den Python Programmen importiert.
Das Notebook muss somit zuerst ausgeführt werden, dass die Datei `calibration_parameters.npz` erstellt wird
und die Python Programme die Parameter importieren können.

### 1. Schritt: Kalibrierung der Kamera

Kalibrierung der Kamera und entzerren der Udacity-Testbilder.
Es werden sowohl die Schachbrettbilder als auch die Udacity-Testbilder entzerrt und beispielhaft angezeigt.
Vor dem Anzeigen werden die Bilder zugeschnitten, sodass der schwarze Rand entfernt wird.
Die entzerrten Bilder werden in dem Array `undistorted_images` gespeichert.

### 2. Schritt: Zuschneiden der Bilder

Die zugeschnittenen Bilder werden in dem Array `cropped_images` gespeichert.
Es werden nur die für die Spurerkennung relevanten Bildbereiche ausgeschnitten.

### 3. Schritt: Perspektivtransformation

Die Bilder werden perspektivisch transformiert, sodass die Spurmarkierungen
von oben betrachtet werden können.
Die Bilder werden in dem Array `warpped_images` gespeichert.

### 4. Schritt: Farbfilter

Es werden die Farbfilter für die Farben weiß und gelb definiert,
sodass die Spurmarkierungen in den Bildern hervorgehoben werden.
Die Bilder werden in dem Array `filtered_images` gespeichert.

### 5. Schritt: Thresholding

Auf die gefilterten Bilder wird ein Thresholding angewendet,
um die Spurmarkierungen besser hervorzuheben.
Die Bilder werden in dem Array `thresh_images` gespeichert.

### 6. Schritt: Curve fitting

Es wird eine Kurve durch die Spurmarkierungen gelegt und der Radius der Kurve berechnet.
Die Bilder werden in dem Array `curve_images` gespeichert.

### 7. Schritt: Unwarping

Mithilfe der Funktion, die im Schritt "Curve Fitting" erstellt wurde,
werden x und y Werte für die Kurve berechnet. Diese werden auf eine Maske gezeichnet.
Da die Kurve in dem Bild perspektivisch transformiert wurde,
muss die Kurve wieder in das Originalbild transformiert werden.
Die Maske mit den Kurven wird somit wieder zurück transformiert
und über das Originalbild gelegt.
Dabei wird die Maske an den richtigen Koordinaten über das Originalbild gelegt.

### Radiusberechnung

Der Radius wurde direkt im Programm `lane_detection.py` für das Video `project_video.mp4`
implementiert.

### Optimierung des Codes
In dem Projekt wird als Beschleunigungsmethode des Programms das Filtern nach Farben der Fahrspur (gelb und weiß), Thresholding und Curve Fitting in einem separaten Thread durchgeführt. Dadurch können die gelben und weißen Bereiche in den Bildern parallel gefiltert werden. Dadurch wird die Verarbeitungsgeschwindigkeit erhöht. 
Die Optimierung wurde direkt in den Python Programmen `lane_detection.py` und `lane_detection_challenge.py` sowie dem Jupyter-Notebook `lane_detection_kitty.ipynb`umgesetzt.

Als Beispiel ein Codeausschnitt aus `LaneDetectionChallange.start()`. Hierbei wird der Farbfilter für die linke und rechte Fahrspur in seperaten Threads angewandt, um die Ausführungsgeschwindigeit zu erhöhen.
````python
left_frame = transformed_frame[:, :(transformed_y_half - 250)]
right_frame = transformed_frame[:, (transformed_y_half + 250):]

with concurrent.futures.ThreadPoolExecutor() as executor:
    # Farbfilter
    left_future = executor.submit(self.filter_color_range, left_frame, *yellow_range)
    right_future = executor.submit(self.filter_color_range, right_frame, *white_range)

    left_filtered_frame = left_future.result()
    right_filtered_frame = right_future.result()
````
Farbfilter, Thresholding und Curve Fitting werden in seperaten Threads für die jeweilige Fahrspur angewandt. Dadurch können die linken und rechten Fahrspuren parallel erkannt und das Polynom berechnet werden. Nachdem die Fahrspuren gefunden wurden werden die Threads wieder zusammengefügt und die Fahrspuren werden auf das entzerrte Bild gezeichnet.  

Laut Callgraph ist die Zeitverteilung vor der Parallelisierung wie folgt:
- 1,3% für Farbfilter
- 0,6% für Thresholdiung
- 18,3% für Curve Fitting

Durch die Parallelisierung des Linken und Rechten Fahrstreifens können somit ~ 20% der Zeit parallelisiert bearbeitet werden. 
Ein Großteil der Rechenleistung nimmt das Entzerren der Bilder mit 56,3% der Zeit in anspruch. Dieser Teil kann leider nicht optimiert werden, weil eine Entzerrung der Kamerabilder obligatorisch ist.

## Python Programm für `project_video.mp4`: `lane_detection.py`

**Hinweis:** D2. Das Jupyter Notebook `Projekt_Spurerkennung_Dokumentation.ipynb` muss zuerst ausgeführt werden, damit
die Datei `calibration_parameters.npz` erstellt wird und die Python Programme die Parameter importieren können.

![](C:\Users\Timo\PycharmProjects\DigitaleBildverarbeitungUebungen\Projekt\Projekt_Spurerkennung_v8\resources\project_video.png)
Die Fahrspurmarkierungen werden in Rot auf dem entzerrten Bild gezeichnet.
Die aktuellen FPS werden oben links in grüner Schrift angezeigt.
Die durchschnittlichen FPS werden oben rechts in schwarzer Schrift angezeigt.
Der aktuelle Kurvenradius in Meter wird in grüner Schrift unten links angezeigt.

In diesem Programm werden die selben Schritte wie im Jupyter Notebook `Projekt_Spurerkennung_Dokumentation.ipynb`
durchgeführt.
Die Reihenvolge kann in dem Codeabschnitt aus der Funktion `LaneDetection.start()` nachvollzogen werden:

```python
frame = self.undistorted_frame(frame)
cropped_frame = self.crop_image(frame)
transformed_frame = self.transform_perspective(cropped_frame)
filtered_frame = self.filter_frame(transformed_frame)
thresholded_frame = self.threshold_frame(filtered_frame)
curve_fitted_frame, radius = self.fit_curve(thresholded_frame, frame)
```

In dem Projekt wird als Beschleunigungsmethode de Programms
das Filtern nach Farben der Fahrspur (gelb und weiß) in einem
separaten Thread durchgeführt (siehe `LaneDetection.filter_frame()`).
Dadurch können die gelben und weißen Bereiche in den Bildern parallel gefiltert werden.
Die Verarbeitungsgeschwindigkeit wird erhöht.

In der Funktion `LaneDetection.fit_curve()` wird die Kurve durch die Spurmarkierungen gelegt.
Gleichzeitig werden die Fahrspurmarkierungen direkt auf das Originalbild gezeichnet.

### Radiusberechnung der Kurve
Die linke und rechte Fahrspur werden als zweidimensionales Polynom mithilfe von `np.polyfit()`
abgebildet. 
Bevor der Kurvenradius berechnet werden kann, muss eine Umrechnung in das Fahrzeugkoordinatensystem
vorgenommen werden. Dafür werden die Werte aus der Vorlesung übernommen:
````python
# Ausschnitt aus LaneDetection.fit_curve()

# Umrechnung in Fahrzeugkoordinatensystem:
# Meter pro Pixel in x (x_m_per_pix): 30 / 720
# Meter pro Pixel in y (y_m_per_pix): 3.7 / 700
# Use x=0 because the car is at x=0
radius = self.calc_curve_radius(np.polyfit(left_x * 30/720, left_y * 3.7 / 700, 2), 0)
````
Um den Kurvenradius zu berechen werden die Berechnungen aus der Vorlesung angewandt.
Dafür werden die ersten beiden Ableitungen der Funktion berechnet, 
um anschließend den Kurvenradius mit der Formel zu berechnen:
````python
# Ausschnitt aus LaneDetection.calc_curve_radius()
res = ((1 + (f_x_derivative(x) ** 2)) ** 1.5) / np.abs(f_x_second_derivative(x))
````

***

# Zusatzleistungen

1. **challenge_video.mp4**:
   In dem Programm `lane_detection_challenge.py` wird das Video `challenge_video.mp4` verarbeitet
   und die Fahrspurmarkierungen werden in Rot auf dem entzerrten Bild gezeichnet.
   In dem Abscnitt "Python Programm für `challenge_video.mp4`: `lane_detection_challenge.py`" wird das Programm genauer
   beschrieben.
   Dabei werden auch die Änderungen zu dem Programm `lane_detection.py` beschrieben, die vorgenommen
   wurden, um das Video `challenge_video.mp4` zu verarbeiten.
2. **?:**
3. **?:**

## 1. Python Programm für `challenge_video.mp4`: `lane_detection_challenge.py`

Das Python Programm `lane_detection_challenge.py` ist eine Erweiterung des Python Programms `lane_detection.py`.
Um die Fahrspurmarkierungen richtig zu erkennen mussten folgende Änderungen vorgenommen werden:

- Image cropping verkleinert, sodass nur die Fahrspur zu sehen ist
- Thresholding angepasst, sodass die gelben Fahrspuren richtig erkannt werden
- ROI für linke und rechte Fahrspurmarkierung angepasst.

In diesem Video werden Fahrspur auf der linken und der rechten Seite in
seperaten Threads gefiltert.
Dadurch kann die Farbfilterung, Thresholding und Curve Fitting
für die linke und rechte Fahrspur parallel durchgeführt werden.
In dem Video sind zwischen den Fahrspuren teilweise weiße Rauten zu sehen.
Diese würde die Fahrspurmarkierungen stören:
Wenn auf den Frames, auf die Curve-Fitting angewandt wird Störgeräusche vorhanden sind,
wird die Kurve durch die Störgeräusche sehr stark beeinflusst.
Deshalb darf auf den Frames, auf die Curve-Fitting angewandt wird, nur die Fahrspurmarkierung zu sehen sein.
Um dieses Problem zu beheben, wurde die ROI für die linke und rechte Fahrspurmarkierung angepasst.
Die linke Fahrspurmarkierung wird nur noch auf der linken Seite des Bildes gesucht.
Die rechte Fahrspurmarkierung wird nur noch auf der rechten Seite des Bildes gesucht.
Der Bereich zwischen den Fahrspuren wird nicht mehr untersucht.

### Probleme bei der Umsetztung von `challenge_video.mp4`

![](C:\Users\Timo\PycharmProjects\DigitaleBildverarbeitungUebungen\Projekt\Projekt_Spurerkennung_v8\resources\challenge_video_frame_140.jpg)
Unter der Brücke (Frame 134:150; beispielhaft wurde Frame 140 ausgewählt)
können die Fahrspurmarkierungen nicht richtig erkannt werden.
Der Kontrast der Fahrspurmarkierungen ist zu gering, um durch Farbfilterung und Thresholding erkannt zu werden.
Auf der linken Seite des Bildes ist die Fahrspurmarkierung in einem sehr dunkeln
gelb zu sehen. Auf der rechten Seite des Bildes ist die Fahrspurmarkierung in einem
sehr dunklen weiß zu sehen. Durch die geringe Sättigung der Farben werden die Fahrbahnmarkierungen
durch `cv2.inRange()` nicht erkannt. Da keine Fahrspurmarkierungen erkannt werden,
kann auch keine Kurve durch die Fahrspurmarkierungen gelegt werden.
Die Fahrspurmarkierungen werden erst wieder erkannt, wenn die Fahrspurmarkierungen wieder deutlicher zu sehen sind.
In den Frames, in den keine Fahrspurmarkierungen erkannt werden, wird die Kurve aus dem vorherigen Frame übernommen.

## 2. KITTY-Datensatz
Das Jupyter Notebook "lane_detection_kitty.ipynb" führt ebenfalls Lane Detection durch. Allerdings mussten ein paar 
Schritte angepasst werden, die beim KITTI Datensatz anders sind als beim Udacity Datensatz. Die einzelnen Änderungen
sind auch nochmal im Notebook-Markdown beschrieben. Die Hauptänderungen:
- Cropped Frame anpassen
- Perspektivtransformation anpassen
- Größem von left/right frame anpassen
- Farbfilter anpassen (gelb -> weiß)
- Zusätzliche Funktionen für die Lane Detection: Vertikale Kantenerkennung implementieren
- Thresholding anpassen
- Fitting der einzelnen Frames (left/right lane) in undistorted image angepasst, da unterschiedlich zugeschnitten wurde
- Error Handling für nicht erkannte Lane: Es wurde eine Funktion für das Erkennen von Bordsteinkanten mithilfe des Sobel-Filters implementiert.
