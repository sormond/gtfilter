# gtfilter
### Filters a vcf file by sample genotype according to sample phenotype.
For diploid organisms. For VCF versions 4.0 and 4.1.
Takes in 'pos' and 'neg' arguments which are lists of samples with and without a phenotype. Returns variants carried (either homozygous or heterozygous) amongst samples within 'pos' that are not carried by samples within 'neg'.
Ignores samples with an unknown genotype.
Has optional 'leniency' (len) argument which takes an integer pertaining to the number of positive phenotype samples that do not have to harbour a variant for the variant to pass. This accounts for false positive testing of phenotype (but not false negative testing).


## Dependencies

1. Python3

2. pyvcf (a Python package)


## File inputs (required)

* Multi-sample VCF v4.0 or 4.1 file
* Text file containing list of 'positive' phenotype samples (pos)
* Text file containing list of 'negative' phenotype samples (neg)


## File outputs

* Filtered VCF file


## Usage
A VCF file (input.vcf) must be given using '-v' flag. A 'positive' sample file (pos.txt) must be given using the '-p' flag, and a 'negative' sample file (neg.txt) must be given using the 'n' flag. A stem name (stem) for the output VCF must be provided using the 'o' flag. An optional '-len' flag can be used for the leniency argument, but must be followed by an integer.

    ./gtfilter.py -v $input.vcf -p $pos.txt -n $neg.txt -o $stem -len $integer
