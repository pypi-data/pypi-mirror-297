import numpy as np
from live_plotter import LiveImagePlotter, scale_image

N = 25
DEFAULT_IMAGE_HEIGHT = 100
DEFAULT_IMAGE_WIDTH = 100

live_plotter = LiveImagePlotter(default_titles="sin")

x_data = []
for i in range(N):
    x_data.append(0.5 * i)
    image_data = (
        np.sin(x_data)[None, ...]
        .repeat(DEFAULT_IMAGE_HEIGHT, 0)
        .repeat(DEFAULT_IMAGE_WIDTH // N, 1)
    )
    live_plotter.plot(image_data=scale_image(image_data, min_val=-1.0, max_val=1.0))
