import json
from typing import List, Optional
from subprocess import CalledProcessError
from .helpers import (
    bfs_tree_traversal,
    get_children_dict,
    create_branch as _create_branch,
    create_empty_commit,
    create_pull_request,
    does_remote_branch_exist,
    get_current_branch,
    get_parent_branch,
    get_pr_output,
    get_trunk_name,
    recursive_rebase,
    push_and_set_upstream,
    push_with_lease,
)
import logging
import traceback

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_branch(branch_name: str) -> None:
    try:
        parent_branch = get_current_branch()
        _create_branch(branch_name, parent_branch)
        commit_message = f"Branch {branch_name} extends {parent_branch}"
        create_empty_commit(commit_message)
        print(f"Created new branch {branch_name}")
    except CalledProcessError as e:
        logger.error(traceback.format_exc())

def create_pr(title: Optional[str] = None) -> None:
    try:
        current_branch, trunk_name = get_current_branch(), get_trunk_name()
        parent_branch = get_parent_branch(current_branch)

        base_branch = trunk_name
        if parent_branch and parent_branch != f"origin/{trunk_name}" and does_remote_branch_exist(parent_branch):
            base_branch = parent_branch

        if title is None:
            title = f"Pull request for {current_branch}"

        parent_pr_url = None
        if base_branch != trunk_name:
            try:
                parent_pr_output = get_pr_output(base_branch)
                parent_pr_url = json.loads(parent_pr_output)['url']
            except (json.JSONDecodeError, KeyError):
                print("Warning: Could not parse parent PR URL.")

        description = f"Depends on: {parent_pr_url}" if parent_pr_url else ""
        output = create_pull_request(base_branch, title, description)
        print(f"Successfully created draft PR: {output}")
    except CalledProcessError as e:
        logger.error(traceback.format_exc())

def anchor_stack(base_branch: str) -> None:
    try:
        recursive_rebase(base_branch)
        print(f"Anchored stack onto {base_branch} successfully")
    except CalledProcessError as e:
        logger.error(traceback.format_exc())

def propagate_changes() -> None:
    try:
        recursive_rebase()
        print("Propagated changes successfully")
    except CalledProcessError as e:
        logger.error(traceback.format_exc())

def publish_stack() -> None:
    try:
        children_dict, current_branch = get_children_dict(), get_current_branch()

        def push_branch(branch: str, _: List[str]) -> None:
            if does_remote_branch_exist(branch):
                push_with_lease(branch)
                print(f"Force-pushed updates to existing branch {branch}")
            else:
                push_and_set_upstream(branch)
                print(f"Pushed new branch {branch} to remote")

        bfs_tree_traversal(current_branch, children_dict, push_branch)
    except CalledProcessError as e:
        logger.error(traceback.format_exc())