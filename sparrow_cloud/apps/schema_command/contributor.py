"""
    获取项目的贡献者
"""
import os
from git import Repo


def get_git_contributors(git_dir_path=None):
    """从项目目录下的.git文件获取贡献者的信息"""
    if git_dir_path is None:
        work_dir = os.getcwd()
        git_dir_path = os.path.join(work_dir, ".git")
    if not os.path.isdir(git_dir_path):
        return
    repo = Repo(git_dir_path)
    names = set()
    contributors = []
    for commit in repo.iter_commits('master', max_count=1024):
        if commit.committer.name not in ("GitHub", ):
            if commit.committer.name in names:
                continue
            names.add(commit.committer.name)
            contributors.append(commit.committer.name)
    return contributors


if __name__ == "__main__":
    print(get_git_contributors("/Users/zhangshishan/Documents/work/pySpace/sparrow_common/.git"))
