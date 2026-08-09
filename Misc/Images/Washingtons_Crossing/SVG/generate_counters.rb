#!/usr/bin/env ruby
# frozen_string_literal: true

# Generates clean, standalone SVG recreations of the distinct counters on
# Washingtons_Crossing_Counters.png.  Each counter is deliberately vector-only:
# there are no embedded raster scans or external dependencies.

require 'fileutils'

OUTPUT = File.expand_path('../../../../Counters/Washingtons_Crossing', __dir__)
SOURCE_SIZE = 300
SIZE = 100

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
  ['cornwallis', 'Cornwallis', '4 6', '6', '3', '5'],
  ['grant-1', 'Grant', '3 3', '2', '2', '3'],
  ['grant-2', 'Grant', '3', '3', '2', '3'],
  ['webster', 'Webster', '1', '3', '1', '3'],
  ['leslie', 'Leslie', '2 1', '4', '2', '3'],
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
  ['von-donop', 'von Donop', '2 1', '5', '2', '2']
].freeze

def escape(value)
  value.gsub('&', '&amp;').gsub('<', '&lt;').gsub('>', '&gt;')
end

def document(label, body, american_leader: false, star_texture: nil)
  american_leader_texture = if american_leader || star_texture == :american
                               texture_id = american_leader ? 'americanLeaderTexture' : 'americanStarTexture'
                               pattern = <<~SVG
                                 <pattern id="#{texture_id}" width="42" height="42" patternUnits="userSpaceOnUse">
                                   <rect width="42" height="42" fill="#083d4c"/>
                                   <text x="10" y="15" fill="#b7d0c6" fill-opacity=".11" font-family="Georgia, serif" font-size="13" text-anchor="middle">★</text>
                                   <text x="31" y="35" fill="#b7d0c6" fill-opacity=".08" font-family="Georgia, serif" font-size="13" text-anchor="middle">★</text>
                                   <text x="40" y="8" fill="#b7d0c6" fill-opacity=".05" font-family="Georgia, serif" font-size="9" text-anchor="middle">★</text>
                                 </pattern>
                               SVG
                               "\n#{pattern.lines.map { |line| "        #{line}" }.join.chomp}"
                             else
                               ''
                             end
  british_star_texture = if star_texture == :british
                            pattern = <<~SVG
                              <pattern id="britishStarTexture" width="42" height="42" patternUnits="userSpaceOnUse">
                                <rect width="42" height="42" fill="#db322c"/>
                                <text x="10" y="15" fill="#ffd3b2" fill-opacity=".11" font-family="Georgia, serif" font-size="13" text-anchor="middle">★</text>
                                <text x="31" y="35" fill="#ffd3b2" fill-opacity=".08" font-family="Georgia, serif" font-size="13" text-anchor="middle">★</text>
                                <text x="40" y="8" fill="#ffd3b2" fill-opacity=".05" font-family="Georgia, serif" font-size="9" text-anchor="middle">★</text>
                              </pattern>
                            SVG
                            "\n#{pattern.lines.map { |line| "        #{line}" }.join.chomp}"
                          else
                            ''
                          end
  <<~SVG
    <?xml version="1.0" encoding="UTF-8"?>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 #{SOURCE_SIZE} #{SOURCE_SIZE}" role="img" aria-labelledby="title desc">
      <title id="title">#{escape(label)}</title>
      <desc id="desc">Vector recreation of the #{escape(label)} counter from Washington's Crossing.</desc>
      <defs>
        <pattern id="blueTexture" width="18" height="18" patternUnits="userSpaceOnUse">
          <rect width="18" height="18" fill="#083d4c"/>
          <path d="M0 3H18 M0 12H18" stroke="#b7d0c6" stroke-opacity=".11" stroke-width="1"/>
          <path d="M5 0V18 M14 0V18" stroke="#d3e0d2" stroke-opacity=".08" stroke-width="1"/>
        </pattern>#{american_leader_texture}#{british_star_texture}
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

def scaled_number(value)
  number = value.to_f / 3
  format('%.2f', number).sub(/\.00\z/, '').sub(/(\.\d)0\z/, '\\1')
end

def scale_path(path)
  path.gsub(/-?\d+(?:\.\d+)?/) { |value| scaled_number(value) }
end

def scale_to_counter_size(svg)
  scaled = svg.sub('viewBox="0 0 300 300"', 'viewBox="0 0 100 100"')
  scaled = scaled.gsub(/((?:x|y|width|height|font-size|stroke-width|letter-spacing|dx|dy|stdDeviation)=")(-?\d+(?:\.\d+)?)(?=")/) do
    "#{$1}#{scaled_number($2)}"
  end
  scaled = scaled.gsub(/(rotate\(\s*-?\d+(?:\.\d+)?\s+)(-?\d+(?:\.\d+)?)(\s+)(-?\d+(?:\.\d+)?)(\s*\))/) do
    "#{$1}#{scaled_number($2)}#{$3}#{scaled_number($4)}#{$5}"
  end
  scaled.gsub(/(d=")([^"]+)(")/) { "#{$1}#{scale_path($2)}#{$3}" }
end

def apply_sullivan_leader_layout(svg)
  adjusted = svg.gsub(/(<text x="14\.33" y=")26(?=" fill)/) { "#{$1}21.67" }
  adjusted = adjusted.gsub(/(<text x="85\.67" y=")26(?=" fill)/) { "#{$1}21.67" }
  adjusted = adjusted.gsub(/(<text x="(?:42\.67|57\.33)" y=")25\.33(?=" fill)/) { "#{$1}20" }
  adjusted = adjusted.gsub(/(<text x="14\.33" y=")91\.67(?=" fill)/) { "#{$1}86.67" }
  adjusted.gsub(/(<text x="85\.67" y=")91\.67(?=" fill)/) { "#{$1}89.33" }
end

def write_counter(filename, content, leader: false)
  output = scale_to_counter_size(content)
  output = apply_sullivan_leader_layout(output) if leader
  File.write(File.join(OUTPUT, filename), output)
end

def counter_base(faction)
  color = faction == :american ? 'url(#blueTexture)' : 'url(#redTexture)'
  "<rect width=\"300\" height=\"300\" fill=\"#{color}\"/>"
end

def british_leader_background
  <<~SVG
    <rect width="300" height="300" fill="#c84739"/>
    <g opacity=".42">
      <path d="M-35 0L300 335M335 0L0 335" stroke="#f4a17f" stroke-width="72"/>
      <path d="M-35 0L300 335M335 0L0 335" stroke="#a82f2b" stroke-width="31"/>
      <path d="M150 0V300M0 150H300" stroke="#f29a78" stroke-width="78"/>
      <path d="M150 0V300M0 150H300" stroke="#b52f2c" stroke-width="35"/>
    </g>
    <rect width="300" height="300" fill="url(#redTexture)" opacity=".16"/>
  SVG
end

def american_leader_background
  '<rect width="300" height="300" fill="url(#americanLeaderTexture)"/>'
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
    <defs><clipPath id="britishFlagClip"><rect x="#{x}" y="#{y}" width="#{width}" height="#{height}"/></clipPath></defs>
    <g filter="url(#shadow)">
      <rect x="#{x}" y="#{y}" width="#{width}" height="#{height}" fill="#243e80" stroke="#eee"/>
      <g clip-path="url(#britishFlagClip)">
        <path d="M#{x} #{y}L#{x + width} #{y + height}M#{x + width} #{y}L#{x} #{y + height}" stroke="#fff" stroke-width="14"/>
        <path d="M#{x} #{y}L#{x + width} #{y + height}M#{x + width} #{y}L#{x} #{y + height}" stroke="#d63136" stroke-width="6"/>
      </g>
      <path d="M#{cx} #{y}V#{y + height}M#{x} #{cy}H#{x + width}" stroke="#fff" stroke-width="24"/>
      <path d="M#{cx} #{y}V#{y + height}M#{x} #{cy}H#{x + width}" stroke="#d63136" stroke-width="12"/>
    </g>
  SVG
end

def troop_counter(faction, strength)
  label = "#{faction.capitalize} troops #{strength}"
  flag = faction == :american ? american_flag(65, 90) : british_flag(55, 105, 190, 62)
  base = faction == :british ? '<rect width="300" height="300" fill="url(#britishStarTexture)"/>' : '<rect width="300" height="300" fill="url(#americanStarTexture)"/>'
  body = <<~SVG
    #{base}
    <text x="150" y="84" fill="#f8f4e9" font-family="Helvetica Neue, Helvetica, Arial, sans-serif" font-size="48" letter-spacing="1.5" text-anchor="middle">TROOPS</text>
    #{flag}
    <text x="150" y="260" fill="#fff" font-family="Times New Roman, Times, serif" font-size="96" text-anchor="middle">#{strength}</text>
  SVG
  document(label, body, star_texture: faction)
end

AMERICAN_LEADER_TILES = %w[
  washington putnam detachment-1 detachment-2 detachment-3 detachment-4 detachment-5 detachment-6
  mifflin dickinson cadwalader griffin glover ewing
].freeze

BRITISH_LEADER_TILES = %w[
  cornwallis grant-1 rall von-donop hessian-detachment-1 hessian-detachment-2
].freeze

def leader_counter(faction, slug, name, top, left, right, _bottom)
  base = faction == :british ? british_leader_background : american_leader_background
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
      "<text x=\"#{position}\" y=\"76\" fill=\"#{color}\" font-family=\"Georgia, serif\" font-size=\"#{font_size}\" text-anchor=\"middle\">★</text>"
    else
      position = non_stars.length == 1 ? 43 : [43, 257][number_index]
      number_index += 1
      "<text x=\"#{position}\" y=\"78\" fill=\"#fff\" font-family=\"Georgia, serif\" font-size=\"64\" text-anchor=\"middle\">#{escape(part)}</text>"
    end
  end.join
  tile_slugs = faction == :american ? AMERICAN_LEADER_TILES : BRITISH_LEADER_TILES
  tile = if tile_slugs.include?(slug)
           '<rect x="75" y="176" width="150" height="36" fill="#f7f6f0"/>'
         else
           ''
         end
  body = <<~SVG
    #{base}
    #{top_markup}
    <rect y="112" width="300" height="62" fill="#{band}"/>
    <text x="150" y="156" fill="#fff" font-family="Arial, sans-serif" font-size="38" font-weight="bold" text-anchor="middle">#{escape(name)}</text>
    #{tile}
    <text x="43" y="275" fill="#fff" font-family="Georgia, serif" font-size="64" text-anchor="middle">#{left}</text>
    <text x="257" y="275" fill="#fff" font-family="Georgia, serif" font-size="64" text-anchor="middle">#{right}</text>
  SVG
  document("#{faction.capitalize} leader: #{name}", body, american_leader: faction == :american)
end

def marker(label, title, subtitle = nil, accent: '#f4ef24', symbol: nil, squares: false, route_symbol: false, solid_background: false)
  symbol_markup = if squares
                    [105, 143, 181].map { |x| "<rect x=\"#{x}\" y=\"96\" width=\"14\" height=\"14\" fill=\"#{accent}\"/>" }.join
                  elsif route_symbol
                    "<text x=\"150\" y=\"115\" fill=\"#{accent}\" font-family=\"Arial, sans-serif\" font-size=\"54\" font-weight=\"bold\" text-anchor=\"middle\">!</text>"
                  elsif symbol
                    "<text x=\"150\" y=\"115\" fill=\"#{accent}\" font-family=\"Arial, sans-serif\" font-size=\"42\" text-anchor=\"middle\">#{symbol}</text>"
                  else
                    ''
                  end
  subtitle_markup = subtitle ? "<text x=\"150\" y=\"202\" fill=\"#{accent}\" font-family=\"Georgia, serif\" font-size=\"28\" text-anchor=\"middle\">#{escape(subtitle)}</text>" : '<!-- no subtitle -->'
  background = solid_background ? '<rect width="300" height="300" fill="#101214"/>' : '<rect width="300" height="300" fill="url(#blackTexture)"/>'
  body = <<~SVG
    #{background}
    <g transform="rotate(45 150 150)">
      #{symbol_markup}
      <text x="150" y="#{symbol || route_symbol ? 166 : 148}" fill="#{accent}" font-family="Arial, sans-serif" font-size="#{title.length > 9 ? 34 : 43}" font-weight="bold" text-anchor="middle">#{escape(title)}</text>
      #{subtitle_markup}
    </g>
  SVG
  document(label, body)
end

def trench_counter(faction)
  top_teeth = [58, 150, 242].map { |x| "<path d=\"M#{x - 38} 108H#{x + 38}L#{x} 35z\" fill=\"#07090b\"/>" }.join
  bottom_teeth = [58, 150, 242].map { |x| "<path d=\"M#{x - 38} 205H#{x + 38}L#{x} 278z\" fill=\"#07090b\"/>" }.join
  texture = faction == :american ? 'americanStarTexture' : 'britishStarTexture'
  document("#{faction.capitalize} trench", <<~SVG, star_texture: faction)
    <rect width="300" height="300" fill="url(##{texture})"/>
    #{top_teeth}
    <text x="150" y="176" fill="#fff" font-family="Arial, sans-serif" font-size="51" font-weight="bold" text-anchor="middle">TRENCH</text>
    #{bottom_teeth}
  SVG
end

def transport_counter(label, bottom)
  title_size = label.length > 11 ? 40 : 51
  document(label, <<~SVG, star_texture: :american)
    <rect width="300" height="300" fill="url(#americanStarTexture)"/>
    <text x="73" y="94" fill="#f8f4e9" font-family="Times New Roman, Times, serif" font-size="66" text-anchor="middle">24</text>
    <path d="M150 29L111 105 150 84 189 105z" fill="#47bee8"/>
    <text x="227" y="94" fill="#f8f4e9" font-family="Times New Roman, Times, serif" font-size="66" text-anchor="middle">12</text>
    <rect y="126" width="300" height="58" fill="#34869f"/>
    <text x="150" y="169" fill="#f8f4e9" font-family="Helvetica Neue, Helvetica, Arial, sans-serif" font-size="#{title_size}" text-anchor="middle">#{escape(label)}</text>
    <text x="150" y="252" fill="#f8f4e9" font-family="Helvetica Neue, Helvetica, Arial, sans-serif" font-size="57" text-anchor="middle">#{escape(bottom)}</text>
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
    write_counter("#{faction}-troops-#{strength}.svg", troop_counter(faction, strength))
  end
end

AMERICAN_LEADERS.each do |slug, name, top, left, right, bottom|
  write_counter("american-leader-#{slug}.svg", leader_counter(:american, slug, name, top, left, right, bottom), leader: true)
end

(1..6).each do |number|
  slug = "detachment-#{number}"
  write_counter(
    "american-#{slug}.svg",
    leader_counter(:american, slug, "( #{number} )", '1 ★ 1', '3', '1', ''),
    leader: true
  )
end

BRITISH_LEADERS.each do |slug, name, top, left, right, bottom|
  write_counter("british-leader-#{slug}.svg", leader_counter(:british, slug, name, top, left, right, bottom), leader: true)
end

{
  'fatigue.svg' => marker('Fatigue', 'FATIGUE', '(12.0)', squares: true, solid_background: true),
  'disorder.svg' => marker('Disorder', 'DISORDER', '(18.1)', accent: '#f8edaa', symbol: '?', solid_background: true),
  'routed.svg' => marker('Routed', 'ROUTED', '(18.2)', accent: '#fff', route_symbol: true, solid_background: true),
  'turn.svg' => marker('Turn', 'TURN', nil, accent: '#b48b53', symbol: '↻'),
  'day.svg' => day_counter,
  'weather.svg' => weather_counter,
  'dawn-attack.svg' => points_counter('Dawn Attack', 'DAWN', '#f9d334')
}.each do |filename, content|
  write_counter(filename, content)
end

%i[american british].each do |faction|
  write_counter("#{faction}-trench.svg", trench_counter(faction))
end

write_counter('durham-boats.svg', transport_counter('Durham', 'BOATS'))
write_counter('pennsylvania-navy.svg', transport_counter('Pennsylvania', 'NAVY'))

readme = <<~README
  # Washington's Crossing SVG counters

  These are vector recreations of the distinct counter designs in
  `../Washingtons_Crossing_Counters.png`. They intentionally replace the scan's
  duplicated standardized markers with one reusable SVG per design. All SVGs
  are standalone and contain no embedded raster artwork.

  The leader counters retain the source scan's sparse numerical layout, name
  band, and side colour. American Detachments 1--6 are supplied individually.
README
File.write(File.join(__dir__, 'README.md'), readme)

puts "Generated #{Dir.glob(File.join(OUTPUT, '*.svg')).length} SVG counters in #{OUTPUT}"
