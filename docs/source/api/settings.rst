Recorder Settings
=================

.. currentmodule:: ad_block.screen_recorder.settings


Module Documentation
--------------------

.. automodule:: ad_block.screen_recorder.settings
   :no-members:


RecorderSettings
----------------

Immutable configuration for ReplayRecorder.

Parameters
~~~~~~~~~~

fps : int
    Frames per second for screen capture.

replay_seconds : float | int
    Number of seconds stored in the replay buffer.

monitor : int
    Monitor index used for capture.


Attributes
~~~~~~~~~~

.. autoattribute:: RecorderSettings.fps
.. autoattribute:: RecorderSettings.replay_seconds
.. autoattribute:: RecorderSettings.monitor
.. autoattribute:: RecorderSettings.num_frames


Methods
~~~~~~~

.. automethod:: RecorderSettings.__init__
.. automethod:: RecorderSettings.replace
.. automethod:: RecorderSettings.to_dict
.. automethod:: RecorderSettings.__repr__
.. automethod:: RecorderSettings.__eq__