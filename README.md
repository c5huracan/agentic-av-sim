# agentic-av-sim

An agentic system for finding edge cases in comma.ai's openpilot data and matching them to video segments using physics.

## Blog Post

Full writeup: [From Telemetry to Video: Bridging comma.ai Datasets with the Power of Physics and Agents](https://c5huracan.github.io/2026/01/03/From-telemetry-to-video.html)

## Quick Start

`from agentic_av_sim import create_agent`

`chat = create_agent() r = chat.toolloop("Find 2 edge cases and match the first one to video segments.")`

## Requirements

- claudette
- datasets
- numpy
