Capture Thread
==============
.. currentmodule:: ad_block.screen_recorder.capture


Module Documentation
--------------------

.. automodule:: ad_block.screen_recorder.capture
   :no-members:


CaptureThread
-------------

Capture all screen related information.

Parameters
~~~~~~~~~~

buffer: RingBuffer
    Stores the most recent captured frames.

settings: RecorderSettings
    Provides validated, immutable recorder configuration.


Attributes
~~~~~~~~~~

.. autoattribute:: CaptureThread.settings
.. autoattribute:: CaptureThread.running
.. autoattribute:: CaptureThread.tot_count
.. autoattribute:: CaptureThread.runtime
.. autoattribute:: CaptureThread.fps


Methods
~~~~~~~

.. automethod:: CaptureThread.__init__
.. automethod:: CaptureThread.start_capture
.. automethod:: CaptureThread.stop_capture
.. automethod:: CaptureThread._validate_monitor
.. automethod:: CaptureThread.run