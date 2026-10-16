@echo off

echo Acceso a Directorios

cmdkey /delete:172.16.111.3
cmdkey /add:172.16.111.3 /user:dfp_usuario /pass:dfp_usuario
start \\172.16.111.3\Dfp_Archivo\

timeout 8

