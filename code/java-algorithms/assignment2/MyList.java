package assignment2;
/** 
* COMPX201Assignment2
* ArtPieceOnSale class BDI2202
* @author XuBoxiao 32211052 */ 
public class MyList implements DoublyLinkedList {
	private DLNode head;
    private DLNode tail;
    private int size;

    public MyList() {
        head = null;
        tail = null;
        size = 0;
    }

    @Override
    public boolean isEmpty() {
        return size == 0;
    }

    @Override
    public String getHead() {
        if (isEmpty()) {
            return null; // or throw an exception
        }
        return head.getData();
    }

    @Override
    public String getTail() {
        if (isEmpty()) {
            return null; // or throw an exception
        }
        return tail.getData();
    }

    @Override
    public int size() {
        return size;
    }

    @Override
    public boolean find(String item) {
        DLNode current = head;
        while (current != null) {
            if (current.getData().equals(item)) {
                return true;
            }
            current = current.getNext();
        }
        return false;
    }

    @Override
    public void addToHead(String item) {
        DLNode newNode = new DLNode(item);
        if (isEmpty()) {
            head = tail = newNode;
        } else {
            newNode.setNext(head);
            head.setPrev(newNode);
            head = newNode;
        }
        size++;
    }

    @Override
    public void addToTail(String item) {
        DLNode newNode = new DLNode(item);
        if (isEmpty()) {
            head = tail = newNode;
        } else {
            tail.setNext(newNode);
            newNode.setPrev(tail);
            tail = newNode;
        }
        size++;
    }

    @Override
    public void addInPosition(String item, int position) {
        
        if (position == 0) {
            addToHead(item);
        } else if (position == size) {
            addToTail(item);
        } else {
            DLNode newNode = new DLNode(item);
            DLNode current = head;
            for (int i = 0; i < position; i++) {
                current = current.getNext();
            }
            newNode.setPrev(current.getPrev());
            newNode.setNext(current);
            current.getPrev().setNext(newNode);
            current.setPrev(newNode);
            size++;
        }
    }

    @Override
    public void removeFirstOccurrence(String item) {
        DLNode current = head;
        while (current != null) {
            if (current.getData().equals(item)) {
                if (current == head) {
                    head = head.getNext();
                    if (head != null) {
                        head.setPrev(null);
                    } else {
                        tail = null; // List becomes empty
                    }
                } else if (current == tail) {
                    tail = tail.getPrev();
                    tail.setNext(null);
                } else {
                    current.getPrev().setNext(current.getNext());
                    current.getNext().setPrev(current.getPrev());
                }
                size--;
                return;
            }
            current = current.getNext();
        }
    }

    @Override
    public void removeAllOccurrences(String item) {
        DLNode current = head;
        while (current != null) {
            if (current.getData().equals(item)) {
                removeFirstOccurrence(item);
            }
            current = current.getNext();
        }
    }

    @Override
    public String[] toArray() {
        String[] array = new String[size];
        DLNode current = head;
        for (int i = 0; i < size; i++) {
            array[i] = current.getData();
            current = current.getNext();
        }
        return array;
    }

    @Override
    public String[] toReversedArray() {
        String[] array = new String[size];
        DLNode current = tail;
        for (int i = 0; i < size; i++) {
            array[i] = current.getData();
            current = current.getPrev();
        }
        return array;
    }
}
