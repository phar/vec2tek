<pre>
# vec2tek
SVG to tektronix 40xx vt340 terminal graphics.. weee

(base) lil-Euclid-10:vec2tek phar$ python svg2tek.py -h
usage: svg2tek.py [-h] [-a AUTO] [-c CLEAR] [-b BEZIERMESH] [-d DECIMATE]
                  [-P PAUSE]
                  file

positional arguments:
  file                  svg file

optional arguments:
  -h, --help            show this help message and exit
  -a AUTO, --auto AUTO  automatically scale image to fit the screen
  -c CLEAR, --clear CLEAR
                        clear the screen before drawing
  -b BEZIERMESH, --beziermesh BEZIERMESH
                        resolution of the mesh to apply to bezier curves
                        (smooth round shapes)
  -d DECIMATE, --decimate DECIMATE
                        decimate the final vector list to reduce its
                        complexity for faster display (and low poly render)
  -P PAUSE, --pause PAUSE
                        wait for <enter> before exiting

<pre>


dont forget to tweak the decimation value otherwise your output files (and display times) will be huge and slow..<br>

</pre>
(base) lil-Euclid-10:vec2tek phar$ python svg2tek.py world-map-continents-country-flat.svg  -a True  -d30 > l1

(base) lil-Euclid-10:vec2tek phar$ python svg2tek.py world-map-continents-country-flat.svg  -a True   > l2

(base) lil-Euclid-10:vec2tek phar$ ls -l l1 l2
-rw-r--r--  1 phar  staff    5296 Nov 18 11:59 l1
-rw-r--r--  1 phar  staff  149696 Nov 18 11:59 l2

</pre>
