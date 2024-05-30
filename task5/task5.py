import os

import matplotlib.pyplot as plt
import pandas as pd
from tqdm import tqdm


# 定义函数来解析每行数据并计算请求大小分布和平均请求大小
def process_trace_file_for_request_size(file_path):
    request_sizes = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in tqdm(lines, desc=f"Processing {os.path.basename(file_path)}"):
            parts = line.split()
            request_size_bytes = int(parts[2])
            request_sizes.append(request_size_bytes)

    return request_sizes


# 定义函数来处理目录中的所有trace文件并计算请求大小分布和平均请求大小
def process_trace_directory_for_request_size(directory_path):
    all_request_sizes = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".txt"):  # 假设日志文件以.txt结尾
            file_path = os.path.join(directory_path, file_name)
            request_sizes = process_trace_file_for_request_size(file_path)
            all_request_sizes.extend(request_sizes)
    return all_request_sizes


# 绘制请求大小分布图表
def plot_request_size_distribution(request_sizes):
    request_sizes_kb = [size / 1024 for size in request_sizes]
    plt.figure(figsize=(12, 6))
    plt.hist(request_sizes_kb, bins=100, color='blue', edgecolor='black')
    plt.xlabel('Request Size (KB)')
    plt.ylabel('Frequency')
    plt.title('Request Size Distribution')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('请求大小分布Org.png')
    plt.show()


# 计算并打印平均请求大小
def calculate_average_request_size(request_sizes):
    avg_size_bytes = sum(request_sizes) / len(request_sizes) if request_sizes else 0
    avg_size_kb = avg_size_bytes / 1024
    print(f"Average Request Size: {avg_size_kb:.2f} KB")
    return avg_size_kb


# 处理指定目录中的所有日志文件
directory_path = r'H:\Documents\Prometheus\BigData\Nexus5\Nexus5_Kernel_BIOTracer_traces\WorkSpace_nexus5\Trace_files'  # 替换为包含日志文件的目录路径
all_request_sizes = process_trace_directory_for_request_size(directory_path)

# 绘制请求大小分布图表
plot_request_size_distribution(all_request_sizes)

# 计算并打印平均请求大小
average_request_size = calculate_average_request_size(all_request_sizes)

# 保存请求大小分布数据到CSV文件
df = pd.DataFrame(all_request_sizes, columns=['Request Size (Bytes)'])
df['Request Size (KB)'] = df['Request Size (Bytes)'] / 1024
df.to_csv('request_size_distribution.csv', index=False)
