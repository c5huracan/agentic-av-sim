---

# agentic-av-sim

An agentic system for finding edge cases in comma.ai's openpilot data and matching them to video segments using physics.

## Blog Post

Full writeup: [From Telemetry to Video: Bridging comma.ai Datasets with the Power of Physics and Agents](https://c5huracan.github.io/)

## Quick Start

```bash
pip install claudette datasets numpy
export ANTHROPIC_API_KEY=your_key_here
```

```python
from agentic_av_sim import create_agent

chat = create_agent()
r = chat.toolloop("Find 2 edge cases and match the first one to video segments.")
for o in r:
    if hasattr(o, 'content'):
        for block in o.content:
            if hasattr(block, 'text'): print(block.text)
```

## Requirements

- claudette
- datasets
- numpy

---

Copy that whole block directly into GitHub's editor.
