# Digitale Bildverarbeitung - Spurerkennung 

## Zusatzleistungen
1. **challenge_video.mp4**:
In dem Programm `lane_detection_challenge.py` wird das Video `challenge_video.mp4` verarbeitet
und die Fahrspurmarkierungen werden in Rot auf dem entzerrten Bild gezeichnet.
In dem Abscnitt "Python Programm für `challenge_video.mp4`: `lane_detection_challenge.py`" wird das Programm genauer beschrieben.
Dabei werden auch die Änderungen zu dem Programm `lane_detection.py` beschrieben, die vorgenommen
wurden, um das Video `challenge_video.mp4` zu verarbeiten.
2. **?:**
3. **?:**

## Jupyter Notebook "Projekt_Spurerkennung_Dokumentation"
Diese Schritte beziehen sich auf das Jupyter Notebook "Projekt_Spurerkennung_Dokumentation".
In diesem Notebook sind alle Schritte der Spurerkennung dokumentiert. 
Darunter befinden sich auch die Schritte, die nicht in der Pipeline verwendet werden.
Die Schritte wurde jedoch nicht aus dem Notebook entfernt, 
um die Entwicklung der Pipeline nachvollziehen zu können.


Teile des Notebooks sind in den Python Programmen übernommen und leicht abgeändert worden.
Die Kalibrierung der Kamera wird nur in dem Notebook durchgeführt, 
da die Kamerakalibrierung nur einmal durchgeführt werden muss.
Die Parameter der Kamerakalibrierung werden in der Datei `calibration_parameters.py` gespeichert
und in den Python Programmen importiert.
Das Notebook muss somit zuerst ausgeführt werden, dass die Datei `calibration_parameters.py` erstellt wird
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


## Python Programm für `project_video.mp4`: `lane_detection.py`
**Hinweis:** Das Jupyter Notebook "Projekt_Spurerkennung_Dokumentation" muss zuerst ausgeführt werden,
damit die Datei `calibration_parameters.py` erstellt wird und die Python Programme die Parameter importieren können.

Die Fahrspurmarkierungen werden in Rot auf dem entzerrten Bild gezeichnet.
Die aktuellen FPS werden oben links in grüner Schrift angezeigt.
Die durchschnittlichen FPS werden oben rechts in schwarzer Schrift angezeigt.

In diesem Programm werden die selben Schritte wie im Jupyter Notebook "Projekt_Spurerkennung_Dokumentation" durchgeführt.
Die Reihenvolge kann in dem Codeabschnitt aus der Funktion `LaneDetection.start()` nachvollzogen werden:
```python
frame = self.undistorted_frame(frame)
cropped_frame = self.crop_image(frame)
transformed_frame = self.transform_perspective(cropped_frame)
filtered_frame = self.filter_frame(transformed_frame)
thresholded_frame = self.threshold_frame(filtered_frame)
curve_fitted_frame = self.fit_curve(thresholded_frame, frame)
```
In dem Projekt wird als Beschleunigungsmethode de Programms 
das Filtern nach Farben der Fahrspur (gelb und weiß) in einem 
separaten Thread durchgeführt (siehe `LaneDetection.filter_frame()`).
Dadurch können die gelben und weißen Bereiche in den Bildern parallel gefiltert werden.
Die Verarbeitungsgeschwindigkeit wird erhöht.

In der Funktion `LaneDetection.fit_curve()` wird die Kurve durch die Spurmarkierungen gelegt.
Gleichzeitig werden die Fahrspurmarkierungen direkt auf dem Originalbild gezeichnet.

## Python Programm für `challenge_video.mp4`: `lane_detection_challenge.py`
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
![challenge_video_frame_140.jpg](img%2FUdacity%2Fchallenge_video_frame_140.jpg)
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



## Python Programm für `harder_challenge_video.mp4`
ToDo: Was mussten wir anpassen?