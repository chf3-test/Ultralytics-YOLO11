import cv2

def extract_frames(video_path, output_dir, frame_interval):
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 检查视频是否成功打开
    if not cap.isOpened():
        print("无法打开视频文件")
        return

    # 初始化帧计数器和输出文件名计数器
    frame_count = 0
    output_count = 0

    # 循环读取视频帧
    while True:
        # 读取一帧
        ret, frame = cap.read()

        # 检查是否成功读取帧
        if not ret:
            break

        # 如果达到指定的帧间隔，则保存当前帧
        if frame_count % frame_interval == 0:
            # 创建输出文件名
            output_file = f"{output_dir}/frame_{output_count:04d}.jpg"

            # 保存帧到文件
            cv2.imwrite(output_file, frame)

            # 增加输出文件名计数器
            output_count += 1

        # 增加帧计数器
        frame_count += 1

    # 释放视频捕获对象
    cap.release()

    print(f"成功从视频中提取了 {output_count} 帧")

# 使用示例
video_path = "datasets\VID20241216154601.mp4"
output_dir = "datasets/originalImgs"
frame_interval = 15  # 每15帧保存一次

extract_frames(video_path, output_dir, frame_interval)
