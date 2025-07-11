import os
import glob
import pandas as pd

def extract_sixth_column(filepath):
    """提取文件中第6列的数据(以分号分隔)"""
    genes_data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()[1:]  # 跳过第一行
        for line in lines:
            columns = line.strip().split('\t')
            if len(columns) >= 6:  # 确保有第6列
                genes_data.append(columns[5])  # 第6列数据
    return ';'.join(genes_data)

def count_semicolons(genes_str):
    """统计分号数量+1"""
    if not genes_str:
        return 0
    return genes_str.count(';') + 1

def main():
    # 设置路径和参数
    input_dir = snakemake.params.input_dir  # 当前目录
    output_file = os.path.join(input_dir, 'summary_all.xlsx')
    databases = ['argannot', 'card', 'ecoh', 'ecoli_vf', 'megares', 'ncbi',
                 'plasmidfinder', 'resfinder', 'vfdb']
    
    # 获取所有txt文件
    txt_files = glob.glob(os.path.join(input_dir, '*.txt'))
    
    # ======================
    # 处理各数据库sheet
    # ======================
    # 为每个数据库准备数据
    db_sheet_data = {db: {'File': [], 'genes': []} for db in databases}
    
    for db in databases:
        # 获取属于当前数据库的所有文件
        db_txt_files = [f for f in txt_files if os.path.basename(f).startswith(f'{db}@')]
        
        # 收集所有唯一的suffix
        db_suffixes = set()
        for f in db_txt_files:
            if '@' in os.path.basename(f):
                _, suffix = os.path.basename(f).split('@', 1)
                db_suffixes.add(suffix)
        
        # 对每个suffix，收集第6列的数据
        for suffix in sorted(db_suffixes):
            genes_data = []
            for txt_file in db_txt_files:
                if '@' in os.path.basename(txt_file):
                    _, file_suffix = os.path.basename(txt_file).split('@', 1)
                    if file_suffix == suffix:
                        genes_str = extract_sixth_column(txt_file)
                        genes_data.append(genes_str)
            
            # 合并同一个suffix下所有文件的基因数据(用分号分隔)
            if genes_data:
                genes_str = ';'.join(genes_data)
            else:
                genes_str = ''  # 没有数据则为空字符串
            
            # 添加到数据结构
            db_sheet_data[db]['File'].append(suffix)
            db_sheet_data[db]['genes'].append(genes_str)
    
    # 创建各数据库的DataFrame
    db_sheets_dfs = {}
    for db in databases:
        df = pd.DataFrame({
            'File': db_sheet_data[db]['File'],
            'genes': db_sheet_data[db]['genes']
        })
        db_sheets_dfs[db] = df
    
    # ======================
    # 处理summary sheet
    # ======================
    # 1. 收集所有唯一的suffix(文件名中@后的部分)
    suffixes = set()
    for txt_file in txt_files:
        filename = os.path.basename(txt_file)
        if '@' in filename:
            _, suffix = filename.split('@', 1)
            suffixes.add(suffix)
    
    # 将suffix排序
    sorted_suffixes = sorted(suffixes)
    
    # 2. 准备summary数据
    summary_data = [['File'] + databases]  # 第一行是表头
    
    # 数据行: 每行对应一个suffix
    for suffix in sorted_suffixes:
        row = [suffix]  # 第一列是File
        
        # 对于每个数据库，从对应的sheet中获取分号数量+1
        for db in databases:
            # 从对应数据库的sheet中查找该suffix对应的genes值
            genes_str = ''
            if db in db_sheets_dfs and not db_sheets_dfs[db].empty:
                # 在数据库sheet中查找File列等于当前suffix的行
                db_df = db_sheets_dfs[db]
                match_row = db_df[db_df['File'] == suffix]
                if not match_row.empty:
                    genes_str = match_row.iloc[0]['genes']
            
            # 统计分号数量+1
            count = count_semicolons(genes_str)
            row.append(count)
        
        summary_data.append(row)
    
    # 3. 创建summary DataFrame
    summary_df = pd.DataFrame(summary_data[1:], columns=summary_data[0])
    
    # ======================
    # 写入Excel文件
    # ======================
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        # 先写入各数据库sheet
        for db in databases:
            db_sheets_dfs[db].to_excel(writer, sheet_name=db, index=False)
        
        # 最后写入summary sheet
        summary_df.to_excel(writer, sheet_name='summary', index=False)
    
    print(f"处理完成，结果已保存到: {output_file}")

if __name__ == '__main__':
    main()