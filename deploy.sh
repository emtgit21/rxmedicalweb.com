#!/usr/bin/env bash
# Deploy this site's files to GoDaddy cPanel hosting via the cPanel UAPI.
#
# One-time setup: create an API token in cPanel (Security -> Manage API Tokens)
# and save it in ~/.config/godaddy-cpanel/env :
#   CPANEL_HOST=p3plzcpnl504300.prod.phx3.secureserver.net
#   CPANEL_USER=itjfn6oc46op
#   CPANEL_TOKEN=<your token>
#
# Usage: ./deploy.sh
# Note: uploads top-level files only (this starter site is a single index.html).
set -euo pipefail
source "$HOME/.config/godaddy-cpanel/env"
DOMAIN=$(basename "$(git rev-parse --show-toplevel)")
DEST="/home/${CPANEL_USER}/public_html/${DOMAIN}"
args=(); i=1
while IFS= read -r f; do
  args+=(-F "file-${i}=@${f}"); i=$((i+1))
done < <(git ls-files | grep -vE '^(\.cpanel\.yml|README\.md|deploy\.sh|\.github/)' | grep -v '/')
echo "Deploying ${DOMAIN} -> ${DEST}"
curl -sS -H "Authorization: cpanel ${CPANEL_USER}:${CPANEL_TOKEN}" \
  "https://${CPANEL_HOST}:2083/execute/Fileman/upload_files?overwrite=1&dir=${DEST}" "${args[@]}"
echo
echo "Done: https://${DOMAIN}/"
