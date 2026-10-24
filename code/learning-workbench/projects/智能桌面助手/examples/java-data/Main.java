import java.util.*;
public class Main {
    record Reading(String device,double temperature) {}
    public static void main(String[] args){
        List<Reading> data=List.of(new Reading("desk-01",26.5),new Reading("desk-02",29));
        for(Reading r:data)System.out.println(r.device()+" -> "+(r.temperature()>=28?"on":"off"));
    }
}