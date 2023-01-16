import cv2
from image_check import * 
import threading

# Initialize the video capture
cap = cv2.VideoCapture(0)

while True:

    ret, frame = cap.read()
    # Draw rectangle in the middle of the frame
    cv2.rectangle(frame, (frame.shape[1]//2-150, frame.shape[0]//2-150), (frame.shape[1]//2+150, frame.shape[0]//2+150), (0, 255, 0), 2)
    
    # take the rectangle line not included.
    x, y, w, h = frame.shape[1]//2-148, frame.shape[0]//2-148, frame.shape[1]//2+148, frame.shape[0]//2+148
    cropped_frame = frame[y:h, x:w]
    # Display the frame
    cv2.imshow("QR Scanner", cropped_frame)

    # Check if the 's' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('s'):
        # Save the screenshot
        #cv2.imwrite("Snap/Snap.png", cropped_frame)
        #print("Screenshot saved!")
        t1 = threading.Thread(target=run, args = (cropped_frame, ))
        t1.start()
        t1.join()

    # Check if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        # Release the video capture and close the window
        cap.release()
        cv2.destroyAllWindows()
        break

