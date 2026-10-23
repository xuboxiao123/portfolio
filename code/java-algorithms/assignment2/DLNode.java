package assignment2;

/** 
 * This class is a node to be used in the implementation of a 
 * Doubly Linked list storing Strings.
 * It is part of COMPX201-21X Assignment 2.
 * This class should not be modified in any way.
 * 
 * @author Andrea Zanibellato
 * @date Oct 2021
 */
public class DLNode {
	private String data;
	private DLNode prev;
	private DLNode next;
	
	/**
	 * Creates a node with the given data
	 * @param data The data in the node
	 */
	public DLNode(String data) {
		this.data = data;
	}

	/**
	 * Returns the data in the node
	 * @return the String in the node
	 */
	public String getData() {
		return data;
	}

	/**
	 * Returns the previous node
	 * @return previous node in the list
	 */
	public DLNode getPrev() {
		return prev;
	}

	/**
	 * Changes the link to the previous node
	 * @param prev the node to set as previous
	 */
	public void setPrev(DLNode prev) {
		this.prev = prev;
	}

	/**
	 * Returns the next node
	 * @return next node in the list
	 */
	public DLNode getNext() {
		return next;
	}

	/**
	 * Changes the link to the next node
	 * @param ext the node to set as previous
	 */
	public void setNext(DLNode next) {
		this.next = next;
	}
	
	
}
