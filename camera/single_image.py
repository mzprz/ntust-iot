import time
import cv2

from tensorflow.keras import Input, Model
from tensorflow.keras.utils import plot_model as plot

from darknet import darknet_base
from predict import predict, predict_with_yolo_head

inputs = Input(shape=(None, None, 3))
outputs, config = darknet_base(inputs, include_yolo_head=False)

model = Model(inputs, outputs)
model.summary()

plot(model, to_file='utils/model.png', show_shapes=True)
start_count = 2
end_count = 4
for count_file in range(start_count, end_count+1):
	file_name = 'frame_{}.png'.format(count_file)
	orig = cv2.imread('./input_jpg_4/' + file_name)

	# Using the YOLO head means that we do *not* use the custom YOLOLayer, and instead
	# just use Darknet, and then process the resulting predictions with `yolo_head`.
	USE_YOLO_HEAD = True

	start = time.time()
	if USE_YOLO_HEAD:
	    predict_with_yolo_head(model, orig, config, confidence=0.3, iou_threshold=0.4, file_name=file_name)
	else:
	    predict(model, orig, config, confidence=0.5, iou_threshold=0.4)

	end = time.time()

	print("Inference time: {:.2f}s".format(end - start))
