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

start_string = "<svg xmlns='http://www.w3.org/2000/svg'>"
end_string = "</svg>"

begin
  ohandle = File.open(out, 'w')

  ohandle.puts(start_string)

  Dir["#{dir}/*.svg"].each do |file|
    begin
      next if excl.include?(File.basename(file))
      handle = File.open(file)
      document = Nokogiri::XML(handle)

      if !document.errors.empty?
        raise "Problem with file: #{file}: #{document.errors}"
      end

      document.remove_namespaces!
      xml = document.xpath("//g[@id='#{key}']").to_xml

      unit_name = File.basename(file).split('_').first
      ohandle.puts("  <g id=\"#{unit_name}\">")
      ohandle.puts(xml)
      ohandle.puts("  </g>")
    ensure
      handle.close if handle
    end
  end
ensure
  ohandle.puts(end_string)
  ohandle.close if ohandle
end
