import cv2
import supervision as sv
from ultralytics import YOLO
import serial
import struct

model = YOLO('best.pt')
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()  
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

def create_data_packet(detections):
    data_packets = []
    for detection in detections:
        x1, y1, x2, y2, conf, cls = detection
        a = 0x00
        if cls['class_name'] == 'medicine':
            a = 0x01
        elif cls['class_name'] == 'battery':
            a = 0x01
        elif cls['class_name'] == 'bottle':
            a = 0x02
        elif cls['class_name'] == 'medicine_box':
            a = 0x02
        elif cls['class_name'] == 'patato':
            a = 0x03
        elif cls['class_name'] == 'turnip':
            a = 0x03
        elif cls['class_name'] == 'carrot':
            a = 0x03
        elif cls['class_name'] == 'others':
            a = 0x04

        confidence = conf.item() if conf is not None else 0.0

        # Build the data packet
        packet = struct.pack('B', 0x0A)  # STX
        packet += struct.pack('B', a)
        packet += struct.pack('B', 0xA0)  # ETX
        data_packets.append(packet)

    return data_packets

def send_data_packets(data_packets, serial_port):
    for packet in data_packets:
        serial_port.write(packet)
    print("Sending data packets...")

def receive_serial_data(serial_port):
    while serial_port.in_waiting > 0:
        data = serial_port.read(serial_port.in_waiting)
        print("Received data:", data)

def main():
    # Set up serial communication
    ser = serial.Serial('COM85', 115200)  # Adjust as necessary
    if not ser.is_open:
        ser.open()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)[0]
        detections = sv.Detections.from_ultralytics(results)
        annotated_image = box_annotator.annotate(scene=frame, detections=detections)
        annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)

        data_packets = create_data_packet(detections)
        send_data_packets(data_packets, ser)
        receive_serial_data(ser)

        cv2.imshow('Webcam', annotated_image)

        # Break if 'ESC' is pressed
        k = cv2.waitKey(1)
        if k % 256 == 27:
            print("Escape hit, closing...")
            break

    cap.release()
    cv2.destroyAllWindows()
    ser.close()

if __name__ == "__main__":
    main()  # Call the main function
