package com.myapplication.shlomi.ihome;

import android.content.Intent;
import android.os.AsyncTask;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import java.io.IOException;
import java.io.PrintWriter;
import java.net.Socket;

public class wifiConfig extends AppCompatActivity {
    private static Socket soc;
    private static PrintWriter writer;
    private String ip = "192.168.1.26";


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_wifi_config);

        Button button= (Button) findViewById(R.id.Next2);
        button.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                EditText name = (EditText) findViewById(R.id.wifiNameEdit);

                EditText pass = (EditText) findViewById(R.id.wifiPasswordEdit);

                String msg = name.getText().toString() + ", " + pass.getText().toString(); // get username and password

                //sendMessage(msg);
                myTask m = new myTask();
                m.execute(msg);

                Toast toast = Toast.makeText(getApplicationContext(), "message sent", Toast.LENGTH_LONG);
                toast.show();

                Intent myIntent = new Intent(wifiConfig.this,
                        MainPage.class);
                startActivity(myIntent);
            }
        });
    }

    class myTask extends AsyncTask<String,Void,Void>{
        @Override
        protected Void doInBackground(String... params) {
            try{
                soc = new Socket(ip, 8200); // open socket and send message
                writer = new PrintWriter(soc.getOutputStream());
                writer.write(params[0]);
                writer.flush();
                writer.close();
                soc.close();

            }catch(IOException e){
                e.printStackTrace();
            }
            return null;
        }
    }
}
