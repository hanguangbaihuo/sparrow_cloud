"""
    获取项目的贡献者
"""
import os
import re
from gitdb import LooseObjectDB
import warnings


# def get_git_contributors(git_dir_path=None):
#     """从项目目录下的.git文件获取贡献者的信息"""
#     if git_dir_path is None:
#         work_dir = os.getcwd()
#         git_dir_path = os.path.join(work_dir, ".git")
#     if not os.path.isdir(git_dir_path):
#         return
#     repo = Repo(git_dir_path)
#     names = set()
#     contributors = []
#     for commit in repo.iter_commits('master', max_count=1024):
#         if commit.committer.name not in ("GitHub", ):
#             if commit.committer.name in names:
#                 continue
#             names.add(commit.committer.name)
#             contributors.append(commit.committer.name)
#     return contributors


def get_git_contributors(git_dir_path=None):
    """从项目目录下的.git文件获取贡献者的信息"""
    try:
        if git_dir_path is None:
            work_dir = os.getcwd()
            git_dir_path = os.path.join(work_dir, ".git/objects")
        if not os.path.isdir(git_dir_path):
            return
        ldb = LooseObjectDB(git_dir_path)
        author_re = re.compile(r".*?author\s(.*?)\s<,*?")
        names = set()
        for sha in ldb.sha_iter():
            if ldb.info(sha)[1] == b"commit":
                ostream = ldb.stream(sha)
                node = ostream.read().decode("utf-8")
                match = re.findall(author_re, node)
                if match:
                    names.add(match[0])
        return list(names)
    except Exception as e:
        warnings.warn("get_git_contributors error {0}".format(e))


if __name__ == "__main__":
    print(get_git_contributors("/Users/zhangshishan/Documents/work/pySpace/sparrow_common/.git/objects"))
