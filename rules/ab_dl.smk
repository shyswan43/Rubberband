configfile: "config.yaml"

input_dir_ab = config["output_dir"]
input_txt = glob_wildcards(os.path.join(input_dir_ab,"*.txt"))
rule ab_dl:
	input:
		[os.path.join(input_dir_ab, f) for f in input_txt]
	output:
		output_file = os.path.join(input_dir_ab, "summary_all.xlsx")
	params:
		input_dir = input_dir_ab
	script:
		"scripts/ab_deal.py"