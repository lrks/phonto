#!/bin/sh
if [ "$#" -ne 3 ]; then
    echo "error" $#
    exit 1
fi

class=`basename "$1"`
cat <<EOF
#!/bin/sh
set -eu
if [ "\$#" -lt 1 ]; then
    echo "\${0} FILE1 FILE2 FILE3 ..."
    exit 1
fi

args=""
for f in "\$@"; do
    dst="/tmp/\$(basename "\$f").ppm"
    convert "\$f" -resize '150x150!' "\$dst"
    args="\${args} \"\${dst}\""
done
EOF

echo 'cat <<INEOF | base64 -d | gzip -d > /tmp/model.json'
base64 $3
echo 'INEOF'

echo 'cat <<INEOF | base64 -d > /tmp/phonto'
base64 $2
echo 'INEOF'
echo 'chmod +x /tmp/phonto'

cat <<EOF
sh -c "/tmp/phonto /tmp/model.json \${args}" | grep predictresult | sed s/predictresult// > /tmp/result.txt
cat /tmp/result.txt | xargs -L1 -I{} sh -c "A=\\\$(basename '{}' | cut -d: -f1 | sed s/.ppm//);B=\\\$(expr \\\$(echo '{}' | cut -d':' -f2) + 1);C=\\\$(echo '$class' | cut -d';' -f\\\$B); echo \\\$A:\\\$C"
EOF
