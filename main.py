import cv2
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time


def video_to_images(video_path, output_folder, step=1):
    start_time = time.time()
    video = cv2.VideoCapture(video_path)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = video.get(cv2.CAP_PROP_FPS)
    info_label.config(text=f"总帧数: {total_frames}, 视频帧率: {fps}")

    os.makedirs(output_folder, exist_ok=True)
    total_output_frames = len(str(total_frames // step))

    progress['maximum'] = total_frames
    frame_count = 0
    while frame_count < total_frames:
        ret, frame = video.read()
        if not ret:
            break
        else:
            frame_count += 1

        if frame_count % step == 0:
            file_serial_number = str(frame_count // step).zfill(total_output_frames)
            output_file = f"{output_folder}/frame_{file_serial_number}.png"
            cv2.imwrite(output_file, frame)

        progress['value'] = frame_count
        speed_label.config(text=f"处理速度: {frame_count / (time.time() - start_time):.2f} 帧/秒")
        root.update_idletasks()

    video.release()
    messagebox.showinfo("完成", "视频转图片完成。")


def select_video():
    file_path = filedialog.askopenfilename()
    if file_path:
        video_path.set(file_path)


def select_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_folder.set(folder_path)


def start_conversion():
    video_path_val = video_path.get()
    output_folder_val = output_folder.get()
    if not video_path_val or not output_folder_val:
        messagebox.showwarning("警告", "请选择一个视频并指定输出文件夹。")
        return
    video_to_images(video_path_val, output_folder_val)


root = tk.Tk()
root.title("视频转图片转换器")

video_path = tk.StringVar()
video_entry = tk.Entry(root, textvariable=video_path, width=40)
video_entry.grid(row=0, column=0, padx=(10, 0), pady=10)

select_video_button = tk.Button(root, text="选择视频", command=select_video, width=10)
select_video_button.grid(row=0, column=1, padx=(5, 10), pady=10)

output_folder = tk.StringVar()
output_entry = tk.Entry(root, textvariable=output_folder, width=40)
output_entry.grid(row=1, column=0, padx=(10, 0), pady=10)

select_output_button = tk.Button(root, text="输出文件夹", command=select_output_folder, width=10)
select_output_button.grid(row=1, column=1, padx=(5, 10), pady=10)

start_button = tk.Button(root, text="开始转换", command=start_conversion, width=20)
start_button.grid(row=2, column=0, columnspan=2, pady=10)

info_label = tk.Label(root, text="未选择视频")
info_label.grid(row=3, column=0, columnspan=2, pady=10)

speed_label = tk.Label(root, text="处理速度: N/A")
speed_label.grid(row=4, column=0, columnspan=2)

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
