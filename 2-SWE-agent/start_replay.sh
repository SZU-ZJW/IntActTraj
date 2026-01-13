#!/bin/bash

# 设置输出日志文件名
log_file="./log/run.log"

# 使用 nohup 运行推理任务，并将输出重定向到日志文件
nohup python run.py --model_name gpt4-0125 --data_path 2-SWE-agent/datasets/python__mypy_final.jsonl > "$log_file" 2>&1 &

# 获取推理任务的PID
train_pid=$!

# 通知用户推理任务已开始并在后台运行，并显示进程ID
echo "推理任务已开始并在后台运行, 进程ID为 $train_pid, 请查看 $log_file 文件获取输出信息。"
