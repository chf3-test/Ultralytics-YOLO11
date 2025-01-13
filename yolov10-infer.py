import cv2
import supervision as sv
from ultralytics import YOLO
import serial
import struct
# import serial.tools.list_ports
#model = YOLOv10('yolo10n.pt')
model = YOLO('best.pt')
box_annotator = sv.BoxAnnotator()
label_annotator = sv.LabelAnnotator()  
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)



def create_data_packet(detections):
    global data_packets
    data_packets = []
    for detection in detections:
        x1, y1, x2, y2, conf, cls = detection
        a = 0
        if cls['class_name'] == 'medicine':
           a = 1
        elif cls['class_name'] == 'battery':
            a = 1
        elif cls['class_name'] == 'bottle':
            a = 2
        elif cls['class_name'] == 'medicine_box':
            a = 2
        elif cls['class_name'] == 'patato':
            a = 3
        elif cls['class_name'] == 'turnip':
            a = 3
        elif cls['class_name'] == 'carrot':
            a = 3
        elif cls['class_name'] == 'others':
            a = 4
        # class_id = int(cls)
        confidence = conf.item() if conf is not None else 0.0

        # 构建数据包
        packet = struct.pack('B', 0x0A)  # STX
        packet += struct.pack('B', a)
        packet += struct.pack('B', 0xA0)  # ETX
        print(a)
        a = 0
        print(a)

        data_packets.append(packet)
    return data_packets
    # 发送数据包
def send_data_packets(data_packets, serial_port):
        for packet in data_packets:
            serial_port.write(packet)
        print("发送")

if not cap.isOpened():
    print("can't open the webcam")

class_names = model.names
ser = serial.Serial('COM89', 115200, 8 ,'N',1)  # 串口端口和波特率
# flag = ser.is_open
# if flag:
#         print('success\n')
#         ser.close()
# else:
#         print('Open Error\n')
#         ser.close()

while True:
    ret,frame=cap.read()  
    if not ret:
        break
    results = model(frame)[0]
    detections = sv.Detections.from_ultralytics(results)
    annotated_image = box_annotator.annotate(
    scene=frame, detections=detections)
    annotated_image = label_annotator.annotate(
    scene=annotated_image, detections=detections)
    data_packets = []
    create_data_packet(detections)
    send_data_packets(data_packets, ser)
    # 将YOLO输出转换为所需的格式并发送


    # 主函数
    def main():
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # # 使用YOLO模型进行推理
            # results = model(frame)
            # detections = results.xyxy[0]  # 获取检测结果

            # 创建数据包
            data_packets = create_data_packet(detections)

            # 发送数据包
            send_data_packets(data_packets, ser)

    # # 将YOLOv11的输出转换为所需的格式
    # yolo_output = []
    # detections = results.xyxy[0]  # xyxy格式的张量，shape: [N, 6]，N是检测框的数量
    # for detection in detections:
    #     x1, y1, x2, y2, conf, cls = detection  # 正确解包每个检测结果
    #     class_id = int(cls)
    #     confidence = conf.item()
    #     yolo_output.append({
    #         "class_id": class_id,
    #         "confidence": confidence,
    #         "bbox": [int(x1), int(y1), int(x2), int(y2)]
    #     })
    #
    #
    #
    # # 在这里可以处理yolo_output，例如打印或显示检测结果
    # for output in yolo_output:
    #     class_id = output["class_id"]
    #     confidence = output["confidence"]
    #     bbox = output["bbox"]
    #     class_name = output["class_name"]
    #     label = f"{class_name} {confidence:.2f}"
    #     cv2.rectangle(frame, (bbox[0], bbox[1]), (bbox[2], bbox[3]), (0, 255, 0), 2)
    #     cv2.putText(frame, label, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    #
    #     # 将YOLO输出转数据格式
    # def create_data_packet(yolo_output):
    #         data_packets = []
    #         for detection in yolo_output:
    #             class_id = detection["class_id"]
    #             #  confidence = detection["confidence"]
    #             #  bbox = detection["bbox"]
    #
    #             # 构建数据包
    #             packet = struct.pack('B', 0x0A)  # STX
    #             packet += struct.pack('B', class_id)
    #             packet += struct.pack('B', 0xA0)  # ETX
    #
    #             data_packets.append(packet)
    #         return data_packets
    #
    #
    #     #发送数据包到下位机
    # def send_to_device(data_packets, serial_port='COM3', baud_rate=115200):
    #         ser = Serial(serial_port, baud_rate)
    #
    #         for packet in data_packets:
    #             ser.write(packet)
    #
    #         ser.close()
    #
    #
    #     # 主函数
    # def main():
    #         # 创建数据包
    #     data_packets = create_data_packet(yolo_output)
    #         # 发送数据包
    #     send_to_device(data_packets)
    #
    #
    #     if __name__ == "__main__":
    #         main()


    cv2.imshow('Webcam',annotated_image)
    k=cv2.waitKey(1000)
    if k%256==27:
        print("Escape hit,closing...")
        break   
cap.release()
cv2.destroyAllWindows()
