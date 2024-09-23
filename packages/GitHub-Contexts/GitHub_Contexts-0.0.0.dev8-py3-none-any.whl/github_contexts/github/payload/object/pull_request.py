from github_contexts.github.enum import ActiveLockReason, AuthorAssociation, State
from github_contexts.github.payload.object.label import Label
from github_contexts.github.payload.object.user import User
from github_contexts.github.payload.object.milestone import Milestone
from github_contexts.github.payload.object.auto_merge import AutoMerge
from github_contexts.github.payload.object.head_base import HeadBase
from github_contexts.github.payload.object.team import Team


class PullRequest:

    def __init__(self, pull_request: dict):
        self._pull_request = pull_request
        return

    @property
    def active_lock_reason(self) -> ActiveLockReason:
        return ActiveLockReason(self._pull_request["active_lock_reason"])

    @property
    def additions(self) -> int | None:
        return self._pull_request.get("additions")

    @property
    def assignee(self) -> User | None:
        return User(self._pull_request["assignee"]) if "assignee" in self._pull_request else None

    @property
    def assignees(self) -> list[User]:
        assignees_list = self._pull_request.get("assignees", [])
        return [User(assignee) for assignee in assignees_list if assignee]

    @property
    def author_association(self) -> AuthorAssociation:
        return AuthorAssociation(self._pull_request["author_association"])

    @property
    def auto_merge(self) -> AutoMerge | None:
        return AutoMerge(self._pull_request["auto_merge"]) if self._pull_request.get("auto_merge") else None

    @property
    def base(self) -> HeadBase:
        """Pull request's base branch info."""
        return HeadBase(self._pull_request["base"])

    @property
    def body(self) -> str | None:
        """Pull request body."""
        return self._pull_request.get("body")

    @property
    def changed_files(self) -> int | None:
        return self._pull_request.get("changed_files")

    @property
    def closed_at(self) -> str | None:
        return self._pull_request.get("closed_at")

    @property
    def comments(self) -> int | None:
        return self._pull_request.get("comments")

    @property
    def comments_url(self) -> str:
        return self._pull_request["comments_url"]

    @property
    def commits(self) -> int | None:
        return self._pull_request.get("commits")

    @property
    def commits_url(self) -> str:
        return self._pull_request["commits_url"]

    @property
    def created_at(self) -> str:
        return self._pull_request["created_at"]

    @property
    def deletions(self) -> int | None:
        return self._pull_request.get("deletions")

    @property
    def diff_url(self) -> str | None:
        return self._pull_request.get("diff_url")

    @property
    def draft(self) -> bool:
        return self._pull_request["draft"]

    @property
    def head(self) -> HeadBase:
        """Pull request's head branch info."""
        return HeadBase(self._pull_request["head"])

    @property
    def html_url(self) -> str | None:
        return self._pull_request.get("html_url")

    @property
    def id(self) -> int:
        return self._pull_request["id"]

    @property
    def issue_url(self) -> str:
        return self._pull_request["issue_url"]

    @property
    def labels(self) -> list[Label]:
        return [Label(label) for label in self._pull_request.get("labels", [])]

    @property
    def locked(self) -> bool:
        return self._pull_request["locked"]

    @property
    def maintainer_can_modify(self) -> bool | None:
        return self._pull_request.get("maintainer_can_modify")

    @property
    def merge_commit_sha(self) -> str | None:
        return self._pull_request.get("merge_commit_sha")

    @property
    def mergeable(self) -> bool | None:
        return self._pull_request.get("mergeable")

    @property
    def mergeable_state(self) -> str | None:
        return self._pull_request.get("mergeable_state")

    @property
    def merged(self) -> bool | None:
        """Whether the pull request has been merged."""
        return self._pull_request.get("merged")

    @property
    def merged_at(self) -> str | None:
        return self._pull_request.get("merged_at")

    @property
    def merged_by(self) -> User | None:
        return User(self._pull_request["merged_by"]) if self._pull_request.get("merged_by") else None

    @property
    def milestone(self) -> Milestone | None:
        return Milestone(self._pull_request["milestone"]) if self._pull_request.get("milestone") else None

    @property
    def node_id(self) -> str:
        return self._pull_request["node_id"]

    @property
    def number(self) -> int:
        """Number uniquely identifying the pull request within its repository."""
        return self._pull_request["number"]

    @property
    def patch_url(self) -> str | None:
        return self._pull_request.get("patch_url")

    @property
    def rebaseable(self) -> bool | None:
        return self._pull_request.get("rebaseable")

    @property
    def requested_reviewers(self) -> list[User]:
        return [User(user) for user in self._pull_request.get("requested_reviewers", [])]

    @property
    def requested_teams(self) -> list[Team]:
        return [Team(team) for team in self._pull_request.get("requested_teams", [])]

    @property
    def review_comment_url(self) -> str:
        return self._pull_request["review_comment_url"]

    @property
    def review_comments(self) -> int | None:
        return self._pull_request.get("review_comments")

    @property
    def review_comments_url(self) -> str:
        return self._pull_request["review_comments_url"]

    @property
    def state(self) -> State:
        return State(self._pull_request["state"])

    @property
    def statuses_url(self) -> str:
        return self._pull_request["statuses_url"]

    @property
    def title(self) -> str:
        """Pull request title."""
        return self._pull_request["title"]

    @property
    def updated_at(self) -> str:
        return self._pull_request["updated_at"]

    @property
    def url(self) -> str | None:
        return self._pull_request.get("url")

    @property
    def user(self) -> User | None:
        return User(self._pull_request["user"]) if self._pull_request.get("user") else None

    @property
    def label_names(self) -> list[str]:
        return [label.name for label in self.labels]
