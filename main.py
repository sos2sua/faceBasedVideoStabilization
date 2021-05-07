import cv2
import numpy as np

USE_TRACKING_AFTER_INITIAL_FACE_DETECTION = True
STABILIZED_WINDOW_HEIGHT_HALF = int(720 / 2)
STABILIZED_WINDOW_WIDTH_HALF = int(1800 / 2)
HEIGHT_OFFSET_FOR_STABILIZED_WINDOW = 2000
WIDTH_OFFSET_FOR_STABILIZED_WINDOW = 0
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

x, y, w, h = [0, 0, 0, 0]
newy_max = newx_max = 0
newy = newx = 0
gotFace = False
writer = 0
roi = 0

if USE_TRACKING_AFTER_INITIAL_FACE_DETECTION:
    tracker = cv2.TrackerKCF_create()
    # tracker = cv2.TrackerMIL_create()

while cv2.waitKey(1) < 113:
    (grabbed, frame) = cap.read()
    if not grabbed:
        if SAVE_OUTPUT_VIDEO:
            writer.release()
            cap.release()
        exit()
    if USE_TRACKING_AFTER_INITIAL_FACE_DETECTION and gotFace == 1:
        ok, box = tracker.update(frame)
        if ok:
            faces = [box]
        else:
            faces = []
    else:
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
                                 (STABILIZED_WINDOW_WIDTH_HALF*2+WIDTH_OFFSET_FOR_STABILIZED_WINDOW, STABILIZED_WINDOW_HEIGHT_HALF*2+HEIGHT_OFFSET_FOR_STABILIZED_WINDOW))

    if len(faces) > 0:
        if USE_TRACKING_AFTER_INITIAL_FACE_DETECTION and not gotFace:
            selected = False
            for face in faces:
                fx, fy, fw, fh = face
                fw += 140+fx
                fh += 140+fy
                fx -= 140
                fy -= 140
                if fx < 0 or fy < 0:
                    continue

                foundFace = frame[fy:fh, fx:fw]
                cv2.imshow('Found Face', foundFace)
                print("Press 's' to select and any other key to proceed.")
                key = cv2.waitKey(0)
                if key == 115:
                    selected = True
                    face = np.array([fx, fy, fw - fx, fh - fy])
                    tracker.init(frame, face)
                    break

            if not selected:
                continue

        gotFace = True
        x1, y1, w, h = faces[0]
        x = int(x1 + w / 2)
        y = int(y1 + h / 2)
        newy_max = frameHeight
        newx_max = frameWidth
        newy = 0
        newx = 0

        if (y-STABILIZED_WINDOW_HEIGHT_HALF) > 0:
            newy = y - STABILIZED_WINDOW_HEIGHT_HALF

        if (y+STABILIZED_WINDOW_HEIGHT_HALF) < frameHeight:
            newy_max= y + STABILIZED_WINDOW_HEIGHT_HALF

        if (x - STABILIZED_WINDOW_WIDTH_HALF) > 0:
            newx = x - STABILIZED_WINDOW_WIDTH_HALF

        if (x + STABILIZED_WINDOW_WIDTH_HALF) < frameWidth:
            newx_max = x + STABILIZED_WINDOW_WIDTH_HALF

    if gotFace:
        roi = frame[newy:newy_max+HEIGHT_OFFSET_FOR_STABILIZED_WINDOW, newx:newx_max+WIDTH_OFFSET_FOR_STABILIZED_WINDOW]
        cv2.imshow('output', roi)
        if SAVE_OUTPUT_VIDEO:
            roi = cv2.resize(roi,(STABILIZED_WINDOW_WIDTH_HALF*2+WIDTH_OFFSET_FOR_STABILIZED_WINDOW,
                                  STABILIZED_WINDOW_HEIGHT_HALF*2+HEIGHT_OFFSET_FOR_STABILIZED_WINDOW))
            writer.write(roi)

writer.release()
cap.release()
