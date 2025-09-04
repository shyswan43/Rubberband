rule run_abricate:
    input:
        fasta = lambda wildcards: os.path.join(
            input_dir, 
            wildcards.filename  # 从输出文件名中提取原始文件名
        )
    output:
        result = os.path.join(output_dir, "{db}@{filename}.txt"),
    params:
        db = "{db}"
    conda:
        "../env/conda_env.yaml"
    shell:
        """
        abricate --db {params.db} --quiet {input.fasta} > {output.result}
        """