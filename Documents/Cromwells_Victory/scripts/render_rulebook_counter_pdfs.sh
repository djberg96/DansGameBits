#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
counter_dir="$project_dir/images/counters"
output_dir="$project_dir/images/rulebook-counters"

mkdir -p "$output_dir"

rsvg-convert -f pdf -o "$output_dir/urry-front.pdf" \
  "$counter_dir/Rupert/urry.svg"
rsvg-convert -f pdf -o "$output_dir/urry-back.pdf" \
  "$counter_dir/Rupert/urry_back.svg"
rsvg-convert -f pdf -o "$output_dir/cromwell-leader-front.pdf" \
  "$counter_dir/Manchester/cromwell_leader.svg"
rsvg-convert -f pdf -o "$output_dir/leven-artillery-1-front.pdf" \
  "$counter_dir/Leven/artillery_1.svg"
rsvg-convert -f pdf -o "$output_dir/leven-artillery-1-back.pdf" \
  "$counter_dir/Leven/artillery_1_back.svg"

printf 'Rendered rulebook counter PDFs in %s\n' "$output_dir"
