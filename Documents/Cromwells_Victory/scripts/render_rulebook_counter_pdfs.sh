#!/bin/sh
set -eu

project_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
counter_dir="$project_dir/images/counters"
output_dir="$project_dir/images/rulebook-counters"
symbol_dir="$project_dir/images/rulebook-symbols"

mkdir -p "$output_dir"
ruby "$project_dir/scripts/extract_rulebook_symbols.rb"

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

rsvg-convert -f pdf -o "$symbol_dir/foot.pdf" \
  "$symbol_dir/foot.svg"
rsvg-convert -f pdf -o "$symbol_dir/light-horse.pdf" \
  "$symbol_dir/light-horse.svg"
rsvg-convert -f pdf -o "$symbol_dir/heavy-horse.pdf" \
  "$symbol_dir/heavy-horse.svg"
rsvg-convert -f pdf -o "$symbol_dir/dragoon.pdf" \
  "$symbol_dir/dragoon.svg"

printf 'Rendered rulebook counter PDFs in %s\n' "$output_dir"
