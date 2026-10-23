package assignment3;


/** 
 * This class holds information about students.
 * It is part of COMPX201-21X Assignment 3.
 * This class should not be modified in any way.
 * 
 * @author Andrea Zanibellato
 * @date Nov 2021
 */
public class Student implements Comparable<Student>{
	private String id;
	private String lastName;
	private String firstName;
	private int points;
	
	public Student(String id, String lastName, String firstName, int points) {
		this.id = id;
		this.lastName = lastName;
		this.firstName = firstName;
		this.points = points;
	}

	/**
	 * @return the id of the student
	 */
	public String getId() {
		return id;
	}

	/**
	 * @return the last name of the student
	 */
	public String getLastName() {
		return lastName;
	}

	/**
	 * @return the first name of the student
	 */
	public String getFirstName() {
		return firstName;
	}
	
	/**
	 * @return the student's points
	 */
	public int getPoints() {
		return points;
	}
	
	/**
	 * Compares students based on their id
	 * @param s the student to compare with this
	 * @return a negative number, zero or positive number if this student has an id
	 * smaller, equal or greater than the id of the given student 
	 */
	@Override
	public int compareTo(Student s) {
		return this.id.compareTo(s.id);
	}
	
	/**
	 * Indicates whether two students are equal based on their id
	 * @param o the object (Student) to compare with this
	 * @return true if the other object is a student and has the same id as this one,
	 * false otherwise
	 */
	@Override
	public boolean equals(Object o) {
		if (o instanceof Student) {
			Student s = (Student) o;
            return this.id.equals(s.id);
        } 
		return false;
	}
	
	/**
	 * Returns a String representation of a Student in the format 
	 * "id lastName firstName: points", i.e. "123456 Smith John: 100"
	 * @return a String representation of the Student
	 */
	@Override
	public String toString() {
		return id + " " + lastName + " " + firstName + ":" + points;
	}
}
