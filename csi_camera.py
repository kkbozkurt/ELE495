from jetcam.csi_camera import CSICamera

camera = CSICamera(width=224, height=224, capture_device=0) # confirm the capture_device number

image = camera.read()

print(image.shape)

print(camera.value.shape)

import ipywidgets
from IPython.display import display
from jetcam.utils import bgr8_to_jpeg

image_widget = ipywidgets.Image(format='jpeg')

image_widget.value = bgr8_to_jpeg(image)

display(image_widget)

camera.running = False
camera.cap.release()