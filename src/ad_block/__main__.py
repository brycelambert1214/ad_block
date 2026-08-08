from ad_block.screen_recorder import ReplayRecorder, ScreenRecordingError, RecorderSettings
import time

if __name__ == "__main__":

    settings = RecorderSettings(expected_fps=30, replay_seconds=5, monitor=1)
    print(settings)

    try:
        recorder = ReplayRecorder()
    except ScreenRecordingError as err:
        print(err)
        raise Exception("ScreenRecordingError: " + str(err))

    print(recorder.running)
    recorder.start()
    print((recorder.running))
    time.sleep(3)

    recorder.stop()

    stats = recorder.stats()
    print(stats.fps)
    print(stats.runtime)
    print(stats.total_frames)

    frames = recorder.frames()
    latest = recorder.latest()
