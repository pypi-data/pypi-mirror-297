import os
import datetime
import shutil
import re
import subprocess
import src.BuildScript_RyzeYang.BuildHelper as bs
import src.BuildScript_RyzeYang.EncryptDllHelper as ed
import src.BuildScript_RyzeYang.FileVersionHelper as UpdateVersion
from multiprocessing.dummy import Pool as ThreadPool

if __name__=="__main__":
    # 配置环境路径
    devenvPath = r'C:\Program Files\Microsoft Visual Studio\2022\Community\Common7\IDE\devenv.com'
    ezirizPath = r'C:\Users\workstation01\A_Programs\Windows\02Code\Eziriz\.NET Reactor\dotNET_Reactor.exe'
    innoSetupPath = r'C:\Program Files (x86)\Inno Setup 6\ISCC.exe'

    # 基本配置
    sourceDir = "../../source"
    binDir = "../../source/bin"
    issFilePath = "../installer.iss"
    slnPaths = [
        "../../source/RebarSkeleton2020.sln",
    ]
    buildConfig = "Release"
    # 要加密的dll前缀名
    dllPrefix = "RebarSkeleton"

    
    currentDir = os.path.dirname(__file__)
    # 设置环境变量
    devenvPath = os.path.dirname(devenvPath)
    innoSetupPath = os.path.dirname(innoSetupPath)
    ezirizPath = os.path.dirname(ezirizPath)
    os.environ['PATH'] += os.pathsep + devenvPath + innoSetupPath + ezirizPath

    # 清理bin目录
    binDir = os.path.join(currentDir, binDir)
    shutil.rmtree(binDir, ignore_errors=True)

    # 更新Dll版本号
    UpdateVersion.UpdateAssemblyVersion(sourceDir)

    # 更新安装包版本号
    issFilePath = os.path.join(currentDir, issFilePath)
    UpdateVersion.UpdateIssProjectVersion(issFilePath)
    # 更新关于界面
    UpdateVersion.UpdateAboutView(sourceDir)

    # 编译sln
    for f in slnPaths:
        fPath = os.path.join(currentDir, f)
        bs.DevBuildSln(fPath, buildConfig)

    # 混淆代码
    obfiles = []
    for root, dirs, files in os.walk(binDir):
        for f in files:
            fPath = os.path.join(root, f)
            if f.startswith(dllPrefix) and f.endswith('.dll'):
                obfiles.append(fPath)
    ed.EncryptDll(obfiles)

    # 清理无用文件
    for root, dirs, files in os.walk(binDir):
        for f in files:
            fPath = os.path.join(root, f)
            if f.endswith('.pdb') or f.endswith('.hash'):
                os.remove(fPath)

    # 编译安装包
    bs.IssBuild(issFilePath)
