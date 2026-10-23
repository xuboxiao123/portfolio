package assignment3;



/**
 * Class for the nodes used in the tree. 
 * Each node has two references to a left and right TreeNode which provide 
 * the necessary links for the tree.
 * This class is part of COMPX201-21X Assignment 3. It should not be modified in any way.
 * 
 * @author Andrea Zanibellato
 * @date Nov 2021
 */
public class StudentTreeNode {
	private Student data;
	private StudentTreeNode left;
	private StudentTreeNode right;
	
	/**
	 * Creates a tree node containing the given Student.
	 * @param data the Student to insert in the node
	 */
	public StudentTreeNode(Student data) {
		this.data = data;
	}

	/**
	 * Returns the Student data stored in the node
	 * @return the Student data
	 */
	public Student getData() {
		return data;
	}

	/**
	 * Changes the Student data in the node
	 * @param data the data to set
	 */
	public void setData(Student data) {
		this.data = data;
	}

	/**
	 * Returns the left child node
	 * @return the left child node
	 */
	public StudentTreeNode getLeft() {
		return left;
	}

	/**
	 * Changes the left child node
	 * @param left the new node to set as the left child
	 */
	public void setLeft(StudentTreeNode left) {
		this.left = left;
	}

	/**
	 * Returns the right child node
	 * @return the right child node
	 */
	public StudentTreeNode getRight() {
		return right;
	}

	/**
	 * Changes the right child node
	 * @param right the new node to set as the right child
	 */
	public void setRight(StudentTreeNode right) {
		this.right = right;
	}
	
	
}