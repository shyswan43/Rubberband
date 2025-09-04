rule scp:
	input:
		config["data_path"]
	output:
		os.path.join(output_dir,"summary_kegg_sp.xlsx")
	shell:
		"""
		cp {input} {output}
		"""

