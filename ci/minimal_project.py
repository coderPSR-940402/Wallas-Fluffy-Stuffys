#!/usr/bin/env python3
import os, shutil
from pathlib import Path
from PIL import Image
from neon_catalog import APPS
from neon_art import generate_icon

root = Path(os.environ.get('NEON_PROJECT_DIR', 'neon_icon_pack')).resolve()
if root.exists(): shutil.rmtree(root)
app = root/'app'; main = app/'src/main'; res = main/'res'
for d in [main/'java/com/neonplush/iconpack', res/'values', res/'xml', res/'drawable-nodpi', main/'assets']:
    d.mkdir(parents=True, exist_ok=True)

(root/'settings.gradle').write_text("""pluginManagement { repositories { google(); mavenCentral(); gradlePluginPortal() } }
dependencyResolutionManagement { repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS); repositories { google(); mavenCentral() } }
rootProject.name='NeonPlushCircuitIconPack'
include ':app'
""")
(root/'build.gradle').write_text("""plugins { id 'com.android.application' version '8.6.1' apply false }
""")
(root/'gradle.properties').write_text("org.gradle.jvmargs=-Xmx2g -Dfile.encoding=UTF-8\nandroid.useAndroidX=false\n")
(app/'build.gradle').write_text("""plugins { id 'com.android.application' }
android {
  namespace 'com.neonplush.iconpack'
  compileSdk 34
  defaultConfig { applicationId 'com.neonplush.iconpack'; minSdk 26; targetSdk 34; versionCode 1; versionName '1.0.0' }
}
""")
(main/'AndroidManifest.xml').write_text("""<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
 <application android:theme="@style/AppTheme" android:label="@string/app_name" android:icon="@drawable/ic_pack_launcher" android:roundIcon="@drawable/ic_pack_launcher">
  <activity android:name=".MainActivity" android:exported="true">
   <intent-filter><action android:name="android.intent.action.MAIN"/><category android:name="android.intent.category.LAUNCHER"/></intent-filter>
   <intent-filter><action android:name="org.adw.launcher.THEMES"/><action android:name="com.anddoes.launcher.THEME"/><action android:name="com.novalauncher.THEME"/></intent-filter>
   <meta-data android:name="com.novalauncher.THEME" android:resource="@xml/appfilter"/>
  </activity>
 </application>
</manifest>
""")
(res/'values/strings.xml').write_text('''<?xml version="1.0" encoding="utf-8"?><resources><string name="app_name">Neon Plush Circuit</string></resources>''')
(res/'values/styles.xml').write_text('''<?xml version="1.0" encoding="utf-8"?><resources><style name="AppTheme" parent="android:style/Theme.Material.NoActionBar"><item name="android:fontFamily">sans</item><item name="android:colorAccent">#FF35C1</item><item name="android:navigationBarColor">#0E0716</item><item name="android:statusBarColor">#0E0716</item></style></resources>''')
(main/'java/com/neonplush/iconpack/MainActivity.java').write_text('''package com.neonplush.iconpack;
import android.app.Activity; import android.os.Bundle; import android.graphics.Color; import android.view.Gravity; import android.widget.*;
public class MainActivity extends Activity {
 @Override public void onCreate(Bundle b){ super.onCreate(b); LinearLayout v=new LinearLayout(this); v.setOrientation(LinearLayout.VERTICAL); v.setGravity(Gravity.CENTER); v.setPadding(48,48,48,48); v.setBackgroundColor(Color.rgb(14,7,22)); ImageView i=new ImageView(this); i.setImageResource(com.neonplush.iconpack.R.drawable.ic_pack_launcher); v.addView(i,new LinearLayout.LayoutParams(256,256)); TextView t=new TextView(this); t.setText("Neon Plush Circuit\\n156 fluffy 3D neon icons\\n\\nApply from your launcher’s Icon Pack / Theme settings.\\nNova • Action • Smart • Total Launcher"); t.setTextColor(Color.WHITE); t.setTextSize(20); t.setGravity(Gravity.CENTER); v.addView(t); setContentView(v); }
}
''')

items=[f'    <item component="ComponentInfo{{{pkg}/{activity}}}" drawable="ic_{drawable}" />' for label,pkg,activity,drawable,symbol in APPS]
appfilter='<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'+'\n'.join(items)+'\n</resources>\n'
drawable='<?xml version="1.0" encoding="utf-8"?>\n<resources>\n'+'\n'.join(f'    <item drawable="ic_{drawable}" />' for label,pkg,activity,drawable,symbol in APPS)+'\n</resources>\n'
(res/'xml/appfilter.xml').write_text(appfilter); (res/'xml/drawable.xml').write_text(drawable)
(main/'assets/appfilter.xml').write_text(appfilter); (main/'assets/drawable.xml').write_text(drawable)

out=res/'drawable-nodpi'
for label,pkg,activity,drawable_name,symbol in APPS: generate_icon(symbol).save(out/f'ic_{drawable_name}.png')
generate_icon('perplexity').save(out/'ic_pack_launcher.png')
components=[f'{p}/{a}' for _,p,a,_,_ in APPS]
assert len(components)==len(set(components))==156
assert len(list(out.glob('ic_*.png')))==157
for p in out.glob('*.png'):
    im=Image.open(p).convert('RGBA'); assert im.size==(512,512) and im.getchannel('A').getbbox()
print(f'Generated {len(APPS)} mapped icons and Android project at {root}')
