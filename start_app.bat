@echo off

echo ==========================================
echo Functional Test Case Generator
echo ==========================================

echo.
echo Checking Python environment...

call venv\Scripts\activate

echo.
echo Starting Streamlit application...
echo.

streamlit run app.py

pause