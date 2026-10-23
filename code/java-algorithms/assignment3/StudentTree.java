package assignment3;

/** 
* COMPX201Assignment2
* ArtPieceOnSale class BDI2202
* @author XuBoxiao 32211052 */ 

public class StudentTree extends BinarySearchTree {

    // Inserts a student into the tree
    @Override
    public void insert(Student s) {
        root = insertRec(root, s);
    }

    private StudentTreeNode insertRec(StudentTreeNode root, Student s) {
        if (root == null) {
            return new StudentTreeNode(s);
        }
        if (s.getPoints() < root.getData().getPoints() ) {
            root.setLeft(insertRec(root.getLeft(), s));
        } else {
            root.setRight(insertRec(root.getRight(), s));
        }
        return root;
    }

    // Finds a student in the tree
    @Override
    public boolean find(Student s) {
        return findRec(root, s);
    }

    private boolean findRec(StudentTreeNode root, Student s) {
        if (root == null) {
            return false;
        }
        if (s.equals(root.getData())) {
            return true;
        } else if (s.compareTo(root.getData()) < 0) {
            return findRec(root.getLeft(), s);
        } else {
            return findRec(root.getRight(), s);
        }
    }

    // Removes a student from the tree
    @Override
    public void remove(Student s) {
        root = removeRec(root, s);
    }

    private StudentTreeNode removeRec(StudentTreeNode root, Student s) {
        if (root == null) {
            return null;
        }

        if (s.equals(root.getData())) {
            // Case 1: No child
            if (root.getLeft() == null && root.getRight() == null) {
                return null;
            }
            // Case 2: One child
            if (root.getLeft() == null) {
                return root.getRight();
            } else if (root.getRight() == null) {
                return root.getLeft();
            }
            // Case 3: Two children
            StudentTreeNode minNode = findMin(root.getRight());
            root.setData(minNode.getData());
            root.setRight(removeRec(root.getRight(), minNode.getData()));
            return root;
        }

        if (s.compareTo(root.getData()) < 0) {
            root.setLeft(removeRec(root.getLeft(), s));
        } else {
            root.setRight(removeRec(root.getRight(), s));
        }
        return root;
    }

    private StudentTreeNode findMin(StudentTreeNode root) {
        while (root.getLeft() != null) {
            root = root.getLeft();
        }
        return root;
    }

    // Performs in-order traversal and returns the tree data as a string
    @Override
    public String inOrderToString() {
        StringBuilder sb = new StringBuilder();
        inOrderRec(root, sb);
        return sb.toString();
    }

//    private void inOrderRec(StudentTreeNode root, StringBuilder sb) {
//        if (root != null) {
//            inOrderRec(root.getLeft(), sb);
//            if (sb.length() > 0) sb.append(",");
//            sb.append(root.getData().toString());
//            inOrderRec(root.getRight(), sb);
//        }
//    }
    
  

    private void inOrderRec(StudentTreeNode root, StringBuilder sb) {
        if (root != null) {
            inOrderRec(root.getLeft(), sb);  // 遍历左子树
            if (sb.length() > 0) {
                sb.append(",");  // 在节点之间添加逗号
                
            }
            // 自定义格式输出
            sb.append("Student{id='")
              .append(root.getData().getId())
              .append("', lastName='")
              .append(root.getData().getLastName())
              .append("', firstName='")
              .append(root.getData().getFirstName())
              .append("', points=")
              .append(root.getData().getPoints())
              .append("}");
            inOrderRec(root.getRight(), sb);  // 遍历右子树
        }
        
    }

    // Counts total number of students in the tree
    @Override
    public int countTotalStudents() {
        return countRec(root);
    }

    private int countRec(StudentTreeNode root) {
        if (root == null) {
            return 0;
        }
        return 1 + countRec(root.getLeft()) + countRec(root.getRight());
    }

    // Finds the student with the maximum ID
    @Override
    public String maxId() {
        return findMaxId(root);
    }

    private String findMaxId(StudentTreeNode root) {
        if (root == null) {
            return null;
        }
        while (root.getRight() != null) {
            root = root.getRight();
        }
        return root.getData().getId();
    }

    // Finds the student with the maximum points
    @Override
    public Integer maxPoints() {
        return findMaxPoints(root);
    }

    private Integer findMaxPoints(StudentTreeNode root) {
        if (root == null) {
            return null;
        }
        int max = root.getData().getPoints();
        Integer leftMax = findMaxPoints(root.getLeft());
        Integer rightMax = findMaxPoints(root.getRight());

        if (leftMax != null) max = Math.max(max, leftMax);
        if (rightMax != null) max = Math.max(max, rightMax);

        return max;
    }
}
