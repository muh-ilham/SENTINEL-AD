@echo off
setlocal enabledelayedexpansion
title SENTINEL-AD - Update GitHub

echo ============================================================
echo   SENTINEL-AD - Sinkronisasi Perubahan ke GitHub
echo ============================================================
echo.

git status
echo.
set /p commit_msg="Masukkan pesan commit (tekan ENTER untuk 'update code'): "
if "%commit_msg%"=="" (
    set commit_msg=update code
)

echo.
echo 1. Menambahkan perubahan (git add)...
git add .

echo 2. Menyimpan commit (git commit)...
git commit -m "%commit_msg%"

echo 3. Mengirim ke GitHub (git push)...
git push origin main

echo.
echo ============================================================
echo   Selesai! Perubahan telah terkirim ke GitHub.
echo ============================================================
pause
