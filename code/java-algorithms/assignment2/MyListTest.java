package assignment2;
/** 
* COMPX201Assignment2
* ArtPieceOnSale class BDI2202
* @author XuBoxiao 32211052 */ 
public class MyListTest {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		MyList list = new MyList();

        // Test isEmpty
        System.out.println(list.isEmpty() ? "PASS" : "FAIL"); // Expected: PASS

        // Test addToHead
        list.addToHead("A");
        System.out.println(list.getHead().equals("A") ? "PASS" : "FAIL"); // Expected: PASS

        // Test size
        System.out.println(list.size() == 1 ? "PASS" : "FAIL"); // Expected: PASS

        // Test addToTail
        list.addToTail("B");
        System.out.println(list.getTail().equals("B") ? "PASS" : "FAIL"); // Expected: PASS

        // Test toArray
        String[] array = list.toArray();
        System.out.println(array[0].equals("A") && array[1].equals("B") ? "PASS" : "FAIL"); // Expected: PASS

        // Test toReversedArray
        String[] reversedArray = list.toReversedArray();
        System.out.println(reversedArray[0].equals("B") && reversedArray[1].equals("A") ? "PASS" : "FAIL"); // Expected: PASS

        // Test find
        System.out.println(list.find("A") ? "PASS" : "FAIL"); // Expected: PASS
        System.out.println(list.find("C") ? "FAIL" : "PASS"); // Expected: PASS

        // Test addInPosition
        list.addInPosition("C", 1);
        array = list.toArray();
        System.out.println(array[1].equals("C") ? "PASS" : "FAIL"); // Expected: PASS

        // Test removeFirstOccurrence
        list.removeFirstOccurrence("A");
        array = list.toArray();
        System.out.println(array[0].equals("C") ? "PASS" : "FAIL"); // Expected: PASS

        // Test removeAllOccurrences
        list.addToTail("B"); 
        list.addToTail("C");
        list.removeAllOccurrences("C");
        array = list.toArray();
        System.out.println(array.length == 2 && array[0].equals("B") ? "PASS" : "FAIL"); // Expected: PASS

        // Test removing from an empty list
        MyList emptyList = new MyList();
        emptyList.removeFirstOccurrence("A"); // Should not throw an error
        emptyList.removeAllOccurrences("B"); // Should not throw an error
        System.out.println(emptyList.size() == 0 ? "PASS" : "FAIL"); // Expected: PASS
    }

	}


