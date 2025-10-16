#!/bin/bash

# filepath: /home/NingyuanXiao/run_script_with_retries.sh

# 定义变量
SCRIPT_PATH="/home/NingyuanXiao/multi-agents/medical_data/kg_gemma3_2.py"
REPEAT_COUNT=30
WAIT_TIME=700  # 15分钟，单位为秒

for ((i=1; i<=REPEAT_COUNT; i++))
do
    echo "运行第 $i 次: $(date)"
    
    # 启动 Python 脚本
    python3 "$SCRIPT_PATH" &
    SCRIPT_PID=$!

    # 等待 15 分钟
    sleep $WAIT_TIME

    # 中断脚本
    echo "中断第 $i 次运行: $(date)"
    kill $SCRIPT_PID

    # 确保进程已终止
    wait $SCRIPT_PID 2>/dev/null
done

echo "所有运行完成: $(date)"