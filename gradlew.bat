@echo off
setlocal
set "APP_HOME=%~dp0"
set "WRAPPER_DIR=%APP_HOME%gradle\wrapper"
set "WRAPPER_JAR=%WRAPPER_DIR%\gradle-wrapper.jar"
set "WRAPPER_URL=https://raw.githubusercontent.com/gradle/gradle/v8.7.0/gradle/wrapper/gradle-wrapper.jar"
set "WRAPPER_SHA256=cb0da6751c2b753a16ac168bb354870ebb1e162e9083f116729cec9c781156b8"

if not exist "%WRAPPER_DIR%" mkdir "%WRAPPER_DIR%"

powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$jar='%WRAPPER_JAR%'; $url='%WRAPPER_URL%'; $expected='%WRAPPER_SHA256%';" ^
  "$ok=(Test-Path $jar) -and ((Get-FileHash $jar -Algorithm SHA256).Hash.ToLower() -eq $expected);" ^
  "if(-not $ok){$tmp=$jar+'.tmp'; Invoke-WebRequest -UseBasicParsing -Uri $url -OutFile $tmp; $actual=(Get-FileHash $tmp -Algorithm SHA256).Hash.ToLower(); if($actual -ne $expected){Remove-Item -Force $tmp; Write-Error ('Gradle wrapper checksum mismatch: '+$actual); exit 1}; Move-Item -Force $tmp $jar}"
if errorlevel 1 exit /b 1

if defined JAVA_HOME (
  set "JAVA_EXE=%JAVA_HOME%\bin\java.exe"
) else (
  set "JAVA_EXE=java.exe"
)

"%JAVA_EXE%" %JAVA_OPTS% %GRADLE_OPTS% -Dorg.gradle.appname=gradlew -classpath "%WRAPPER_JAR%" org.gradle.wrapper.GradleWrapperMain %*
exit /b %ERRORLEVEL%
