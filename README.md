# DansGameBits
Various SVG bits for virtual board games

# XML Versions

It is not necessary to specify an xml version or encoding within an SVG file
since XML version 1.0 and UTF-8 is the default anyway. Since XML version 1.1
does not appear to be widely supported, and provides no benefit to the things
being created here, XML version 1.1 should absolutely NOT be used.

# On DOCTYPE Declarations

As per the W3 org recommendations, do NOT specify a DTD within an SVG file:

https://www.w3.org/TR/2015/WD-SVG2-20150709/intro.html#Namespace

Instead, set the "xmlns" attribute to "http://www.w3.org/2000/svg" within
the top level `svg` tag.

# External Resources

* Country flags: https://github.com/hampusborgos/country-flags/tree/main/svg
* NATO style unit generator: https://spatialillusions.com/unitgenerator
