import os
import pandas as pd
from collections import defaultdict

def generate_summary(folder1, folder2, output_filename="summary_kegg.xlsx"):
    """
    生成总结xlsx文件
    
    参数:
    folder1: 包含多个txt文件的文件夹(这些txt文件不分列，数据以制表符或换行符间隔)
    folder2: 包含目标txt文件的文件夹(3列)
    output_filename: 输出的xlsx文件名
    """
    
    # 1. 读取文件夹二中的目标txt文件(3列)
    target_file = None
    for file in os.listdir(folder2):
        if file.endswith('.txt'):
            target_file = os.path.join(folder2, file)
            break
    
    if not target_file:
        raise FileNotFoundError(f"在文件夹 {folder2} 中未找到txt文件")
    
    # 读取目标文件内容(6列，制表符分隔)
    target_data = []
    with open(target_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():  # 跳过空行
                parts = line.strip().split('\t')
                if len(parts) >= 6:
                    ko_num = parts[0]
                    func = parts[1]
                    gene_name = parts[2]
                    universal_name = parts[3]
                    pathway = parts[4]
                    branch = parts[5]
                    target_data.append((ko_num, func, gene_name, universal_name, pathway, branch))
    
    if not target_data:
        raise ValueError(f"目标文件 {target_file} 中没有有效数据")
    
    # 2. 处理文件夹一中的所有txt文件(不分列，数据以制表符或换行符间隔)
    txt_files = [f for f in os.listdir(folder1) if f.endswith('.txt')]
    if not txt_files:
        raise FileNotFoundError(f"文件夹 {folder1} 中没有txt文件")
    
    # 获取文件夹一中所有txt文件的名称(不含扩展名)，用于表头
    file_names = [os.path.splitext(f)[0] for f in txt_files]
    
    # 创建一个字典来存储每个ko_num在每个文件中的出现次数
    # 结构: {ko_num: {file_name: count}}
    ko_counts = defaultdict(lambda: defaultdict(int))
    
    # 处理每个txt文件(不分列)
    for file in txt_files:
        file_path = os.path.join(folder1, file)
        file_name_key = os.path.splitext(file)[0]  # 文件名(不含扩展名)
        
        with open(file_path, 'r', encoding='utf-8') as f:
            # 读取文件内容，按制表符和换行符分割所有数据项
            content = f.read()
            # 先按换行符分割，再对每行按制表符分割
            all_items = []
            for line in content.split('\n'):
                if line.strip():  # 跳过空行
                    items = line.strip().split('\t')
                    all_items.extend(items)
            
            # 统计每个ko_num的出现次数
            # ko_num格式为K后面跟5个数字(如K00000)
            for item in all_items:
                item = item.strip()
                # 检查是否符合K后面跟5个数字的格式
                if len(item) == 6 and item.startswith('K') and item[1:].isdigit():
                    ko_num = item
                    ko_counts[ko_num][file_name_key] += 1
    
    # 3. 构建DataFrame
    # 准备表头
    headers = ['ko_num', 'func', 'gene_name', 'universal_name', 'pathway', 'branch'] + file_names
    
    # 准备数据行
    data_rows = []
    
    # 对于目标文件中的每一行数据
    for ko_num, func, gene_name, universal_name, pathway, branch in target_data:
        # 只处理符合K后面跟5个数字格式的ko_num
        if len(ko_num) == 6 and ko_num.startswith('K') and ko_num[1:].isdigit():
            row = [ko_num, func, gene_name, universal_name, pathway, branch]
            
            # 对于文件夹一中的每个文件，查找该ko_num出现的次数
            for file in file_names:
                count = ko_counts.get(ko_num, {}).get(file, 0)
                row.append(count)
            
            data_rows.append(row)
    
    # 创建DataFrame
    df = pd.DataFrame(data_rows, columns=headers)
    
    # 4. 保存为xlsx文件
    output_path = os.path.join(folder1, output_filename)
    df.to_excel(output_path, index=False)
    
    print(f"总结文件已生成: {output_path}")

if __name__ == "__main__":
    script_dir = os.path.dirname(__file__)	
    
    # 设置文件夹路径
    folder1 = snakemake.params.input_dir# 包含多个txt文件的文件夹(不分列)
    folder2 = os.path.join(script_dir, "data")  # 包含目标txt文件的文件夹(3列)
    
    # 执行处理
    generate_summary(folder1, folder2)