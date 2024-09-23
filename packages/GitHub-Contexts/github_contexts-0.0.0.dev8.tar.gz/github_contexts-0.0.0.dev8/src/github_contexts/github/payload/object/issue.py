from github_contexts.github.enum import ActiveLockReason, AuthorAssociation, State
from github_contexts.github.payload.object.label import Label
from github_contexts.github.payload.object.user import User
from github_contexts.github.payload.object.milestone import Milestone
from github_contexts.github.payload.object.performed_via_github_app import PerformedViaGitHubApp
from github_contexts.github.payload.object.pull_request import PullRequest
from github_contexts.github.payload.object.reactions import Reactions


class Issue:
    """
    The `issue` object contained in the payload of the `issues` and `issue_comment` events.
    """

    def __init__(self, issue: dict):
        """
        Parameters
        ----------
        issue : dict
            The `issue` dictionary contained in the payload.
        """
        self._issue = issue
        return

    @property
    def active_lock_reason(self) -> ActiveLockReason:
        return ActiveLockReason(self._issue["active_lock_reason"])

    @property
    def assignee(self) -> User | None:
        return User(self._issue["assignee"]) if "assignee" in self._issue else None

    @property
    def assignees(self) -> list[User]:
        assignees_list = self._issue.get("assignees", [])
        return [User(assignee) for assignee in assignees_list if assignee]

    @property
    def author_association(self) -> AuthorAssociation:
        return AuthorAssociation(self._issue["author_association"])

    @property
    def body(self) -> str | None:
        """Contents of the issue."""
        return self._issue["body"]

    @property
    def closed_at(self) -> str | None:
        return self._issue["closed_at"]

    @property
    def comments(self) -> int:
        return self._issue["comments"]

    @property
    def comments_url(self) -> str:
        return self._issue["comments_url"]

    @property
    def created_at(self) -> str:
        return self._issue["created_at"]

    @property
    def draft(self) -> bool | None:
        return self._issue.get("draft")

    @property
    def events_url(self) -> str:
        return self._issue["events_url"]

    @property
    def html_url(self) -> str:
        return self._issue["html_url"]

    @property
    def id(self) -> int:
        return self._issue["id"]

    @property
    def labels(self) -> list[Label]:
        return [Label(label) for label in self._issue.get("labels", [])]

    @property
    def labels_url(self) -> str:
        return self._issue["labels_url"]

    @property
    def locked(self) -> bool | None:
        return self._issue.get("locked")

    @property
    def milestone(self) -> Milestone | None:
        return Milestone(self._issue["milestone"]) if self._issue.get("milestone") else None

    @property
    def node_id(self) -> str:
        return self._issue["node_id"]

    @property
    def number(self) -> int:
        return self._issue["number"]

    @property
    def performed_via_github_app(self) -> PerformedViaGitHubApp | None:
        return PerformedViaGitHubApp(self._issue["performed_via_github_app"]) if self._issue.get("performed_via_github_app") else None

    @property
    def pull_request(self) -> PullRequest | None:
        return PullRequest(self._issue["pull_request"]) if self._issue.get("pull_request") else None

    @property
    def reactions(self) -> Reactions:
        return Reactions(self._issue["reactions"])

    @property
    def repository_url(self) -> str:
        return self._issue["repository_url"]

    @property
    def state(self) -> State | None:
        return State(self._issue["state"]) if self._issue.get("state") else None

    @property
    def state_reason(self) -> str | None:
        return self._issue.get("state_reason")

    @property
    def timeline_url(self) -> str | None:
        return self._issue.get("timeline_url")

    @property
    def title(self) -> str:
        """Title of the issue."""
        return self._issue["title"]

    @property
    def updated_at(self) -> str:
        return self._issue["updated_at"]

    @property
    def url(self) -> str:
        return self._issue["url"]

    @property
    def user(self) -> User | None:
        return User(self._issue["user"]) if self._issue.get("user") else None

    @property
    def label_names(self) -> list[str]:
        return [label.name for label in self.labels]
