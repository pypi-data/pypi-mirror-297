from pydantic import BaseModel, field_validator


class StoredConnection(BaseModel):
    """Single element from store as python object

    """
    hostname: str
    remote_user: str
    named_passwd: str

    @field_validator('*')
    @classmethod
    def prohibit_blank_string(cls, _):
        """Stricter validation for models, that prohibits empty strings
        """
        if len(_) != 0:
            return _
        raise ValueError


class Connection:
    """Basic stored connection

    """
    hostname: str
    remote_user: str
    named_passwd: str

    def __init__(
            self,
            hostname: str,
            remote_user: str,
            named_passwd: str
    ):
        """Create a new stored connection

        :param hostname: Remote hostname or IP
        :param remote_user: User on remote machine
        :param named_passwd: First part of env var password that declares a shortened hostname
                            (eg *chkitty* for $chkitty_sweety)
        """
        self.hostname = hostname
        self.remote_user = remote_user
        self.named_passwd = named_passwd

    def env_passwd(self) -> str:
        """Return a specified env var for selected connection

        :return: $server_user like variable
        """
        return f"{self.named_passwd}_{self.remote_user}"

    def sshpass(self) -> str:
        """Returns a sshpass prepared action

        :return: sshpass -p passwd ssh user@host
        """
        return f"sshpass -p ${self.env_passwd()} ssh {self.remote_user}@{self.hostname}"

    def to_model(self) -> StoredConnection:
        """Validate instance using :StoredConnection model

        :return: :StoredConnection model instance
        """
        return StoredConnection.model_validate({
            "hostname": self.hostname,
            "remote_user": self.remote_user,
            "named_passwd": self.named_passwd
        })

    def __str__(self) -> str:
        """User-readable entry

        :return: user@host
        """
        return f"{self.remote_user}@{self.hostname}"
