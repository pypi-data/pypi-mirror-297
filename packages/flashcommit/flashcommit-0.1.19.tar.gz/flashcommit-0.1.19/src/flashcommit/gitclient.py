import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

import git
from git import Repo, Tree

from flashcommit import RepoDetails, logger
from flashcommit.client import BaseClient

git_apply_cmd = ['git', 'apply', '--recount', '--unidiff-zero', '--allow-overlap', '--inaccurate-eof',
                 '--whitespace=fix']


def get_name_from_url(url: str):
    path = url.split("/")[-1]
    if path.endswith(".git"):
        return path[0:-4]
    else:
        return path


def _repo_from_url(url):
    return {
        'owner': None,
        'repository': get_name_from_url(url),
        'url': url
    }


class PatchResult:

    def __init__(self, fixed_diff: str, original_diff: str, success: bool, msg: str | None = None):
        super().__init__()
        self.msg = msg
        self.success = success
        self.original_diff = original_diff
        self.fixed_diff = fixed_diff


class GitClient(object):

    def __init__(self, directory="."):
        super().__init__()
        self.codex_client: BaseClient | None = None
        try:
            root = self._find_git_root(directory)
            os.chdir(root)
            self.repo = Repo(root)
            self.repo_url = self._get_repo()["url"]
        except git.exc.InvalidGitRepositoryError:
            logger.error("Current directory is not a valid git repository")
            sys.exit(1)

    def _find_git_root(self, directory):
        """
        Recursively search for the git root directory.
        """
        if os.path.isdir(os.path.join(directory, ".git")):
            return directory
        parent_dir = os.path.abspath(os.path.join(directory, ".."))
        if parent_dir == directory:
            return None
        return self._find_git_root(parent_dir)

    def _get_repo(self):
        for remote in self.repo.remotes:
            for url in remote.urls:
                return _repo_from_url(url)
        return _repo_from_url(f"file:///{self.repo.common_dir}")

    def get_repo_details(self) -> RepoDetails:
        return RepoDetails(**self._get_repo())

    def get_diff(self):
        t = self.repo.head.commit.tree
        return self.repo.git.diff(t)

    def get_git_files(self):
        files = list()
        tree = self.repo.tree()
        self._read_tree(files, tree)
        return files

    def _read_tree(self, files: list[str], tree: Tree):
        for f in tree:
            if f.type == "blob":
                files.append(f.path)
            elif f.type == "tree":
                self._read_tree(files, f)

    def patch(self, description: str, diff: str, filename: str) -> list[PatchResult]:
        results = list()
        with open(filename) as sourcefile:
            source = sourcefile.read()
            parser = self.codex_client.to_patch(diff, filename, source)
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmp:
                diff_file = tmp.name
                fixed_diff = str(parser)
                tmp.write(fixed_diff)
                tmp.flush()
                try:
                    Path(".backup").mkdir(parents=True, exist_ok=True)
                    shutil.copy2(diff_file, ".backup/")
                    shutil.copy2(filename, ".backup/")
                    logger.info(f"Saving backup copy of {filename} to .backup")
                    self.repo.git.execute(
                        [*git_apply_cmd, diff_file])
                    logger.info(f"Successfully applied {description} to {filename}")
                    results.append(PatchResult(fixed_diff, diff_file, True))
                    os.unlink(diff_file)
                except git.GitCommandError as e:
                    logger.error(f"Error applying {description} to {filename}", exc_info=True)
                    self.save_for_debug(diff, filename, fixed_diff, source)
                    results.append(PatchResult(fixed_diff, diff_file, False, str(e)))
            return results

    def save_for_debug(self, diff, filename, fixed_diff, file_content):
        tempdir = f"debug-info/{int(time.time())}"
        os.makedirs(tempdir, exist_ok=True)
        logger.info(f"Saving debug info to {tempdir}")
        with open(os.path.join(tempdir, "diff"), "w") as file:
            file.write(diff)
        with open(os.path.join(tempdir, os.path.basename(filename)), "w") as file:
            file.write(file_content)
        with open(os.path.join(tempdir, "diff.fixed"), "w") as file:
            file.write(fixed_diff)

    def commit(self, message, add_all: bool = False):
        if add_all:
            self.repo.git.add(A=True)
            self.repo.git.refresh()
        index = self.repo.index
        index.commit(message)

    def diff_file(self, filename: str, content: str) -> str:
        with tempfile.NamedTemporaryFile(mode='w+', delete=True) as tmp:
            tmp.write(content)
            tmp.flush()
            return self.repo.git.diff("--no-index", filename, tmp.name, with_exceptions=False)
