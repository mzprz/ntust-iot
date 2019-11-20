import cv2
import numpy as np

height,width,layers= cv2.imread('./output_jpg_3/frame_{}'.format(0)+'.jpg').shape

fourcc = cv2.VideoWriter_fourcc(*'MP4V')
video=cv2.VideoWriter('./demonstrasi_3.mp4',fourcc,60.0,(width,height))

for i in range(0, 651):
	print(i)
	video.write(cv2.imread('./output_jpg_3/frame_{}'.format(i)+'.jpg'))

cv2.destroyAllWindows()
video.release()