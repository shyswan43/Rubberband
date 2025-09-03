configfile: "config.yaml"

rule run_kofamscan:
    input:
        faa = os.path.join(input_dir, "{genome2}.faa"),
        db = config["profile"],
        ko_list = config["ko_list"]
    output:
        annotation = os.path.join(output_dir, "{genome2}.kofam_annotation.txt")
    conda:
        "../env/conda_env.yaml"
    shell:
        """
        exec_annotation -k {input.ko_list} -p {input.db} --cpu 20 -f mapper -T 1 -E 1e-5 -o {output} {input.faa} 
        """