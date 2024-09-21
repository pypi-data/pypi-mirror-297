# This module defines the public API for the silverriver package.
# It provides core components for creating and interacting with
# web automation agents, including abstract interfaces and client classes.

from silverriver.interfaces.base_agent import AbstractAgent
from silverriver.interfaces.chat import AgentChatInterface
from silverriver.client import Crux, BrowserSession
from silverriver.golden_paths.record_golden_draft import track_interactions_to_file

__all__ = [
    "AbstractAgent",
    "AgentChatInterface",
    "Crux",
    "BrowserSession",
    "track_interactions_to_file",
]
