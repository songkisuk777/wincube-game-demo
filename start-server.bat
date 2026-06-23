@echo off
chcp 65001 > nul
cd /d "%~dp0"
echo.
echo ============================================
echo   WinCube 게임 데모 서버 (3종 게임)
echo ============================================
echo.
for /f "delims=" %%i in ('powershell -NoProfile -Command "(Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.InterfaceAlias -notmatch 'Loopback' -and $_.IPAddress -notlike '169.*' -and $_.IPAddress -notlike '127.*' } | Sort-Object PrefixLength | Select-Object -Last 1).IPAddress"') do set LOCAL_IP=%%i
echo  [ 노트북과 폰을 같은 WiFi에 연결하세요 ]
echo.
echo  폰 브라우저 주소창에 입력:
echo.
echo    ^>^>  http://%LOCAL_IP%:8000  ^<^<
echo.
echo  Ctrl+C 로 서버 종료
echo ============================================
echo.
python -m http.server 8000
pause
