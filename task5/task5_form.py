import os

import pandas as pd
from matplotlib import pyplot as plt
from tqdm import tqdm


# 定义函数来解析每行数据并计算请求大小分布
def process_trace_file_for_request_size(file_path):
    request_sizes = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in tqdm(lines, desc=f"Processing {os.path.basename(file_path)}"):
            parts = line.split()
            access_size_bytes = int(parts[2])
            request_sizes.append(access_size_bytes)

    return request_sizes


# 定义函数来处理目录中的所有trace文件并计算请求大小分布
def process_trace_directory_for_request_sizes(directory_path):
    results = []
    file_names = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".txt"):  # 假设日志文件以.txt结尾
            file_path = os.path.join(directory_path, file_name)
            request_sizes = process_trace_file_for_request_size(file_path)
            results.append((file_name, request_sizes))
            file_names.append(file_name)
    return file_names, results


# 计算请求大小分布的百分比
def calculate_size_distribution(request_sizes):
    total_requests = len(request_sizes)
    bins = [0, 1024, 4096, 16384, 65536, 262144, 1048576, float('inf')]
    bin_labels = ['<1KB', '1KB-4KB', '4KB-16KB', '16KB-64KB', '64KB-256KB', '256KB-1MB', '>1MB']
    bin_counts = [0] * (len(bins) - 1)

    for size in request_sizes:
        for i in range(1, len(bins)):
            if bins[i - 1] <= size < bins[i]:
                bin_counts[i - 1] += 1
                break

    bin_percentages = [(count, round(100 * count / total_requests, 0)) for count in bin_counts]
    bin_distribution = [f"{count}({percentage:.0f}%)" for count, percentage in bin_percentages]

    return bin_distribution


# 生成总表格
def generate_summary_table(file_names, results):
    distribution_columns = ['<1KB', '1KB-4KB', '4KB-16KB', '16KB-64KB', '64KB-256KB', '256KB-1MB', '>1MB']
    summary_data = []

    for file_name, request_sizes in results:
        distribution = calculate_size_distribution(request_sizes)
        summary_data.append([file_name] + distribution)

    df = pd.DataFrame(summary_data, columns=['Name'] + distribution_columns)

    fig, ax = plt.subplots(figsize=(20, 9))
    ax.axis('off')
    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(10)
    table.scale(1.2, 1.2)

    plt.title('Request Size Distribution for Different Trace Files', fontsize=14)
    plt.savefig('请求大小分布总表.pdf', format='pdf', bbox_inches='tight')
    plt.show()


# 处理指定目录中的所有日志文件
directory_path = r'H:\Documents\Prometheus\BigData\Nexus5\Nexus5_Kernel_BIOTracer_traces\WorkSpace_nexus5\Trace_files'  # 替换为包含日志文件的目录路径
file_names, results = process_trace_directory_for_request_sizes(directory_path)

# 生成总表格
generate_summary_table(file_names, results)
