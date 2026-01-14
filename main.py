import cv2
import matplotlib.pyplot as plt
import upperlimbs
import time


def run_demo():
    # 1. Initialize your UpperLimbs class
    ul = upperlimbs.UpperLimbs()

    # You can change this to 0 for a webcam or keep the path to a video file.
    video_source = 0  # '/path/to/your/video.mp4'
    cap = cv2.VideoCapture(video_source, cv2.CAP_AVFOUNDATION)
    if not cap.isOpened():
        print(f"Error: Could not open video source: {video_source}")
        return
    print("Warming up camera...")
    for _ in range(20):
        if cap.isOpened():
            success, _ = cap.read()
            if success:
                print("Camera ready!")
                break
        time.sleep(0.1)
    # --- END OF FIX ---

    visualize_mode = True
    print("Starting demo. Press 'v' to turn on/off 3D plot, 'q' to quit.")

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("End of video or empty frame.")
            break

        # 2. Process the frame to get coordinates
        coords = ul.process_frame(image)

        # 3. Draw the 2D landmarks on the image for the preview window
        annotated_image = ul.draw_landmarks(image.copy())
        cv2.imshow('UpperLimbs Preview', annotated_image)

        # 4. If visualization is on, update the 3D plot
        if visualize_mode and coords:
            ul.visualize()

        key = cv2.waitKey(5) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('v'):
            visualize_mode = not visualize_mode
            if not visualize_mode:
                plt.close()  # Close plot window when turning off

    # 5. Clean up
    cap.release()
    cv2.destroyAllWindows()
    ul.close()


if __name__ == '__main__':
    run_demo()