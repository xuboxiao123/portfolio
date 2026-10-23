package assignment2;

/** 
 * This class describes an interface for a Doubly Linked List 
 * that can store collections of Strings.
 * A Doubly Linked List should keep references to its head and its tail.
 * It is to be used as part of COMPX201-21X Assignment 2.
 * This interface should not be modified in any way.
 * 
 * @author Andrea Zanibellato
 * @date Oct 2021
 */
public interface DoublyLinkedList {
	
	/**
	 * Checks if the list is empty
	 * @return true if empty, false if not empty
	 */
    boolean isEmpty();
    
    /**
     * Returns the String inside the head of the list
     * @return the String in the head
     */
    String getHead();
    
    /**
     * Returns the String inside the tail of the list
     * @return the String in the tail
     */
    String getTail();
    
    /**
     * Returns the size of the list
     * @return the number of nodes currently in the list
     */
    int size();
    
    
    /**
     * Checks if a given String is present in the list or not
     * @param item the item to find
     * @return true if the String is present in the list, false otherwise
     */
    boolean find(String item);
    
    /**
     * Adds a given String to the head of the list
     * @param item the String to add
     */
    void addToHead(String item);
    
    /**
     * Adds a given String to the tail of the list
     * @param item the String to add
     */
    void addToTail(String item);
    
    /**
     * Adds a given String as a node in the given position.
     * In a list of size n, position 0 is the head of the list,
     * position 1 is between the head and the second element and so on,
     * position n-1 is before the tail of the list and position n
     * is at the tail of the list.
     * If the position is negative, or the position is greater than the list size,
     * the method throws an IndexOutOfBoundsException.
     * @param item the String to add
     * @param position the position where to place the new node
     */
    void addInPosition(String item, int position);
    
    /**
     * Removes the first occurrence (starting from the head) 
     * of the given String from the list if present. Does nothing if 
     * the String is not present.
     * @param item the String to remove
     */
    void removeFirstOccurrence(String item);
    
    /**
     * Removes all the occurrences of the given String from the list if present.
     * Does nothing if the String is not present.
     * @param item the String to remove
     */
    void removeAllOccurrences(String item);
    
    /**
     * Converts the list to an array of Strings, keeping the order of the list.
     * Example: the list ["d"]<->["r"]<->["s"]<->["a"] should return ["d","r","s","a"]
     * @return the array of Strings with all the elements of the list from head to tail
     */
    String[] toArray();
    
    /**
     * Converts the list to an array of Strings, in reverse order.
     * @return the array of Strings with all the elements of the list from tail to head
     */
    String[] toReversedArray();
    

}
