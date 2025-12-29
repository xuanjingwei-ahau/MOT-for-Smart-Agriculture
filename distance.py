import cv2
import numpy as np
import os

def generate_progressive_faded_background(rgb_path, depth_path, min_m, max_m, interval_m, output_folder):
    """
    近处正常显示，背景部分变淡（不完全剔除），便于区分深度界限
    """
    # 1. 读取图像
    rgb_img = cv2.imread(rgb_path)
    depth_img = cv2.imread(depth_path, cv2.IMREAD_UNCHANGED)

    if rgb_img is None or depth_img is None:
        print("错误：无法读取图像，请检查路径。")
        return

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 2. 转换单位
    min_mm = int(min_m * 1000)
    max_mm = int(max_m * 1000)
    step_mm = int(interval_m * 1000)

    print(f"开始分层处理：前景保持正常，背景淡化显示。范围 {min_m}m 至 {max_m}m")

    # 3. 循环处理
    current_limit = min_mm + step_mm
    
    while current_limit <= max_mm:
        # 创建前景掩码 (逻辑：深度在范围内且有效)
        mask = (depth_img > 0) & (depth_img <= current_limit)
        
        # 4. 实现淡化效果
        # 创建一个背景副本并降低亮度（乘以0.2表示亮度降低80%）
        faded_bg = (rgb_img.astype(np.float32) * 0.2).astype(np.uint8)
        
        # 创建结果图：默认全是淡化后的背景
        result_img = faded_bg.copy()
        
        # 将前景部分（掩码区域）替换回原始的高亮图像
        result_img[mask] = rgb_img[mask]
        
        # 5. 保存
        dist_str = f"{current_limit / 1000:.2f}"
        file_name = f"focus_within_{dist_str}m.png"
        save_path = os.path.join(output_folder, file_name)
        
        cv2.imwrite(save_path, result_img)
        print(f"已生成：{file_name} (前景范围 0-{dist_str}m)")
        
        current_limit += step_mm

    print("-" * 30)
    print(f"分层处理完成！结果保存至: {output_folder}")

if __name__ == "__main__":
    input_rgb = r"E:\dataset\tomato\TEST\501.png"
    input_depth = r"E:\dataset\tomato\TEST\501-d1.png"
    target_dir = r"E:\dataset\tomato\TEST\distance"

    # 参数：0.1m到3.0m，每0.1m一档
    generate_progressive_faded_background(input_rgb, input_depth, 0.0, 3.0, 0.1, target_dir)