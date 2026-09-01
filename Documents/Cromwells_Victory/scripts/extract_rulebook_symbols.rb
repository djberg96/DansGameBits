#!/usr/bin/env ruby
# frozen_string_literal: true

project_dir = File.expand_path("..", __dir__)
output_dir = File.join(project_dir, "images", "rulebook-symbols")
Dir.mkdir(output_dir) unless Dir.exist?(output_dir)

symbols = {
  "foot" => {
    source: "images/counters/Newcastle/newcastle_infantry_1.svg",
    x: 24, y: 5, width: 52, height: 90
  },
  "light-horse" => {
    source: "images/counters/Leven/balcares.svg",
    x: 8, y: 17, width: 84, height: 66
  },
  "heavy-horse" => {
    source: "images/counters/Rupert/urry.svg",
    x: 9, y: 11, width: 82, height: 78
  }
}.freeze

symbols.each do |name, spec|
  source = File.read(File.join(project_dir, spec.fetch(:source)))
  nested = source.match(%r{<svg x="[^"]+" y="[^"]+" width="[^"]+" height="[^"]+" viewBox="[^"]+"[^>]*>.*?</svg>}m)
  abort "Could not find unit symbol in #{spec.fetch(:source)}" unless nested

  symbol = nested[0].sub(/\A<svg\b[^>]*>/) do |opening|
    view_box = opening.match(/viewBox="[^"]+"/)[0]
    format(
      '<svg x="%d" y="%d" width="%d" height="%d" %s preserveAspectRatio="xMidYMid meet">',
      spec.fetch(:x), spec.fetch(:y), spec.fetch(:width), spec.fetch(:height), view_box
    )
  end

  output = <<~SVG
    <?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
      #{symbol}
    </svg>
  SVG

  File.write(File.join(output_dir, "#{name}.svg"), output)
end

File.write(
  File.join(output_dir, "dragoon.svg"),
  <<~SVG
    <?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" width="100" height="100" viewBox="0 0 100 100">
      <polygon points="22,50 36,28 64,28 78,50 64,72 36,72" fill="#111510"/>
    </svg>
  SVG
)

puts "Extracted rulebook symbols in #{output_dir}"
