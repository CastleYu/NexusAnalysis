import os

import pandas as pd
from tqdm import tqdm


# 定义函数来解析每行数据并计算指标
def process_trace_file(file_path):
    total_io_size = 0
    read_count = 0
    write_count = 0
    io_count = 0
    io_sizes = []
    min_time = float('inf')
    max_time = 0

    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in tqdm(lines):
            # 解析每行数据
            parts = line.split()
            start_address = int(parts[0])
            access_size_sectors = int(parts[1])
            access_size_bytes = int(parts[2])
            access_type_wait = int(parts[3])
            request_generate_time = float(parts[4])
            request_start_time = float(parts[5])
            request_submit_time = float(parts[6])
            request_finish_time = float(parts[7])

            # 计算指标
            max_time = max(max_time, request_finish_time)
            min_time = min(min_time, request_generate_time)
            total_io_size += access_size_bytes
            io_count += 1
            io_sizes.append(access_size_bytes)
            if access_type_wait & 1 == 0:
                read_count += 1
            else:
                write_count += 1

    iops = round(io_count / (max_time - min_time), 2) if max_time > min_time else 0
    wt_rd_ratio = round(write_count / read_count, 1) if write_count != 0 else "N/A"
    avg_req_size = round(total_io_size / io_count / 1024, 1) if io_count != 0 else "N/A"

    return {
        'Total IO Count': io_count,
        'Total Read Count': read_count,
        'Total Write Count': write_count,
        'IOPS': iops,
        'Read/Write Ratio': wt_rd_ratio,
        'Average Request Size (KB)': avg_req_size,
        'Request Sizes (Bytes)': io_sizes
    }


# 调用函数并输出结果
file_path = r'H:\Documents\Prometheus\BigData\Nexus5\Nexus5_Kernel_BIOTracer_traces\WorkSpace_nexus5\Trace_files'  # 替换为你的日志文件路径
print(*os.listdir(file_path),sep= ' ')
# result = process_trace_file(file_path)
#
# # 打印结果
# for key, value in result.items():
#     if key != 'Request Sizes (Bytes)':
#         print(f"{key}: {value}")
#
# # 输出请求大小分布
# request_sizes = result['Request Sizes (Bytes)']
# df = pd.DataFrame(request_sizes, columns=['Request Size (Bytes)'])
# df['Request Size (KB)'] = df['Request Size (Bytes)'] / 1024
# print("\nRequest Size Distribution (KB):")
# print(df.describe())
