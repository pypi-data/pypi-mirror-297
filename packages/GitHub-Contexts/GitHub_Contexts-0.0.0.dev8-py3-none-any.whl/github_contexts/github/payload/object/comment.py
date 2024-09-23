from github_contexts.github.enum import AuthorAssociation
from github_contexts.github.payload.object.user import User
from github_contexts.github.payload.object.performed_via_github_app import PerformedViaGitHubApp
from github_contexts.github.payload.object.reactions import Reactions


class Comment:

    def __init__(self, comment: dict):
        self._comment = comment
        return

    @property
    def author_association(self) -> AuthorAssociation:
        return AuthorAssociation(self._comment["author_association"])

    @property
    def body(self) -> str:
        """Contents of the issue comment."""
        return self._comment["body"]

    @property
    def created_at(self) -> str:
        """Timestamp of when the comment was created."""
        return self._comment["created_at"]

    @property
    def html_url(self) -> str:
        """URL of the comment on GitHub."""
        return self._comment["html_url"]

    @property
    def id(self) -> int:
        """Unique identifier of the comment."""
        return self._comment["id"]

    @property
    def issue_url(self) -> str:
        """URL of the issue on GitHub."""
        return self._comment["issue_url"]

    @property
    def node_id(self) -> str:
        """Node ID of the comment."""
        return self._comment["node_id"]

    @property
    def performed_via_github_app(self) -> PerformedViaGitHubApp | None:
        """GitHub App that performed the comment."""
        return PerformedViaGitHubApp(self._comment["performed_via_github_app"]) if self._comment.get("performed_via_github_app") else None

    @property
    def reactions(self) -> Reactions:
        """Reactions to the comment."""
        return Reactions(self._comment["reactions"])

    @property
    def updated_at(self) -> str:
        """Timestamp of when the comment was last updated."""
        return self._comment["updated_at"]

    @property
    def url(self) -> str:
        """URL of the comment API resource."""
        return self._comment["url"]

    @property
    def user(self) -> User | None:
        """User who created the comment."""
        return User(self._comment["user"]) if self._comment.get("user") else None
