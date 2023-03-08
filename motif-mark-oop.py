#!/usr/bin/env python

import cairo
import math
import re
import bioinfo
import argparse

########
# Prep #
########

def get_args():
    '''Defines variables for input. Helpful information is in the descriptions.'''
    parser = argparse.ArgumentParser(description="f and m are required variables for input files. f is a FASTA file and m is a .txt file of motif sequences \
        separated by new lines.")
    parser.add_argument("-f", help="Inputs a FASTA file with .fasta. This file will be translated from a FASTA file to a 'one-line' FASTA file and will be \
        stored in the current working directory as oneline.fasta. Do not modify oneline.fasta.", required=True)
    parser.add_argument("-m", help="Inputs a motifs file with .txt. Motifs must be separated by new lines, one motif sequence per line. Case will be maintained \
        by the output visualization.", required=True)
    return parser.parse_args()
args=get_args()

#sets the variables to 0 for finding the longest gene 
long_line = ''
long_line_len = 0

#converts the input -f to a oneline fasta
bioinfo.oneline_fasta(args.f, 'oneline.fasta')

fasta = args.f
name = fasta.split(".")[0]
svgname = name + '.svg'
pngname = name + '.png'

#opens the oneline fasta and parses it to find the longest gene
with open("oneline.fasta", 'r') as i:
    gene_count = 0
    while True:
        line = i.readline()
        if line == "": #when the readline reaches an empty line it stops
            break
        elif line.startswith('>'): #finds the header lines
            header = line.strip()
            gene_count += 1
        else:
            seq = line.strip() #finds the sequence lines
            #this loop compares the length of the sequence lines and 
            #finds the longest one in order to set the window size
            if len(seq) > long_line_len: 
                long_line_len = len(seq)

#opening context with the size of x = longest gene length and y adjusted by the number of genes 
surface = cairo.SVGSurface(svgname, long_line_len + 125, (gene_count*100)-15)
ctx = cairo.Context(surface)
ctx.set_source_rgb(1,1,1)
ctx.paint()

#creates a list of motif sequences
m_list = []

#creates an IUPAC dictionary
iupac_dict = {
    "A":"[Aa]",
    "C":"[Cc]",
    "G":"[Gg]",
    "T":"[Tt]",
    "U":"[UuTt]",
    "W":"[AaTtUu]",
    "S":"[CcGg]",
    "M":"[AaCc]",
    "K":"[GgTtUu]",
    "R":"[AaGg]",
    "Y":"[CcTtUu]",
    "B":"[CcGgTt]",
    "D":"[AaGgTtUu]",
    "H":"[AaCcTtUu]",
    "V":"[AaCcGg]",
    "N":"[AaCcGgTtUu]",
    "Z":"[]"
}

class Gene:
    '''This is how to define a gene with this program. \
    Inputting length of the gene and the y-value it will be incremented at.'''
    def __init__(self, length, height):
        self.length = length
        self.height = height

    def draw(self, length, height):
        '''This draw function will draw a gene represented by a black line.'''
        ctx.set_source_rgba(0, 0, 0, 1) #set the line color to black
        ctx.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, #set the font to bold
        cairo.FONT_WEIGHT_BOLD) 
        ctx.set_font_size(6)
        ctx.move_to(25, height-12) #the starting position at x is 25 to create a margin, y-12 to put the text above
        ctx.show_text(header) #writes the header line to label the gene
        ctx.set_line_width(1)
        ctx.move_to(25, height) 
        ctx.line_to((25+gene_stop), height)
        ctx.stroke()

class Exon:
    '''This is how to define an exon with this program. \
    Inputting the start, stop, and height of the exon'''
    def __init__(self, start, stop, height):
        self.start = start
        self.stop = stop
        self.height = height

    def draw(self, start, stop, height):
        '''This draw function will draw an exon represented by a black box.'''
        ctx.set_source_rgba(0, 0, 0, 1)
        ctx.set_line_width(8)
        ctx.move_to((25+exon_start), height)
        ctx.line_to((25+exon_start+exon_stop), height)
        ctx.stroke()

class Motif:
    '''This is how to define a motif with this program. \
    Inputting the start, stop, height, and motif_kind which will assign colors to unique motifs'''
    def __init__(self, start, stop, height, motif_kind=None):
        self.start = start
        self.stop = stop
        self.height = height
        self.motif_kind = None

    def draw(self, start, stop, height, motif_kind):
        '''This draw function will draw a motif represented by a colored box.'''
        ctx.set_source_rgba(motif_kind[0], motif_kind[1], motif_kind[2], 0.90) #this sets the RGB values based on the motif_kind and opacity 0.9 for overlapping
        ctx.set_line_width(8)
        ctx.move_to((25+motif_start), height)
        ctx.line_to((25+motif_start+motif_stop), height)
        ctx.stroke()

########
# Main #
########

#this badly worded list will be populated with case-adjusted motifs 
#that have been interpreted with the IUPAC dictionary
new_list = []  

#opening and parsing motif file
with open(args.m, 'r') as i:
    while True:
        line = i.readline()
        if line == "":
            break
        else:
            motif = line.strip()
            m_list.append(motif) #appends the motifs to a list

    for motif_seq in m_list: #for motif sequence in the list
        motif_seq = motif_seq.upper() #change all to upper-case
        for iupac_code, iupac_seq in iupac_dict.items(): #this for loop interprets the IUPAC dictionary
            motif_seq = motif_seq.replace(iupac_code, iupac_seq) #and replaces the motifs with the IUPAC possibilities
        new_list.append(motif_seq) #then it appends the interpreted motifs to a badly named new list.

#This sets a list of lists of RGB values from colorblind friendly palette from Masataka Okabe and Kei Ito's Color Universal Design (CUD) website
#pycairo uses RGB percentage so everything has to be divided by 255.
unique_colors = []
blue = [(0/255),(114/255),(178/255)]
skyblue = [(86/255),(180/255),(233/255)]
green = [(0/255),(158/255),(115/255)]
orange = [(230/255),(159/255),(0/255)]
vermillion = [(213/255),(94/255),(0/255)]
reddishpurple = [(204/255),(121/255),(167/255)]
yellow = [(240/255),(228/255),(66/255)]

#This appends those colors to the list of lists in the order that they will be used by the motifs
unique_colors.append(blue)
unique_colors.append(green)
unique_colors.append(orange)
unique_colors.append(vermillion)
unique_colors.append(skyblue)
unique_colors.append(reddishpurple)
unique_colors.append(yellow)

#using oneline fasta to get the header and sequence
with open("oneline.fasta", 'r') as i:
    height = 0 #sets height to 0
    count = 0 #sets motif count to 0
    while True:
        line = i.readline()
        if line == "": #when the readline reaches an empty line it stops
            break
        elif line.startswith('>'): #extracts header lines
            header = line.strip()
        else:
            motif_count = -1 #starts motif count at -1 (because it starts at the beginning, I could've set it to 0 at the end of the loop but oh well)
            height += 75 #adds 75 to the y for every gene
            seq = line.strip() #extracts the sequence
            gene_stop = len(seq) #finds the length of the sequence
            exon_name = re.findall("[A-Z]+", seq)[0] #finds the exon sequence
            exon_stop = len(exon_name) #finds the length of the exon sequence
            exon_start = len(re.findall("([a-z]+)[A-Z]", seq)[0]) #finds the length of the intron before the exon for the start
            Gene.draw(header, gene_stop, height) #draws the gene line
            Exon.draw(exon_name, exon_start, exon_stop, height) #draws the exon box
            for motif_sequence in new_list: #for motifs in the list of intepreted motifs
                motif_count += 1 #adds 1 to the count
                motif_list = [m.start() for m in re.finditer(motif_sequence, seq)] #searches for every instance of the motif sequence in the gene sequence
                motif_kind = unique_colors[motif_count] #assigns a color from the list to each unique motif
                motif_stop = len(m_list[motif_count]) #finds the length of the motif
                for value in motif_list: #finds where the motifs start
                    motif_start = value
                    Motif.draw(motif, motif_start, motif_stop, height, motif_kind) #draws the motifs
            count += 1 #count goes up by one and the next motif will be read

############################
# This part is for the key #
############################

motif_count = 0 
keylength = 45

for motif in m_list:
    ctx.set_source_rgba(0,0,0,1)
    ctx.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    ctx.set_font_size(6)
    ctx.move_to(long_line_len + 50, keylength + 7) #moves the key to the right side of the longest line so it's never overlapped
    ctx.show_text(motif) #writes the motif name in the key

    motif_kind = unique_colors[motif_count] #assigns the colors to the appropriate motif

    ctx.set_source_rgba(motif_kind[0], motif_kind[1], motif_kind[2], 0.9) #see above
    ctx.rectangle(long_line_len + 35, keylength, 10, 10) #draws a little square for each color
    ctx.fill()

    motif_count += 1
    keylength += 15 #separates them
    

#This is setting a title based on the input file name
ctx.set_source_rgba(0,0,0,1)
ctx.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
ctx.set_font_size(10)
ctx.move_to(25, 25)
ctx.show_text("Motif Mark Visualization from " + args.f)

#by Jack Peplinski
ctx.set_source_rgba(0,0,0,1)
ctx.select_font_face("Purisa", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_NORMAL)
ctx.set_font_size(6)
ctx.move_to(25, 35)
ctx.show_text("Created By: Jack Peplinski, 03-07-2023")

#writing out to a png to preview in vs code
surface.write_to_png(pngname)

surface.finish()
                    
#printing the file saved to check when properly run
print("File Saved")