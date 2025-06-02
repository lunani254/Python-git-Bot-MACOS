import git
import os
from git.exc import InvalidGitRepositoryError, GitCommandError


def get_repo_status(repo_path):
    """Check Git repository status and return changes"""
    try:
        repo = git.Repo(repo_path)
        changed_files = [item.a_path for item in repo.index.diff(None)]
        untracked_files = repo.untracked_files
        return {
            'is_repo': True,
            'branch': repo.active_branch.name,
            'changed': changed_files,
            'untracked': untracked_files,
            'has_changes': bool(changed_files or untracked_files)
        }
    except InvalidGitRepositoryError:
        return {'is_repo': False}


def commit_and_push(repo_path, commit_message):
    """Stage, commit, and push changes"""
    repo = git.Repo(repo_path)

    if repo.is_dirty(untracked_files=True):
        repo.git.add(A=True)
        repo.index.commit(commit_message)

    origin = repo.remote(name='origin')
    origin.push()
    return True
