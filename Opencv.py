
# Requirements: pip install opencv-contrib-python
import cv2
import time
from pathlib import Path

def apply_bw(frame):
    """
    Convert a BGR frame (OpenCV default) to grayscale and return a 3-channel BGR version
    so it can be displayed/encoded the same as the color frames.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)      # single channel
    gray_bgr = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)   # convert back to 3-channel BGR
    return gray_bgr

def start_camera(device_index=0):
    """
    Open camera and enter main loop:
      - 'b' toggles black & white filter on/off
      - 'r' starts/stops recording to a file
      - 'c' captures a single frame as JPEG
      - 'q' quits
    """
    cap = cv2.VideoCapture(device_index)
    if not cap.isOpened():
        print("ERROR: Cannot open camera. Check device index or camera access.")
        return

    # Get some properties to configure writer
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
    fps    = cap.get(cv2.CAP_PROP_FPS) or 20.0  # fallback if camera doesn't provide fps

    print(f"Camera opened: {width}x{height} @ {fps:.2f} FPS")

    bw_mode = False         # toggle black & white
    recording = False
    out = None
    record_filename = None

    # FourCC code — use a common codec. On some systems you may prefer 'MJPG' or 'XVID'.
    fourcc = cv2.VideoWriter_fourcc(*'XVID')

    print("Controls: 'b' toggle B/W | 'r' start/stop recording | 'c' capture frame | 'q' quit")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Frame capture failed, stopping.")
            break

        display_frame = apply_bw(frame) if bw_mode else frame

        # Show text overlay for status
        status_text = f"{'B/W' if bw_mode else 'COLOR'}  "
        status_text += "REC" if recording else "----"
        cv2.putText(display_frame, status_text, (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0) if recording else (0, 150, 255), 2)

        cv2.imshow("Camera (press q to quit)", display_frame)

        # If recording, write the frame (must be same shape as writer expects)
        if recording and out is not None:
            # Ensure writer frame size matches; convert if needed
            out.write(display_frame)

        # WaitKey: 1 ms is typical for live view; returns ASCII code or -1
        key = cv2.waitKey(1) & 0xFF

        if key == ord('b'):
            bw_mode = not bw_mode
            print("B/W mode:", "ON" if bw_mode else "OFF")

        elif key == ord('r'):
            # toggle recording
            if not recording:
                # start recording: create a filename with timestamp
                record_filename = f"record_{int(time.time())}.avi"
                # create VideoWriter with same frame size as display_frame
                out = cv2.VideoWriter(record_filename, fourcc, fps, (display_frame.shape[1], display_frame.shape[0]))
                if not out.isOpened():
                    print("ERROR: VideoWriter failed to open. Recording won't start.")
                    out = None
                else:
                    recording = True
                    print(f"Recording started -> {record_filename}")
            else:
                # stop recording
                recording = False
                if out:
                    out.release()
                    out = None
                print(f"Recording stopped. Saved -> {record_filename}")

        elif key == ord('c'):
            # capture single frame (save as JPEG)
            captures_dir = Path("captures")
            captures_dir.mkdir(exist_ok=True)
            fname = captures_dir / f"capture_{int(time.time())}.jpg"
            # Save the frame in the current display mode
            cv2.imwrite(str(fname), display_frame)
            print("Captured frame saved to", fname)

        elif key == ord('q'):
            print("Quitting...")
            break

    # Cleanup
    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_camera(0)
