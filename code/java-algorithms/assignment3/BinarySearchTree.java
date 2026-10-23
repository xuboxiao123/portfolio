package assignment3;


/**
 * This is an abstract class describing a partial implementation of a 
 * Binary Search Tree storing Student objects. The tree is sorted
 * by the property that all nodes to the left of the root are smaller and all
 * nodes to the right of the root are larger or equal, where the order is 
 * given by the compareTo method of Students.
 * This class is part of COMPX201-21X Assignment 3. It should not be modified in any way.
 * 
 * @author Andrea Zanibellato
 * @date Nov 2021
 */
public abstract class BinarySearchTree {
	
	protected StudentTreeNode root;
	
	/**
	 * Inserts a new Student into the tree, following the BST order
	 * 
	 * @param s the Student to insert
	 **/
	public abstract void insert(Student s);
	
	/**
	 * Checks if a Student is present in the tree or not. 
	 * Comparisons are made with the equals method of Student.
	 * 
	 * @param s the Student to search for
	 * @return true if the Student is in the tree, false if not present
	 */
	public abstract boolean find(Student s);
	
	/**
	 * Removes a given Student from the tree. 
	 * Comparisons are made with the equals method of Student.
	 * If the student is not present, the method does nothing
	 * and does not throw any exception.
	 * 
	 * @param s the Student to remove
	 */
	public abstract void remove(Student s);
	
	/**
	 * Performs an in-order traversal of the tree and returns one String containing 
	 * the Student data in order, separated by commas. The output format must use 
	 * the Student toString method and commas to separate student data:
	 * "id lastName firstName: points,id lastName firstName: points,id lastName firstName: points", 
	 * (no spaces between students) ex: "001 Smith John: 100,002 Black Jack: 80,003 Ross Jane: 85".
	 * 
	 * @return a String containing all the data of the tree in order in the format described
	 */
	public abstract String inOrderToString();
	
	/**
	 * Performs a traversal of the tree and returns the number of Students in the tree.
	 * The traversal order is not defined and should not matter.
	 * 
	 * @return an int representing the number of Students stored in the tree
	 */
	public abstract int countTotalStudents();
	
	/**
	 * Returns the maximum ID of the Students stored in the tree, or null if the tree is empty.
	 * @return the maximum ID stored in the tree
	 */
	public abstract String maxId();
	
	/**
	 * Returns the maximum points of the Students stored in the tree, or null if the tree is empty.
	 * @return the maximum points stored in the tree
	 */
	public abstract Integer maxPoints();
	
}
