"""
    获取项目的贡献者
"""
import os
import re


def get_git_contributors(head_file_path=None):
    """从项目目录下的.git文件获取作者信息"""
    if head_file_path is None:
        head_file_path = ".git/logs/HEAD"
    head_info_re = re.compile("\w+\s\w+\s(.*?)\s.*?\n")
    if os.path.isfile(head_file_path):
        with open(head_file_path, "r") as f:
            head_text = f.read()
            names = re.findall(head_info_re, head_text)
            if names:
                unique_names = set(names)
                return list(unique_names)


if __name__ == "__main__":
    print(get_git_contributors("/Users/zhangshishan/Documents/work/pySpace/sparrow_cloud/.git/logs/HEAD"))
