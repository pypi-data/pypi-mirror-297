from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip
from PIL import Image
import numpy as np
import cv2
import os


def pan_right(
    image_path: str,
    output_video: str,
    audio_path: str,
    output_width: int,
    output_height: int,
    fps: int = 30,
    audio_volume: float = 1.0,
    sound_effect_path: str = None,
    sound_effect_start: float = 0.0,
    sound_effect_end: float = None,
    sound_effect_volume: float = 1.0,
) -> str:
    """
    Apply the pan right effect to an image and return the video clip.

    :param image_path: Path to the image file
    :param output_video: Path to the output video file
    :param audio_path: Path to the audio file
    :param output_width: Width of the output video
    :param output_height: Height of the output video
    :param fps: Frames per second for the output video
    :param audio_volume: Volume of the main audio
    :param sound_effect_path: Path to the sound effect file
    :param sound_effect_start: Start time of the sound effect
    :param sound_effect_end: End time of the sound effect
    :param sound_effect_volume: Volume of the sound effect
    :return: Path to the output video file
    """

    # Check if output dimensions are larger than the image
    img = Image.open(image_path)
    if output_width > img.width or output_height > img.height:
        raise ValueError(f"Output dimensions ({output_width}x{output_height}) cannot be larger than the image dimensions ({img.width}x{img.height})")

    # Set the size of the mobile aspect ratio crop (9:16)
    crop_height = output_height
    crop_width = output_width
    # Load the audio file to get its duration
    audio_clip = AudioFileClip(audio_path).volumex(audio_volume)
    audio_duration = audio_clip.duration
    # Calculate the step size based on the audio duration and fps
    total_frames = int(audio_duration * fps)
    step_size = max(1, (img.width - crop_width) // total_frames)
    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Use 'mp4v' codec for better compatibility
    temp_video = f"temp_pan_right_{os.path.basename(image_path)}.mp4"
    video_writer = cv2.VideoWriter(temp_video, fourcc, fps, (crop_width, crop_height))
    if not video_writer.isOpened():
        raise Exception("Failed to open video writer. Check codec and file path.")

    # Create frames by moving the crop window from left to right
    for left in range(0, img.width - crop_width + 1, step_size):
        # Crop the image using Pillow
        box = (left, 0, left + crop_width, crop_height)
        cropped_img = img.crop(box)
        # Convert the PIL image to a NumPy array for OpenCV
        frame = np.array(cropped_img)
        # Convert RGB to BGR format for OpenCV compatibility
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # Write the frame to the video file
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


def pan_left(
    image_path: str,
    output_video: str,
    audio_path: str,
    output_width: int,
    output_height: int,
    fps: int = 30,
    audio_volume: float = 1.0,
    sound_effect_path: str = None,
    sound_effect_start: float = 0.0,
    sound_effect_end: float = None,
    sound_effect_volume: float = 1.0,
) -> str:
    """
    Create a video with a pan left effect from an image.

    :param image_path: Path to the input image
    :param output_video: Path for the output video
    :param audio_path: Path to the audio file
    :param output_width: Width of the output video
    :param output_height: Height of the output video
    :param fps: Frames per second for the video
    :param audio_volume: Volume of the main audio
    :param sound_effect_path: Path to the sound effect file
    :param sound_effect_start: Start time of the sound effect
    :param sound_effect_end: End time of the sound effect
    :param sound_effect_volume: Volume of the sound effect
    :return: Path to the output video file
    """

    # Check if output dimensions are larger than the image
    img = Image.open(image_path)
    if output_width > img.width or output_height > img.height:
        raise ValueError(f"Output dimensions ({output_width}x{output_height}) cannot be larger than the image dimensions ({img.width}x{img.height})")

    # Set the size of the mobile aspect ratio crop (9:16)
    crop_height = output_height
    crop_width = output_width
    # Load the audio file to get its duration
    audio_clip = AudioFileClip(audio_path).volumex(audio_volume)
    audio_duration = audio_clip.duration
    # Calculate the step size based on the audio duration and fps
    total_frames = int(audio_duration * fps)
    step_size = max(1, (img.width - crop_width) // total_frames)
    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Use 'mp4v' codec for better compatibility
    temp_video = f"temp_pan_left_{os.path.basename(image_path)}.mp4"
    video_writer = cv2.VideoWriter(temp_video, fourcc, fps, (crop_width, crop_height))
    if not video_writer.isOpened():
        raise Exception("Failed to open video writer. Check codec and file path.")

    # Create frames by moving the crop window from right to left
    for right in range(img.width - crop_width, -1, -step_size):
        # Crop the image using Pillow
        box = (right, 0, right + crop_width, crop_height)
        cropped_img = img.crop(box)
        # Convert the PIL image to a NumPy array for OpenCV
        frame = np.array(cropped_img)
        # Convert RGB to BGR format for OpenCV compatibility
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        # Write the frame to the video file
        video_writer.write(frame)

    # Release the video writer
    video_writer.release()
    # Ensure the temporary video file exists
    if not os.path.exists(temp_video):
        raise FileNotFoundError(f"Temporary video file {temp_video} not found!")

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
