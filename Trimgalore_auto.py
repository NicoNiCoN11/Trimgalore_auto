import os
import sys


def trim_auto(data, output):
    # data 数据文件的路径
    # output 输出文件的路径
    if data.endswith(".fq_1") and data.replace("_1", "_2") in os.listdir(os.path.dirname(data)):  # 双端测序
        data_2 = data.replace("_1", "_2")  # 生成配对文件路径
        output_1 = output.replace(".fq_1", "trimmed_1.fq")
        output_2 = output.replace(".fq_2", "trimmed_2.fq")  # 生成输出文件的路径
        # 生成trim_galore命令，指定输出文件的路径，添加--paired和--rrbs参数，适应双端和链特异性的数据
        cmd = f"trim_galore -o {output_1} -o {output_2} --paired --rrbs {data} {data_2}"
    elif data.endswith(".fastq"):  # 单端测序
        cmd = f"trim_galore -o {output} -q 30 {data}"
    else:  # 无效数据文件
        print(f"invalid data file: {data}")
        return

    print(f"Finish trimming for {data}")
    os.system(cmd)
    print(f"Finish trimming for {data}")  # 打印完成信息


# 获取数据目录的路径
data_dir = sys.argv[1]  # 命令行第一个参数
# 获取输出目录的路径
output_dir = sys.argv[2]  # 命令行第二个参数
# 获取目录下的所有文件名
file_list = os.listdir(data_dir)
# 用列表推导式过滤掉格式不对的文件
data_list = [file for file in file_list if file.endswith("fastq") or file.endswith("fq_1")]
# 用sorted函数对文件进行排序
data_list = sorted(data_list)
for file in data_list:
    # 拼接数据文件的路径
    data = os.path.join(data_dir, file)
    # 分割文件的基本名和扩展名
    base, ext = os.path.splitext(file)
    # 生成输出文件的路径
    output = os.path.join(output_dir, base + "_trimmed" + ext)
    trim_auto(data, output)