require 'getopt/std'
require 'nokogiri'

opts = Getopt::Std.getopts('d:r:c:e:o:')

# Rows and columns
rows = opts.fetch('r'){ 1 }.to_i
cols = opts.fetch('c'){ 1 }.to_i

# Directory to search
dir  = opts.fetch('d'){ Dir.pwd }

# Fetch content within this group key
key  = opts.fetch('k'){ 'unit' }

# Output file
out  = opts.fetch('o'){ 'temp.svg' }

# Ignore these comma separated files when parsing
excl = opts['e'].to_s.split(',')

# Horizontal and Vertical Spacing
hspace = opts.fetch('h'){ 10 }
vspace = opts.fetch('v'){ 10 }

width  = (100 * cols) + (hspace * cols)
height = (100 * rows) + (vspace * rows)

start_string = "<svg viewBox='0 0 #{width} #{height}' xmlns='http://www.w3.org/2000/svg'>"
end_string = "</svg>"

begin
  ohandle = File.open(out, 'w')

  ohandle.puts(start_string)

  current_row = 0
  current_col = 0

  Dir["#{dir}/*.svg"].each do |file|
    begin
      next if excl.include?(File.basename(file))
      handle = File.open(file)
      document = Nokogiri::XML(handle)

      if !document.errors.empty?
        raise "Problem with file: #{file}: #{document.errors}"
      end

      document.remove_namespaces!

      if current_col == 0
        common_defs = document.xpath("//defs[@id='common']").to_xml
        ohandle.puts("  #{common_defs}")
      end

      xml = document.xpath("//g[@id='#{key}']").to_xml

      unit_name = File.basename(file).split('_').first

      # Assume size 100 for now, fix this to use viewbox
      x = (hspace * current_col) + (100 * current_col)
      y = (vspace * current_row) + (100 * current_row)

      current_col += 1

      if current_col > cols
        current_col = 0
        current_row += 1
      end

      break if current_row > rows

      ohandle.puts("  <g id=\"#{unit_name}\" transform=\"translate(#{x},#{y})\">")
      ohandle.puts("    #{xml}")
      ohandle.puts("  </g>")
    ensure
      handle.close if handle
    end
  end
ensure
  ohandle.puts(end_string)
  ohandle.close if ohandle
end