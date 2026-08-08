# Ad Block

A Python-based computer vision system for detecting and replacing full-screen advertisements.

## Documentation

Full documentation is available here:

https://github.com/brycelambert1214/ad_block

## Overview

Ad Block is a research and development project focused on building a system capable of identifying unwanted advertisements and replacing them with user-selected content.

The project is currently in the early development phase, with the primary focus being the construction of a reliable, low-latency screen capture and replay system. Future development will integrate computer vision models for advertisement detection and automated replacement.

## Current Development Status

The current implementation focuses on the **screen recorder subsystem**, which provides:

* configurable screen capture
* thread-based frame acquisition
* thread-safe frame buffering
* replay buffer functionality
* runtime capture statistics
* configurable recording settings

## Architecture

The current screen recorder architecture is organized around three main layers:

```
ReplayRecorder
      |
      v
CaptureManager
      |
      +-- CaptureThread
      |
      +-- RingBuffer
      |
      +-- CaptureStats
```

## Installation

Clone the repository:

```bash
git clone https://github.com/brycelambert1214/ad_block
```

Navigate into the project:

```bash
cd ad-block
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

### Windows

```bash
.venv\Scripts\activate
```

### Linux/macOS

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -e .
```

## Testing

The project uses `pytest` for testing.

Run the test suite:

```bash
pytest
```

Current tests cover:

* configuration validation
* ring buffer behavior
* frame storage and retrieval
* resizing behavior
* exception handling

## Development Goals

### Completed

* [x] Thread-safe frame buffer
* [x] Configurable recording settings
* [x] Basic screen capture implementation
* [x] Recording lifecycle management
* [x] Initial unit test suite

### In Progress

* [ ] Capture manager abstraction
* [ ] Improved capture backend architecture
* [ ] Expanded statistics tracking
* [ ] Hardware capture support

### Future

* [ ] Multiple capture sources
* [ ] HDMI/video input support
* [ ] Advertisement detection model
* [ ] Automated advertisement replacement
* [ ] User-specific advertisement training data

## License

This project is currently under development.
License information will be added when the project is prepared for release.
