# LLM Tool Store Python Library

This library provides a Python interface to the Tool Store API.

## Installation

```bash
pip install llm-tool-store
```

## Usage

```python
from llm_tool_store import ToolStore

# Connect to the Tool Store service
tool_store = ToolStore(base_url="http://localhost:2121")

# Get a list of all tools
tools = tool_store.tools()
```
