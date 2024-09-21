import json

from flashcommit import logger
from flashcommit.client.reviewclient import ReviewClient


class ReviewClientV3(ReviewClient):

    class InvalidResponseError(Exception):
        pass

    def review_with_files(self, diff: str, files: dict[str, str]) -> list[tuple[str, str, str]]:
        self._send_msg("review", {"diff": diff, "files": files})
        recv = self.ws.recv()
        try:
            logger.debug(f"Answer: {recv}")
            answer_msg = json.loads(recv)
            changes = answer_msg.get("message", {}).get("changes")
            if not isinstance(changes, list):
                raise self.InvalidResponseError("Expected 'changes' to be a list")
            return [(change[0], change[1], change[2]) for change in changes]
        except json.JSONDecodeError:
            logger.error(f"Cannot parse JSON response: {recv}")
            raise
        except KeyError as e:
            logger.error(f"Missing key in response: {e}")
            raise self.InvalidResponseError(f"Missing key in response: {e}")
        except IndexError as e:
            logger.error(f"Invalid change format in response: {e}")
            raise self.InvalidResponseError(f"Invalid change format in response: {e}")
        except Exception as e:
            logger.error(f"Unexpected error processing response: {e}")
            raise
