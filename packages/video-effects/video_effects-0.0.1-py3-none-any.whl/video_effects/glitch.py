import numpy as np
import cv2
from PIL import Image
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, afx
import random
import os


def apply_glitch_effect(image_path, seed=None, min_amount=1, max_amount=10):
    """Apply a glitch effect to the image by corrupting its data."""
    out = f"/tmp/glitched_{os.path.basename(image_path)}"
    prng = random.Random(seed)

    with open(image_path, "rb") as f:
        original = f.read()

        start = original.index(b"\xFF\xDA") + 2
        end = original.rindex(b"\xFF\xD9")

        data = bytearray(original[start:end])
        glitched = set()

        amount = prng.randint(min_amount, max_amount)
        for _ in range(amount):
            while True:
                index = prng.randrange(len(data))
                if index not in glitched and data[index] not in [0, 255]:
                    glitched.add(index)
                    break

            while True:
                value = prng.randint(1, 254)
                # Avoid colors that result in red, white, or green
                if data[index] != value and value not in [0, 255, 76, 150, 29]:
                    data[index] = value
                    break

    with open(out, "wb") as f:
        f.write(original[:start] + data + original[end:])

    return out

def glitch(
    image_path: str,
    audio_path: str,
    output_video: str,
    start_glitch: int = 0,
    end_glitch: int = None,
    fps: int = 30,
    glitch_intensity: float = 0.3,
    audio_volume: float = 1.0,
    sound_effect_path: str = None,
    sound_effect_start: int = 0,
    sound_effect_end: int = None,
    sound_effect_volume: float = 1.0
) -> str:
    """
    Create a video with a hacking-style glitch effect from an image.

    :param image_path: Path to the input image
    :param audio_path: Path to the audio file
    :param output_video: Path for the output video
    :param start_glitch: Start time of the glitch effect in seconds
    :param end_glitch: End time of the glitch effect in seconds
    :param fps: Frames per second for the video
    :param glitch_intensity: Intensity of the glitch effect
    :param audio_volume: Volume of the main audio
    :param sound_effect_path: Path to the sound effect file
    :param sound_effect_start: Start time of the sound effect in seconds
    :param sound_effect_end: End time of the sound effect in seconds
    :param sound_effect_volume: Volume of the sound effect
    :return: Path to the output video file
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Unable to load image from {image_path}")

    # Get image dimensions
    height, width = img.shape[:2]

    # Load audio and get duration
    audio_clip = AudioFileClip(audio_path).volumex(audio_volume)
    duration = audio_clip.duration
    if end_glitch is None or end_glitch > duration:
        end_glitch = duration

    # Create temporary video file
    temp_video = f"temp_glitch_{os.path.basename(image_path)}.mp4"
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video_writer = cv2.VideoWriter(temp_video, fourcc, fps, (width, height))

    if not video_writer.isOpened():
        raise Exception("Failed to open video writer. Check codec and file path.")

    # Generate frames with glitch effect
    for t in range(int(duration * fps)):
        current_time = t / fps
        if start_glitch <= current_time <= end_glitch:
            glitched_image_path = apply_glitch_effect(image_path, seed=t, min_amount=int(glitch_intensity * 10), max_amount=int(glitch_intensity * 20))
            glitched_frame = cv2.imread(glitched_image_path)
            os.remove(glitched_image_path)
        else:
            glitched_frame = img.copy()
        video_writer.write(glitched_frame)

    video_writer.release()

    # Add audio to the video
    video_clip = VideoFileClip(temp_video)

    # Add sound effect if provided
    if sound_effect_path:
        sfx_clip = AudioFileClip(sound_effect_path).volumex(sound_effect_volume)
        if sound_effect_end is None or sound_effect_end > duration:
            sound_effect_end = duration
        sfx_clip = sfx_clip.subclip(0, sound_effect_end - sound_effect_start)
        sfx_clip = sfx_clip.set_start(sound_effect_start)
        audio_clip = CompositeAudioClip([audio_clip, sfx_clip])

    final_clip = video_clip.set_audio(audio_clip)

    final_clip.write_videofile(output_video, codec="libx264", audio_codec="aac")

    # Clean up temporary file
    if os.path.exists(temp_video):
        os.remove(temp_video)

    return output_video

def glitch_video(
    input_video: str,
    output_video: str,
    start_glitch: float = 0,
    end_glitch: float | None = None,
    fps: int | None = None,
    glitch_intensity: float = 0.3,
    sound_effect_path: str | None = None,
    sound_effect_start: float = 0,
    sound_effect_end: float | None = None,
    sound_effect_volume: float = 1.0
) -> str:
    """
    Create a video with a glitch effect applied between start_glitch and end_glitch times.

    :param input_video: Path to the input video file.
    :param output_video: Path for the output video file.
    :param start_glitch: Start time of the glitch effect in seconds.
    :param end_glitch: End time of the glitch effect in seconds.
    :param fps: Frames per second for the output video.
    :param glitch_intensity: Intensity of the glitch effect (higher is more intense).
    :param sound_effect_path: Path to an additional sound effect file.
    :param sound_effect_start: Start time for the sound effect in seconds.
    :param sound_effect_end: End time for the sound effect in seconds.
    :param sound_effect_volume: Volume for the sound effect.
    :return: Path to the output video file.
    """
    # Load input video
    video = VideoFileClip(input_video)
    duration = video.duration
    if fps is None:
        fps = video.fps

    if end_glitch is None or end_glitch > duration:
        end_glitch = duration

    def apply_glitch_frame(get_frame, t):
        """
        Apply glitch effect to a frame at time t if within the glitch duration.

        :param get_frame: Callable to retrieve the frame at time t.
        :param t: Current time in seconds.
        :return: The modified or original frame.
        """
        frame = get_frame(t)
        if start_glitch <= t <= end_glitch:
            temp_frame_path = f"/tmp/temp_frame_{int(t*1000)}.jpg"
            cv2.imwrite(temp_frame_path, frame)

            # Apply glitch effect
            glitched_frame_path = apply_glitch_effect(
                temp_frame_path,
                seed=int(t * fps),
                min_amount=int(glitch_intensity * 10),
                max_amount=int(glitch_intensity * 20)
            )

            # Read the glitched frame
            glitched_frame = cv2.imread(glitched_frame_path)
            # Clean up temporary files
            os.remove(temp_frame_path)
            os.remove(glitched_frame_path)

            return glitched_frame
        return frame

    # Apply glitch effect to video frames
    glitched_clip = video.fl(apply_glitch_frame)

    # Add sound effect if provided
    if sound_effect_path:
        video_audio = video.audio.volumex(1.0)  # Ensure main audio volume is set
        sfx_clip = AudioFileClip(sound_effect_path).volumex(sound_effect_volume)  # Apply volume to sound effect
        if sound_effect_end is None or sound_effect_end > duration:
            sound_effect_end = duration
        # Ensure the subclip duration is positive
        sfx_duration = sound_effect_end - sound_effect_start
        if sfx_duration > 0:
            sfx_clip = sfx_clip.subclip(0, sfx_duration).set_start(sound_effect_start)
            final_audio = CompositeAudioClip([video_audio, sfx_clip])
            glitched_clip = glitched_clip.set_audio(final_audio)

    # Write the final video to the output file
    glitched_clip.write_videofile(output_video, codec="libx264", audio_codec="aac")

    return output_video
