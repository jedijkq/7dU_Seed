#!/usr/bin/env bash
set -euo pipefail
# Generate SHA-256 checksums for all files in this directory (excluding the manifest itself)
outfile="sha256_manifest.txt"
tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT

# Exclude the manifest and common web files we don't want to hash
exclude_regex="(sha256_manifest\.txt|index\.html|README\.md|LICENSE\.txt|CITATION\.cff|compute_hashes\.sh|supplementary_summary\.md)$"

: > "$tmp"
for f in *; do
  if [[ -f "$f" ]] && ! [[ "$f" =~ $exclude_regex ]]; then
    sha256sum "$f" >> "$tmp"
  fi
done

mv "$tmp" "$outfile"
echo "Wrote $outfile"
