第一步：在conda中创建新环境并安装snakemake：conda install snakemake

第二步：在配置文件config.yaml中按照注释和本机环境情况修改配置

第三步：command :  snakemake -j 2(number of threads) --use-conda --config mode_type=[kegg/kegg_sum/abricate/abricate_sum]

		（mode_type=abricate：对vfdb的blastn）
		（mode_type=abricate_sum:统计数量和基因名称）
		（mode_type=kegg：批量注释文件夹中的faa文件生成txt）
		（mode_type=kegg_sum:运行上一条后将结果与预设进行比对生成xlsx）

（如未安装pandas和openpyxl ：pip install pandas openpyxl）