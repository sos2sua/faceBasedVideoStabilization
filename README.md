# faceBasedVideoStabilization

The following parameters allows you to customize
1. Output Video size (STABILIZED_WINDOW_HEIGHT_HALF, STABILIZED_WINDOW_WIDTH_HALF)
2. SAVE_OUTPUT_VIDEO = True, will save the output video as pointed by OUTPUT_VIDEO_FILE
3. OUTPUT_VIDEO_FPS sets the frame rate for the video to be recored if SAVE_OUTPUT_VIDEO = True
4. VIDEO_SRC_IS_CAM = True uses available camera as input(Note: OUTPUT_VIDEO_FPS is set to 15fps), if false will read take the input video file set by INPUT_VIDEO_FILE