from ultralytics import YOLO
import cv2
import numpy as np  # Import numpy
from sort import Sort  # Import the SORT tracker
import time
import torch

# Constants

VEHICLE_LENGTHS = {
    0: 3.8,
    1: 5.0,
    2: 6.4,
    3: 22.0,
    4: 14.0,
    5: 2.4
}
QUEUE_ZONES = [
    {
        "lane": 1,
        "corners": [(1530, 140), (965, 1015), (500, 1000), (1500, 140)],  # Updated coordinates for lane 1
        "color": (0, 165, 255),  # Orange for lane 1
        "text_position": (500, 1100)  # Adjusted position for queue text (x, y)
    },
    {
        "lane": 2,
        "corners": [(1655, 60), (1490, 1020), (970, 1020), (1630, 60)],  # Coordinates for lane 2
        "color": (255, 0, 0),  # Blue for lane 2
        "text_position": (1000, 1100)  # Adjusted position for queue text
    },
    {
        "lane": 3,
        "corners": [(1660, 60), (1500, 1020), (2030, 1030), (1690, 60)],  # Coordinates for lane 3
        "color": (0, 255, 0),  # Green for lane 3
        "text_position": (1700, 1100)  # Adjusted position for queue text
    }
]

WAITING_ZONE_1 = [(1315, 500), (965, 1015), (300, 1000), (990, 500)]  # 4 points for the first zone
WAITING_ZONE_2 = [(1850, 500), (2065, 1055), (970, 1020), (1325, 500)]  # 4 points for the second zone

def get_color(class_id):
    colors = [
        (255, 0, 0),  # Blue
        (0, 255, 0),  # Green
        (0, 0, 255),  # Red
        (255, 255, 0),  # Cyan
        (255, 0, 255),  # Magenta
        (0, 255, 255)  # Yellow
    ]
    return colors[class_id % len(colors)]


def draw_custom_labels(frame, tracked_objects, result, waiting_times, queue_lengths):
    # Initialize waiting time counters for each zone
    zone_waiting_times = {1: [], 2: []}

    for i, track in enumerate(tracked_objects):
        track_id = int(track[4])  # The unique tracking ID
        x1, y1, x2, y2 = map(int, track[:4])

        if i < len(result.boxes):
            class_id = int(result.boxes[i].cls[0])  # Get the class for the current box
            confidence = float(result.boxes[i].conf[0])  # Get the confidence for the current box
            label_class = f"Class: {result.names[class_id]}"
            label_conf = f"Conf: {confidence:.2%}"  # Confidence as a percentage (2 decimal points)
        else:
            label_class = "Class: No vehicle"
            label_conf = "Conf: No vehicle"

        label_id = f"ID: {track_id}"
        color = get_color(class_id)

        # Draw bounding box and labels
        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 4)
        font_scale = 0.75
        font_thickness = 2
        y_offset = 20  # Vertical offset for text spacing

        cv2.putText(frame, label_id, (x1, y1 - y_offset), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255),
                    font_thickness)
        cv2.putText(frame, label_class, (x1, y1 - y_offset - 30), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255),
                    font_thickness)
        cv2.putText(frame, label_conf, (x1, y1 - y_offset - 60), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255),
                    font_thickness)

        # Display waiting time if the vehicle is in the waiting zone
        if track_id in waiting_times:
            waiting_time = time.time() - waiting_times[track_id]['entry_time']
            waiting_times[track_id]['total_time'] += waiting_time  # Increment total time for average calculation
            waiting_times[track_id]['count'] += 1  # Increment count for average calculation

            # Check which zone the vehicle is in and update waiting times
            if is_in_waiting_zone(x1, y1, x2, y2):
                if is_in_waiting_zone_1(x1, y1, x2, y2):
                    zone_waiting_times[1].append(waiting_time)
                elif is_in_waiting_zone_2(x1, y1, x2, y2):
                    zone_waiting_times[2].append(waiting_time)

    # Define positions for the waiting time display for each zone
    WAITING_ZONE_1_LABEL_POS = (500, 1050)  # Position for the first zone
    WAITING_ZONE_2_LABEL_POS = (1300, 1100)  # Position for the second zone

    # Draw waiting times for each zone
    for i, zone_label_pos in enumerate([WAITING_ZONE_1_LABEL_POS, WAITING_ZONE_2_LABEL_POS], start=1):
        if zone_waiting_times[i]:
            avg_wait = sum(zone_waiting_times[i]) / len(zone_waiting_times[i])
            max_wait = max(zone_waiting_times[i])
            cv2.putText(frame, f"Avg Wait: {avg_wait:.1f}s", zone_label_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                        (255, 255, 255), 2)
            cv2.putText(frame, f"Max Wait: {max_wait:.1f}s", (zone_label_pos[0], zone_label_pos[1] + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)
        else:
            cv2.putText(frame, "Avg Wait: No vehicle", zone_label_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.75,
                        (255, 255, 255), 2)
            cv2.putText(frame, "Max Wait: No vehicle", (zone_label_pos[0], zone_label_pos[1] + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 255, 255), 2)

    # Draw queue lengths and queue zones
    for zone in QUEUE_ZONES:
        corners = np.array(zone["corners"], dtype=np.int32)  # Convert corners to NumPy array
        color = zone["color"]
        cv2.polylines(frame, [corners], isClosed=True, color=color, thickness=2)  # Draw queue zone
        queue_length = queue_lengths[zone["lane"]]
        text_position = zone["text_position"]  # Get the text position from the zone
        cv2.putText(frame, f"Queue: {queue_length:.2f} m", text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)

    return frame

def measure_queue_length(results):
    queue_lengths = {1: 0.0, 2: 0.0, 3: 0.0}  # Initialize queue lengths for each lane

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            class_id = int(box.cls[0])  # Get the class ID for the detected object

            # Get the length for the detected vehicle class, default to 0 if class not found
            vehicle_length = VEHICLE_LENGTHS.get(class_id, 0.0)

            for zone in QUEUE_ZONES:
                corners = np.array(zone["corners"], dtype=np.int32)
                mask = cv2.pointPolygonTest(corners, (x1, y1), False) >= 0 or cv2.pointPolygonTest(corners, (x2, y2), False) >= 0
                if mask:
                    queue_lengths[zone["lane"]] += vehicle_length  # Add the length of the detected vehicle

    return queue_lengths


def is_in_waiting_zone(x1, y1, x2, y2):
    """Check if the bounding box is within either waiting zone."""
    return is_in_waiting_zone_1(x1, y1, x2, y2) or is_in_waiting_zone_2(x1, y1, x2, y2)


def is_in_waiting_zone_1(x1, y1, x2, y2):
    """Check if the bounding box is within the first waiting zone."""
    zone1 = np.array(WAITING_ZONE_1, dtype=np.int32)
    center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
    return cv2.pointPolygonTest(zone1, (center_x, center_y), False) >= 0


def is_in_waiting_zone_2(x1, y1, x2, y2):
    """Check if the bounding box is within the second waiting zone."""
    zone2 = np.array(WAITING_ZONE_2, dtype=np.int32)
    center_x, center_y = (x1 + x2) // 2, (y1 + y2) // 2
    return cv2.pointPolygonTest(zone2, (center_x, center_y), False) >= 0


def test_model_on_rtsp_stream(model_path, rtsp_url):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(rtsp_url)

    if not cap.isOpened():
        print("Error: Cannot open RTSP stream")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1080)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    tracker = Sort()  # Initialize the SORT tracker
    waiting_times = {}  # Initialize a dictionary to track vehicle waiting times

    # Create a named window for fullscreen display
    cv2.namedWindow("RTSP Stream - Vehicle Detection", cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty("RTSP Stream - Vehicle Detection", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Draw the waiting zones (yellow and magenta polygons)
        cv2.polylines(frame, [np.array(WAITING_ZONE_1, dtype=np.int32)], isClosed=True, color=(0, 255, 255),
                      thickness=2)
        cv2.polylines(frame, [np.array(WAITING_ZONE_2, dtype=np.int32)], isClosed=True, color=(255, 0, 255),
                      thickness=2)

        # Run detection on the frame
        results = model(frame)

        # Initialize an empty list for storing detections
        detections = []
        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                detections.append([x1, y1, x2, y2, conf])

        # Update tracker with detections if not empty
        if len(detections) > 0:
            tracked_objects = tracker.update(np.array(detections))
        else:
            tracked_objects = np.empty((0, 5))  # Ensure tracked_objects has the correct shape even if empty

        # Update waiting times based on vehicle positions
        current_ids = set()  # Track current vehicle IDs
        for track in tracked_objects:
            track_id = int(track[4])  # Get the tracker ID
            current_ids.add(track_id)
            x1, y1, x2, y2 = map(int, track[:4])

            if is_in_waiting_zone(x1, y1, x2, y2):  # Check if vehicle is in the waiting zone
                if track_id not in waiting_times:
                    # Vehicle entered one of the waiting zones
                    waiting_times[track_id] = {'entry_time': time.time(), 'total_time': 0, 'count': 0}
            else:
                if track_id in waiting_times:
                    # Vehicle left the waiting zone
                    waiting_times.pop(track_id)

        # Measure queue lengths for display (from the second version)
        queue_lengths = measure_queue_length(results)

        # Visualize the results with custom labels, queue lengths, and tracker IDs
        annotated_frame = draw_custom_labels(frame, tracked_objects, results[0], waiting_times, queue_lengths)

        # Display the frame in full screen
        cv2.imshow("RTSP Stream - Vehicle Detection", annotated_frame)

        # Exit the loop when 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources when done
    cap.release()
    cv2.destroyAllWindows()


def main():
    model_path = 'runs/train/vehicle_detection16/weights/best.pt'
    rtsp_url = 'rtsp://admin:Dyna1234@180.74.167.65:551/stream1'
    test_model_on_rtsp_stream(model_path, rtsp_url)


if __name__ == "__main__":
    main()
