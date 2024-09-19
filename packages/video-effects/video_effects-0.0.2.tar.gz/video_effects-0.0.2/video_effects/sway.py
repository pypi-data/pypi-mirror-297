import numpy as np
from PIL import Image
from moviepy.editor import ImageSequenceClip, AudioFileClip, CompositeAudioClip
import cv2


def sway(
    image_path: str,
    output_video: str,
    audio_path: str | None = None,
    sway_angle: float = 2.0,  # Maximum sway angle in degrees
    sway_speed: float = 1.5,  # Speed of the sway effect
    fps: int = 30,
    start_time: float = 0,
    end_time: float | None = None,
    sound_effect_path: str | None = None,
    sound_effect_start: float = 0,
    sound_effect_end: float | None = None,
    audio_volume: float = 1.0,
    sound_effect_volume: float = 1.0,
    move_amplitude: float = 15.0,  # Amplitude for x, y movement in pixels
    move_speed_x: float = 1.0,    # Speed of x movement
    move_speed_y: float = 1.0     # Speed of y movement
) -> str:
    """
    Apply a sway effect to an image and create a video with optional audio.

    :param image_path: Path to the input image
    :param output_video: Path for the output video
    :param audio_path: Path to the audio file
    :param sway_angle: Maximum sway angle for the image (degrees)
    :param sway_speed: Speed of the sway effect
    :param fps: Frames per second for the video
    :param start_time: Start time of the sway effect in seconds
    :param end_time: End time of the sway effect in seconds
    :param sound_effect_path: Path to the sound effect file
    :param sound_effect_start: Start time of the sound effect in seconds
    :param sound_effect_end: End time of the sound effect in seconds
    :param audio_volume: Volume of the main audio
    :param sound_effect_volume: Volume of the sound effect
    :param move_amplitude: Amplitude for x, y movement in pixels
    :param move_speed_x: Speed of the x-axis movement
    :param move_speed_y: Speed of the y-axis movement
    :return: Path to the output video file
    """
    if audio_path is None:
        raise ValueError("Audio path must be provided for determining video duration")

    # Load the image
    image = Image.open(image_path)
    image_np = np.array(image)

    # Image dimensions
    h, w = image_np.shape[:2]

    # Calculate the zoom factor to avoid black corners based on sway_angle
    max_angle_rad = np.radians(sway_angle)
    zoom_factor = 1 / np.cos(max_angle_rad)

    # Calculate additional zoom to accommodate x and y movements
    # Assuming maximum movement is move_amplitude pixels in any direction
    # Convert pixel movement to a proportion of the image dimensions
    move_zoom_x = (move_amplitude * 2) / w
    move_zoom_y = (move_amplitude * 2) / h
    # Use the maximum of the movement zoom factors
    zoom_factor += max(move_zoom_x, move_zoom_y)

    # Apply the zoom
    zoomed_width = int(w * zoom_factor)
    zoomed_height = int(h * zoom_factor)
    zoomed_image = cv2.resize(image_np, (zoomed_width, zoomed_height), interpolation=cv2.INTER_LINEAR)

    # Calculate cropping coordinates to maintain center
    crop_x = (zoomed_width - w) // 2
    crop_y = (zoomed_height - h) // 2
    zoomed_image = zoomed_image[crop_y:crop_y + h, crop_x:crop_x + w]

    # Load audio to determine the video duration
    audio_clip = AudioFileClip(audio_path).volumex(audio_volume)
    duration = audio_clip.duration  # Set duration to audio duration

    total_frames = int(fps * duration)  # Convert duration to total frames
    if end_time is None or end_time > duration:
        end_time = duration
    start_frame = int(start_time * fps)
    end_frame = int(end_time * fps)

    # Function to apply rotation and translation to the image
    def transform_image(image, angle, tx, ty):
        # Rotation
        M_rotate = cv2.getRotationMatrix2D((w // 2, h // 2), angle, 1.0)
        rotated = cv2.warpAffine(image, M_rotate, (w, h), borderMode=cv2.BORDER_REPLICATE)
        # Translation
        M_translate = np.float32([[1, 0, tx], [0, 1, ty]])
        translated = cv2.warpAffine(rotated, M_translate, (w, h), borderMode=cv2.BORDER_REPLICATE)
        return translated

    frames = []

    for frame_number in range(total_frames):
        if start_frame <= frame_number <= end_frame:
            # Calculate progress ratio
            progress = frame_number / total_frames

            # Sway angle using sine wave for smooth back and forth rotation
            angle = sway_angle * np.sin(2 * np.pi * sway_speed * progress)

            # Smooth x and y movements using separate sine waves
            tx = move_amplitude * np.sin(2 * np.pi * move_speed_x * progress)
            ty = move_amplitude * np.cos(2 * np.pi * move_speed_y * progress)

            # Apply transformations
            transformed_frame = transform_image(zoomed_image, angle, tx, ty)
            frames.append(transformed_frame)
        else:
            frames.append(zoomed_image)

    # Create video clip from the frames (frames should be NumPy arrays)
    clip = ImageSequenceClip(frames, fps=fps)

    # Add audio if provided
    if audio_path:
        audio_clip = AudioFileClip(audio_path).volumex(audio_volume)
    if sound_effect_path:
        sound_effect_clip = AudioFileClip(sound_effect_path).volumex(sound_effect_volume)
        if sound_effect_end is None or sound_effect_end > duration:
            sound_effect_end = duration
        sound_effect_clip = sound_effect_clip.subclip(0, sound_effect_end - sound_effect_start)
        sound_effect_clip = sound_effect_clip.set_start(sound_effect_start)

        if audio_path:
            audio_clip = CompositeAudioClip([audio_clip, sound_effect_clip])
        else:
            audio_clip = sound_effect_clip

    if audio_clip:
        clip = clip.set_audio(audio_clip)  # Set audio to the clip

    # Write video to output
    clip.write_videofile(output_video, codec="libx264")

    return output_video
