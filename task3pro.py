import os

import matplotlib.pyplot as plt
from tqdm import tqdm


# 定义函数来解析每行数据并计算平均IOPS
def process_trace_file_for_iops(file_path):
    io_count = 0
    min_time = float('inf')
    max_time = 0

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in tqdm(lines, desc=f"Processing {os.path.basename(file_path)}"):
            parts = line.split()
            request_generate_time = float(parts[4])
            request_finish_time = float(parts[7])

            max_time = max(max_time, request_finish_time)
            min_time = min(min_time, request_generate_time)
            io_count += 1

    total_time = max_time - min_time
    iops = io_count / total_time if total_time > 0 else 0

    return iops


# 定义函数来处理目录中的所有trace文件并计算平均IOPS
def process_trace_directory_for_iops(directory_path):
    results = []
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".txt"):  # 假设日志文件以.txt结尾
            file_path = os.path.join(directory_path, file_name)
            iops = process_trace_file_for_iops(file_path)
            results.append((file_name, iops))
    return results


# 绘制横向平均IOPS的图表
def plot_average_iops_horizontal(results):
    results_sorted = sorted(results, key=lambda x: x[1], reverse=True)
    file_names = [item[0] for item in results_sorted]
    iops_values = [item[1] for item in results_sorted]

    plt.figure(figsize=(12, 6))
    bars = plt.barh(file_names, iops_values, color='black')

    # 确定最大IOPS值
    max_iops = max(iops_values)
    threshold = max_iops * 0.02  # 5%的阈值

    # 在每个柱上添加数值
    for bar, value in zip(bars, iops_values):
        x_position = bar.get_width()
        if value == max_iops or value < threshold:
            plt.text(x_position, bar.get_y() + bar.get_height() / 2, f'{value:.1f}', va='center')

    plt.xlabel('Average IOPS')
    plt.ylabel('Trace Files')
    plt.title('Average IOPS for Different Trace Files')
    plt.grid(True, axis='x')
    plt.tight_layout()
    plt.savefig('平均IOPS_排序.png')
    plt.show()


# 处理指定目录中的所有日志文件
directory_path = r'..\Nexus5\Nexus5_Kernel_BIOTracer_traces\WorkSpace_nexus5\Trace_files'  # 替换为包含日志文件的目录路径
results = process_trace_directory_for_iops(directory_path)

# 绘制排序后的图表
plot_average_iops_horizontal(results)
