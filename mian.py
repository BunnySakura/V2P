import cv2
import os
import base64
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time

supported_image_formats = (
    "bmp", "dib",  # Windows bitmaps
    "jpeg", "jpg", "jpe",  # JPEG files
    "jp2",  # JPEG 2000 files
    "png",  # Portable Network Graphics
    "webp",  # WebP
    "tiff", "tif",  # TIFF files
    "hdr", "pic",  # Radiance HDR
    "ppm", "pgm", "pbm",  # PPM, PBM, and PGM
)


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string


def video_to_images(video_path, output_folder, image_extension, step=1):
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
            # 使用用户指定的图片后缀名
            output_file = f"{output_folder}/frame_{file_serial_number}.{image_extension}"
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
    # 获取用户输入的图片后缀名，未输入或格式不支持则默认为jpg
    image_extension_val = "jpg" if image_extension.get() not in supported_image_formats else image_extension.get()
    if not video_path_val or not output_folder_val or not image_extension_val:
        messagebox.showwarning("警告", "请选择一个视频并指定输出文件夹和图片后缀名。")
        return
    video_to_images(video_path_val, output_folder_val, image_extension_val)  # 传递图片后缀名


root = tk.Tk()
root.title("V2P | 视频转图片")
root.iconphoto(True, tk.PhotoImage(data=image_to_base64("icon.png")))

select_video_button = tk.Button(root, text="选择视频", command=select_video, width=10)
select_video_button.grid(row=0, column=0, padx=(5, 10), pady=10)

video_path = tk.StringVar()
video_entry = tk.Entry(root, textvariable=video_path, width=40)
video_entry.grid(row=0, column=1, padx=(10, 0), pady=10)

select_output_button = tk.Button(root, text="输出文件夹", command=select_output_folder, width=10)
select_output_button.grid(row=1, column=0, padx=(5, 10), pady=10)

output_folder = tk.StringVar()
output_entry = tk.Entry(root, textvariable=output_folder, width=40)
output_entry.grid(row=1, column=1, padx=(10, 0), pady=10)

start_button = tk.Button(root, text="导出", command=start_conversion, width=10)
start_button.grid(row=2, column=0, padx=(5, 10), pady=10)

image_extension = tk.StringVar(value="图片后缀（默认：jpg）")  # 默认值为jpg
image_extension_entry = tk.Entry(root, textvariable=image_extension, width=40)
image_extension_entry.grid(row=2, column=1, padx=(10, 0), pady=10, sticky='w')

info_label = tk.Label(root, text="未选择视频")
info_label.grid(row=3, column=0, columnspan=2, pady=10)

speed_label = tk.Label(root, text="处理速度: N/A")
speed_label.grid(row=4, column=0, columnspan=2)

progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
progress.grid(row=5, column=0, columnspan=2, pady=10)

root.mainloop()
