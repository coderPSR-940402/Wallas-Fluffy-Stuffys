package com.wallathemes.fluffystuffys;

import android.app.Activity;
import android.os.Bundle;
import android.widget.TextView;

public final class MainActivity extends Activity {
    @Override public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        TextView view = new TextView(this);
        view.setText("Walla's Fluffy Stuffy's\n\nIcon pack assets are installed.");
        view.setTextSize(20f);
        view.setPadding(48, 48, 48, 48);
        setContentView(view);
    }
}
