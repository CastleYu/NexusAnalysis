import os

import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm


# 定义函数来解析每行数据并计算指标
def process_trace_file(file_path):
    total_io_size = 0
    read_count = 0
    write_count = 0
    io_count = 0
    min_time = float('inf')
    max_time = 0

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in tqdm(lines, desc=f"Processing {os.path.basename(file_path)}"):
            parts = line.split()
            access_size_bytes = int(parts[2])
            request_generate_time = float(parts[4])
            request_finish_time = float(parts[7])
            access_type_wait = int(parts[3])

            max_time = max(max_time, request_finish_time)
            min_time = min(min_time, request_generate_time)
            total_io_size += access_size_bytes
            io_count += 1
            if access_type_wait & 1 == 0:
                read_count += 1
            else:
                write_count += 1

    iops = round(io_count / (max_time - min_time), 2) if max_time > min_time else 0
    read_percentage = round(100 * read_count / io_count, 1) if io_count > 0 else 0
    write_percentage = round(100 * write_count / io_count, 1) if io_count > 0 else 0
    rd_wt_ratio = f"{read_percentage}/{write_percentage}"
    avg_req_size = round(total_io_size / io_count / 1024, 1) if io_count != 0 else "N/A"
    total_size = round(total_io_size / 1024 / 1024, 1) if io_count != 0 else "N/A"

    return {
        'Name': os.path.basename(file_path),
        'Number of IOs': io_count,
        'IOPS': iops,
        'RD/WT Ratio': rd_wt_ratio,
        'Req. Size(AVG)': f"{avg_req_size}KB",
        'Req. Size(Total)': f"{total_size}MB"
    }


# 定义函数来处理目录中的所有trace文件
def process_trace_directory(directory_path):
    results = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".txt"):  # 假设日志文件以.txt结尾
            file_path = os.path.join(directory_path, file_name)
            result = process_trace_file(file_path)
            results.append(result)
    return results


# 计算总计项
def calculate_totals(results):
    total_io_count = sum(item['Number of IOs'] for item in results)
    total_io_size = sum(float(item['Req. Size(Total)'].replace('MB', '')) for item in results) * 1024 * 1024
    total_time = sum(item['Number of IOs'] for item in results if item['IOPS'] > 0)
    avg_iops = round(total_io_count / total_time, 2) if total_time > 0 else 0
    avg_req_size = round(total_io_size / total_io_count / 1024, 1) if total_io_count != 0 else "N/A"
    total_size = round(total_io_size / 1024 / 1024, 1) if total_io_count != 0 else "N/A"

    total_read_count = sum(float(item['RD/WT Ratio'].split('/')[0]) * item['Number of IOs'] / 100 for item in results)
    total_write_count = sum(float(item['RD/WT Ratio'].split('/')[1]) * item['Number of IOs'] / 100 for item in results)
    total_rd_wt_ratio = f"{round(100 * total_read_count / total_io_count, 1)}/{round(100 * total_write_count / total_io_count, 1)}"

    totals = {
        'Name': 'Total',
        'Number of IOs': total_io_count,
        'IOPS': avg_iops,
        'RD/WT Ratio': total_rd_wt_ratio,
        'Req. Size(AVG)': f"{avg_req_size}KB",
        'Req. Size(Total)': f"{total_size}MB"
    }
    return totals


# 处理指定目录中的所有日志文件
directory_path = r'..\Nexus5_Kernel_BIOTracer_traces\WorkSpace_nexus5\Trace_files'  # 替换为包含日志文件的目录路径
results = process_trace_directory(directory_path)

# 计算总计项并添加到结果中
totals = calculate_totals(results)
results.append(totals)

# 转换结果为DataFrame
df = pd.DataFrame(results,
                  columns=['Name', 'Number of IOs', 'IOPS', 'RD/WT Ratio', 'Req. Size(AVG)', 'Req. Size(Total)'])

# 输出表格并保存为PDF
fig, ax = plt.subplots(figsize=(15, 9))
ax.axis('off')
table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)

plt.title('Load total number of requests and read/write ratio', fontsize=14)
plt.savefig('负载总的请求数量和读写比例_sum_line.pdf', format='pdf', bbox_inches='tight')
plt.savefig('负载总的请求数量和读写比例_sum_line.png')
plt.show()
