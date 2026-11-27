import cv2

for index in range(5):
    camera = cv2.VideoCapture(index, cv2.CAP_DSHOW)

    if camera.isOpened():
        ret, frame = camera.read()

        if ret:
            print(f"Camera index {index} is working")
            cv2.imshow(f"Camera {index}", frame)
            cv2.waitKey(3000)
            cv2.destroyAllWindows()

        camera.release()