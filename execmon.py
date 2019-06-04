# -*- coding: utf-8 -*-  
import os
import logging
import time
import traceback
import copy
# 创建一个logger
logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)

# 创建一个handler，用于写入日志文件
fh = logging.FileHandler('/tmp/getcmd.log')
fh.setLevel(logging.DEBUG)

# 再创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)

def getcmd():
    #捕捉进程信息
    jc = os.popen("ps -o \"%a\" --ppid 1 --no-headers").readlines()
    #去重
    return set(jc)
#获取进程为1的进程基线，监控人工启动的恶意进程
exec_base = getcmd()
while 1:    
    try:
        time.sleep( 300 )
        exec_result = getcmd()
        #求新增
        exec_result = exec_result - exec_base
        exec_tmp_add = copy.deepcopy(exec_result)
        #根据过滤条件过滤
        f = open('filter.txt','r')
        filter = f.readlines()
        if exec_tmp_add:
            for a in exec_tmp_add:
                for b in filter:
                    #判断不为空行
                    if (b.strip()!='') and (b.strip() in a):
                        exec_result.remove(a)
                        break
        print exec_result
        if exec_result: 
		    logger.info('[ADD]'+ str(exec_result) )
            #更新基线，效果为新增进程只会告警一次
            exec_base = getcmd()
    except Exception,e:

        logger.error(traceback.format_exc())
