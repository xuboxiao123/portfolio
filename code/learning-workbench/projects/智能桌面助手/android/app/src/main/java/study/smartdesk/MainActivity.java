package study.smartdesk;
import android.app.Activity;
import android.os.Bundle;
import android.widget.*;
import org.json.JSONObject;
import java.net.*;
import java.io.*;
public class MainActivity extends Activity {
 private TextView result; private EditText address;
 public void onCreate(Bundle b){super.onCreate(b); LinearLayout box=new LinearLayout(this);box.setOrientation(1);box.setPadding(32,48,32,32);
 TextView title=new TextView(this);title.setText("智能桌面助手 · 手机界面");title.setTextSize(24);box.addView(title);
 TextView hint=new TextView(this);hint.setText("填写实际HTTPS接口。开发时可通过adb reverse把模拟器端口映射到电脑；本示例只读取状态，不连接真实硬件。");box.addView(hint);
 address=new EditText(this);address.setSingleLine(true);address.setHint("https://你的服务/data");box.addView(address);
 Button read=new Button(this);read.setText("读取产品状态");box.addView(read);result=new TextView(this);result.setText("先在学习工作台启动Java后端，再配置开发连接。");box.addView(result);setContentView(box);
 read.setOnClickListener(v->{String url=address.getText().toString().trim();read.setEnabled(false);result.setText("读取中…");new Thread(()->{String text;try{URL u=new URL(url);if(!u.getProtocol().equals("https")&&!u.getHost().equals("127.0.0.1"))throw new IOException("请输入HTTPS或本机开发接口");HttpURLConnection c=(HttpURLConnection)u.openConnection();c.setConnectTimeout(5000);c.setReadTimeout(5000);try{if(c.getResponseCode()!=200)throw new IOException("HTTP "+c.getResponseCode());ByteArrayOutputStream out=new ByteArrayOutputStream();try(InputStream in=c.getInputStream()){byte[] buf=new byte[1024];int n;while((n=in.read(buf))!=-1){out.write(buf,0,n);if(out.size()>65536)throw new IOException("响应过大");}}JSONObject data=new JSONObject(out.toString("UTF-8"));text="温度："+data.getDouble("temperature")+"℃\n控制命令："+data.getString("command");}finally{c.disconnect();}}catch(Exception e){text="连接失败："+e.getMessage();}String message=text;runOnUiThread(()->{result.setText(message);read.setEnabled(true);});}).start();});
 }
}
