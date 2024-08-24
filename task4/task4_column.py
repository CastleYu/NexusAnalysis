import os
import matplotlib.pyplot as plt
from tqdm import tqdm
from collections import defaultdict


# 定义函数来解析每行数据并生成IOPS随时间变化的图
def process_trace_file_for_iops_plot(file_path, interval=60):
    time_buckets = defaultdict(int)

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in tqdm(lines, desc=f"Processing {os.path.basename(file_path)}"):
            parts = line.split()
            request_generate_time = float(parts[4])

            # 将时间戳转换为时间段
            time_bucket = int(request_generate_time // interval) * interval
            time_buckets[time_bucket] += 1

    times = sorted(time_buckets.keys())
    io_counts = [time_buckets[time] for time in times]

    return times, io_counts


# 定义函数来处理目录中的所有trace文件并生成IOPS随时间变化的图
def process_trace_directory_for_iops_plots(directory_path, interval=60):
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".txt"):  # 假设日志文件以.txt结尾
            file_path = os.path.join(directory_path, file_name)
            times, io_counts = process_trace_file_for_iops_plot(file_path, interval)
            plot_iops(times, io_counts, file_name)


# 绘制IOPS随时间变化的图表
def plot_iops(times, io_counts, file_name):
    plt.figure(figsize=(12, 6))
    plt.bar(times, io_counts, width=60, color='black', align='edge')
    plt.xlabel('Time (s)')
    plt.ylabel('Total Requests (IOPS)')
    plt.title(f'Total Requests (IOPS) Over Time\n{file_name}')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'iops_over_time/{file_name}_iops_over_time.png')
    plt.show()


# 处理指定目录中的所有日志文件
os.makedirs("iops_over_time", exist_ok=True)
directory_path = r'..\Nexus5_Kernel_BIOTracer_traces\WorkSpace_nexus5\Trace_files'  # 替换为包含日志文件的目录路径
process_trace_directory_for_iops_plots(directory_path, interval=60)
