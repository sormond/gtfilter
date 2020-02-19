# gtfilter
## Filters a vcf file by sample genotype according to sample phenotype.

## Details
For diploid organisms.
Takes in 'pos' and 'neg' arguments which are lists of samples with and without a phenotype. Returns variants carried (either homozygous or heterozygous) amongst samples within 'pos' that are not carried by samples within 'neg'.
Ignores samples with an unknown genotype.
Has optional 'len' argument which takes an integer
