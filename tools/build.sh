#!/bin/bash
# Build the WTP DLL under Wine. Usage: tools/build.sh [Release|Assert|Debug|FinalRelease]
set -e
cd "$(dirname "$0")/../Project Files"
WINEDEBUG=-all wine cmd /c build.bat "${1:-Release}"
ls -la ../Assets/CvGameCoreDLL.dll
