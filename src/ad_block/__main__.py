from ad_block.screen_recorder import ReplayRecorder, ScreenRecordingError, RecorderSettings
import time

if __name__ == "__main__":

    replay_seconds = 4
    settings = RecorderSettings(expected_fps=31, replay_seconds=replay_seconds,
                                monitor=1)
    try:
        recorder = ReplayRecorder(settings)
    except ScreenRecordingError as err:
        print(err)
        raise Exception("ScreenRecordingError: " + str(err))

    settings = RecorderSettings(expected_fps=31, replay_seconds=replay_seconds,
                                    monitor=2)
    print(recorder.running)
    recorder.start()
    print((recorder.running))
    time.sleep(replay_seconds/2)

    time.sleep(replay_seconds/2)

    recorder.stop()

    stats = recorder.stats()
    print(stats)

    frames = recorder.frames()
    print(len(frames))
    latest = recorder.latest()
