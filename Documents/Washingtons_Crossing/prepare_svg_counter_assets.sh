#!/bin/sh
# Render the SVG sources needed by Washington's Crossing Playbook for the
# LaTeX svg package.  This deliberately uses librsvg, not Inkscape.
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
counter_dir="$script_dir/../../Counters/Washingtons_Crossing"
output_dir="$counter_dir/svg-inkscape"

mkdir -p "$output_dir"
for counter in american-leader-cadwalader british-leader-rall durham-boats washington-leader-display; do
  rsvg-convert -f pdf -o "$output_dir/${counter}_svg-raw.pdf" "$counter_dir/$counter.svg"
done
