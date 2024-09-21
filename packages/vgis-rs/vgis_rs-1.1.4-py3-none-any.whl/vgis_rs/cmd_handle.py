import json
import os
import platform
import subprocess

test_tif_path = ""
sysstr = platform.system()
if sysstr == "Windows":
    test_tif_path = "y:/data/test_images/TW2015_3857.TIF"
    # test_tif_path = "Y:/data/test_images/2015_4b.tif"
elif sysstr == "Linux":
    test_tif_path = "/mnt/share/data/test_images/TW2015_3857.TIF"

# 执行cmd命令
cmd = "gdalinfo -json {}".format(test_tif_path)
result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

# 获取标准输出和错误信息
stdout = result.stdout
stderr = result.stderr

# 打印输出结果
print(stdout)

# 如果有错误信息，也打印它们
if stderr:
    print(stderr)
info_dict = json.loads(stdout)
proj_wkt = info_dict['coordinateSystem']['wkt']
print(proj_wkt)

# # 一次读完输出结果
# sysstr = platform.system()
# if sysstr == "Windows":
#     cmd = "wmic cpu get ProcessorId"
#     with os.popen(cmd, "r") as p:
#         r = p.read()
#
# elif sysstr == "Linux":
#     pass
#
# # 分行读输出结果
# output = os.popen(cmd, "r")
# info = output.readlines()
# for line in info:
#     print(line.replace("\n", "").replace(" ", ""))
#     server_cpu_id = line.replace("\n", "").replace(" ", "").split(":")[1]
#     print(server_cpu_id)
#     break
