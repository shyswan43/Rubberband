# Rubberband

## Intro
Rubberband is a bioinfo pipeline tool made with Snakemake which can use abricate dealing with multiple fasta files and generate summary xslx file that showing the virulence genes and resistance genes of these genomes. Also, it can annotate fasta files in batches and generate summary xlsx file showing the hits in the preset gene list of some genes that may express beneficial functions.

## Dependencies
- python3
- snakemake
- abricate
- kofamscan
- pandas
- openpyxl

## Installation
### step 1
create conda enviroment
```
conda create -n rubberband python=3.12        #python3.12
```
### step 2
alter to the env and install snakemake and openpyxl
```
conda activate rubberband
conda install snakemake openpyxl
```
### step 3
install rubberband
```
conda install shyswan43::rubberband
```
```
conda deactivate
```
### step 4
kofamscan annotation needs database which can be download by:
```
wget https://www.genome.jp/ftp/db/kofam/ko_list.gz # ko_list
wget https://www.genome.jp/ftp/db/kofam/profiles.tar.gz # profiles 
```
## Usage
you can get help info by
```
rubberband -h
```
### Using abricate to generate summary
```
rubberband --input path/to/your/data --output path/to/result --type abricate        #run databases
```
```
rubberband --input path/to/your/data --output path/to/result --type abricate_sum        #generate summary xlsx
```
### Using kegg annotation and get summary generated from preset gene list    
```
rubberband --input path/to/your/data --output path/to/result --type kegg -p path/to/profile -k path/to/ko_list        #kegg annotation
```
```
rubberband --input path/to/your/data --output path/to/result --type kegg_sum        #generate summary xlsx
```
