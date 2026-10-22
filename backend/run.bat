@echo off
rem 用 venv 里的 Python 启动后端（flask 等依赖都装在 venv 里）
cd /d %~dp0
venv\Scripts\python.exe run.py
pause
