Ring Buffer
===========
.. currentmodule:: ad_block.screen_recorder.ring_buffer


Module Documentation
--------------------

.. automodule:: ad_block.screen_recorder.ring_buffer
   :no-members:


RingBuffer
-------------

Keeps track of the current and recent screens.

Parameters
~~~~~~~~~~

capacity: int
    Maximum number of frames the buffer can hold.


Attributes
~~~~~~~~~~

.. autoattribute:: RingBuffer.capacity
.. autoattribute:: RingBuffer.frames
.. autoattribute:: RingBuffer.lock


Methods
~~~~~~~

.. automethod:: RingBuffer.__init__
.. automethod:: RingBuffer.__len__
.. automethod:: RingBuffer.add
.. automethod:: RingBuffer.snapshot
.. automethod:: RingBuffer.latest
.. automethod:: RingBuffer.resize
.. automethod:: RingBuffer.clear
