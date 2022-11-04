#!/bin/bash

# source: https://github.com/terraform-providers/terraform-provider-aws/issues/10104

if [[ -z "${ATLAS_WORKSPACE_SLUG}" ]]; then
  APP="tail -r"
else
  APP="tac"
fi

THUMBPRINT=$(echo | openssl s_client -servername oidc.eks.${1}.amazonaws.com -showcerts -connect oidc.eks.${1}.amazonaws.com:443 2>&- | ${APP} | sed -n '/-----END CERTIFICATE-----/,/-----BEGIN CERTIFICATE-----/p; /-----BEGIN CERTIFICATE-----/q' | ${APP} | openssl x509 -fingerprint -noout | sed 's/://g' | awk -F= '{print tolower($2)}')
THUMBPRINT_JSON="{\"thumbprint\": \"${THUMBPRINT}\"}"
echo $THUMBPRINT_JSON