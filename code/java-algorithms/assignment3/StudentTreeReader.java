package assignment3;

/** 
* COMPX201Assignment2
* ArtPieceOnSale class BDI2202
* @author XuBoxiao 32211052 */ 

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;

public class StudentTreeReader {

    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Please provide a filename.");
            return;
        }
        System.out.println("NZUWI2024F_COMPX201");
        

        String filename = args[0];
        StudentTree studentTree = new StudentTree();
        
        

        try (BufferedReader br = Files.newBufferedReader(Paths.get(filename))) {
            String line;
            br.readLine(); // Skip header line
            while ((line = br.readLine()) != null) {
                String[] data = line.split(",");
                String lastName = data[0].trim();
                String firstName = data[1].trim();
                String id = data[2].trim();
                int points = Integer.parseInt(data[3].trim());

                Student student = new Student(id, lastName, firstName, points);
                studentTree.insert(student);
                System.out.println();
            }

            System.out.println(studentTree.inOrderToString());
            System.out.println("Total number of students: " + studentTree.countTotalStudents());
            Integer maxPoints = studentTree.maxPoints();
            System.out.println("Maximum points: " + (maxPoints != null ? maxPoints : "None"));

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
