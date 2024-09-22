# SmartUp Python Package

The **SmartUp Python Package** is a Python interface to the SmartUp API, providing methods for interacting with the SmartUp platform.

SmartUp uses LLMs and ML models for communication, language understanding, and data analysis to accelerate business processes.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Features](#features)
- [License](#license)

## Installation

Install it from PyPI:

```bash
pip install smartup
```

And keep updated:

```bash
pip install --upgrade smartup
```

### Configuration

Once installed, set up the `SMARTUP_SERVER_URL` environment variable which points to your SmartUp server URL. You can set up temporarily the server url like this on MacOS/Linux:

```bash
export SMARTUP_SERVER_URL="https://yourapifromsmartup.dev"
```

## Usage

You can checkout [hello_world.py](hello_world.py) for a functional example that you can run.

### Chat with an agent

It's very easy to chat with an agent. Based on previous messages, you can chat with an agent.

```python
response = SmartUp.chat.create(
    agent_name="moishele",
    messages=[{
        "role": "user",
        "content": "Hola Moishele, ¿cómo estás?"
    }]
)

print(response) # "¡Shalom y un montón de alegrías para ti! Estoy tan bien como un bagel en un brunch dominical 😄."
```

## Features

This section will be updated soon.

- Communication with an agent
- Make a flow between agents
- Compile system prompts
- Validates variables

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for more details.
