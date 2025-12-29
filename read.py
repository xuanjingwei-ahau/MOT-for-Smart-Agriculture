import os
import glob
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import threading
import time

class ImageSequencePlayer:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("图片序列播放器")
        self.window.geometry("1000x700")
        
        # 变量
        self.image_files = []
        self.current_index = 0
        self.is_playing = False
        self.fps = 24
        self.loop = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # 控制面板
        control_frame = tk.Frame(self.window)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # 文件夹选择
        tk.Button(control_frame, text="选择文件夹", command=self.select_folder).pack(side=tk.LEFT, padx=5)
        
        # FPS控制
        tk.Label(control_frame, text="帧率:").pack(side=tk.LEFT, padx=5)
        self.fps_var = tk.IntVar(value=24)
        fps_spinbox = tk.Spinbox(control_frame, from_=1, to=120, textvariable=self.fps_var, width=5)
        fps_spinbox.pack(side=tk.LEFT, padx=5)
        
        # 循环播放复选框
        self.loop_var = tk.BooleanVar()
        tk.Checkbutton(control_frame, text="循环播放", variable=self.loop_var).pack(side=tk.LEFT, padx=5)
        
        # 播放控制按钮
        self.play_btn = tk.Button(control_frame, text="播放", command=self.toggle_play, state=tk.DISABLED)
        self.play_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(control_frame, text="上一张", command=self.prev_image).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="下一张", command=self.next_image).pack(side=tk.LEFT, padx=5)
        tk.Button(control_frame, text="停止", command=self.stop_play).pack(side=tk.LEFT, padx=5)
        
        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Scale(control_frame, from_=0, to=100, variable=self.progress_var,
                                      command=self.on_progress_change, length=300)
        self.progress_bar.pack(side=tk.LEFT, padx=10)
        
        # 状态标签
        self.status_label = tk.Label(control_frame, text="请选择包含图片的文件夹")
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        # 图片显示区域
        self.image_frame = tk.Frame(self.window, bg='black')
        self.image_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.image_label = tk.Label(self.image_frame)
        self.image_label.pack(expand=True)
        
    def select_folder(self):
        folder_path = filedialog.askdirectory(title="选择图片文件夹")
        if folder_path:
            self.load_images(folder_path)
    
    def load_images(self, folder_path):
        # 支持的图片格式
        image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff', '*.gif', '*.webp']
        
        self.image_files = []
        for ext in image_extensions:
            self.image_files.extend(glob.glob(os.path.join(folder_path, ext)))
            self.image_files.extend(glob.glob(os.path.join(folder_path, ext.upper())))
        
        if self.image_files:
            # 按文件名排序
            self.image_files.sort(key=lambda x: os.path.basename(x).lower())
            self.current_index = 0
            self.play_btn.config(state=tk.NORMAL)
            self.progress_bar.config(state=tk.NORMAL)
            self.status_label.config(text=f"已加载 {len(self.image_files)} 张图片")
            self.show_current_image()
        else:
            self.status_label.config(text="未找到图片文件")
    
    def show_current_image(self):
        if not self.image_files or self.current_index >= len(self.image_files):
            return
        
        img_path = self.image_files[self.current_index]
        try:
            # 打开图片并调整大小以适应窗口
            img = Image.open(img_path)
            
            # 获取显示区域大小
            display_width = self.image_frame.winfo_width() - 20
            display_height = self.image_frame.winfo_height() - 20
            
            if display_width > 1 and display_height > 1:
                # 调整图片大小保持纵横比
                img.thumbnail((display_width, display_height), Image.Resampling.LANCZOS)
            
            # 转换为PhotoImage并显示
            photo = ImageTk.PhotoImage(img)
            self.image_label.config(image=photo)
            self.image_label.image = photo  # 保持引用
            
            # 更新状态
            filename = os.path.basename(img_path)
            self.status_label.config(text=f"图片 {self.current_index + 1}/{len(self.image_files)}: {filename}")
            
            # 更新进度条
            progress = (self.current_index / len(self.image_files)) * 100
            self.progress_var.set(progress)
            
        except Exception as e:
            print(f"无法加载图片 {img_path}: {e}")
    
    def toggle_play(self):
        if self.is_playing:
            self.stop_play()
        else:
            self.start_play()
    
    def start_play(self):
        if not self.image_files:
            return
        
        self.is_playing = True
        self.play_btn.config(text="暂停")
        self.loop = self.loop_var.get()
        self.fps = self.fps_var.get()
        
        # 在新线程中播放
        self.play_thread = threading.Thread(target=self.play_sequence, daemon=True)
        self.play_thread.start()
    
    def play_sequence(self):
        while self.is_playing and self.image_files:
            if not self.is_playing:
                break
            
            # 显示当前图片
            self.window.after(0, self.show_current_image)
            
            # 等待下一帧
            time.sleep(1 / self.fps)
            
            # 移动到下一张图片
            self.current_index += 1
            
            if self.current_index >= len(self.image_files):
                if self.loop:
                    self.current_index = 0
                else:
                    self.stop_play()
                    break
    
    def stop_play(self):
        self.is_playing = False
        self.play_btn.config(text="播放")
    
    def prev_image(self):
        if self.image_files:
            self.current_index = (self.current_index - 1) % len(self.image_files)
            self.show_current_image()
    
    def next_image(self):
        if self.image_files:
            self.current_index = (self.current_index + 1) % len(self.image_files)
            self.show_current_image()
    
    def on_progress_change(self, value):
        if self.image_files and not self.is_playing:
            index = int((float(value) / 100) * len(self.image_files))
            if index < len(self.image_files):
                self.current_index = index
                self.show_current_image()
    
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    app = ImageSequencePlayer()
    app.run()