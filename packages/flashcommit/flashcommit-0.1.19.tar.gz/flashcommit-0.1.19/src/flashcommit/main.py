import argparse
import json
import os
import sys
from collections import defaultdict
from contextlib import contextmanager
from pathlib import Path
from typing import Optional
from xml.etree import ElementTree
from xml.etree.ElementTree import XML

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from prompt_toolkit.shortcuts import button_dialog
from rich.progress import Progress
# noinspection PyProtectedMember
from websocket import _exceptions

from flashcommit import get_api_url, logger, set_batch_mode, is_batch_mode
from flashcommit.client import PlatformAdapter
from flashcommit.client.queryclient import QueryClient
from flashcommit.client.reviewclient import ReviewClient
from flashcommit.client.reviewclientV3 import ReviewClientV3
from flashcommit.flash_comit_adapter import FlashCommitAdapter
from flashcommit.gitclient import GitClient
from flashcommit.prompt_generator import PromptGenerator
from flashcommit.ui import UI
from flashcommit.version import version

NO_API_KEY_MSG = "CODEX_API_KEY environment variable not set"
NO_CHANGES_FOUND_MSG = "[yellow]No changes found.[/yellow]"
QUERY_PROGRESS_MSG = "[cyan]Thinking about your question..."
REVIEWING_PROGRESS_MSG = "[cyan]Reviewing your changes..."
COMMIT_MSG_PROGRESS_MSG = "[cyan]Generating your commit message..."


class LocalFilesystemAdapter(PlatformAdapter):

    def __init__(self, git_client: GitClient):
        self.git_client = git_client

    def read_file(self, file: str) -> Optional[str]:
        if self.is_readable(file):
            return Path(file).read_text()
        return None

    def write_file(self, file_, content):
        with open(file_, 'w') as f:
            f.write(content)

    def get_file_list(self) -> list[str]:
        return [f for f in self.git_client.get_git_files() if self.is_readable(f)]

    @staticmethod
    def is_readable(file: str) -> bool:
        return os.path.isfile(file) and os.access(file, os.R_OK)


def etree_to_dict(t):
    d = {t.tag: {} if t.attrib else None}
    children = list(t)
    if children:
        dd = defaultdict(list)
        for dc in map(etree_to_dict, children):
            for k, v in dc.items():
                dd[k].append(v)
        d = {t.tag: {k: v[0] if len(v) == 1 else v for k, v in dd.items()}}
    if t.attrib:
        d[t.tag].update(('@' + k, v) for k, v in t.attrib.items())
    if t.text:
        text = t.text.strip()
        if children or t.attrib:
            if text:
                d[t.tag]['#text'] = text
        else:
            d[t.tag] = text
    return d


def from_xml(param) -> dict:
    xml_start = param.index("<")
    xml_end = param.rfind(">")
    xml_string = param[xml_start:xml_end + 1]
    soup = BeautifulSoup(xml_string, "html5lib")
    try:
        xml: XML = ElementTree.fromstring(str(soup))
    except:
        logger.error(f"Cannot parse xml {soup}")
        raise
    to_dict = etree_to_dict(xml)
    return to_dict["html"]["body"]


def extract_dicts_with_key(data, key: str):
    result = []

    def recursive_search(item):
        if isinstance(item, dict):
            if key in item:
                result.append(item)
            for value in item.values():
                recursive_search(value)
        elif isinstance(item, list):
            for element in item:
                recursive_search(element)

    recursive_search(data)
    return result


class FlashCommit:
    def __init__(self):
        load_dotenv()
        self.git_client = GitClient()
        self.git_client.codex_client = self.create_client()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    @contextmanager
    def show_progress(self, description: str):
        if is_batch_mode():
            yield
        else:
            with Progress(refresh_per_second=10) as progress:
                task = progress.add_task(description, total=None, transient=True)
                yield
                progress.update(task, completed=True)

    def review(self) -> None:
        try:
            diff = self.git_client.get_diff()
            if diff:
                with self.show_progress(REVIEWING_PROGRESS_MSG):
                    comments = self.create_review_client().review(diff)
                self.handle_review(comments)
            else:
                logger.info(NO_CHANGES_FOUND_MSG)
        except Exception as e:
            logger.error(f"Error reviewing your changes: {str(e)}", exc_info=True)
            if isinstance(e, _exceptions.WebSocketException):
                logger.error("WebSocket connection error. Please check your internet connection.")
            elif isinstance(e, json.JSONDecodeError):
                logger.error("Error parsing server response. Please try again later.")
            sys.exit(3)

    def handle_review(self, changes):
        self.parse_review(changes)

    def parse_review(self, review_steps):

        adapter = FlashCommitAdapter(self.git_client, self.create_client(), LocalFilesystemAdapter(self.git_client))
        if not is_batch_mode():
            UI(adapter, review_steps).run()
        else:
            for file_, content, intention in review_steps:
                adapter.replace(file_, intention, content)

    def create_client(self) -> QueryClient:
        apikey = self.get_api_key()
        platform_adapter = LocalFilesystemAdapter(self.git_client)
        try:
            client = QueryClient(get_api_url() + "/v3/flashcommit/websocket/agent/query", apikey, platform_adapter)
        except _exceptions.WebSocketBadStatusException as e:
            logger.error(f"Cannot connect to server: {e.status_code}")
            if e.status_code == 403:
                logger.error("You are not authorized to access this server, check your api key")
            sys.exit(3)
        client.auth()
        return client

    def create_review_client(self) -> ReviewClient:
        apikey = self.get_api_key()
        platform_adapter = LocalFilesystemAdapter(self.git_client)
        try:
            client = ReviewClientV3(get_api_url() + "/v3/flashcommit/websocket/review", apikey, platform_adapter)
        except _exceptions.WebSocketBadStatusException as e:
            logger.error(f"Cannot connect to server: {e.status_code}")
            if e.status_code == 403:
                logger.error("You are not authorized to access this server, check your api key")
            sys.exit(3)
        client.auth()
        return client

    @staticmethod
    def get_api_key() -> Optional[str]:
        apikey = os.getenv("CODEX_API_KEY")
        if not apikey:
            raise ValueError(NO_API_KEY_MSG)
        return apikey

    def display_answer(self, comments: str) -> None:
        print(comments)

    def get_commit_message_prompt(self) -> Optional[str]:
        diff = self.git_client.get_diff()
        if not diff:
            return None
        return PromptGenerator.get_commit_message_prompt(diff)

    def generate_message(self) -> Optional[str]:
        try:
            prompt = self.get_commit_message_prompt()
            if prompt:
                with self.show_progress(COMMIT_MSG_PROGRESS_MSG):
                    client = self.create_client()
                    answer = client.to_json(client.send_single_query(prompt, temperature=0.3))
                return answer["msg"]
            else:
                logger.info(NO_CHANGES_FOUND_MSG)
                return None
        except Exception as e:
            logger.error("Error generating a commit message", exc_info=True)
            return None

    def commit(self, add_all: bool = False) -> None:
        message = self.generate_message()
        result = button_dialog(
            title='Use this as the commit message?',
            text=message,
            buttons=[
                ('Yes', 1),
                ('No', 2),
                ('Try again', 3)
            ],
        ).run()
        if result == 1:
            self.git_client.commit(message, add_all)
            logger.info("Changes committed successfully.")
        elif result == 2:
            return
        elif result == 3:
            self.commit()

    def query(self, query):
        with self.show_progress(QUERY_PROGRESS_MSG):
            msg = self.create_client().query(query)
        try:
            comments = msg["answer"]
            logger.debug(f"{msg}")
            if "changes" in msg and len(msg["changes"]) > 0:
                adapter = FlashCommitAdapter(self.git_client, self.create_client(),
                                             LocalFilesystemAdapter(self.git_client))
                if not is_batch_mode():
                    UI(adapter, msg["changes"], comments.strip()).run()
                else:
                    for obj in msg["changes"]:
                        adapter.replace(obj["filename"], obj["intention"], obj["source"])
                    self.display_answer(comments.strip())
            else:
                self.display_answer(comments.strip())
        except Exception as e:
            logger.error(f"Error processing your query, msg: {msg}", exc_info=True)

    def send_ignore(self, file_: str, comment_: str, diff_: str) -> None:
        self.create_client().save_ignore(file_, comment_, diff_)

    def replay(self, json_file: str) -> None:
        try:
            with open(json_file, "r") as f:
                recv = f.read()
                answer_msg = json.loads(recv)
                answer = answer_msg["message"]["answer"]
                self.handle_review(answer)
        except FileNotFoundError:
            logger.error(f"File not found: {json_file}")
            sys.exit(1)
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Error replaying from file {json_file}: {str(e)}", exc_info=True)
            sys.exit(1)
        logger.info(f"Successfully replayed review from {json_file}")


def main():
    parser = argparse.ArgumentParser(description='Flash Commit')
    parser.add_argument('-m', '--message', help='Generate a commit message', action='store_true')
    parser.add_argument('-c', '--commit', help='Generate a commit message and commit the changes (implies -m)',
                        action='store_true')
    parser.add_argument('-a', '--add-all', help='When committing, add all changed and new files to the index',
                        action='store_true')
    parser.add_argument('-q', '--query', help='Submit a query about the whole codebase', action='store', type=str)
    parser.add_argument('-r', '--review', help='Review the current changes - the default action', action='store_true')
    parser.add_argument('-V', '--version', help='Show version information and exit', action='store_true')
    parser.add_argument('-b', '--batch', help='Batch mode, no interactive displays, assume yes on everything',
                        default=False,
                        action='store_true')
    parser.add_argument('-R', '--replay', action='store', help=argparse.SUPPRESS)
    args = parser.parse_args()

    if args.version:
        print(version)
        sys.exit(0)
    set_batch_mode(args.batch)
    with FlashCommit() as flash:
        if args.commit:
            flash.commit(args.add_all)
        elif args.replay:
            flash.replay(args.replay)
        elif args.message:
            flash.generate_message()
        elif args.query is not None:
            flash.query(args.query)
        elif args.review or (not args.commit and not args.message and args.query is None):
            flash.review()


if __name__ == "__main__":
    main()
