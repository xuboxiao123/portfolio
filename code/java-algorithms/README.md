# Java algorithms and OOP / Java 算法与面向对象

Four completed COMPX201 coursework exercises recovered from the original Eclipse workspace. / 从原 Eclipse 工作区整理的四组已完成课程作业。

| Exercise | Implementation by Boxiao Xu | Focus |
|---|---|---|
| [assignment1](assignment1) | ArtPieceOnSale, Catalogue | Inheritance, catalogue display / 继承与目录展示 |
| [assignment2](assignment2) | MyList, MyListTest | Doubly linked list / 双向链表 |
| [assignment3](assignment3) | StudentTree, StudentTreeReader, StudentTreeTest | Binary search tree, file input, JUnit / 二叉搜索树与测试 |
| [assignment4](assignment4) | MyHashTable, MyHashTableTest, SpellChecker | Double hashing and spell checking / 双重哈希与拼写检查 |

## Attribution / 贡献范围

These are coursework implementations built on course-supplied classes. ArtPiece, DLNode, DoublyLinkedList, BinarySearchTree, Student and StudentTreeNode retain Andrea Zanibellato's original attribution. Those support classes are included for compilation, and are not claimed as original work by Boxiao Xu. Original implementation and test files retain their author comments. Course templates and third-party components retain their original ownership; no blanket license is added.

本人的实现与测试按上表标明；教师提供的父类、节点与接口保留原署名，不归为本人原创。归档保持历史实现，未重写算法。

## Build / 编译

Use a JDK (validated with JDK 21). From this directory:

```powershell
javac -encoding UTF-8 -d out assignment1/*.java assignment2/*.java assignment3/BinarySearchTree.java assignment3/Student.java assignment3/StudentTreeNode.java assignment3/StudentTree.java assignment3/StudentTreeReader.java assignment4/MyHashTable.java assignment4/SpellChecker.java
java -cp out assignment2.MyListTest
```

StudentTreeTest and MyHashTableTest require JUnit Jupiter 5; add it to your IDE/build classpath. JUnit tests are archived as written, not claimed to have been run in this publication pass. Student CSV data, spreadsheets, compiled classes and Eclipse metadata are excluded. / JUnit 测试需另配依赖；本次不声称已运行。未上传学生数据表、编译产物和 IDE 缓存。

