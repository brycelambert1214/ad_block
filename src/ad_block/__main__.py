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

    print(recorder.running)
    recorder.start()
    print((recorder.running))
    time.sleep(replay_seconds)

    recorder.stop()

    stats = recorder.stats()
    print(stats.fps)
    print(stats.duration)
    print(stats.total_frames)

    frames = recorder.frames()
    print(len(frames))
    latest = recorder.latest()
