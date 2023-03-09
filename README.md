# motif-mark
#### Created By: Jack Peplinski, Updated: 3/8/23
---------------------------------------------------------------------------------------------------------------------------------------------------

`motif-mark-oop.py` lets you visualize the relative locations of unique motifs and exons on a gene with just a FASTA file and a list of motifs. 

![alt text](https://github.com/jpeplin/motif-mark/blob/main/Figure_1.svg "motif-mark figure 1")

### Contents

• [Features](#Features)                                                                                         
• [Installation](#Installation)                                                                                             
• [Usage](#Usage)                                                                                   

### Features
---------------------------------------------------------------------------------------------------------------------------------------------------

#### To-Scale Gene-Exon-Motif Visualization

The main feature of `motif-mark-oop.py` is the visualization of genes, exons, and motifs drawn to scale. The window of the outputted files will automatically adjust to the length of the longest gene and exons and motifs will be spaced according to their position in the input FASTA sequence. 

#### Up to Seven Unique Motifs

`motif-mark-oop.py` can handle an input list of up to seven unique motifs. These motifs use a color-blind friendly color palette from [Masataka Okabe and Kei Ito's Color Universal Design website](https://jfly.uni-koeln.de/color/). However, this can be easily modified in the color portion of the script by simply adding more colors. 

#### One-line FASTA

`motif-mark-oop.py` will input a FASTA file of any size and first turn it into a one-line FASTA with headers and sequences on alternating lines. 

#### Easy Visualization

Genes will be evenly spaced and populated with corresponding introns and exons shown as thin and thick black lines respectively. The headers for each gene will be printed above the corresponding gene line. Motifs will be shown as boxes, color-coded for unique motifs and printed onto a corresponding key shown in the top right of the output. 

#### .png and .svg Formats

In addition to a one-line FASTA, the visualizations will be outputted as a .png and a .svg file.

### Installation
---------------------------------------------------------------------------------------------------------------------------------------------------

Installation of `motif-mark-oop.py` is as simple as downloading `motif-mark-oop.py` and `bioinfo.py` to your working directory. The following packages are required to run the programs:

#### `motif-mark-oop.py`

• cairo                             
• math                              
• re                                
• argparse                              
• bioinfo                               

#### `bioinfo.py`

• re                                
• math                                  
• matplotlib.pylab as plt                           
• numpy as np                                   
• argparse                                           

### Usage
---------------------------------------------------------------------------------------------------------------------------------------------------

In order to use `motif-mark-oop.py`, you must have `motif-mark-oop.py`, `bioinfo.py`, a FASTA file with .fasta as the suffix, and a file of motifs with .txt as the suffix in the working directory. The FASTA file must be a standard FASTA with header and sequence lines and the motif file must have unique motifs separated by new lines, one motif to a line.

Once you have navigated to the current working directory in your terminal, input `$ ./motif-mark-oop.py -f your_fasta_file.fasta -m your_motif_file.txt` in the terminal and hit enter. When run correctly, you should see no error messages, just a "file saved" message and the oneline.fasta, the .png, and the .svg files in your working directory.  