import time
import cv2
import matplotlib.pyplot as plt

stream = cv2.VideoCapture(1)
def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
       print("x = {}, y = {}".format(x, y))


while True:
    # Capture frame-by-frame
    grabbed, frame = stream.read()
    if not grabbed:
        break
    
    cv2.setMouseCallback('', onMouse)

    # Display the resulting frame
    cv2.imshow('', frame)
    # plt.imshow(frame)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

# When everything done, release the capture
stream.release()
cv2.destroyAllWindows()
