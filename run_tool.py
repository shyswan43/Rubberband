#!/usr/bin/env python3
import os
import yaml
import subprocess
from pathlib import Path
import click
import importlib.resources as pkg_resources
from pathlib import Path
import snakemake

# ======================
# 配置脚本路径等信息
# ======================

# 当前脚本所在目录
SCRIPT_DIR = Path(__file__).parent.resolve()
# 动态生成的 config 文件存放位置
CONFIG_DIR = SCRIPT_DIR 
DYNAMIC_CONFIG_PATH = CONFIG_DIR / "config.yaml"

# ======================
# 默认配置模板
# ======================

DEFAULT_CONFIG = {

}

def get_package_file(relative_path: str) -> str:
    """获取包内资源的绝对路径，如 Snakefile, rules/xxx.smk"""
    # "mysnaketool" 是你的包名，请确保与 setup.py 中的包名一致
    package = "rubberband"
    file_path = pkg_resources.files(package) / relative_path
    return str(file_path)

# ======================
# Helper 函数
# ======================

def generate_config(user_input_config):
    """
    根据用户传入的参数，生成最终的 config.yaml 文件内容
    并写入到 DYNAMIC_CONFIG_PATH
    """
    config = DEFAULT_CONFIG.copy()
    config.update(user_input_config)

    with open(DYNAMIC_CONFIG_PATH, "w", encoding="utf-8") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)
    click.echo(click.style(f"✅ 已生成动态配置文件: {DYNAMIC_CONFIG_PATH}", fg="green"))

def run_snakemake(dry_run=False):
    snakefile_path = get_package_file("Snakefile")
    """
    调用 snakemake 命令执行流程
    """
    cmd = [
        "snakemake",
        "-j 1",
        "--snakefile",snakefile_path,
        "--configfile",str(DYNAMIC_CONFIG_PATH),
        "--use-conda",
    ]

    if dry_run:
        cmd.append("--dry-run")

    click.echo(click.style("🚀 执行命令: " + " ".join(cmd), fg="blue"))
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        click.echo(click.style(f"❌ Snakemake 运行失败: {e}", fg="red"))
        raise click.Abort()

# ======================
# Click 命令行接口
# ======================

@click.command(context_settings={"help_option_names": ["-h", "--help"]})
@click.option("--input", required=True, help="输入文件或目录路径")
@click.option("--output", required=True, help="输出目录路径")
@click.option("--type", required=True, help="分析类型")
@click.option("-p", help="输入profile路径")
@click.option("-k", help="输入路径")
@click.option("--dry-run", is_flag=True, help="试运行，不实际执行任务")

def main(input, output, type, p, k, dry_run):
    """
    🧪 运行rubberband 生信分析流程工具

    示例：

        python run_tool.py --input input_dir/ --output output_dir/ --type abricate  使用abricate

        python run_tool.py --input input_dir/ --output output_dir/ --type abricate_sum  生成abricate总结表格

        python run_tool.py --input input_dir/ --output output_dir/ --type kegg -p profile_path/ -k ko_list_path/  使用kofamscan注释

        python run_tool.py --input input_dir/ --output output_dir/ --type kegg_sum  生成kegg总结表格

    """
    data_path=get_package_file("rules/scripts/data/Probiotic-derived_metabolite_biosynthesis_genes.xlsx")
    # 构造用户传入的配置参数（只覆盖用户指定的部分）
    user_config = {
        "input_dir": input,
        "output_dir": output,
        "mode_type": type,
        "profile": p,
        "ko_list": k,
        "data_path": str(data_path)
    }

    # 生成动态 config.yaml
    generate_config(user_config)

    # 调用 snakemake
    run_snakemake(dry_run=dry_run)

# ======================
# 脚本入口
# ======================

if __name__ == "__main__":
    main()