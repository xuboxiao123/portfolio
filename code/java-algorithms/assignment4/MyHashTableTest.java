

/** 
 * COMPX201Assignment4
 * MyHashTableTest class BDI2202
 * @author XuBoxiao 32211052
 */
import static org.junit.jupiter.api.Assertions.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

public class MyHashTableTest {
    private MyHashTable hashTable;

    /**
     * Initializes the hash table before each test.
     * Creates a hash table with an initial size of 10.
     * 
     * @throws Exception If the initialization fails, it throws an exception.
     */
    @BeforeEach
    public void setUp() throws Exception {
        // Initialize hash table with a size of 10
        hashTable = new MyHashTable(10);
    }

    /**
     * Tests the put and has methods to verify correct insertion and lookup of strings.
     * 
     * @param null.
     * @return void This method does not return any value.
     */
    @Test
    public void testPutAndHas() {
        // Insert "apple" into the hash table and check if it exists
        hashTable.put("apple");
        assertTrue(hashTable.has("apple"));  // Check if the hash table contains "apple"
        
        // Check that "banana" is not in the hash table
        assertFalse(hashTable.has("banana"));
    }

    /**
     * Tests the calculation of the load factor and verifies if it is calculated correctly.
     * 
     * @param null.
     * @return void This method does not return any value.
     */
    @Test
    public void testLoadFactor() {
        // Insert two elements into the hash table
        hashTable.put("apple");
        hashTable.put("banana");
        
        // Check the load factor, it should be 2/10 = 0.2
        assertEquals(0.2, hashTable.getLoadFactor());
    }

    /**
     * Tests collision resolution in the hash table.
     * Verifies that the hash table handles hash collisions correctly.
     * Assumes that "apple" and "pale" will hash to the same index.
     * 
     * @param null.
     * @return void This method does not return any value.
     */
    @Test
    public void testCollisionResolution() {
        // Insert "apple" and "pale" into the hash table, assuming a collision
        hashTable.put("apple");
        hashTable.put("pale");  // Might collide with "apple"
        
        // Ensure that both "apple" and "pale" exist in the hash table
        assertTrue(hashTable.has("apple"));
        assertTrue(hashTable.has("pale"));
    }

    /**
     * Tests that an IllegalStateException is thrown when trying to insert an element into a full hash table.
     * 
     * @param null.
     * @return void This method does not return any value.
     * @throws IllegalStateException If the hash table is full and an attempt to insert a new element is made.
     */
    @Test
    public void testTableFullException() {
        // Fill the hash table with 10 elements
        for (int i = 0; i < 10; i++) {
            hashTable.put("word" + i);  // Insert "word0" to "word9"
        }
        
        // Trying to insert a new element when the table is full should throw an IllegalStateException
        assertThrows(IllegalStateException.class, () -> hashTable.put("overflow"));
    }
}
