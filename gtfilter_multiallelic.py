#!/usr/bin/env python3

""" Function of gtfilter: filter vcf files with genotype. Can invoke argument which allows one or more disease-phenotype positive sample to not carry variant.
Code written by Shannon Ormond 2018. Contact email: s.ormond@massey.ac.nz """

import vcf

import argparse

from functools import reduce


# command line stuff
parser = argparse.ArgumentParser()

parser.add_argument('-p', '--positive', help = "Required argument. Tab-delimited file containing disease-positive sample names.")

parser.add_argument('-n', '--negative', help = "Required argument. Tab-delimited file containing disease-negative sample names.")

parser.add_argument('-v', '--inputvcf', help = "Required argument. Input VCF.")

parser.add_argument('-o', '--outputvcf', help = "Required argument. Stem name of VCF file to make.")

parser.add_argument('-len', '--leniency', type = int, help = "Optional argument. Number of disease positive samples that do not have to carry variant.")

args = parser.parse_args()


# reads in samples from disease-pos .txt sample file and puts in list 'pos'
f = open(args.positive, 'r')

pos = f.read().splitlines()

f.close


# reads in samples from disease-neg .txt sample file and puts in list 'neg'
f = open(args.negative, 'r')

neg = f.read().splitlines()

f.close


# sets leniency if argument is made
if args.leniency :
    setlen = args.leniency
    num = setlen * 2
else :
    setlen = 0


# reads in vcf file line by line
vcf_reader = vcf.Reader(open(args.inputvcf, 'r'))


# creates new vcf file
vcf_writer = vcf.Writer(open(args.outputvcf + ".vcf", 'w'), vcf_reader)

prev_genomic_pos = -101

thres_list = [0] * (len(pos) + len(neg))

nearby_allele = False

# iterates through each variant
for variant in vcf_reader:

    genomic_position = variant.POS

    if genomic_position - 100 <= prev_genomic_pos <= genomic_position + 100 :

        nearby_allele = True

    # list which will be used to test whether variant is passed on rejected
    thres_list = []

    # iterates through pos sample
    for element in pos :

        if variant.genotype(element)['GT'] == "1/1" or variant.genotype(element)['GT'] == "0/1" or variant.genotype(element)['GT'] == "./." :
            thres_list.append(1)

        else :
            thres_list.append(2)
    
    # iterates through neg sample
    for element in neg :

        if variant.genotype(element)['GT'] == "0/0" or variant.genotype(element)['GT'] == "./." :
            thres_list.append(1)

        else :
            thres_list.append(0)

    # product of thres_list
    product = reduce(lambda x, y: x*y, thres_list)

    # disallows disease negative to carry variant as product will be zero if neg sample carries variant
    if product == 0 :

        exit

    else :

        # if product is 1 it will pass variant
        if product == 1 :

            # writes the record (line from input vcf file) to new vcf
                vcf_writer.write_record(variant)

        # if product is not 1 it will check whether a value > 0 for setlen exists, and if so it will check pass variant if product is below threshold. I.e. if setlen = 1, num will be 2, and product cannot be > 2 for variant to be passed.
        elif setlen != 0 :

            if product <= num :

                # writes the record (line from input vcf file) to new vcf
                vcf_writer.write_record(variant)

        elif nearby_allele == True :

            print('found one')

    prev_genomic_pos = variant.POS

    prev_threshold_list = thres_list

    nearby_allele = False

vcf_writer.close