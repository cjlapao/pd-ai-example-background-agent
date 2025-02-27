# Example Background Agent

This is an example project demonstrating how to create background agents for the PRL AI Agent system.

## Overview

Background agents run independently of chat sessions and can:

- Process messages from various parts of the application
- Perform periodic tasks on a timer
- Monitor system status and resources
- Interact with external systems

## Structure

- `agents/` - Contains the background agent implementations
- `requirements.txt` - Dependencies for the agents
- `package.json` - Metadata for the agent package

## Installation

This package can be installed through the PRL AI Agent registry:

```
# From the agent registry UI
1. Go to Settings > Agent Registry
2. Click "Add Package"
3. Enter the repository URL: https://github.com/yourusername/example-background-agent
4. Click "Install"
```

## Creating Your Own Background Agent

1. Create a class that inherits from `BackgroundAgent`
2. Implement the required methods:
   - `process()` - Called periodically based on the interval
   - `process_message()` - Called when a subscribed message is received
3. Subscribe to message types in the constructor
4. Register your agent in the package.json file

## Example Usage

See the `agents/example_agent.py` file for a complete example of a background agent.

## License

MIT
