Architecture
============

The screen recorder package is organized into several components.

ReplayRecorder
--------------

The main public interface. It coordinates recording, buffering,
and configuration.

RecorderSettings
----------------

Provides validated recorder configuration.

CaptureThread
-------------

Runs the screen capture process asynchronously.

RingBuffer
----------

Stores recent frames using a fixed-size thread-safe buffer.