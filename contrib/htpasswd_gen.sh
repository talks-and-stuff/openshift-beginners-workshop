#!/bin/bash
set -e

if [ ! -f "$1" ]; then
    echo "'$1' is not a regular file" >&2
    exit 1
fi

input_file=$1

# generate the htpasswd file first
htpasswd_tmp="$(mktemp /tmp/htpasswd.XXXXX)"
while read -r line; do
    user=$(awk '{print $1}' <<< "$line" )
    passwd=$(awk '{print $2}' <<< "$line" )

    htpasswd -bB "$htpasswd_tmp" "$user" "$passwd"
done < "$input_file"

echo "populated $htpasswd_tmp with user credentials"

# use the file to create the htpasswd IdP in OpenShift
oc create secret generic htpasswd-secret -n openshift-config --from-file="htpasswd=$htpasswd_tmp"

oc apply -f - <<EOF
apiVersion: config.openshift.io/v1
kind: OAuth
metadata:
  name: cluster
spec:
  identityProviders:
  - name: htpassidp
    type: HTPasswd
    htpasswd:
      fileData:
        name: htpasswd-secret
EOF
