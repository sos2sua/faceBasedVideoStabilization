import cv2

STABILIZED_WINDOW_HEIGHT_HALF = int(480 / 2)
STABILIZED_WINDOW_WIDTH_HALF = int(720 / 2)
SAVE_OUTPUT_VIDEO = True
OUTPUT_VIDEO_FPS = 30
VIDEO_SRC_IS_CAM = True
INPUT_VIDEO_FILE = 'input/test.mp4'
OUTPUT_VIDEO_FILE = 'output/output.avi'

face_cascade = cv2.CascadeClassifier('model/haarcascade_frontalface_default.xml')

if VIDEO_SRC_IS_CAM :
    cap = cv2.VideoCapture(0)
    OUTPUT_VIDEO_FPS = 15
else:
    cap = cv2.VideoCapture(INPUT_VIDEO_FILE)

x, y, w, h = [0,0,0,0]
newy_max = newx_max = 0
newy = newx = 0
got_face = 0
writer = 0
roi = 0
while cv2.waitKey(1) < 1:
    (grabbed, frame) = cap.read()
    if not grabbed:
        if SAVE_OUTPUT_VIDEO:
            writer.release()
            cap.release()
        exit()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=3,
        minSize=(130, 130)
    )

    frameHeight, frameWidth, _ = frame.shape

    if SAVE_OUTPUT_VIDEO and writer == 0:
        writer = cv2.VideoWriter(OUTPUT_VIDEO_FILE, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), OUTPUT_VIDEO_FPS,
                                 (STABILIZED_WINDOW_WIDTH_HALF*2, STABILIZED_WINDOW_HEIGHT_HALF*2))

    if len(faces) > 0:
        got_face = 1
        x1, y1, w, h = faces[0]
        x = int(x1 + w / 2)
        y = int(y1 + h / 2)
        newy_max = frameHeight
        newx_max = frameWidth
        newy = 0
        newx = 0

        if (y-STABILIZED_WINDOW_HEIGHT_HALF) > 0:
            newy = y - STABILIZED_WINDOW_HEIGHT_HALF

        if (y+STABILIZED_WINDOW_HEIGHT_HALF)<frameHeight:
            newy_max= y + STABILIZED_WINDOW_HEIGHT_HALF

        if (x - STABILIZED_WINDOW_WIDTH_HALF) > 0:
            newx = x - STABILIZED_WINDOW_WIDTH_HALF

        if (x + STABILIZED_WINDOW_WIDTH_HALF) < frameWidth:
            newx_max = x + STABILIZED_WINDOW_WIDTH_HALF

    if got_face == 1:
        roi = frame[newy:newy_max, newx:newx_max]
        cv2.imshow('output', roi)
        if SAVE_OUTPUT_VIDEO:
            roi = cv2.resize(roi,(STABILIZED_WINDOW_WIDTH_HALF*2, STABILIZED_WINDOW_HEIGHT_HALF*2))
            writer.write(roi)
writer.release()
cap.release()
