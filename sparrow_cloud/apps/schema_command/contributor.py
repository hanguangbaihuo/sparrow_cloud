"""
    获取项目的贡献者
"""
import os
import re
from io import StringIO
import warnings
from dulwich import porcelain


def get_git_contributors(project_dir=None):
    """从项目目录下的.git文件获取贡献者的信息"""
    try:
        if project_dir is None:
            project_dir = os.getcwd()
        commit_info = StringIO()
        porcelain.log(project_dir, outstream=commit_info, max_entries=100)
        commit_text = commit_info.getvalue()
        author_re = re.compile(r".*?Author:\s(.*?)\s<,*?")
        names = set()
        for line in commit_text.splitlines():
            match = re.findall(author_re, line)
            if match:
                names.add(match[0])
        return list(names)

    except Exception as e:
        warnings.warn("get_git_contributors error {0}".format(e))


if __name__ == "__main__":
    print(get_git_contributors("/Users/zhangshishan/Documents/work/pySpace/sparrow_group_buying"))

