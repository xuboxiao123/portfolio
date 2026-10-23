package assignment1;
/** 
* COMPX201Assignment1
* ArtPieceOnSale class BDI2202
* @author XuBoxiao 32211052 */ 
import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
public class Catalogue {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		ArrayList<ArtPiece> artPieces = new ArrayList<>();
		try (BufferedReader br = new BufferedReader(new FileReader("test.txt"))) {
            String line;
            while ((line = br.readLine()) != null) {
                if (line.equalsIgnoreCase("y")) {
                    // 读取 ArtPieceOnSale
                    String title = br.readLine();
                    String code = br.readLine();
                    String author = br.readLine();
                    String type = br.readLine();
                    int year = Integer.parseInt(br.readLine());
                    double price = Double.parseDouble(br.readLine());
                    boolean taxable = br.readLine().equalsIgnoreCase("Y");
                    String seller = br.readLine();
                    ArtPieceOnSale artPieceOnSale = new ArtPieceOnSale(title, author, type, code, year, price, taxable, seller);
                    artPieces.add(artPieceOnSale);
                } else {
                    // 读取 ArtPiece
                    String title = br.readLine();
                    String code = br.readLine();
                    String author = br.readLine();
                    String type = br.readLine();
                    int year = Integer.parseInt(br.readLine());
                    ArtPiece artPiece = new ArtPiece(title, author, type, code, year);
                    artPieces.add(artPiece);
                }
            }

        } catch (IOException e) {
            System.out.println("Error reading file: " + e.getMessage());
        }

        // 打印所有艺术作品的详细信息
        for (ArtPiece artPiece : artPieces) {
            artPiece.printPieceDetails();
            System.out.println();
        }
    }
		
		

	

}
