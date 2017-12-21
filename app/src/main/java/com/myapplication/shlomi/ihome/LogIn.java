package com.myapplication.shlomi.ihome;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;

public class LogIn extends AppCompatActivity {
    EditText userName;
    EditText pass;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_log_in);

        Button next = (Button) findViewById(R.id.btnNext);  // When next button is pressed
        next.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                userName = (EditText) findViewById(R.id.NameEdit);
                pass = (EditText) findViewById(R.id.PasswordEdit);
                //TODO VALIDATE INFORMATION WITH RASPBERRY PI

               // Intent myIntent = new Intent(LogIn.this,
                  //          Menu.class);
                //startActivity(myIntent);
            }

        });

        Button register = (Button) findViewById(R.id.btnRegister);  // When register button is pressed
        next.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                Intent myIntent = new Intent(LogIn.this,
                        Register.class);
                startActivity(myIntent);
            }

        });
    }
}

