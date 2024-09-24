import os
import re
import datetime


def UpdateAssemblyVersion(srcDir):
    """
    更新soource文件夹下所有Assembly.cs文件,最后一位版本号自增1,

    # [assembly: AssemblyVersion("1.0.0.0")]
    # [assembly: AssemblyFileVersion("1.0.0.0")]

    即:[assembly: AssemblyVersion("1.0.0.0")] 变成[assembly: AssemblyVersion("1.0.0.1")]
    """
    # 获得Assembly 文件
    assemblyInfoFiles = []
    for root, dirs, files in os.walk(srcDir):
        for f in files:
            if (f == "AssemblyInfo.cs"):
                fPath = os.path.join(root, f)
                assemblyInfoFiles.append(fPath)
    # 读取版本号那一行
    for f in assemblyInfoFiles:
        fContent = open(f, 'r', encoding='utf-8')
        lines = fContent.readlines()
        fContent.close()
        for i, curLine in enumerate(lines):
            if ((curLine.__contains__("AssemblyVersion") or
                 (curLine.__contains__("AssemblyFileVersion")))
                    and not curLine.startswith("//")):
                mathchStr = "\"(.+?)\""
                # 获得版本号
                oldVersion = re.findall(mathchStr, curLine)
                numList = oldVersion[0].split(".")
                # 最后1位加1
                lastNum = int(numList[-1]) + 1
                numList[-1] = str(lastNum)
                # 重新合并成字符串
                newVersion = '"' + '.'.join(numList) + '"'
                # 替换原先的版本号
                curLine = re.sub(mathchStr,
                                 newVersion,
                                 curLine,
                                 count=0,
                                 flags=re.IGNORECASE)
                lines[i] = curLine
                print("oldVersion:" + oldVersion[0].removesuffix('\n'))
                print("newVersion:" + newVersion + "\n")
        # 重新写入文件
        fReWrite = open(f, "w", encoding='utf-8')
        for line in lines:
            fReWrite.write(line)
        fReWrite.close()

    # 修改增加版本号

    # 重新写入文件
    print("update Assembly Version")


def UpdateIssProjectVersion(issFilePath):
    """
    更新安装包制作文件的版本号 

    #define MyAppVersion "1.0.0"
    OutputBaseFilename =  xxxx(20240829-V1.0.0)
    """
    with open(file=issFilePath, mode='r', encoding='utf-8') as issFile:
        issContent = issFile.readlines()
        for index, value in enumerate(issContent):
            if value.startswith('#define MyAppVersion'):
                dot = value.rfind('.') + 1
                num = int(value[dot:-2]) + 1
                value = value[:dot] + str(num) + value[-2:]
                issContent[index] = value
            elif value.startswith('OutputBaseFilename='):
                # today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                today = datetime.datetime.now().strftime('%Y%m%d')
                lastDate = value[value.index('(') + 1:value.index('-')]
                dot = value.rfind('.') + 1
                num = int(value[dot:-2]) + 1
                value = value[:dot] + str(num) + value[-2:]
                issContent[index] = value.replace(lastDate, today)
    with open(file=issFilePath, mode='w', encoding='utf-8') as issFile:
        issFile.writelines(issContent)


def UpdateAboutView(sourceDir, aboutViewModel='AboutViewModel.cs'):
    """
    更新界面版本号
        public string ReleaseNumber { get; set; } = "3.0.3";
        public string ReleaseDate { get; set; } = "2024-09-03 15:14:52";
    """
    # 更新界面版本号
    aboutFile = ''
    isFound = False
    for root, dirs, files in os.walk(sourceDir):
        for f in files:
            if f == aboutViewModel:
                aboutFile = os.path.join(root, f)
                isFound = True
                break
        if isFound:
            break
    if not os.path.exists(aboutFile):
        print("没有【关于】界面")
        return
    with open(file=aboutFile, mode='r', encoding='utf-8') as f:
        fContent = f.readlines()
        for index, content in enumerate(fContent):
            if content.__contains__('ReleaseNumber'):
                dot = content.rfind('.') + 1
                num = int(content[dot:-3]) + 1
                content = content[:dot] + str(num) + content[-3:]
                # content = content.replace('.'+content[-4], '.' + str(num))
                fContent[index] = content
            elif content.__contains__('ReleaseDate'):
                today = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                fContent[index] = content.replace(
                    content[content.index('=') + 3:-3], today)
                pass
    with open(file=aboutFile, mode='w', encoding='utf-8') as f:
        f.writelines(fContent)
