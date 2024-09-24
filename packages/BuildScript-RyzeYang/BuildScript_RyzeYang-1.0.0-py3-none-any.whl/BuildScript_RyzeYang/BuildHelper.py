import os
import subprocess

def MsBuildSln(slnPath, config="Release"):
    """
    获取sln路径,拼接出要执行的cmd命令

    """
    if not os.path.exists(slnPath):
        print('sln文件不存在')
        return
    cmd = ['Msbuild.exe', slnPath, "-r",
           "/t:rebuild",  f"/p:Configuration={config}"]
    subprocess.run(cmd, shell=False, capture_output=False, text=False)

def DevBuildSln(slnPath, config="Release|Any CPU"):
    """
    获取sln路径,拼接出要执行的cmd命令

    """
    if not os.path.exists(slnPath):
        print('sln文件不存在')
        return
    cmd = ['devenv.com', slnPath, 
           "/Rebuild",  config]
    subprocess.run(cmd, shell=False, capture_output=False, text=False)

def IssBuild(issFile):
    if not os.path.exists(issFile):
        print('sln文件不存在')
        return
    cmd = ['ISCC.exe', issFile]
    subprocess.run(cmd, shell=False, capture_output=False, text=False)
