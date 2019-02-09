#!/bin/sh
if [ "$#" -ne 1 ]; then
    echo "error" $#
    exit 1
fi

sedstr=""
counter="0"
for x in `basename "$1" | tr ';' '\n'`; do
    sedstr="${sedstr} | sed s/:${counter}\$/:${x}/"
    counter=`expr "$counter" + 1`
done

cat <<'EOF'
#!/bin/sh
set -eu
if [ "$#" -lt 1 ]; then
    echo "${0} FILE1 FILE2 FILE3 ..."
    exit 1
fi

args=""
for f in "$@"; do
    dst="/tmp/$(basename "$f").ppm"
    convert "$f" -resize '150x150!' "$dst"
    args="${args} \"${dst}\""
done

sed '1,18 d' < "$0" | tar zxf - -C /
sh -c "/tmp/phonto/phonto /tmp/phonto/model.json ${args}" | grep predictresult | sed s/predictresult// | sed s%/tmp/%% | sed s/\.ppm// > /tmp/result.txt
EOF
echo sh -c "'cat /tmp/result.txt ${sedstr}'"
echo "exit 0"
