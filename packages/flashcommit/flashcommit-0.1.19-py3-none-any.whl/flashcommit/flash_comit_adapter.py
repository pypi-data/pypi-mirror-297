from flashcommit import logger
from flashcommit.client import BaseClient, PlatformAdapter
from flashcommit.gitclient import GitClient, PatchResult


class FlashCommitAdapter:
    def __init__(self, git_client: GitClient, codex_client: BaseClient, adapter: PlatformAdapter):
        super().__init__()
        self.adapter = adapter
        self.codex_client = codex_client
        self.git_client = git_client

    def apply(self, file: str, comment: str, diff: str) -> list[PatchResult]:
        try:
            logger.info(f"Applying {comment} to {file}")
            return self.git_client.patch(comment, diff, file)
        except Exception as e:
            logger.exception(e)
            raise ValueError(f"Cannot apply: {diff} for {file}")

    def skip(self, file_, comment_, diff_):
        logger.info(f"Skipping {comment_} for {file_}")

    def ignore(self, file_, comment_, diff_):
        self.codex_client.save_ignore(file_, comment_, diff_)

    def replace(self, file_, intention, content):
        self.adapter.write_file(file_, content)
