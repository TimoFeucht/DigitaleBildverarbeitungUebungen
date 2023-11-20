import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt

# Lade das Bild
image = cv.imread('./img/Udacity/image001.jpg')
image = cv.cvtColor(image, cv.COLOR_BGR2RGB)  # Farbkanäle korrigieren

# Konvertiere das Bild in Graustufen
gray = cv.cvtColor(image, cv.COLOR_RGB2GRAY)

# Reduziere das Rauschen mit einem Gaußschen Weichzeichner
blur = cv.GaussianBlur(gray, (5, 5), 0)

# Wende den Canny-Kantendetektor an
edges = cv.Canny(blur, 50, 150)

# Definiere die Hough-Transformation-Parameter
rho = 1
theta = np.pi / 180
threshold = 100
min_line_length = 50
max_line_gap = 5

# Hough-Transformation durchführen, um Linien zu erkennen
lines = cv.HoughLinesP(edges, rho, theta, threshold, np.array([]),
                        minLineLength=min_line_length, maxLineGap=max_line_gap)

# Zeichne die erkannten Linien auf das Originalbild
line_image = np.copy(image)
for line in lines:
    for x1, y1, x2, y2 in line:
        cv.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5)

# Kombiniere das Originalbild mit den erkannten Linien
result = cv.addWeighted(image, 0.8, line_image, 1, 0)

# Zeige die Ergebnisse
plt.figure(figsize=(10, 5))

plt.subplot(131)
plt.imshow(image)
plt.title('Originalbild')

plt.subplot(132)
plt.imshow(edges, cmap='gray')
plt.title('Kantenerkennung')

plt.subplot(133)
plt.imshow(result)
plt.title('Spurmarkierungen hervorgehoben')

plt.show()
