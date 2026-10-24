import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.atomic.AtomicReference;
public class Main {
 public static void main(String[] args)throws Exception {
  AtomicReference<Double> temperature=new AtomicReference<>(26.5);
  HttpServer server=HttpServer.create(new InetSocketAddress("127.0.0.1",18867),0);
  server.createContext("/data",exchange->{
   int status=200;
   try {if(exchange.getRequestMethod().equals("POST")){
    double value=Double.parseDouble(new String(exchange.getRequestBody().readAllBytes(),StandardCharsets.UTF_8));
    if(!Double.isFinite(value)||value< -50||value>100)throw new IllegalArgumentException();temperature.set(value);
   }}catch(Exception e){status=400;}
   double value=temperature.get();String body="{\"service\":\"study-java\",\"temperature\":"+value+",\"command\":\""+(value>=28?"on":"off")+"\"}";
   byte[] bytes=body.getBytes(StandardCharsets.UTF_8);exchange.getResponseHeaders().set("Content-Type","application/json; charset=utf-8");exchange.sendResponseHeaders(status,bytes.length);exchange.getResponseBody().write(bytes);exchange.close();
  });server.start();System.out.println("Study Java backend: 127.0.0.1:18867");
 }
}
