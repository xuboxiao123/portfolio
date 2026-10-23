# Ultralytics-derived source: AGPL-3.0, https://ultralytics.com/license
"""Historical object-slicing function extracted from detect copy 2.py.

One correction flushes the CSV writer before reopening the same file for append. Imports and logger are isolated so the slicing
logic can be reviewed and smoke-tested without loading YOLOv5 weights.
Detection coordinates must already be scaled to the original image.
"""
import csv
import logging
from pathlib import Path
import cv2
import numpy as np
LOGGER = logging.getLogger(__name__)

def save_complete_objects(im0, det, names, save_path):
    """
    保存每个完整的检测目标，并生成包含所有目标的总外接矩形
    - 每个目标用自身检测框裁剪（确保完整）
    - 所有目标用一个总外接矩形包裹
    """
    img_name = Path(save_path).name
    LOGGER.info(f"\n开始处理图像: {img_name}，共检测到 {len(det)} 个目标")
    
    # 创建保存目录
    base_save_dir = Path(save_path).parent / "complete_objects"
    base_save_dir.mkdir(parents=True, exist_ok=True)
    
    # 记录目标信息的CSV
    csv_path = base_save_dir / f"{Path(save_path).stem}_object_info.csv"
    with open(csv_path, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["目标序号", "类别名称", "类别ID", "置信度", "x1", "y1", "x2", "y2", "保存路径"])
        
        # 存储所有目标的坐标（用于计算总外接矩形）
        all_boxes = []
        
        # 保存每个完整目标（用自身检测框）
        for idx, (*xyxy, conf, cls) in enumerate(reversed(det)):
            cls_id = int(cls)
            cls_name = names[cls_id]
            conf_val = float(conf)
            
            # 关键：将模型输出的坐标转换为原始图像尺寸（确保不截断）
            x1, y1, x2, y2 = map(int, [coord.item() for coord in xyxy])
            
            # 确保坐标在图像范围内（防止越界）
            h, w = im0.shape[:2]
            x1, y1 = max(0, x1), max(0, y1)
            x2, y2 = min(w, x2), min(h, y2)
            
            # 裁剪单个完整目标（使用自身检测框，确保完整）
            cropped_obj = im0[y1:y2, x1:x2]
            save_filename = f"{Path(save_path).stem}_obj{idx}_{cls_name}.jpg"
            save_file = base_save_dir / save_filename
            
            try:
                cv2.imwrite(str(save_file), cropped_obj)
                LOGGER.info(f"✅ 目标 {idx}（{cls_name}）完整保存至: {save_file}")
                writer.writerow([idx, cls_name, cls_id, f"{conf_val:.2f}", x1, y1, x2, y2, str(save_file)])
                all_boxes.append([x1, y1, x2, y2])  # 收集坐标用于总框计算
            except Exception as e:
                LOGGER.error(f"❌ 目标 {idx} 保存失败: {str(e)}")
        
        # 生成包含所有目标的总外接矩形
        if all_boxes:
            all_boxes = np.array(all_boxes)
            total_x1, total_y1 = all_boxes[:, 0].min(), all_boxes[:, 1].min()
            total_x2, total_y2 = all_boxes[:, 2].max(), all_boxes[:, 3].max()
            
            # 裁剪总区域
            total_cropped = im0[total_y1:total_y2, total_x1:total_x2]
            total_save_file = base_save_dir / f"{Path(save_path).stem}_all_objects.jpg"
            cv2.imwrite(str(total_save_file), total_cropped)
            LOGGER.info(f"📦 所有目标总外接矩形保存至: {total_save_file}")
            # 记录总框信息到CSV
            f.flush()  # Preserve buffered rows before reopening the CSV for append.
            with open(csv_path, mode="a", newline="", encoding="utf-8") as f_append:
                append_writer = csv.writer(f_append)
                append_writer.writerow(["-", "所有目标", "-", "-", total_x1, total_y1, total_x2, total_y2, str(total_save_file)])
    
    LOGGER.info(f"📊 目标信息已记录至: {csv_path}")
    return True
