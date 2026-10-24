[← Portfolio](README.md)

# YOLOv5-guided Object Slicing

**中科院实习：基于目标检测结果的图像切片算法**

**[查看核心切片代码](code/yolo-object-slicing/object_slicing.py) · [浏览源码与运行说明](code/yolo-object-slicing/) · [原始推理集成代码](code/yolo-object-slicing/detect_with_object_slicing.py)**

该项目围绕遥感图像处理展开。YOLOv5 负责目标识别，我的重点工作是利用识别结果进行切片：把检测框还原到原图坐标，进行边界裁剪，保存单个目标，并计算覆盖多个目标的总外接矩形，输出对应的切片和 CSV 记录。

**技术：** Python · YOLOv5 integration · NumPy · OpenCV · Bounding boxes · CSV

## My contribution
Post-detection object slicing and result export, identified by the project owner as the main internship contribution. The upstream YOLOv5 detector and network are separately attributed.

## Code-backed results
- Detection boxes are scaled to the original image before slicing.
- Object regions are cropped within image boundaries.
- Individual crops and one combined axis-aligned enclosing crop are written.
- CSV records include object class, confidence, coordinates and output paths.

## Validation
The extracted original function passed a synthetic-data execution check: two individual crops, a combined crop, boundary clipping and CSV output were verified. An empty detection case also completed. No model weights or internship imagery were published.

## Scope
This archive documents the implemented slicing variant. It does not supply a measured transmission/compression improvement or demonstrate a complete background-compression pipeline. The isolated function includes one documented CSV-flush correction; the original inference script is retained separately.
