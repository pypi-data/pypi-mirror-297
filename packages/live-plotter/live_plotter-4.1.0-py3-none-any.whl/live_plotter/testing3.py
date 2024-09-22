import matplotlib.pyplot as plt
import numpy as np

image = np.zeros((100, 100, 3)).astype(np.uint8) + 128
plt.imshow(image)
plt.show()
