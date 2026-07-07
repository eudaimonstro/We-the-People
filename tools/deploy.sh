#!/bin/bash
# Copy built DLL + automation XML into the installed WTP 4.2.1 mod.
# Usage: tools/deploy.sh            deploy built files (backs up originals once)
#        tools/deploy.sh --restore  put the stock files back
set -e
cd "$(dirname "$0")/.."
MOD="/home/steve/.local/share/Steam/steamapps/common/Civilization IV Colonization/Mods/WeThePeople-4.2.1"

if [ "$1" = "--restore" ]; then
  cp "$MOD/Assets/CvGameCoreDLL.dll.stock" "$MOD/Assets/CvGameCoreDLL.dll"
  cp "$MOD/Assets/XML/GlobalDefinesAlt.xml.stock" "$MOD/Assets/XML/GlobalDefinesAlt.xml"
  echo "Restored stock files."
  exit 0
fi

[ -f "$MOD/Assets/CvGameCoreDLL.dll.stock" ] || cp "$MOD/Assets/CvGameCoreDLL.dll" "$MOD/Assets/CvGameCoreDLL.dll.stock"
[ -f "$MOD/Assets/XML/GlobalDefinesAlt.xml.stock" ] || cp "$MOD/Assets/XML/GlobalDefinesAlt.xml" "$MOD/Assets/XML/GlobalDefinesAlt.xml.stock"
cp Assets/CvGameCoreDLL.dll "$MOD/Assets/CvGameCoreDLL.dll"
cp Assets/XML/GlobalDefinesAlt.xml "$MOD/Assets/XML/GlobalDefinesAlt.xml"
echo "Deployed. Restore originals with: tools/deploy.sh --restore"
