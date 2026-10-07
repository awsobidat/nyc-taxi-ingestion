"""Pendo Track Events for the NYC taxi ingestion pipeline.

The ingestion steps run in Jupyter, not in a browser, so events are sent to
Pendo's server-side Track Event API (POST <data host>/data/track) instead of
through pendo.track(). Only the standard library is used, so the Jupyter
environment needs no extra packages.

Configuration is read from the environment:

- PENDO_TRACK_EVENT_SECRET: the Track Event shared secret, sent as the
  x-pendo-integration-key header. While it is unset, events are skipped
  with a warning and the pipeline runs as before.
- PENDO_DATA_HOST: the data host of your Pendo subscription. Optional,
  defaults to https://data.pendo.io.

Tracking never raises: delivery failures are logged as warnings, so a Pendo
outage cannot stop an ingestion run.
"""

from __future__ import annotations

import json
import logging
import os
import time
import urllib.request
from typing import Any

# TODO: PENDO_TRACK_EVENT_SECRET is required for server-side tracking, and
# PENDO_DATA_HOST must match your Pendo subscription if it is not on the
# default host below. Neither was available when this module was added: set
# them on the host before `docker compose up` (docker-compose.yml passes both
# into the Jupyter container) and never commit the secret.
DEFAULT_DATA_HOST = "https://data.pendo.io"

# The pipeline is a batch job with no signed-in user, so events are
# attributed to a "system" visitor and account.
SYSTEM_ID = "system"

# Pendo's limit for the serialized properties, "properties" key included.
MAX_PROPERTIES_BYTES = 512

TIMEOUT_SECONDS = 5

logger = logging.getLogger(__name__)


def track_event(
    event: str,
    properties: dict[str, Any] | None = None,
    visitor_id: str = SYSTEM_ID,
    account_id: str = SYSTEM_ID,
) -> bool:
    """Send one Track Event to Pendo.

    Returns True if Pendo accepted the event and False if it was skipped or
    could not be delivered. Never raises.
    """
    secret = os.environ.get("PENDO_TRACK_EVENT_SECRET")
    if not secret:
        logger.warning(
            "PENDO_TRACK_EVENT_SECRET is not set; skipped Pendo event %r",
            event,
        )
        return False

    try:
        properties = properties or {}
        properties_size = len(_to_json({"properties": properties}))
        if properties_size > MAX_PROPERTIES_BYTES:
            logger.warning(
                "Pendo event %r has %d bytes of properties (limit %d)",
                event,
                properties_size,
                MAX_PROPERTIES_BYTES,
            )
        payload = {
            "type": "track",
            "event": event,
            "visitorId": visitor_id,
            "accountId": account_id,
            "timestamp": int(time.time() * 1000),
            "properties": properties,
        }
        data_host = os.environ.get("PENDO_DATA_HOST") or DEFAULT_DATA_HOST
        request = urllib.request.Request(
            data_host.rstrip("/") + "/data/track",
            data=_to_json(payload),
            headers={
                "Content-Type": "application/json",
                "x-pendo-integration-key": secret,
            },
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS):
            return True
    except Exception as exc:  # tracking must never stop the pipeline
        logger.warning("Could not send Pendo event %r: %s", event, exc)
        return False


def _to_json(value: Any) -> bytes:
    return json.dumps(value, separators=(",", ":"), default=str).encode()
