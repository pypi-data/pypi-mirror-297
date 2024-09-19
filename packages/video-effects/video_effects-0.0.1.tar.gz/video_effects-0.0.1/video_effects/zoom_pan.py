from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, ImageClip
from PIL import Image
import numpy as np
import cv2
import os


def zoom_out_pan_top_right(
    image_path: str,
    output_video: str,
    audio_path: str,
    output_width: int = 576,
    output_height: int = 1024,
    zoom_factor: float = 1.5,
    fps: int = 30,
    audio_volume: float = 1.0,
    sound_effect_path: str = None,
    sound_effect_start: float = 0.0,
    sound_effect_end: float = None,
    sound_effect_volume: float = 1.0,
) -> str:
    """
    Apply a pan right effect with gradual zoom out to an image and return the video clip.

    :param image_path: Path to the image file
    :param output_video: Path to the output video file
    :param audio_path: Path to the audio file
    :param output_width: Width of the output video
    :param output_height: Height of the output video
    :param zoom_factor: Starting zoom factor (default 1.5)
    :param fps: Frames per second for the output video
    :param audio_volume: Volume of the main audio
    :param sound_effect_path: Path to the sound effect file
    :param sound_effect_start: Start time of the sound effect
    :param sound_effect_end: End time of the sound effect
    :param sound_effect_volume: Volume of the sound effect
    :return: Path to the output video file
    """
    # Load the image
    img = Image.open(image_path)
    img_width, img_height = img.size

    # Load the audio file to get its duration
    audio_clip = AudioFileClip(audio_path).volumex(audio_volume)
    audio_duration = audio_clip.duration

    # Calculate the total number of frames
    total_frames = int(audio_duration * fps)

    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    temp_video = f"temp_zoom_pan_{os.path.basename(image_path)}.mp4"
    video_writer = cv2.VideoWriter(temp_video, fourcc, fps, (output_width, output_height))
    if not video_writer.isOpened():
        raise Exception("Failed to open video writer. Check codec and file path.")

    # Create frames with zoom out and pan right effect
    for frame_number in range(total_frames):
        t = frame_number / total_frames
        zoom = zoom_factor - (zoom_factor - 1) * t  # Zoom out linearly
        left = int((img_width - output_width / zoom) * t)
        top = int((img_height - output_height / zoom) * t)  # Pan to top-right

        # Crop and resize the image
        box = (left, top, left + int(output_width / zoom), top + int(output_height / zoom))
        cropped_img = img.crop(box)
        resized_img = cropped_img.resize((output_width, output_height), Image.LANCZOS)

        # Convert the PIL image to a NumPy array for OpenCV
        frame = np.array(resized_img)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        video_writer.write(frame)

    # Release the video writer
    video_writer.release()

    # Ensure the temporary video file exists
    if not os.path.exists(temp_video):
        raise FileNotFoundError(f"Temporary video file {temp_video} not found!")

    # Load and configure the sound effect if provided
    if sound_effect_path:
        sound_effect_clip = AudioFileClip(sound_effect_path).volumex(sound_effect_volume)
        if sound_effect_end is None or sound_effect_end > audio_duration:
            sound_effect_end = audio_duration
        sound_effect_clip = sound_effect_clip.subclip(0, sound_effect_end - sound_effect_start)
        sound_effect_clip = sound_effect_clip.set_start(sound_effect_start)
        audio_clip = CompositeAudioClip([audio_clip, sound_effect_clip])

    # Add audio to the video
    video_clip = VideoFileClip(temp_video)
    final_clip = video_clip.set_audio(audio_clip).set_duration(audio_duration)
    final_clip.write_videofile(output_video, codec="libx264", audio_codec="aac")

    if not os.path.exists(output_video):
        raise FileNotFoundError(f"Output video file {output_video} not found!")

    if os.path.exists(temp_video):
        os.remove(temp_video)

    return output_video
