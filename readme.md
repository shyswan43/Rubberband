# Rubberband

## Intro
Rubberband is bioinfo pipeline tool made with Snakemake which can use abricate dealing with multiple fasta files and generate summary xslx file that showing the virulence genes and resistance genes of these genomes. Also, it can annotation fasta files in batches and generate summary xlsx file showing the hits in the preset gene list of some genes that may express beneficial functions.

## Dependencies
- python3
- snakemake
- abricate
- kofamscan
- pandas
- openpyxl

## Installation
github clone
```
git clone https://github.com/shyswan43/Rubberband.git
```
can be installed by using conda
```
conda install shyswan43::rubberband
```

## Usage
### step 1
this tool depends on snakemake
```
conda create -n snakemake
conda activate snakemake
conda install snakemake
```
it also needs pandas and openpyxl
```
conda install pandas openpyxl
```
### step 2
this tool is a pipeline tool using abricate and kofamscan, make sure these tools have been installed and are available
abricate:
```
conda create -n your_abricate_env 
conda activate your_abricate_env
conda install abricate
```
kofamscan:
```
conda create -n your_kofamscan_env
conda activate your_kofamscan_env
conda install bioconda::kofamscan
```
kofamscan annotation needs database which can be download by:
```
wget https://www.genome.jp/ftp/db/kofam/ko_list.gz # ko_list
wget https://www.genome.jp/ftp/db/kofam/profiles.tar.gz # profiles 
```
### step 3
change the config.yaml settings
```
input_dir: "path/to/your/fasta" # if using abricate fasta is required
input_dir: "path/to/your/faa" # if using kegg annotation faa is required
output_dir: "path/to/your/results" # folder to save the results
kofam_db: "path/to/your/profiles" # profiles in upper step
kofam_ko_list: "path/to/your/ko_list" # ko_list in upper step
abricate_env: "your_abricate_env" # abricate conda enviroment named by yourself
kofamscan_env: "your_kofamscan_env" # kofamscan conda enviroment named by yourself

```
### step 4
RUN
alter to snakemake conda enviroment
```
conda activate snakemake
```
```
cd path/to/rubberband # if download by conda the path is: anaconda/your_env/bin/rubberband
```
deal with fasta using abricate:
```
snakemake -j 5 --use-conda --config mode_type=abricate # run abricate 
snakemake -j 1 --use-conda --config mode_type=abricate_sum # generate summary file
```
deal with faa using kofamscan:
```
snakemake -j 1 --use-conda --config mode_type=kegg # kegg annotation only allows 1 thread
snakemake -j 1 --use-conda --config mode_type=kegg_sum # generate summary file
```
to rerun the tasks move the inputs and outputs to other places
        
