#!/usr/bin/env python3

""" Function of gtfilter: filter vcf files with genotype.
Code written by Shannon Ormond 2018. Contact email: s.ormond@massey.ac.nz """

import vcf
import argparse
from functools import reduce


# command line stuff
parser = argparse.ArgumentParser()

parser.add_argument('-p', '--positive', help = "Required argument. VCF file to use.")

parser.add_argument('-n', '--negative', help = "Required argument. Stem name of VCF file to make.")

parser.add_argument('-v', '--inputvcf', help = "Required argument. Stem name of VCF file to make.")

parser.add_argument('-o', '--outputvcf', help = "Required argument. Stem name of VCF file to make.")

parser.add_argument('-len', '--leniency', type = int, help = "Optional argument. Number of disease positive samples that do not have to carry variant.")

args = parser.parse_args()

# calling main function
a = args.inputvcf

b = args.outputvcf

f = open(args.positive, 'r')
pos = f.read().splitlines()
f.close

f = open(args.negative, 'r')
neg = f.read().splitlines()
f.close

# listlen = len(pos) + len(neg)
# expectedList = [1] * listlen


if args.leniency :
    setlen = args.leniency
else :
    setlen = 0


# reads in vcf file line by line
vcf_reader = vcf.Reader(open(args.inputvcf, 'r'))

# creates new vcf file
vcf_writer = vcf.Writer(open(args.outputvcf + ".vcf", 'w'), vcf_reader)

for variant in vcf_reader:

    newlist = []

    for element in pos :

        if variant.genotype(element)['GT'] == "1/1" or variant.genotype(element)['GT'] == "0/1" or variant.genotype(element)['GT'] == "./." :
            newlist.append(1)

        else :
            newlist.append(2)
    
    for element in neg :

        if variant.genotype(element)['GT'] == "0/0" or variant.genotype(element)['GT'] == "./." :
            newlist.append(1)

        else :
            newlist.append(0)

    # product of newlist
    product = reduce(lambda x, y: x*y, newlist)

    # disallows disease negative to carry variant
    if product == 0 :

        exit

    else :

        if product == 1 :

            # writes the record (line from input vcf file) to new vcf
                vcf_writer.write_record(variant)

        elif setlen != 0 :

            num = setlen * 2

            if product <= num :

                print(product)

                # writes the record (line from input vcf file) to new vcf
                vcf_writer.write_record(variant)


vcf_writer.close