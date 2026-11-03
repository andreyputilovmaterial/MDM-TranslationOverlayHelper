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
echo "Update program version"
mkdir -p src/GENERATED
printf "%s\n" "'''For auto-generated files'''" > src/GENERATED/__init__.py
printf "%s\n" "# THIS IS AUTO-GENERATED" > src/GENERATED/_VERSION.py
python -c "from datetime import datetime; print(f'# {datetime.now()}')" >> src/GENERATED/_VERSION.py
printf "%s\n" "_VERSION = '''" >> src/GENERATED/_VERSION.py
git describe --tags --dirty >> src/GENERATED/_VERSION.py
printf "%s\n" "'''" >> src/GENERATED/_VERSION.py
echo "Done"

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
echo "Bring LICENSE and README.md to dist..."
cp LICENSE dist/LICENSE
cp README.md dist/README.md
echo "Done"

echo "-"
echo "-"
echo "Inline run_init (venv setup + explicit pip installs) into dist launchers..."
python src_dev_build/inline_run_init.py || fail
echo "Done"

echo "-"
echo "-"
echo "Verify the bundle: run --program done..."
python dist/mdmoverlayhelper_bundle.py --program done || fail
echo "Done"

echo "End"
