# DigitaleBildverarbeitungUebungen

## Projektübersicht: Spurerkennung
### Mindestanforderungen (entspricht der Note 2,0)
- Segmentierung des Bildes: schränken Sie das Bild auf den Bereich ein, in dem sich die Spurmarkierungen befinden
- Vorverarbeitung: Führen Sie eine Kamerakalibrierung (für Udacity-Bildquellen) und die Perspektivtransformation durch
- Farbräume, Histogramme: erkennen Sie die Spurmarkierungen in den Farben der angegebenen Quellen. Falls weitere Spurmarkierungen auf dem Bild gefunden werden, müssen die der eigenen Fahrspur priorisiert werden
- Allgemeines: Die Verarbeitung von Bildern muss in Echtzeit stattfinden --> Ziel: > 20 FPS für reine Verarbeitung ohne Anzeige) Prozessor, Grafikkarte, Arbeitsspeicher
- Allgemeines: Beschleunigen Sie die Verarbeitung durch weitere Maßnahmen (bspw. Erkennung der Spurmarkierung in den ersten Frames, Tracking der Spurmarkierung in weiteren Frames solange, bis sich Spurmarkierungspositionen zu stark ändern) mind. eine Maßnahme im Projekt verwenden
- Curve / Polynom Fitting: Erkennen Sie die Krümmung der Fahrspur und geben Sie diese im Ausgabebild aus
- Validierung des Verfahrens: Umrechnung auf Straßenkrümmung, sodass Simulation erfolgreich bestanden wird
- Allgemeines: relevante Spurmarkierungen werden in den Udacity-Bildern und im Video „project_video“ durchgehend erkannt

### Zusatzaufgaben (jeweils – 0,33; Mindestanforderungen + 3x Zusatzaufgaben = 1,0)
- relevante Spurmarkierungen werden im Video "challenge_video" oder "harder_challenge_video" (nahezu) durchgehend erkannt (sowohl „challenge_video“ als auch „harder_challenge_video“ werden als Zusatzaufgabe gewertet)
- relevante Spurmarkierungen werden auf den Datensatz KITTI angewendet. Welche Anpassungen müssen vorgenommen werden, damit Ihr Algorithmus übertragen werden kann?
- erkennen Sie Objekte im Bild und visualisieren Sie diese (z.B. weitere Fahrzeuge, Motorräder, etc.) Die Objekterkennung bitte so implementieren, dass sie deaktivierbar ist und nicht in FPS-Berechnung einzahlt.
- nutzen Sie alternative Möglichkeiten der Spurerkennung (z.B. mit Neuronalen Netzen)
- ergänzen Sie Ihren Algorithmus um eine Kennzeichenerkennung inkl. Texterkennung
- Gerne können Sie eigene Zusatzaufgaben zur Verbesserung Ihres Algorithmus einführen. (Aufwand sollte vergleichbar sein zu o.g. Punkten).
- Alle durchgeführten Aufgaben müssen dokumentiert, kommentiert und abgegeben werden.


### Zusatzaufgabe Android (- 0,7; Mindestanforderungen + 1x Zusatzaufgaben + Android-Portierung = 1,0)
- entwickelter Algorithmus wurde auf Android übertragen
- Dokumentation der erkannten Fahrspuren
- Diskussion über die Herausforderungen bei der Portierung der Python-Umsetzung mit der Java-Umsetzung
- Alle durchgeführten Aufgaben müssen dokumentiert, kommentiert und abgegeben werden.
