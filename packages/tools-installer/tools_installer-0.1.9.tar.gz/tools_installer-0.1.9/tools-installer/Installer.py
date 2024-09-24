import shutil


def Append(directory, Target):
    shutil.copytree(directory, Target)

def reAppend(directory, Target):
    shutil.copyfile(directory, Target)
    shutil.copyfile(directory, Target)

def doAppend(directory, Target):
    shutil.copytree(directory, Target)