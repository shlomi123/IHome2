package com.myapplication.shlomi.ihome;

import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class Register extends AppCompatActivity {
    EditText userName;
    EditText pass;
    EditText codeEdit;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_register);

        codeEdit = (EditText) findViewById(R.id.CodeEdit);

        Button next = (Button) findViewById(R.id.btnNext);  // When next button is pressed
        next.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                String code = codeEdit.getText().toString();

                if (code.compareTo(getString(R.string.code)) != 0)  // If the code doesn't match the registration code
                {
                    Toast toast = Toast.makeText(getApplicationContext(), getString(R.string.error_wrongCode), Toast.LENGTH_LONG);
                    toast.show();
                }
                else
                {
                    userName = (EditText) findViewById(R.id.NameEdit);
                    pass = (EditText) findViewById(R.id.PasswordEdit);

                   //TODO  SEND INFO TO RASPBERRY PI


                    Intent myIntent = new Intent(Register.this,
                            LogIn.class);
                    startActivity(myIntent);
                }

            }
        });
    }
}