configfile: "config.yaml"

rule scp:
	input:
		"rules/scripts/data/Probiotic-derived_metabolite_biosynthesis_genes.xlsx"
	output:
		os.path.join(output_dir,"summary_kegg_sp.xlsx")
	shell:
		"""
		cp {input} {output}
		"""

