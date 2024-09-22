import matplotlib.pyplot as plt
import numpy as np
import time

# Creating two images: one grey, one red
image_grey = np.zeros((100, 100, 3), dtype=np.uint8) + 64
image_red = np.zeros((100, 100, 3), dtype=np.uint8)
image_red[:, :, 0] = 255

# Setting up the Matplotlib figure and axes
fig, ax = plt.subplots()
ax_img = ax.imshow(image_grey)
plt.show(block=False)

# Alternating between grey and red images
for _ in range(5):  # Repeat the alternation 5 times
    ax_img.set_data(image_red)
    fig.canvas.draw()
    plt.pause(1)  # Pause for 1 second
    ax_img.set_data(image_grey)
    fig.canvas.draw()
    plt.pause(1)  # Pause for 1 second
