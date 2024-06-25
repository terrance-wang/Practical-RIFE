import os
import shutil
from pathlib import Path
from tempfile import TemporaryDirectory

def transferAudio(sourceVideo, targetVideo):
    with TemporaryDirectory() as tmpdir:
        tempAudioFileName = Path(tmpdir) / "audio.mkv"
        os.system(
            'ffmpeg -y -i "{}" -c:a copy -vn {}'.format(sourceVideo, tempAudioFileName)
        )

        targetNoAudio = (
            os.path.splitext(targetVideo)[0] + "_noaudio" + os.path.splitext(targetVideo)[1]
        )
        os.rename(targetVideo, targetNoAudio)
        # combine audio file and new video file
        os.system(
            'ffmpeg -y -i "{}" -i {} -c copy "{}"'.format(
                targetNoAudio, tempAudioFileName, targetVideo
            )
        )

        if (
            os.path.getsize(targetVideo) == 0
        ):  # if ffmpeg failed to merge the video and audio together try converting the audio to aac
            tempAudioFileName = Path(tmpdir) / "audio.m4a"
            os.system(
                'ffmpeg -y -i "{}" -c:a aac -b:a 160k -vn {}'.format(
                    sourceVideo, tempAudioFileName
                )
            )
            os.system(
                'ffmpeg -y -i "{}" -i {} -c copy "{}"'.format(
                    targetNoAudio, tempAudioFileName, targetVideo
                )
            )
            if (
                os.path.getsize(targetVideo) == 0
            ):  # if aac is not supported by selected format
                os.rename(targetNoAudio, targetVideo)
                print("Audio transfer failed. Interpolated video will have no audio")
            else:
                print(
                    "Lossless audio transfer failed. Audio was transcoded to AAC (M4A) instead."
                )

                # remove audio-less video
                os.remove(targetNoAudio)
        else:
            os.remove(targetNoAudio)
