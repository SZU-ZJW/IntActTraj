#!/bin/bash

# 设置输出日志文件名
log_file="Rank_final_RM_init.log"

#export CUDA_VISIBLE_DEVICES=1,2,3,4

# 使用 nohup 运行训练任务，并将输出重定向到日志文件
nohup python rank_bsz.py > "$log_file" 2>&1 &

# 获取训练任务的PID
train_pid=$!

# 通知用户训练任务已开始并在后台运行，并显示进程ID
echo "训练任务已开始并在后台运行，进程ID为 $train_pid，请查看 $log_file 文件获取输出信息。"
