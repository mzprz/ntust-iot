import cv2
vidcap = cv2.VideoCapture('input_video_3/demonstrasi_3.mp4')
success,image = vidcap.read()
count = 0
while success:
  cv2.imwrite("input_jpg_3/frame_%d.jpg" % count, image)     # save frame as JPEG file      
  success,image = vidcap.read()
  print('Read a new frame_{}: {}'.format(count, success))
  count += 1