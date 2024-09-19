from moviepy.editor import ImageSequenceClip, AudioFileClip, CompositeAudioClip, VideoFileClip
from PIL import Image
import numpy as np
import os


def camera_shake(
    image_path: str,
    output_video: str,
    duration: int | None = None,
    audio_path: str | None = None,
    shift_distance: int = 5,
    fps: int = 30,
    start_time: float = 0,
    end_time: float | None = None,
    sound_effect_path: str | None = None,
    sound_effect_start: float = 0,
    sound_effect_end: float | None = None,
    audio_volume: float = 1.0,
    sound_effect_volume: float = 1.0,
) -> str:
    """
    Apply a camera shake effect to an image and create a video.

    :param image_path: Path to the input image
    :param output_video: Path for the output video
    :param audio_path: Path to the audio file
    :param duration: Duration of the video in seconds
    :param shift_distance: Maximum pixel shift for shaking
    :param fps: Frames per second for the video
    :param start_time: Start time of the shake effect in seconds
    :param end_time: End time of the shake effect in seconds
    :param sound_effect_path: Path to the sound effect file
    :param sound_effect_start: Start time of the sound effect in seconds
    :param sound_effect_end: End time of the sound effect in seconds
    :param audio_volume: Volume of the main audio
    :param sound_effect_volume: Volume of the sound effect
    :return: Path to the output video file
    """
    if duration is None and audio_path is None:
        raise ValueError("Either \"duration\" or \"audio_path\" must be provided")

    image = Image.open(image_path)
    image_np = np.array(image)

    if audio_path:
        audio_clip = AudioFileClip(audio_path).volumex(audio_volume)
        duration = audio_clip.duration  # Set duration to audio duration

    total_frames = int(fps * duration)  # Convert to integer
    if end_time is None or end_time > duration:
        end_time = duration
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)
    directions = [
        (-shift_distance, 0),
        (shift_distance, 0),
        (0, -shift_distance),
        (0, shift_distance),
    ]
    frames = []

    for frame_number in range(total_frames):
        if start_frame <= frame_number <= end_frame:
            dx, dy = directions[np.random.randint(0, len(directions))]
            shifted_image = np.roll(image_np, shift=(dy, dx), axis=(0, 1))
            cropped_frame = shifted_image[
                shift_distance:-shift_distance, shift_distance:-shift_distance
            ]
            frames.append(cropped_frame)
        else:
            frames.append(
                image_np[shift_distance:-shift_distance, shift_distance:-shift_distance]
            )

    clip = ImageSequenceClip(frames, fps=fps)

    if sound_effect_path:
        sound_effect_clip = AudioFileClip(sound_effect_path).volumex(sound_effect_volume)
        if sound_effect_end is None or sound_effect_end > duration:
            sound_effect_end = duration
        sound_effect_clip = sound_effect_clip.subclip(0, sound_effect_end - sound_effect_start)
        sound_effect_clip = sound_effect_clip.set_start(sound_effect_start)

        if audio_path:
            audio_clip = CompositeAudioClip([audio_clip, sound_effect_clip])
        else:
            audio_clip = sound_effect_clip.set_start(sound_effect_start)

    clip = ImageSequenceClip(frames, fps=fps)

    if audio_path or sound_effect_path:
        clip = clip.set_audio(audio_clip)  # Add audio to the clip

    clip.write_videofile(output_video, codec="libx264")

    return output_video


def camera_shake_video(
    input_video: str,
    output_video: str,
    shift_distance: int = 5,
    fps: int | None = None,
    start_time: float = 0,
    end_time: float | None = None,
    sound_effect_path: str | None = None,
    sound_effect_start: float = 0,
    sound_effect_end: float | None = None,
    sound_effect_volume: float = 1.0,
) -> str:
    """
    Apply a camera shake effect to a video.

    :param input_video: Path to the input video
    :param output_video: Path for the output video
    :param shift_distance: Maximum pixel shift for the shake effect
    :param fps: Frames per second for the output video (if None, uses input video's fps)
    :param start_time: Start time of the shake effect in seconds
    :param end_time: End time of the shake effect in seconds (if None, applies to end of video)
    :param sound_effect_path: Path to the sound effect file
    :param sound_effect_start: Start time of the sound effect in seconds
    :param sound_effect_end: End time of the sound effect in seconds
    :param sound_effect_volume: Volume of the sound effect
    :return: Path to the output video file
    """
    video = VideoFileClip(input_video)
    duration = video.duration
    if fps is None:
        fps = video.fps

    total_frames = int(fps * duration)
    if end_time is None or end_time > duration:
        end_time = duration
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)
    directions = [
        (-shift_distance, 0),
        (shift_distance, 0),
        (0, -shift_distance),
        (0, shift_distance),
    ]

    def shake_frame(get_frame, t):
        frame = get_frame(t)
        if start_frame <= int(t * fps) <= end_frame:
            dx, dy = directions[np.random.randint(0, len(directions))]
            shifted_frame = np.roll(frame, shift=(dy, dx), axis=(0, 1))
            return shifted_frame[shift_distance:-shift_distance, shift_distance:-shift_distance]
        return frame[shift_distance:-shift_distance, shift_distance:-shift_distance]

    shaken_clip = video.fl(shake_frame)

    if sound_effect_path:
        sound_effect_clip = AudioFileClip(sound_effect_path).volumex(sound_effect_volume)
        if sound_effect_end is None or sound_effect_end > duration:
            sound_effect_end = duration
        sound_effect_clip = sound_effect_clip.subclip(0, sound_effect_end - sound_effect_start)
        sound_effect_clip = sound_effect_clip.set_start(sound_effect_start)
        final_audio = CompositeAudioClip([video.audio, sound_effect_clip])
        shaken_clip = shaken_clip.set_audio(final_audio)

    shaken_clip.write_videofile(output_video, codec="libx264", audio_codec="aac")

    return output_video
