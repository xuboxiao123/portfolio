# Source audit / 源码核对清单

Audit date / 核对日期: 2026-10-24

Compared the current public portfolio and capstone repository trees against relevant project locations on E: (downloads, Eclipse workspace and Codex project directory), plus a shallow scan for project markers in other non-game/non-runtime folders. Reviewed 37 ZIP archives and 59 loose source-file candidates. Counts include duplicates and course material, not independent projects. / 数量包含备份、课程示例与依赖骨架，不代表项目数量。

| Recovered material / 找回内容 | Publication / 处理结果 |
|---|---|
| Java coursework 1: catalogue / 艺术品目录 | [Source](code/java-algorithms/assignment1/) |
| Java coursework 2: doubly linked list / 双向链表 | [Source](code/java-algorithms/assignment2/) |
| Java coursework 3: student BST / 学生二叉搜索树 | [Source](code/java-algorithms/assignment3/) |
| Java coursework 4: hash table and spell checker / 哈希表与拼写检查 | [Source](code/java-algorithms/assignment4/) |
| Echo lecture extension v0.2.0 / 讲座学习插件 | [Source](code/echo-study-helper/) |
| ExpressEventsAPI course companion / 课程配套 API | [Reference source](code/event-api-reference/), authorship unverified / 作者未确认 |

## Already published / 已有源码

[React frontend](code/react-events/), [PHP + MySQL contact manager](code/php-contacts/), [Arduino + Python IoT](code/arduino-iot/), [YOLOv5-guided slicing](code/yolo-object-slicing/), and [capstone frontend/backend/ESP32 firmware](https://github.com/xuboxiao123/NFC---3D-character-modeling/blob/main/CODE_INDEX.md).

## Excluded / 未当作新项目上传

- Repeated source-code ZIPs, DogAPI, skeleton assignments, example SQL and lecture C/Arduino samples: course or vendor examples, not established as independent projects. / 教学示例、空骨架、重复压缩包未充作本人新作品。
- Eclipse bin/src duplicate archives, compiled classes, IDE metadata, student CSV/spreadsheets and application installers. / 去除重复编译目录、学生数据与安装包。
- Original database settings and Wi-Fi configuration values are not included. The companion API now reads database settings from environment variables. / 未上传原数据库和 Wi-Fi 配置值。
- CAD files in downloads include possible capstone parts and generic models; ownership and project mapping were not established for every file, so this pass does not publish them as new model projects. / 模型文件尚未全部对应项目，未据文件名直接新增作品。

## Attribution and checks / 归属与检查

Java course helper classes retain Andrea Zanibellato's author credits; original student implementations retain Boxiao Xu's comments. The Echo extension is labelled as an AI-assisted personal prototype. API reference authorship remains unverified.

JDK 21 compilation passed; original MyListTest: 12 PASS. Nine JavaScript files passed node --check. JSON manifests were parsed. JUnit tests, hardware, live MySQL and live EchoVideo integration were not run in this audit. No end-to-end success is implied by syntax checks. / 编译与语法检查通过，联调验证范围如上。

Original E: files were read only; publication copies and source archives were prepared separately. / E 盘原件未改动，整理与发布使用副本。
