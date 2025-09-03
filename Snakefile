# Snakefile

import os
from glob import glob

# 读取配置文件
configfile: "config.yaml"
include: "rules/fetch_db.smk"

# 定义输入和输出目录
input_dir = config["input_dir"]
output_dir = config["output_dir"]

# 获取所有输入基因组文件
fasta_files = glob(os.path.join(input_dir, "*.fasta"))
# input_files_fasta = glob_wildcards(os.path.join(input_dir, "{genome}.fasta")).genome
databases = ["argannot", "card", "ecoh", "ecoli_vf", "megares", "ncbi", "plasmidfinder", "resfinder", "vfdb"]


input_files_faa = glob_wildcards(os.path.join(input_dir, "{genome2}.faa")).genome2


if "mode_type" not in config:
    raise ValueError("请通过命令行参数指定分析模式：--config mode_type=abricate 或 mode_type=kegg 或 mode_type=summary")

if config["mode_type"] == "abricate":
    output_files_abricate =  []

    for fasta_file in fasta_files:
        filename = os.path.basename(fasta_file)
        for db in databases:
            output_files_abricate.append(os.path.join(output_dir, f"{db}@{filename}.txt"))

    target_file = output_files_abricate

    include: "rules/abricate.smk"

elif config["mode_type"] == "abricate_sum":
    output_xlsx = os.path.join(output_dir,"summary_all.xlsx")
    target_file = output_xlsx
    include: "rules/ab_dl.smk"

elif config["mode_type"] == "kegg":
    output_files_kegg = [os.path.join(output_dir, f"{genome2}.kofam_annotation.txt") for genome2 in input_files_faa]
    target_file = output_files_kegg
    include: "rules/kegg.smk"

elif config["mode_type"] == "kegg_sum":
    output_xlsx1 = os.path.join(output_dir,"summary_kegg.xlsx")
    target_file = output_xlsx1
    include:"rules/scp.smk"
    include: "rules/kegg_dl.smk"


# 规则：默认目标，即所有输出文件
rule all:
    input:
        target_file

