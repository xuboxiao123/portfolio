


/** 
* COMPX201Assignment4
* MyHashTable class BDI2202
* @author XuBoxiao 32211052 */ 
import java.util.Arrays;

public class MyHashTable {
    private String[] table;
    private int size;
    private int capacity;

    // Constructor to create an empty table with a given size
    public MyHashTable(int capacity) {
        this.capacity = capacity;
        this.table = new String[capacity];
        this.size = 0;
    }

    // Primary hash function (based on the String's hashCode)
    private int primaryHash(String s) {
    	
        return Math.abs(s.hashCode()) % capacity;
    }

    // Secondary hash function (ensuring it never returns 0)
    private int secondaryHash(String s) {
        int hash = Math.abs(s.hashCode()) % (capacity - 1) + 1;  // Ensuring it never returns 0
        return hash;
    }

    // Method to put a string in the hash table
    public void put(String s) {
        if (size >= capacity) {
            throw new IllegalStateException("Hash table is full");
        }
        int index = primaryHash(s);
        int step = secondaryHash(s);

        // Probing to resolve collisions using double hashing
        while (table[index] != null) {
            index = (index + step) % capacity;
        }
        table[index] = s;
        size++;
    }

    // Method to check if a string is in the hash table
    public boolean has(String s) {
        int index = primaryHash(s);
        int step = secondaryHash(s);

        // Probing to find the string
        while (table[index] != null) {
            if (table[index].equals(s)) {
                return true;
            }
            index = (index + step) % capacity;
        }
        return false;
    }

    // Method to get the load factor of the hash table
    public double getLoadFactor() {
        return (double) size / capacity;
    }
}

