import cv2
import supervision as sv
from sympy.codegen import Print

from ultralytics import YOLO
import serial
import struct

from PyQt5.QtWidgets import QApplication, QMainWindow, QVideoWidget, QVBoxLayout, QPushButton, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from ui_mainwindow import Ui_MainWindow



model = YOLO('best.pt')
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()  
cap = cv2.VideoCapture(1)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)





class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.camera = None
        self.viewfinder = None
        self.startCamera()
        self.setupUi(self)
        self.label_video_yolo()
        self.self.label_pic()
        self.camera_capture = cv2.VideoCapture(0)  
        self.media_player = QMediaPlayer()
        self.media_warn = QMediaPlayer()
        self.text_label_recycle.setText('可回收垃圾计数:0')
        self.text_label_other.setText('其他垃圾计数:0')
        self.text_label_harmful.setText('有害垃圾计数:0')
        self.text_label_other_kitchen.setText('厨余垃圾计数:0')
        self.rec_count = 0
        self.harm_count = 0
        self.other_count = 0
        self.kitchen_count = 0

        

    def startCamera(self):
        self.camera = QCamera()
        self.viewfinder = QCameraViewfinder(self.label_video_yolo)
        self.label_video_yolo.layout().addWidget(self.viewfinder)
        self.camera.setViewfinder(self.viewfinder)
        self.camera.start()

    def closeEvent(self, event):
        if self.camera:
            self.camera.stop()
        super(MainWindow, self).closeEvent(event)


    def create_data_packet(detections):
        data_packets = []
        for detection in detections:
            x1, y1, x2, y2, conf, cls = detection
            a = 0
            if cls['class_name'] == 'medicine':
                a = 1
                self.harm_count +=1
                self.text_label_other_harmful.setText(f'有害垃圾计数:{self.harmful_count}')
            elif cls['class_name'] == 'battery':
                a = 1
                self.harm_count +=1
                self.text_label_other_harmful.setText(f'有害垃圾计数:{self.harmful_count}')
            elif cls['class_name'] == 'bottle':
                a = 2
                self.rec_count +=1
                self.text_label_other_recycle.setText(f'可回收垃圾计数:{self.recycle_count}')
            elif cls['class_name'] == 'medicine_box':
                a = 2
                self.rec_count +=1
                self.text_label_other_recycle.setText(f'可回收垃圾计数:{self.recycle_count}')
            elif cls['class_name'] == 'patato':
                a = 3
                self.kitchen_count +=1
                self.text_label_other_kitchen.setText(f'厨余垃圾计数:{self.kitchen_count}')
            elif cls['class_name'] == 'turnip':
                a = 3
                self.kitchen_count +=1
                self.text_label_other_kitchen.setText(f'厨余垃圾计数:{self.kitchen_count}')
            elif cls['class_name'] == 'carrot':
                a = 3
                self.kitchen_count +=1
                self.text_label_other_kitchen.setText(f'厨余垃圾计数:{self.kitchen_count}')
            elif cls['class_name'] == 'others':
                a = 4
                self.other_count +=1
                self.text_label_other.setText(f'其他垃圾计数:{self.other_count}')

            confidence = conf.item() if conf is not None else 0.0

            # Build the data packet
            packet = struct.pack('B', a)
            data_packets.append(packet)
            # print('sha',packet)

        return data_packets
        print('1',data_packets)

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
        ser = serial.Serial('COM90', 115200)  # Adjust as necessary
        if not ser.is_open:
            ser.open()

        while True:
            print('2222')
            ret, frame = cap.read()
            if not ret:
                break

            results = model(frame)[0]
            detections = sv.Detections.from_ultralytics(results)
            annotated_image = box_annotator.annotate(scene=frame, detections=detections)
            annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)

            data_packets = create_data_packet(detections)
            print('1123',data_packets)
            send_data_packets(data_packets, ser)
            print('3333',data_packets)
            receive_serial_data(ser)
            print('4444',receive_serial_data(ser))

            cv2.imshow('Webcam', annotated_image)

            # Break if 'ESC' is pressed
            k = cv2.waitKey(6000)
            if k % 256 == 27:
                print("Escape hit, closing...")
                break

    cap.release()
    cv2.destroyAllWindows()
    ser.close()

if __name__ == "__main__":
    main()  # Call the main function

    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    setTheme(Theme.DARK)
    app = QApplication(sys.argv)
    test = Window()
    test.show()
    app.exec_()
