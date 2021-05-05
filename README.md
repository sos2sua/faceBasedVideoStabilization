# Face Based Video Stabilization

To Exit the code press 'q' (this will ensure the video is saved gracefull if recording is used)

If Using tracking:
1. Press any key to skip
2. Press 's' key to select

The following parameters allows you to customize
1. Output Video size (STABILIZED_WINDOW_HEIGHT_HALF, STABILIZED_WINDOW_WIDTH_HALF)
2. SAVE_OUTPUT_VIDEO = True, will save the output video as pointed by OUTPUT_VIDEO_FILE
3. OUTPUT_VIDEO_FPS sets the frame rate for the video to be recored if SAVE_OUTPUT_VIDEO = True
4. VIDEO_SRC_IS_CAM = True uses available camera as input(Note: OUTPUT_VIDEO_FPS is set to 15fps), if false will read take the input video file set by INPUT_VIDEO_FILE
5. USE_TRACKING_AFTER_INITIAL_FACE_DETECTION = True, Adds Tracking of face using opencv trackers to:
- Resolve the issue of multiple face detection causing flickering
- Tracking performs as a better anchor than Face detection

Checkout the example output:
https://youtu.be/iQT9xuDh_ek
https://youtu.be/lau9HY31Nhc
