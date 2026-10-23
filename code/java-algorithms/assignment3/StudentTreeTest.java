package assignment3;



/** 
* COMPX201Assignment2
* ArtPieceOnSale class BDI2202
* @author XuBoxiao 32211052 */ 
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class StudentTreeTest {

    private StudentTree studentTree;

    @BeforeEach
    void setUp() {
        studentTree = new StudentTree();
    }

    @Test
    void testInsertAndInOrderTraversal() {
        Student student1 = new Student("123", "Doe", "John", 85);
        Student student2 = new Student("124", "Smith", "Jane", 90);
        Student student3 = new Student("125", "Brown", "Charlie", 80);

        studentTree.insert(student1);
        studentTree.insert(student2);
        studentTree.insert(student3);

        String expected = "Student{id='125', lastName='Brown', firstName='Charlie', points=80},Student{id='123', lastName='Doe', firstName='John', points=85},Student{id='124', lastName='Smith', firstName='Jane', points=90}";
        assertEquals(expected, studentTree.inOrderToString());
    }

    @Test
    void testCountTotalStudents() {
        Student student1 = new Student("123", "Doe", "John", 85);
        Student student2 = new Student("124", "Smith", "Jane", 90);

        studentTree.insert(student1);
        studentTree.insert(student2);

        assertEquals(2, studentTree.countTotalStudents());
    }

    @Test
    void testMaxPoints() {
        Student student1 = new Student("123", "Doe", "John", 85);
        Student student2 = new Student("124", "Smith", "Jane", 90);
        Student student3 = new Student("125", "Brown", "Charlie", 80);

        studentTree.insert(student1);
        studentTree.insert(student2);
        studentTree.insert(student3);

        assertEquals(90, studentTree.maxPoints());
    }

    @Test
    void testFindStudent() {
        Student student1 = new Student("123", "Doe", "John", 85);
        Student student2 = new Student("124", "Smith", "Jane", 90);

        studentTree.insert(student1);
        studentTree.insert(student2);

        assertTrue(studentTree.find(student1));
        assertFalse(studentTree.find(new Student("999", "Not", "InTree", 50)));
    }

    @Test
    void testRemoveStudent() {
        Student student1 = new Student("123", "Doe", "John", 85);
        Student student2 = new Student("124", "Smith", "Jane", 90);
        studentTree.insert(student1);
        studentTree.insert(student2);

        studentTree.remove(student1);
        assertFalse(studentTree.find(student1));
        assertTrue(studentTree.find(student2));
    }

    @Test
    void testMaxId() {
        Student student1 = new Student("123", "Doe", "John", 85);
        Student student2 = new Student("124", "Smith", "Jane", 90);
        studentTree.insert(student1);
        studentTree.insert(student2);

        assertEquals("124", studentTree.maxId());
    }
}
