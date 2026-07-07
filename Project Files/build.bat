@echo off
rem Non-interactive build. Usage: build.bat <Target>  (Debug|Release|FinalRelease|Assert|Profile)
SET STRAWBERRY=z:\home\steve\workspace\wtp_automate\strawberry
SET PATH=%STRAWBERRY%\perl\bin;%STRAWBERRY%\perl\site\bin;%STRAWBERRY%\c\bin;%PATH%;..\..\Compiler\Microsoft Visual C++ Toolkit 2003\bin
set TARGET=%1
if "%TARGET%"=="" set TARGET=Release
bin\jom source_list /NOLOGO && nmake precompile /NOLOGO && bin\jom build
