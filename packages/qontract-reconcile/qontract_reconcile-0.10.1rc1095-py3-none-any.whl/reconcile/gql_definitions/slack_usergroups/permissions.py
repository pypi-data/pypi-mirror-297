"""
Generated by qenerate plugin=pydantic_v1. DO NOT MODIFY MANUALLY!
"""
from collections.abc import Callable  # noqa: F401 # pylint: disable=W0611
from datetime import datetime  # noqa: F401 # pylint: disable=W0611
from enum import Enum  # noqa: F401 # pylint: disable=W0611
from typing import (  # noqa: F401 # pylint: disable=W0611
    Any,
    Optional,
    Union,
)

from pydantic import (  # noqa: F401 # pylint: disable=W0611
    BaseModel,
    Extra,
    Field,
    Json,
)

from reconcile.gql_definitions.fragments.user import User
from reconcile.gql_definitions.fragments.vault_secret import VaultSecret


DEFINITION = """
fragment User on User_v1 {
  name
  org_username
  github_username
  slack_username
  pagerduty_username
  tag_on_merge_requests
}

fragment VaultSecret on VaultSecret_v1 {
    path
    field
    version
    format
}

query SlackUsergroupPermission {
  permissions: permissions_v1 {
    service
    ... on PermissionSlackUsergroup_v1 {
      name
      channels
      description
      handle
      ownersFromRepos
      skip
      pagerduty {
        name
        instance {
          name
        }
        scheduleID
        escalationPolicyID
      }
      roles {
        users {
          ...User
        }
      }
      schedule {
        schedule {
          start
          end
          users {
            ...User
          }
        }
      }
      workspace {
        name
        api_client {
          global {
            max_retries
            timeout
          }
          methods {
            name
            args
          }
        }
        integrations {
          name
          token {
            ...VaultSecret
          }
          channel
        }
        managedUsergroups
      }
    }
  }
}
"""


class ConfiguredBaseModel(BaseModel):
    class Config:
        smart_union=True
        extra=Extra.forbid


class PermissionV1(ConfiguredBaseModel):
    service: str = Field(..., alias="service")


class PagerDutyInstanceV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")


class PagerDutyTargetV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    instance: PagerDutyInstanceV1 = Field(..., alias="instance")
    schedule_id: Optional[str] = Field(..., alias="scheduleID")
    escalation_policy_id: Optional[str] = Field(..., alias="escalationPolicyID")


class RoleV1(ConfiguredBaseModel):
    users: list[User] = Field(..., alias="users")


class ScheduleEntryV1(ConfiguredBaseModel):
    start: str = Field(..., alias="start")
    end: str = Field(..., alias="end")
    users: list[User] = Field(..., alias="users")


class ScheduleV1(ConfiguredBaseModel):
    schedule: list[ScheduleEntryV1] = Field(..., alias="schedule")


class SlackWorkspaceApiClientGlobalConfigV1(ConfiguredBaseModel):
    max_retries: Optional[int] = Field(..., alias="max_retries")
    timeout: Optional[int] = Field(..., alias="timeout")


class SlackWorkspaceApiClientMethodConfigV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    args: Json = Field(..., alias="args")


class SlackWorkspaceApiClientV1(ConfiguredBaseModel):
    q_global: Optional[SlackWorkspaceApiClientGlobalConfigV1] = Field(..., alias="global")
    methods: Optional[list[SlackWorkspaceApiClientMethodConfigV1]] = Field(..., alias="methods")


class SlackWorkspaceIntegrationV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    token: VaultSecret = Field(..., alias="token")
    channel: str = Field(..., alias="channel")


class SlackWorkspaceV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    api_client: Optional[SlackWorkspaceApiClientV1] = Field(..., alias="api_client")
    integrations: Optional[list[SlackWorkspaceIntegrationV1]] = Field(..., alias="integrations")
    managed_usergroups: list[str] = Field(..., alias="managedUsergroups")


class PermissionSlackUsergroupV1(PermissionV1):
    name: str = Field(..., alias="name")
    channels: list[str] = Field(..., alias="channels")
    description: str = Field(..., alias="description")
    handle: str = Field(..., alias="handle")
    owners_from_repos: Optional[list[str]] = Field(..., alias="ownersFromRepos")
    skip: Optional[bool] = Field(..., alias="skip")
    pagerduty: Optional[list[PagerDutyTargetV1]] = Field(..., alias="pagerduty")
    roles: Optional[list[RoleV1]] = Field(..., alias="roles")
    schedule: Optional[ScheduleV1] = Field(..., alias="schedule")
    workspace: SlackWorkspaceV1 = Field(..., alias="workspace")


class SlackUsergroupPermissionQueryData(ConfiguredBaseModel):
    permissions: list[Union[PermissionSlackUsergroupV1, PermissionV1]] = Field(..., alias="permissions")


def query(query_func: Callable, **kwargs: Any) -> SlackUsergroupPermissionQueryData:
    """
    This is a convenience function which queries and parses the data into
    concrete types. It should be compatible with most GQL clients.
    You do not have to use it to consume the generated data classes.
    Alternatively, you can also mime and alternate the behavior
    of this function in the caller.

    Parameters:
        query_func (Callable): Function which queries your GQL Server
        kwargs: optional arguments that will be passed to the query function

    Returns:
        SlackUsergroupPermissionQueryData: queried data parsed into generated classes
    """
    raw_data: dict[Any, Any] = query_func(DEFINITION, **kwargs)
    return SlackUsergroupPermissionQueryData(**raw_data)
