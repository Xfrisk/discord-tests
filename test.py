from PIL import Image
import numpy as np

img = Image.open("bg_0.png").convert("RGBA")
data = np.array(img)

# Pega pixels transparentes (alpha < 50)
transparent = np.where(data[:,:,3] < 50)

if len(transparent[0]) > 0:
    ys, xs = transparent
    mid_x = (xs.min() + xs.max()) // 2
    mid_y = (ys.min() + ys.max()) // 2
    print(f"Área transparente: X {xs.min()}~{xs.max()}, Y {ys.min()}~{ys.max()}")
    print(f"Centro: ({mid_x}, {mid_y})")
    print(f"Tamanho: {xs.max()-xs.min()}x{ys.max()-ys.min()}")