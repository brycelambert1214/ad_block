ReplayRecorder
==============
.. currentmodule:: ad_block.screen_recorder.recorder


Module Documentation
--------------------

.. automodule:: ad_block.screen_recorder.recorder
   :no-members:


ReplayRecorder
----------------

Class for recording the current screen information.

Parameters
~~~~~~~~~~

settings : ReplayRecorder | None
    Configuration for the recorder, including fps, replay_seconds, and monitor index.


Attributes
~~~~~~~~~~

.. autoattribute:: ReplayRecorder.settings
.. autoattribute:: ReplayRecorder.buffer
.. autoattribute:: ReplayRecorder.capture
.. autoattribute:: ReplayRecorder.running


Methods
~~~~~~~

.. automethod:: ReplayRecorder.__init__
.. automethod:: ReplayRecorder.start
.. automethod:: ReplayRecorder.stop
.. automethod:: ReplayRecorder._configure
.. automethod:: ReplayRecorder.latest
.. automethod:: ReplayRecorder.frames
.. automethod:: ReplayRecorder.runtime_fps
.. automethod:: ReplayRecorder.runtime
.. automethod:: ReplayRecorder.total_frames