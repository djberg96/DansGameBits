#!/usr/bin/env ruby
# frozen_string_literal: true

# Generates clean, standalone SVG recreations of the distinct counters on
# Washingtons_Crossing_Counters.png.  Each counter is deliberately vector-only:
# there are no embedded raster scans or external dependencies.

require 'fileutils'

OUTPUT = File.expand_path(__dir__)
SIZE = 300

AMERICAN_LEADERS = [
  ['washington', 'Washington', '4 ★ ★ ★ 6', '8', '4', '1 • 5'],
  ['sullivan', 'Sullivan', '3 ★ ★ 4', '5', '2', '3 • 3'],
  ['lord-stirling', 'Lord Stirling', '1 ★ 1', '5', '1', '2 • 2'],
  ['stephen', 'Stephen', '1 ★ 2', '4', '1', '1 • 3'],
  ['st-clair', 'St. Clair', '1 ★ 2', '5', '1', '1 • 3'],
  ['sargent', 'Sargent', '1 ★ 1', '4', '1', '1 • 3'],
  ['putnam', 'Putnam', '2 ★ ★ 2', '2', '1', '2 • 5'],
  ['mifflin', 'Mifflin', '1 ★ 2', '5', '1', '1 • 4'],
  ['mercer', 'Mercer', '1 ★ 1', '5', '1', '1 • 4'],
  ['mcdougall', 'McDougall', '1 ★ 1', '5', '1', '1 • 4'],
  ['dickinson', 'Dickinson', '1 ★ 1', '3', '1', '1 • 3'],
  ['cadwalader', 'Cadwalader', '2 ★ 2', '5', '2', '2 • 5'],
  ['griffin', 'Griffin', '1 ★ 1', '3', '1', '1 • 3'],
  ['hitchcock', 'Hitchcock', '1 ★ 1', '4', '1', '1 • 4'],
  ['glover', 'Glover', '1 ★ 1', '5', '1', '1 • 5'],
  ['greene', 'Greene', '3 ★ ★ 5', '6', '2', '2 • 6'],
  ['fermoy', 'Fermoy', '1 ★ 1', '2', '1', '1 • 2'],
  ['ewing', 'Ewing', '1 ★ 1', '4', '1', '1 • 4']
].freeze

BRITISH_LEADERS = [
  ['cornwallis', 'Cornwallis', '4', '6', '3', '5'],
  ['grant-1', 'Grant', '6', '3', '2', '3'],
  ['grant-2', 'Grant', '3', '3', '2', '3'],
  ['webster', 'Webster', '1', '3', '1', '3'],
  ['leslie', 'Leslie', '2', '4', '2', '3'],
  ['matthew', 'Matthew', '1', '3', '2', '3'],
  ['vaughan', 'Vaughan', '1', '3', '2', '3'],
  ['light-infantry', 'Light Infantry', '1', '3', '2', '3'],
  ['vanguard', 'Vanguard', '1', '5', '2', '3'],
  ['grenadiers', 'Grenadiers', '1', '3', '2', '3'],
  ['mawhood', 'Mawhood', '1', '5', '3', '3'],
  ['stirling', 'Stirling', '1', '3', '1', '3'],
  ['monckton', 'Monckton', '1', '4', '1', '3'],
  ['detachment-1', '( 1 )', '1', '3', '1', '3'],
  ['detachment-2', '( 2 )', '1', '3', '1', '3'],
  ['detachment-3', '( 3 )', '1', '3', '1', '3'],
  ['hessian-detachment-1', '( 1 )', '1', '3', '1', '3'],
  ['hessian-detachment-2', '( 2 )', '1', '3', '1', '3'],
  ['rall', 'Rall', '1', '5', '3', '5'],
  ['von-donop', 'von Donop', '2', '5', '1', '2']
].freeze

def escape(value)
  value.gsub('&', '&amp;').gsub('<', '&lt;').gsub('>', '&gt;')
end

def document(label, body)
  <<~SVG
    <?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 #{SIZE} #{SIZE}" role="img" aria-labelledby="title desc">
      <title id="title">#{escape(label)}</title>
      <desc id="desc">Vector recreation of the #{escape(label)} counter from Washington's Crossing.</desc>
      <defs>
        <pattern id="blueTexture" width="18" height="18" patternUnits="userSpaceOnUse">
          <rect width="18" height="18" fill="#083d4c"/>
          <path d="M0 3H18 M0 12H18" stroke="#b7d0c6" stroke-opacity=".11" stroke-width="1"/>
          <path d="M5 0V18 M14 0V18" stroke="#d3e0d2" stroke-opacity=".08" stroke-width="1"/>
        </pattern>
        <pattern id="redTexture" width="24" height="24" patternUnits="userSpaceOnUse">
          <rect width="24" height="24" fill="#d94234"/>
          <path d="M0 0L24 24M24 0L0 24" stroke="#ffc0a4" stroke-opacity=".14" stroke-width="2"/>
          <path d="M6 0V24M18 0V24" stroke="#831e22" stroke-opacity=".14" stroke-width="2"/>
        </pattern>
        <pattern id="blackTexture" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
          <rect width="12" height="12" fill="#101214"/>
          <path d="M0 2H12" stroke="#6a6a6a" stroke-opacity=".35" stroke-width="1"/>
        </pattern>
        <filter id="shadow" x="-15%" y="-15%" width="130%" height="130%">
          <feDropShadow dx="0" dy="2" stdDeviation="2" flood-opacity=".38"/>
        </filter>
      </defs>
      #{body}
    </svg>
  SVG
end

def counter_base(faction)
  color = faction == :american ? 'url(#blueTexture)' : 'url(#redTexture)'
  "<rect width=\"300\" height=\"300\" fill=\"#{color}\"/>"
end

def american_flag(x, y, width = 170, height = 64)
  stripes = (0...13).map { |i| "<rect x=\"#{x}\" y=\"#{y + i * height / 13}\" width=\"#{width}\" height=\"#{height / 13.0 + 1}\" fill=\"#{i.even? ? '#d93639' : '#f8eee1'}\"/>" }.join
  canton_width = width * 0.34
  canton_height = height * 0.57
  # The Continental Colours used a thirteen-star circle rather than a modern grid.
  stars = (0...13).map do |index|
    angle = -Math::PI / 2 + index * 2 * Math::PI / 13
    cx = x + canton_width / 2 + canton_height * 0.34 * Math.cos(angle)
    cy = y + canton_height / 2 + canton_height * 0.34 * Math.sin(angle)
    "<text x=\"#{format('%.2f', cx)}\" y=\"#{format('%.2f', cy + 2)}\" fill=\"#fff\" font-family=\"Georgia, serif\" font-size=\"6\" text-anchor=\"middle\">★</text>"
  end.join
  "<g filter=\"url(#shadow)\"><rect x=\"#{x}\" y=\"#{y}\" width=\"#{width}\" height=\"#{height}\" fill=\"#f8eee1\" stroke=\"#eee\"/>#{stripes}<rect x=\"#{x}\" y=\"#{y}\" width=\"#{canton_width}\" height=\"#{canton_height}\" fill=\"#2d3e8f\"/>#{stars}</g>"
end

def british_flag(x, y, width = 118, height = 62)
  cx = x + width / 2.0
  cy = y + height / 2.0
  <<~SVG.gsub("\n", '')
    <g filter="url(#shadow)">
      <rect x="#{x}" y="#{y}" width="#{width}" height="#{height}" fill="#243e80" stroke="#eee"/>
      <path d="M#{x} #{y}L#{x + width} #{y + height}M#{x + width} #{y}L#{x} #{y + height}" stroke="#fff" stroke-width="14"/>
      <path d="M#{x} #{y}L#{x + width} #{y + height}M#{x + width} #{y}L#{x} #{y + height}" stroke="#d63136" stroke-width="6"/>
      <path d="M#{cx} #{y}V#{y + height}M#{x} #{cy}H#{x + width}" stroke="#fff" stroke-width="24"/>
      <path d="M#{cx} #{y}V#{y + height}M#{x} #{cy}H#{x + width}" stroke="#d63136" stroke-width="12"/>
    </g>
  SVG
end

def troop_counter(faction, strength)
  label = "#{faction.capitalize} troops #{strength}"
  flag = faction == :american ? american_flag(65, 90) : british_flag(91, 94)
  body = <<~SVG
    #{counter_base(faction)}
    <text x="150" y="63" fill="#f8f4e9" font-family="Arial, sans-serif" font-size="48" letter-spacing="1.5" text-anchor="middle">TROOPS</text>
    #{flag}
    <text x="150" y="245" fill="#fff" font-family="Georgia, serif" font-size="76" font-weight="bold" text-anchor="middle">#{strength}</text>
  SVG
  document(label, body)
end

AMERICAN_LEADER_TILES = %w[
  washington putnam detachment-1 detachment-2 detachment-3 detachment-4 detachment-5 detachment-6
  mifflin dickinson cadwalader griffin glover ewing
].freeze

BRITISH_LEADER_TILES = %w[
  cornwallis grant-1 rall von-donop hessian-detachment-1 hessian-detachment-2
].freeze

def leader_counter(faction, slug, name, top, left, right, _bottom)
  base = counter_base(faction)
  band = faction == :american ? '#c9283e' : '#073d4d'
  top_parts = top.split
  star_count = top_parts.count('★')
  non_stars = top_parts.reject { |part| part == '★' }
  star_positions = case star_count
                   when 1 then [150]
                   when 2 then [128, 172]
                   when 3 then [106, 150, 194]
                   else []
                   end
  number_index = 0
  star_index = 0
  top_markup = top_parts.map do |part|
    if part == '★'
      position = star_positions[star_index]
      color = slug == 'washington' && star_count == 3 && star_index == 1 ? '#e4b322' : '#fff'
      font_size = slug == 'washington' && star_count == 3 ? 46 : 52
      star_index += 1
      "<text x=\"#{position}\" y=\"70\" fill=\"#{color}\" font-family=\"Georgia, serif\" font-size=\"#{font_size}\" text-anchor=\"middle\">★</text>"
    else
      position = non_stars.length == 1 ? 43 : [43, 257][number_index]
      number_index += 1
      "<text x=\"#{position}\" y=\"70\" fill=\"#fff\" font-family=\"Georgia, serif\" font-size=\"52\" text-anchor=\"middle\">#{escape(part)}</text>"
    end
  end.join
  tile_slugs = faction == :american ? AMERICAN_LEADER_TILES : BRITISH_LEADER_TILES
  tile = if tile_slugs.include?(slug)
           '<rect x="112" y="176" width="76" height="36" fill="#f7f6f0"/>'
         else
           ''
         end
  body = <<~SVG
    #{base}
    #{top_markup}
    <rect y="115" width="300" height="50" fill="#{band}"/>
    <text x="150" y="151" fill="#fff" font-family="Arial, sans-serif" font-size="31" text-anchor="middle">#{escape(name)}</text>
    #{tile}
    <text x="43" y="266" fill="#fff" font-family="Georgia, serif" font-size="56" text-anchor="middle">#{left}</text>
    <text x="257" y="266" fill="#fff" font-family="Georgia, serif" font-size="56" text-anchor="middle">#{right}</text>
  SVG
  document("#{faction.capitalize} leader: #{name}", body)
end

def marker(label, title, subtitle = nil, accent: '#f4ef24', symbol: nil)
  symbol_markup = symbol ? "<text x=\"150\" y=\"115\" fill=\"#{accent}\" font-family=\"Arial, sans-serif\" font-size=\"42\" text-anchor=\"middle\">#{symbol}</text>" : ''
  subtitle_markup = subtitle ? "<text x=\"150\" y=\"202\" fill=\"#{accent}\" font-family=\"Georgia, serif\" font-size=\"28\" text-anchor=\"middle\">#{escape(subtitle)}</text>" : '<!-- no subtitle -->'
  body = <<~SVG
    <rect width="300" height="300" fill="url(#blackTexture)"/>
    <g transform="rotate(45 150 150)">
      #{symbol_markup}
      <text x="150" y="#{symbol ? 166 : 148}" fill="#{accent}" font-family="Arial, sans-serif" font-size="#{title.length > 9 ? 34 : 43}" font-weight="bold" text-anchor="middle">#{escape(title)}</text>
      #{subtitle_markup}
    </g>
  SVG
  document(label, body)
end

def trench_counter
  teeth = (0...5).map { |i| x = 35 + i * 50; "<path d=\"M#{x} 176l25 43 25-43z\" fill=\"#111\"/>" }.join
  document('Trench', <<~SVG)
    #{counter_base(:american)}
    <text x="150" y="120" fill="#fff" font-family="Arial, sans-serif" font-size="39" text-anchor="middle">TRENCH</text>
    #{teeth}
  SVG
end

def day_counter
  document('Day turn', <<~SVG)
    <rect width="300" height="300" fill="url(#blackTexture)"/>
    <g transform="rotate(45 150 150)">
      <text x="150" y="148" fill="#d6a75e" font-family="Arial, sans-serif" font-size="52" text-anchor="middle">DAY</text>
    </g>
  SVG
end

def weather_counter
  document('Weather', <<~SVG)
    <rect width="300" height="300" fill="url(#blackTexture)"/>
    <g transform="rotate(45 150 150)">
      <text x="150" y="150" fill="#e6cd21" font-family="Arial, sans-serif" font-size="37" font-weight="bold" text-anchor="middle">WEATHER</text>
      <text x="113" y="208" fill="#e6cd21" font-family="Arial, sans-serif" font-size="35">☀</text>
      <text x="168" y="208" fill="#e6cd21" font-family="Arial, sans-serif" font-size="35">❄</text>
    </g>
  SVG
end

def points_counter(kind, abbreviation, color)
  document(kind, <<~SVG)
    <rect width="300" height="300" fill="url(#redTexture)"/>
    <text x="150" y="116" fill="#fff" font-family="Georgia, serif" font-size="42" text-anchor="middle">#{abbreviation}</text>
    <text x="150" y="166" fill="#fff" font-family="Arial, sans-serif" font-size="34" text-anchor="middle">#{escape(kind)}</text>
  SVG
end

FileUtils.mkdir_p(OUTPUT)

[:american, :british].each do |faction|
  %w[10 100 1000].each do |strength|
    File.write(File.join(OUTPUT, "#{faction}-troops-#{strength}.svg"), troop_counter(faction, strength))
  end
end

AMERICAN_LEADERS.each do |slug, name, top, left, right, bottom|
  File.write(File.join(OUTPUT, "american-leader-#{slug}.svg"), leader_counter(:american, slug, name, top, left, right, bottom))
end

(1..6).each do |number|
  slug = "detachment-#{number}"
  File.write(
    File.join(OUTPUT, "american-#{slug}.svg"),
    leader_counter(:american, slug, "( #{number} )", '1 ★ 1', '3', '1', '')
  )
end

BRITISH_LEADERS.each do |slug, name, top, left, right, bottom|
  File.write(File.join(OUTPUT, "british-leader-#{slug}.svg"), leader_counter(:british, slug, name, top, left, right, bottom))
end

{
  'fatigue.svg' => marker('Fatigue', 'FATIGUE', '(12.0)', symbol: '✦'),
  'routed.svg' => marker('Routed', 'ROUTED', '(18.2)', accent: '#fff', symbol: '↗'),
  'orders.svg' => marker('Orders', 'ORDERS', '(18.3)', symbol: '↪'),
  'turn.svg' => marker('Turn', 'TURN', nil, accent: '#b48b53', symbol: '↻'),
  'trench.svg' => trench_counter,
  'day.svg' => day_counter,
  'weather.svg' => weather_counter,
  'durham-boats.svg' => marker('Durham Boats', 'DURHAM', 'BOATS', accent: '#bde3f7', symbol: '⛵'),
  'navy.svg' => marker('Navy', 'NAVY', nil, accent: '#bde3f7', symbol: '⚓'),
  'victory-points.svg' => points_counter('Victory Points', 'VP', '#fff'),
  'activation-points.svg' => points_counter('Activation Points', 'AP', '#fff'),
  'dawn-attack.svg' => points_counter('Dawn Attack', 'DAWN', '#f9d334')
}.each do |filename, content|
  File.write(File.join(OUTPUT, filename), content)
end

readme = <<~README
  # Washington's Crossing SVG counters

  These are vector recreations of the distinct counter designs in
  `../Washingtons_Crossing_Counters.png`. They intentionally replace the scan's
  duplicated standardized markers with one reusable SVG per design. All SVGs
  are standalone and contain no embedded raster artwork.

  The leader counters retain the source scan's sparse numerical layout, name
  band, and side colour. American Detachments 1--6 are supplied individually.
README
File.write(File.join(OUTPUT, 'README.md'), readme)

puts "Generated #{Dir.glob(File.join(OUTPUT, '*.svg')).length} SVG counters in #{OUTPUT}"
