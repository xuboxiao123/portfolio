package assignment1;
/** 
* COMPX201Assignment1
* ArtPieceOnSale class BDI2202
* @author XuBoxiao 32211052 */ 
import java.text.DecimalFormat;
public class ArtPieceOnSale extends ArtPiece{
	private double price;  // Price of the art piece
    private boolean taxable; // Availability status of the art piece
    private String seller;
    DecimalFormat df = new DecimalFormat("#.00");

	public ArtPieceOnSale(String title, String author, String type, String code, int year,double price,boolean taxable,String seller) {
		super(title, author, type, code, year);
		this.price = price;
		this.taxable = taxable;
		this.seller = seller;
		// TODO Auto-generated constructor stub
	}
	public String getter() {
		
		if (seller == null || seller.isEmpty() || seller.equalsIgnoreCase("secret")) {
            return "Information not available";
        }
        return seller;
	}
	@Override
	protected String getPieceDetails(){
	    return super.getPieceDetails() + 
	           " Price: $" + df.format(price) +
	           " Taxable: " + (taxable ? "Yes" : "No") + 
	           " Seller: " + getter();
	}
	public double getTotalCost() {
        if (taxable) {
            return price * 1.13; // 13% tax
        }
        return price;
    }
	

	
	
	
}
