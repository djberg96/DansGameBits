#!/bin/sh
# Render the SVG sources needed by Washington's Crossing Playbook for the
# LaTeX svg package.  This deliberately uses librsvg, not Inkscape.
set -eu

script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
counter_dir="$script_dir/../../Counters/Washingtons_Crossing"
output_dir="$counter_dir/svg-inkscape"

mkdir -p "$output_dir"
for counter in \
  american-detachment-4 \
  american-leader-cadwalader \
  american-leader-dickinson \
  american-leader-fermoy \
  american-leader-greene \
  american-leader-hitchcock \
  american-leader-lord-stirling \
  american-leader-mcdougall \
  american-leader-mercer \
  american-leader-mifflin \
  american-leader-sargent \
  american-leader-sullivan \
  american-leader-washington \
  british-leader-rall \
  durham-boats \
  washington-leader-display
do
  rsvg-convert -f pdf -o "$output_dir/${counter}_svg-raw.pdf" "$counter_dir/$counter.svg"
done
