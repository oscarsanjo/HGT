# Cersei
This script allows you to automatize the search of HGT candidates using DarkHorse, MAFFT AND PhyML. Given at least a FASTA file and an output directory, the program will save your alignments and trees from HGT candidates together.
## Requeriments
You must have installed DIAMOND, DarkHorse, MAFFT and PhyML. Also you need Python 2 and Internet connection, because Entrez module from NCBI is required.

DIAMOND: https://github.com/bbuchfink/diamond

DarkHorse: http://darkhorse.ucsd.edu/

MAFFT: https://mafft.cbrc.jp/alignment/software/

PhyML: http://www.atgc-montpellier.fr/phyml/


## Usage
This program is command-line based. The arguments given are:
### Required
- -f: Directory where your FASTA file is set
- -o: Directory where you want to save all your outputs
- -m: Your e-mail. This is required because Entrez module needs the user e-mail
- -g: Name assigned to your organism in NCBI. This is needed to non-self matches. Although this results in avoiding catching proteins from this organism, if BLAST didn't catch proteins with a 100.0% identity, you would lose interesting HGTs
### Optional
- -h: Show a help message
- -d: DIAMOND database folder.
- -k: Directory where you have installed Darkhorse
- -c: Directory where your config file of DarkHorse is set
- -e: Directory where you have your exclude list of DarkHorse
- -s: Number of target sequences to report alignment for in DIAMOND. Default value is 4. This is only for .daa file. DIAMOND automatically will report 200 seqs. This is because if you would like to add more sequences to your analysis, you would have to repeat BLAST again. Thanks to this, you don't have to repeat BLAST.
- -b: Bootstrap replicates. Default value is 4
- -a: Apikey from NCBI. This apikey allows you more requests from Entrez. More info in NCBI webpage
- -v: If you type "y" (without quotation marks), you will avoid the BLAST search. This is useful if you want to do the process and you don't need another BLAST.

## Example
```python cersei.py -f /path/to/FASTA -o /path/where/you/save/output -m varys_little_birds@gmail.com -g "White walker" -s 40 -b 10```

## Important information
Although DIAMOND database, DarkHorse directory, DarkHorse config and DarkHorse exclude list are marked as optional, they are required for the script.
This is because I have set default directories for this. You can change the default directories in the code if you want.

You must create the folder where you want to save your output before running script, otherwise there will be an error

If you want to retry the script without BLAST search, make sure you have erased the output and raw_data folder, HGT_IDs.txt, .xlsx file and .m8 file

## FAQ
> My directories are't recognized

- Make sure you have written your directory properly. If you forgot a "/", that's the problem

> There was a problem while I was running PhyML

- This usually happens due to rare characters, such as "#". If you find a mistake like this, please let me know and I'll fix it

> How can I change DarkHorse, MAFFT or PhyML parameters?

  Unfortunately, you can't do it from command line because the aim of this script is automatization. However, you can change some parameters in the code.

> What's the threshold for HGTs?

  LPI value < 0.55. The aim of this threshold is to avoid false positives, because values between 0.55-0.70 are difficult to interpret.

> I have done the analysis avoiding BLAST search but it doesn't work

  Take into account your BLAST search (.daa file) must be in the folder where you want to store your output.

> Why cersei.py?

  Well, because she loves horizontal gene transfer...
