import os

import pandas as pd
from matplotlib import pyplot as plt
from tqdm import tqdm


# 定义函数来解析每行数据并计算请求大小
def process_trace_file_for_size_metrics(file_path):
    request_sizes = []
    total_size = 0
    min_time = float('inf')
    max_time = 0

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in tqdm(lines, desc=f"Processing {os.path.basename(file_path)}"):
            parts = line.split()
            access_size_bytes = int(parts[2])
            request_generate_time = float(parts[4])
            request_finish_time = float(parts[7])

            request_sizes.append(access_size_bytes)
            total_size += access_size_bytes
            max_time = max(max_time, request_finish_time)
            min_time = min(min_time, request_generate_time)

    avg_req_size = total_size / len(request_sizes) if request_sizes else 0
    total_time = max_time - min_time
    unit_time_size = total_size / total_time if total_time > 0 else 0

    return total_size, avg_req_size, unit_time_size


# 定义函数来处理目录中的所有trace文件并计算请求大小指标
def process_trace_directory_for_size_metrics(directory_path):
    results = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".txt"):  # 假设日志文件以.txt结尾
            file_path = os.path.join(directory_path, file_name)
            total_size, avg_req_size, unit_time_size = process_trace_file_for_size_metrics(file_path)
            results.append((file_name, total_size, f"{avg_req_size:.1f}", f"{unit_time_size:.1f}"))
    return results


# 生成总结表格
def generate_summary_table(results):
    df = pd.DataFrame(results, columns=['Name', 'Total Request Size (Bytes)', 'Average Request Size (Bytes)',
                                        'Request Size per Unit Time (Bytes/s)'])

    fig, ax = plt.subplots(figsize=(12, 9))
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    plt.title('Request Size Metrics for Different Trace Files', fontsize=14)
    plt.savefig('请求大小指标总表.pdf', format='pdf', bbox_inches='tight')
    plt.savefig('请求大小指标总表.png')


# 处理指定目录中的所有日志文件
directory_path = r'H:\Documents\Prometheus\BigData\Nexus5\Nexus5_Kernel_BIOTracer_traces\WorkSpace_nexus5\Trace_files'  # 替换为包含日志文件的目录路径
results = process_trace_directory_for_size_metrics(directory_path)


# 生成总结表格
generate_summary_table(results)
