configfile: "config.yaml"

kofamscan_env = config["kofamscan_env"]
db = config["kofam_db"]
ko_list = config["kofam_ko_list"]

rule run_kofamscan:
    input:
        faa = os.path.join(input_dir, "{genome2}.faa")
    output:
        annotation = os.path.join(output_dir, "{genome2}.kofam_annotation.txt")
    conda:
        kofamscan_env
    params:
        db = db,
        ko_list = ko_list
    shell:
        """
        exec_annotation -k {params.ko_list} -p {params.db} --cpu 20 -f mapper -T 1 -E 1e-5 -o {output} {input.faa} 
        """