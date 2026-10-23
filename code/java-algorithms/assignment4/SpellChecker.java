
/** 
* COMPX201Assignment2
* SpellChecker class BDI2202
* @author XuBoxiao 32211052 */ 
import java.io.*;
import java.util.*;

public class SpellChecker {

    public static void main(String[] args) throws IOException {
        if (args.length != 1) {
            System.out.println("Usage: java SpellChecker <dictionary file>");
            return;
        }

        // Read the dictionary file
        String dictionaryFile = args[0];
        List<String> dictionary = new ArrayList<>();
        try (BufferedReader reader = new BufferedReader(new FileReader(dictionaryFile))) {
            String line;
            while ((line = reader.readLine()) != null) {
                dictionary.add(line.trim().toLowerCase());
            }
        }

        // Create a hash table and load the dictionary
        MyHashTable hashTable = new MyHashTable(dictionary.size() * 2);  // Double the size of dictionary
        if(dictionary.size()!=0) { // avoid dictionary is empty
        for (String word : dictionary) {
            hashTable.put(word);
        }

        Scanner scanner = new Scanner(System.in);
        while (true) {
            System.out.print("Enter a word (or 'exit' to quit): ");
            String inputWord = scanner.nextLine().toLowerCase();

            if (inputWord.equals("exit")) {
                break;
            }

            if (hashTable.has(inputWord)) {
                System.out.println("Correct");
            } else {
                System.out.println("Incorrect");
                List<String> similarWords = findSimilarWords(inputWord, hashTable);
                if (similarWords.isEmpty()) {
                    System.out.println("No similar words found.");
                } else {
                    System.out.println("Similar words: " + String.join(", ", similarWords));
                }
            }
        }
        

        scanner.close();}else {
        	 System.out.println("There is empty");
        	
        }
        
    }

    // Generate similar words by deleting one character, inserting one character, or swapping characters
    private static List<String> findSimilarWords(String word, MyHashTable hashTable) {
        Set<String> similarWords = new HashSet<>();

        // Deleting one character
        for (int i = 0; i < word.length(); i++) {
            String modified = word.substring(0, i) + word.substring(i + 1);
            if (hashTable.has(modified)) {
                similarWords.add(modified);
            }
        }

        // Inserting one character
        for (int i = 0; i <= word.length(); i++) {
            for (char c = 'a'; c <= 'z'; c++) {
                String modified = word.substring(0, i) + c + word.substring(i);
                if (hashTable.has(modified)) {
                    similarWords.add(modified);
                }
            }
        }

        // Swapping two adjacent characters
        for (int i = 0; i < word.length() - 1; i++) {
            char[] chars = word.toCharArray();
            char temp = chars[i];
            chars[i] = chars[i + 1];
            chars[i + 1] = temp;
            String modified = new String(chars);
            if (hashTable.has(modified)) {
                similarWords.add(modified);
            }
        }

        return new ArrayList<>(similarWords);
    }
}


