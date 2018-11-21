#!/usr/bin/env python3


""" Function of gtfilter: filter vcf files with genotype. Code is non-flexible, must be manually edited for each vcf.
Code written by Shannon Ormond 2018. Contact email: s.ormond@massey.ac.nz """


import vcf
import argparse


# main function
def filter(input, output) :

    # reads in vcf file line by line
    vcf_reader = vcf.Reader(open(input, 'r'))

    # creates new vcf file
    vcf_writer = vcf.Writer(open(output + ".vcf", 'w'), vcf_reader)

    # samples 1731, 1772, 82, 456, 1367, 1412, 533 and 919 must be het, hom, or not called (cannot be reference). sample 26 must be hom ref or not called.
    for variant in vcf_reader :
        if variant.genotype('1731')['GT'] == "1/1" or variant.genotype('1731')['GT'] == "0/1" or variant.genotype('1731')['GT'] == "./." :
            if variant.genotype('1772')['GT'] == "1/1" or variant.genotype('1772')['GT'] == "0/1" or variant.genotype('1772')['GT'] == "./." :
                if variant.genotype('1863-L1-82')['GT'] == "1/1" or variant.genotype('1863-L1-82')['GT'] == "0/1" or variant.genotype('1863-L1-82')['GT'] == "./." :
                    if variant.genotype('1863-L2-456')['GT'] == "1/1" or variant.genotype('1863-L2-456')['GT'] == "0/1" or variant.genotype('1863-L2-456')['GT'] == "./." :
                        if variant.genotype('1863-L4-1367')['GT'] == "1/1" or variant.genotype('1863-L4-1367')['GT'] == "0/1" or variant.genotype('1863-L4-1367')['GT'] == "./." :
                            if variant.genotype('1863-L5-1412')['GT'] == "1/1" or variant.genotype('1863-L5-1412')['GT'] == "0/1" or variant.genotype('1863-L5-1412')['GT'] == "./." :
                                if variant.genotype('533')['GT'] == "1/1" or variant.genotype('533')['GT'] == "0/1" or variant.genotype('533')['GT'] == "./." :
                                    if variant.genotype('919')['GT'] == "1/1" or variant.genotype('919')['GT'] == "0/1" or variant.genotype('919')['GT'] == "./." :
                                        if variant.genotype('2345-L1-26')['GT'] == "0/0" or variant.genotype('2345-L1-26')['GT'] == "./." :
                                            
                                            # writes the record (line from input vcf file) to new vcf
                                            vcf_writer.write_record(variant)

    vcf_writer.close


# command line stuff
parser = argparse.ArgumentParser()

parser.add_argument('-i', '--inputvcf', help = "Required argument. VCF file to use.")

parser.add_argument('-o', '--outputvcf', help = "Required argument. Stem name of VCF file to make.")

args = parser.parse_args()


# calling main function
a = args.inputvcf

b = args.outputvcf

filter(a, b)