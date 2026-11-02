#!/usr/bin/env bash
# POSIX (macOS / Linux) counterpart of build.bat.

set -u

fail() {
    echo "ERROR: Failure" >&2
    exit 1
}

echo "Clear up dist/..."
rm -rf dist
mkdir -p dist

echo "-"
echo "-"
echo "Build submodule src/lib/mdmreadpy (generates its GENERATED files)..."
(
    set -e
    cd src/lib/mdmreadpy
    bash build.sh
) || fail
echo "Done"

echo "Calling pinliner..."
python src_dev_build/lib/pinliner/pinliner/pinliner.py src -o dist/mdmoverlayhelper_bundle.py || fail
echo "Done"

echo "Patching mdmoverlayhelper_bundle.py..."
cat >> dist/mdmoverlayhelper_bundle.py <<'EOF'
# ...
# print('within mdmoverlayhelper_bundle')
from src import launcher
launcher.main()
# print('out of mdmoverlayhelper_bundle')
EOF
echo "Done"

echo "-"
echo "-"
echo "Copy BAT run scripts"
cp run_make_excel.bat dist/run_overlayhelper_excel.bat
cp run_produce_scripts.bat dist/run_overlayhelper_scripts.bat
sed -i.bak \
    -e 's#dist/mdmoverlayhelper_bundle\.py#mdmoverlayhelper_bundle.py#g' \
    dist/run_overlayhelper_excel.bat dist/run_overlayhelper_scripts.bat
rm -f dist/run_overlayhelper_excel.bat.bak dist/run_overlayhelper_scripts.bat.bak
echo "Done"

echo "-"
echo "-"
echo "Bring LICENSE, README.md and requirements.txt to dist..."
cp LICENSE dist/LICENSE
cp README.md dist/README.md
cp requirements.txt dist/requirements.txt
echo "Done"

echo "-"
echo "-"
echo "Collect optional per-submodule requirements into dist/optional_dependencies/"
mkdir -p dist/optional_dependencies
for requirements in $(find src/lib -type f -name 'requirements.txt' -not -path '*/.git/*' -not -path '*/dist/*' -not -path '*/GENERATED/*' | sort); do
    rel="${requirements#src/}"
    dest="dist/optional_dependencies/$rel"
    mkdir -p "$(dirname "$dest")"
    echo "copying optional requirements: $requirements -> $dest"
    cp "$requirements" "$dest"
done
echo "Done"

echo "-"
echo "-"
echo "Copy and adapt run_init scripts to dist..."
sed -e 's#src/lib#optional_dependencies#g' -e 's#-m src\.launcher#mdmoverlayhelper_bundle.py#g' run_init.sh > dist/run_init.sh
sed -e 's#src\\lib#optional_dependencies#g' -e 's#-m src\.launcher#mdmoverlayhelper_bundle.py#g' run_init.bat > dist/run_init.bat
chmod +x dist/run_init.sh
chmod +x dist/run_init.bat
echo "Done"

echo "-"
echo "-"
echo "Verifying the bundle imports correctly..."
python dist/mdmoverlayhelper_bundle.py --program done || fail
echo "Done"

echo "End"
