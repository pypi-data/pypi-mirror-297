# -*- coding: utf-8 -*-
#
# This file is part of the invenio-remote-user-data-kcworks package.
# Copyright (C) 2023, MESH Research.
#
# invenio-remote-user-data-kcworks is free software; you can redistribute it
# and/or modify it under the terms of the MIT License; see
# LICENSE file for more details.

"""Invenio extension for drawing user and groups data from a Remote API.

This extension provides a service and event triggers to draws user data
from a remote API associated with a SAML login ID provider. (This is
user data that cannot be derived from the SAML response itself at login,
but must be pulled separately from an API.)

The service checks to see whether the current user logged in with a SAML
provider. If so, it sends an API request to the appropriate remote API
associated with that server and stores or updates the user's data on the
remote service in the Invenio database.

By default this service is triggered when a user first registers and then
each time the user logs in. The service can also be called directly to
update user data during a logged-in session, and it can be triggered by
the remote service via a webhook signal.

Group memberships (Invenio roles)
---------------------------------

The service fetches, records, and updates a user's group memberships. The
service checks to see whether the user is a member of any groups on the
remote ID provider. If so, it adds the user to the corresponding groups
on the Invenio server via the `groups` service. If a group does not exist
on the Invenio server, the `groups` service will handle creation of the
group. If a user is the last member of a group and is removed, the
`groups` service deletes the group (i.e., the invenio-accounts role).
The `remote-user-data-kcworks` service, though, only sends the signal for the
`groups` service to add or remove the user from the group.

Note that the group membership updates are one-directional. If a user is
added to or removed from a group (role) on the Invenio server, the service
does not add the user to the corresponding group on the remote ID provider.
There may also be groups (roles) in Invenio that are strictly internal and do
not correspond with any groups on the remote ID provider (e.g., 'admin').

Once a user has been assigned the Invenio role, the user's Invenio Identity
object will be updated (on the next request) to provide role Needs
corresponding with the user's updated roles.

Note that if a remote group is associated with an Invenio collection
("community"), the service will NOT add the user to the corresponding
community. This is handled by the `groups` service.

Keeping remote data updated
---------------------------

The service is always called when a user logs in (triggered by the
user_logged_in signal emitted by flask-login). During a logged-in
session updates may be triggered by a background task or by a webhook
signal from the user's remote service. In this case the user's data for the
current session will be updated immediately and will become visible in the
UI on the next page refresh.

Update webhook
--------------

The service can be triggered by a webhook signal from the remote service. A
webhook signal should be sent to the endpoint https://example.org/api/webhooks
/user_data_update/ and the request must include a security token (provided by
the Invenio instance admins) in the request header. This token is set in the
REMOTE_USER_DATA_WEBHOOK_TOKEN configuration variable for the InvenioRDM
instance.

The webhook signal should be a POST request with a JSON body. The body should
be a JSON object whose top-level keys are

:idp: The name of the IDP registered for the remote service that is sending
      the signal. This is a
      string that must match one of the keys in the
      REMOTE_USER_DATA_API_ENDPOINTS configuration variable.

:updates: A JSON object whose top-level keys are the types of data object that
          have been updated on the remote service. The value of each key is an
          array of objects representing the updated entities. Each of these
          objects should include the "id" property, whose value is the entity's
          string identifier on the remote service. It should also include the
          "event" property, whose value is the type of event that is being
          signalled (e.g., "updated", "created", "deleted", etc.).

E.g.,

.. code-block:: json

    {"idp": "knowledgeCommons",
        "updates": {
            "users": [
                {"id": "1234", "event": "updated"},
                {"id": "5678", "event": "created"}
            ],
            "groups": [
                {"id": "1234", "event": "deleted"}
            ]
        }
    }

Logging
-------

The `remote-user-data-kcworks` extension will log each POST request to the webhook
endpoint, each signal received, and each task initiated to update the data.
These logs will be written to a dedicated log file,
`logs/remote_data_updates.log`.

Configuration
-------------

Invenio config variables
~~~~~~~~~~~~~~~~~~~~~~~~

The extension is configured via the following InvenioRDM config variables:

REMOTE_USER_DATA_API_ENDPOINTS

    A dictionary of remote ID provider names and their associated API
    information for each kind of user data. The dictionary keys are the
    names of SAML or oath IDPs registered for remote services. For each ID provider, the value is a dictionary whose
    keys are the different data categories ("groups", etc.).

    For each kind of user data, the value is again a dictionary shaped like this:

    ```python
    REMOTE_USER_DATA_API_ENDPOINTS = {
        "knowledgeCommons": {
            "users": {
                "remote_endpoint": (
                    "https://hcommons-dev.org/wp-json/commons/v1/users/"
                ),
                "remote_identifier": "id",
                "remote_method": "GET",
                "token_env_variable_label": "COMMONS_API_TOKEN",
            },
            "groups": {
                "remote_endpoint": (
                    "https://hcommons-dev.org/wp-json/commons/v1/groups/"
                ),
                "remote_identifier": "id",
                "remote_method": "GET",
                "token_env_variable_label": "COMMONS_API_TOKEN",
            },
            "entity_types": {
                "users": {"events": ["created", "updated", "deleted"]},
                "groups": {"events": ["created", "updated", "deleted"]},
            },
        }
    }
    ```

    The top level keys are the names of the remote ID providers. For each
    ID provider, the value is a dictionary with the following keys:

    :users: providing the configuration for the user data
    :groups: providing the configuration for the group data
    :entity_types: providing the configuration for the types of events that
                   can be signalled by the remote service for each kind of data

    For the `users` and `groups` keys, the value is a dictionary with the
    following keys:

    :remote_endpoint: the URL for the API endpoint where that kind of data can
                      be retrieved, including a placeholder (the string
                      "{placeholder}" for the user's identifier in the
                      API request.:
                      e.g., "https://example.com/api/user/{placeholder}"

    :remote_identifier: the property of the Invenio record (user, group role)
                        to be used as an identifier in the API request (e.g.,
                        "id", "email", etc.)

    :remote_method: the method for the request to the remote API

    :token_env_variable_label: the label used for the environment variable
                               that will hold the security token required by
                               the request. The token should be stored in the
                               .env file in the root directory of the Invenio
                               instance or set in the server system
                               environment.

    In addition, the `groups` key may include a `group_roles` key, whose value
    is a dictionary mapping the Invenio role names for group collection
    privilege roles to the corresponding role names on the remote ID provider.

REMOTE_USER_DATA_ENTITY_TYPES

    Defines

REMOTE_USER_DATA_UPDATE_INTERVAL

    The period (in minutes) between background calls to the remote API to
    update user data during a logged-in session. Default is 60 minutes.

REMOTE_USER_DATA_MQ_EXCHANGE

    The configuration for the message queue exchange used to trigger the
    background update calls. Default is a direct exchange with transient
    delivery mode (in-memory queue).

Environment variables
~~~~~~~~~~~~~~~~~~~~~

The extension also requires the following environment variables to be set:

REMOTE_USER_DATA_WEBHOOK_TOKEN (SECRET!! DO NOT place in config file!!)

    This token is used to authenticate webhook signals received from a
    remote ID provider. It should be stored in the .env file in the
    root directory of the Invenio instance or set in the server system
    environment.

Other environment variables

    The names of the environment variables for the security tokens for
    API requests to each remote ID provider should be set in the
    REMOTE_USER_DATA_API_ENDPOINTS configuration variable. The values of
    these variables should be set in the .env file in the root directory of
    the Invenio instance or set in the server system environment.

"""

from __future__ import absolute_import, print_function
from .ext import InvenioRemoteUserData

__version__ = "0.5.4-beta0"

__all__ = ("__version__", "InvenioRemoteUserData")
