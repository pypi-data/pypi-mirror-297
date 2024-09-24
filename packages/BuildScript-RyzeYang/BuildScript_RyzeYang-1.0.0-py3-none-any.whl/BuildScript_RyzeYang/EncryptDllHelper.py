import subprocess
import os
from multiprocessing.dummy import Pool as ThreadPool


def NetReactorEncrypt(self, files):
    """
    加密dll
    """
    ezirizPath = r'dotNET_Reactor.exe'
    # 拼接加密参数
    para1 = '-showloadingscreen 0'.split(' ')
    para4 = '-necrobit 1 -necrobit_comp 1 -suppressildasm 0 -obfuscation 0 -mapping_file 0 -antitamp 0 -stringencryption 1 -resourceencryption 1 -control_flow_obfuscation 1 -flow_level 9'.split(
        ' ')
    encryptCmds = []
    encryptCmds.clear()
    for f in files:
        # 加密前的dll和加密后的dll为相同路径
        # 即加密后，直接覆盖原先的dll
        if not os.path.exists(f):
            continue
        beforeObf = f
        afterObf = f
        para2 = ['-file', beforeObf]
        para3 = ['-targetfile', afterObf]
        para = para1+para2+para3+para4
        cmd = [ezirizPath]+para
        encryptCmds.append(cmd)
    # for cmd in encryptCmds:
    #     ExcuteEncryptCmd(cmd)
    pool = ThreadPool()
    pool.map(self.__ExcuteEncryptCmd, encryptCmds)
    pool.close()
    pool.join()


def ExcuteCmd(self, cmd):
    ret = subprocess.run(cmd, shell=False, capture_output=True, text=True)
    try:
        if ret.stdout.__contains__('Successfully'):
            print('加密: '+cmd[4].split('\\')[-1])
            print(ret.stdout)
        elif len(ret.stdout) == 0:
            print("已加密"+cmd[4].split('\\')[-1])
        else:
            print("加密失败"+cmd[4].split('\\')[-1])
    except:
        pass
