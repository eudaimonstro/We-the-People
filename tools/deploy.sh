#!/bin/bash
# Copy built DLL + automation XML + changed Python screens into the installed
# WTP 4.2.1 mod.
# Usage: tools/deploy.sh            deploy built files (backs up originals once)
#        tools/deploy.sh --restore  put the stock files back
set -e
cd "$(dirname "$0")/.."
MOD="/home/steve/.local/share/Steam/steamapps/common/Civilization IV Colonization/Mods/WeThePeople-4.2.1"

# Files we deploy: source path (in repo) -> destination path (in mod), relative to Assets.
FILES=(
  "CvGameCoreDLL.dll"
  "XML/GlobalDefinesAlt.xml"
  "Python/Screens/CvEuropeScreen.py"
  "Python/Screens/CvTradeRoutesAdvisor.py"
)

if [ "$1" = "--restore" ]; then
  for f in "${FILES[@]}"; do
    [ -f "$MOD/Assets/$f.stock" ] && cp "$MOD/Assets/$f.stock" "$MOD/Assets/$f"
  done
  echo "Restored stock files."
  exit 0
fi

for f in "${FILES[@]}"; do
  [ -f "$MOD/Assets/$f.stock" ] || cp "$MOD/Assets/$f" "$MOD/Assets/$f.stock"
  cp "Assets/$f" "$MOD/Assets/$f"
done
echo "Deployed. Restore originals with: tools/deploy.sh --restore"
