import cv2
import numpy as np

# Lade ein Bild im Grayscale-Modus
img = cv2.imread("./img/Udacity/image001.jpg", cv2.IMREAD_GRAYSCALE)

# Wende Thresholding an (angepasst an deine Bedürfnisse)
_, thresh = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY)

# Konvertiere das Bild zu einem 4-Kanal-Bild (RGBA) mit Transparenz
img_rgba = cv2.cvtColor(img, cv2.COLOR_GRAY2RGBA)

# Setze den Alpha-Kanal basierend auf dem Thresholding
img_rgba[:, :, 3] = thresh

# Zeige das resultierende Bild an
cv2.imshow("Image with Transparency", img_rgba)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Speichere das Bild mit Transparenz
cv2.imwrite("dein_bild_mit_transparenz.png", img_rgba)
