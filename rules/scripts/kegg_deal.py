import os
import re
from openpyxl import load_workbook

def count_keywords_in_txt(txt_path, keyword):
    """
    统计txt文件中关键词出现的次数
    """
    try:
        with open(txt_path, 'r', encoding='utf-8') as f:
            text = f.read()
            # 使用正则表达式匹配关键词（支持中文、英文、数字）
            pattern = re.compile(re.escape(keyword))
            return len(pattern.findall(text))
    except Exception as e:
        print(f"读取文件 {txt_path} 时出错: {e}")
        return 0

def merge_xlsx_with_txts():
    """
    复制原xlsx文件并添加统计结果，保留所有格式
    """
    # 1. 定义文件夹路径（根据实际情况修改）
    script_dir = os.path.dirname(__file__)
    xlsx_path = os.path.join(script_dir, "data/Probiotic-derived_metabolite_biosynthesis_genes.xlsx")  # 目标xlsx文件路径
    txt_folder = snakemake.params.input_dir  # 包含txt文件的文件夹路径
    output_path = os.path.join(txt_folder,"summary_kegg.xlsx")  # 输出文件名

    # 2. 复制原文件（保留格式）
    wb = load_workbook(xlsx_path)
    new_wb = load_workbook(xlsx_path)  # 直接加载原文件作为副本

    # 3. 获取txt文件列表（不含扩展名）
    txt_files = [f[:-4] for f in os.listdir(txt_folder) if f.endswith('.txt')]
    if not txt_files:
        print("目标文件夹中没有找到txt文件")
        return

    # 4. 在第八列及之后添加数据
    for sheet in new_wb.sheetnames:
        ws = new_wb[sheet]
        txt_col = 8  # 第八列的列号（openpyxl中列索引从1开始）
        
        # 在第一行写入txt文件名（从第八列开始）
        ws.cell(row=1, column=txt_col, value=txt_files[0])  # 第八列第一行
        for i, txt_file in enumerate(txt_files[1:], start=1):
            ws.cell(row=1, column=txt_col + i, value=txt_file)  # 后续列第一行
        
        # 从第二行开始处理
        for row in range(2, ws.max_row + 1):
            keyword = ws.cell(row=row, column=5).value  # 第五列的数据作为关键词
            if not keyword or keyword == '':
                continue
                
            # 从第八列开始处理每一列
            for i, txt_file in enumerate(txt_files, start=0):
                col = txt_col + i
                # 构建txt文件路径
                full_txt_path = os.path.join(txt_folder, txt_file + '.txt')
                if os.path.exists(full_txt_path):
                    # 统计关键词出现次数
                    count = count_keywords_in_txt(full_txt_path, keyword)
                else:
                    count = 0
                ws.cell(row=row, column=col, value=count)

    # 5. 保存结果
    new_wb.save(output_path)
    print(f"结果已保存到 {output_path}")

if __name__ == "__main__":
    merge_xlsx_with_txts()