configfile: "config.yaml"

input_dir_kg = config["output_dir"]
input_anno = glob_wildcards(os.path.join(input_dir_kg,"*.txt"))
rule kegg_dl:
	input:
		[os.path.join(input_dir_kg, f) for f in input_anno]
	output:
		output_file = os.path.join(input_dir_kg, "summary_kegg.xlsx")
	params:
		input_dir = input_dir_kg
	script:
		"scripts/kegg_deal.py"
