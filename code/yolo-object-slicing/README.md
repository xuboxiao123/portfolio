# YOLOv5-guided Object Slicing

[Portfolio case study](../../project-yolo-slicing.md) · **[Core slicing function](object_slicing.py)** · [Original modified inference script](detect_with_object_slicing.py)

## Personal contribution
Boxiao Xu identified the post-detection slicing algorithm as his principal internship contribution. YOLOv5 is the upstream detector. The code here demonstrates the processing added around detector output, rather than authorship of the detection network.

## Implemented flow
1. Run YOLOv5 inference and non-maximum suppression.
2. Scale detection boxes back to the original image dimensions.
3. Clamp box coordinates to image bounds.
4. Save each detected object's rectangular crop.
5. Calculate the axis-aligned enclosing rectangle of all valid saved objects and save that combined region.
6. Export class, confidence, coordinates and saved paths as CSV.

The core function is extracted into object_slicing.py with isolated imports/logger and one correction: flush the CSV writer before reopening the file for the combined-box row, preventing the buffered writer from overwriting that appended row. The complete modified script is retained for integration context. It is designed to be placed in a compatible YOLOv5 checkout and is not a standalone detector package.

## Verification
The isolated function was smoke-tested using a synthetic 120×100 image and two synthetic detection boxes. It produced two individual crops, the combined crop and CSV output. An empty detection set produced a header-only CSV. No institutional images, weights, servers or datasets were used.

## Limits
This archived version implements object crops and their enclosing region. It does not establish a measured compression ratio, a complete background-compression pipeline, or a minimum-area rotated rectangle. Invalid/zero-area boxes and failed image writes are not fully handled by the historical code. A detector's bounding box cannot guarantee full semantic object coverage.

## Attribution
The original inference script carries the Ultralytics AGPL-3.0 notice, which is retained. The extracted function is distributed with the same notice. Upstream model/runtime code and model weights are not bundled.
