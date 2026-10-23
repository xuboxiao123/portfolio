package assignment1;

/** 
 * This class describes a generic art piece of a gallery
 * It is to be used as part of COMPX201-22X Assignment1
 * This class should not be modified in any way
 * 
 * @author Andrea Zanibellato
 * @date Sep 2021
 */
public class ArtPiece {
	
	protected String title;
	protected String author;
	protected String type;
	protected String code;
	protected int year;
	
	/**
	 * Creates an ArtPiece. Requires all its data as parameters.
	 * @param title   the title of the art piece
	 * @param author  the author of the art piece
	 * @param type    the type of the piece
	 * @param code    the code of the piece
	 * @param year    the year of the piece
	 */
	public ArtPiece(String title, String author, String type, String code, int year){
		this.title = title;
		this.author = author;
		this.code = code;
		this.type = type;
		this.year = year;
	}

	/**
	 * @return The title of the art piece
	 */
	public String getTitle(){
		return title;
	}
	
	/**
	 * @return The author of the art piece
	 */
	public String getAuthor() {
		return author;
	}

	/**
	 * @return The type of the art piece
	 */
	public String getType() {
		return type;
	}

	/**
	 * @return The code of the art piece
	 */
	public String getCode() {
		return code;
	}

	/**
	 * @return The year of the art piece
	 */
	public int getYear() {
		return year;
	}
	
	
	/**
	 * Collects all the data of an item into a String
	 * @return The details of the art piece
	 */
	protected String getPieceDetails(){
		return ("Art piece: " + title + " by " + author + ", " + 
				type + ", code: " + code + ", year: " + year );
	}
	
	/**
	 * Prints out the data for an item to standard output
	 */
	public void printPieceDetails(){
		System.out.println(getPieceDetails());
	}

	
		
}