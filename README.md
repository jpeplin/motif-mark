# motif-mark

## Motif Mark Notes
#### Jack Peplinski 2/16/23

### Input
    • FASTA file
    • The introns flanking the cassette exon (not all of the intron, just the close bits)
    • How to denote introns vs exons? Uppercase is the exon, lowercase is the intron.

### Output
    • Single, vector-based image
    • To scale
    • Drawing with a black line for the introns, black box for the exon, and colored boxes for the motifs (colors for multiple motifs with a key) with a gene label on the top left and key with motif sequences/colors on the bottom right. 

### Pycairo
    • c-based drawing library
    • origin is top left

conda install -c conda-forge pycairo
import cairo
import math
import re
surface = cairo.SVGSurface("plot.svg", width, height)
context = cairo.Context(surface)
context.set_line_width(1)
context.move_to(50,25)
context.line_to(intron1+exon+intron2,25)
context.stroke()

### Functions
    • Ideas: Find, introns v exons, ambiguous motifs

    • Parse FASTA (multi-length FASTA into one?)
    • Parse file with motifs
    • Drawing function

### Multiple Motifs & Multiple Genes?

### Motifs with flexibility
    • Regex (must use)