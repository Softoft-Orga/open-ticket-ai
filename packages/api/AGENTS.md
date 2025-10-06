# AGENTS

This page lists available agents and their usage in the API package.

## Overview

Agents are modular components for automation and integration. Each agent provides a specific capability, such as ticket classification, note addition, or external system integration.

## Usage

Import and use agents in your workflow or API endpoints as needed.

## Example

from open_ticket_ai.agents import SomeAgent
agent = SomeAgent()
result = agent.run(data)

## Adding Agents

To add a new agent, create a class in the agents module and register it if required.

## License

LGPL-2.1
