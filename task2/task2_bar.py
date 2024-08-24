import os
from datetime import datetime

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from tqdm import tqdm


# 定义函数来解析每行数据并生成读写请求随时间变化的图
def process_trace_file_for_plot(file_path):
    read_counts = []
    write_counts = []
    timestamps = []

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in tqdm(lines, desc=f"Processing {os.path.basename(file_path)}"):
            parts = line.split()
            request_generate_time = float(parts[4])
            access_type_wait = int(parts[3])

            # 转换时间戳为秒级时间
            timestamp = int(request_generate_time)

            # 初始化时间戳
            if len(timestamps) == 0 or timestamp > timestamps[-1]:
                timestamps.append(timestamp)
                read_counts.append(0)
                write_counts.append(0)

            if access_type_wait & 1 == 0:
                read_counts[-1] += 1
            else:
                write_counts[-1] += 1

    return timestamps, read_counts, write_counts


# 定义函数来处理目录中的所有trace文件并绘制图表
def process_trace_directory_for_plots(directory_path):
    for file_name in os.listdir(directory_path):
        if file_name.endswith(".txt"):  # 假设日志文件以.txt结尾
            file_path = os.path.join(directory_path, file_name)
            timestamps, read_counts, write_counts = process_trace_file_for_plot(file_path)
            plot_read_write_counts(timestamps, read_counts, write_counts, file_name)


# 将秒级时间戳转换为可视化时间戳
def convert_timestamps(timestamps):
    readable_timestamps = [datetime.fromtimestamp(ts) for ts in timestamps]
    return readable_timestamps


# 绘制读写请求随时间变化的图表
def plot_read_write_counts(timestamps, read_counts, write_counts, file_name):
    readable_timestamps = convert_timestamps(timestamps)
    plt.figure(figsize=(10, 6))
    plt.plot(readable_timestamps, read_counts, color='green', label='Reads')
    plt.plot(readable_timestamps, write_counts, color='red', label='Writes')
    plt.xlabel('Time')
    plt.ylabel('Number of requests')
    plt.title(f'Numbers of reads and writes per second\n{file_name}')
    plt.legend()
    plt.grid(True)

    # 设置x轴刻度和格式
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    plt.gca().xaxis.set_major_locator(locator)
    plt.gca().xaxis.set_major_formatter(formatter)

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f'rwcount_img_date/{file_name}_read_write_counts.png')


# 处理指定目录中的所有日志文件
os.makedirs("rwcount_img_date", exist_ok=True)
directory_path = r'..\Nexus5_Kernel_BIOTracer_traces\WorkSpace_nexus5\Trace_files'  # 替换为包含日志文件的目录路径
process_trace_directory_for_plots(directory_path)
