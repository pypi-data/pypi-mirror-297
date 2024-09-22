import matplotlib.pyplot as plt
import numpy as np

image = np.zeros((100, 100, 3)).astype(np.uint8) + 64
image2 = np.zeros((100, 100, 3)).astype(np.uint8)
image2[:, :, 0] = 255

fig, ax = plt.subplots(1, 1)
ax_img = ax.imshow(image2)
plt.pause(0.001)
plt.show(block=False)
plt.pause(0.001)
print("HELLO")
import time

time.sleep(10)

plt.pause(0.001)
# ax_img.set_data(image)
# print("HELLO2")
