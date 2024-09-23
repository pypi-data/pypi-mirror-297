from github_contexts.github.payload.object.issue import Issue
from github_contexts.github.payload.object.repository import Repository


class IssueOpenedChanges:

    def __init__(self, changes: dict):
        self._changes = changes
        return

    @property
    def old_issue(self) -> Issue | None:
        return Issue(self._changes["old_issue"]) if self._changes.get("old_issue") else None

    @property
    def old_repository(self) -> Repository:
        return Repository(self._changes["old_repository"])


class IssueTransferredChanges:

    def __init__(self, changes: dict):
        self._changes = changes
        return

    @property
    def new_issue(self) -> Issue:
        return Issue(self._changes["new_issue"])

    @property
    def new_repository(self) -> Repository:
        return Repository(self._changes["new_repository"])


class IssueEditedChanges:

    def __init__(self, changes: dict):
        self._changes = changes
        return

    @property
    def body(self) -> dict | None:
        return self._changes.get("body")

    @property
    def title(self) -> dict | None:
        return self._changes.get("title")


class PullRequestEditedChanges:

    def __init__(self, changes: dict):
        self._changes = changes
        return

    @property
    def base_ref(self) -> str | None:
        return self._changes.get("base", {}).get("ref", {}).get("from")

    @property
    def base_sha(self) -> str | None:
        return self._changes.get("base", {}).get("sha", {}).get("from")

    @property
    def body(self) -> str | None:
        """"The previous version of the body."""
        return self._changes.get("body", {}).get("from")

    @property
    def title(self) -> dict | None:
        """The previous version of the title."""
        return self._changes.get("title", {}).get("from")


class IssueCommentEditedChanges:

    def __init__(self, changes: dict):
        self._changes = changes
        return

    @property
    def body(self) -> str | None:
        """The previous version of the body."""
        return self._changes.get("body", {}).get("from")
