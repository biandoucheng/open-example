#!/bin/bash
#author:biandou
#启动脚本

#启动任务定时器
cd /path-to-you-workdir/crontaber/camp
nohup python3.10  -u run_task.py > your_task.log 2>&1 & echo $! > run.pid

#启动server占据窗口
cd /path-to-your-workdir/tasks/
python3.10 ./server.py