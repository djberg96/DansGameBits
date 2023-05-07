require 'getopt/std'
require 'nokogiri'

opts = Getopt::Std.getopts('d:r:c:e:o:')

rows = opts['r'].to_i
cols = opts['c'].to_i
dir  = opts['d']
excl = opts['e'].to_s.split(',')
out  = opts['o'] || 'temp.svg'
key  = opts['k'] || 'unit'

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
