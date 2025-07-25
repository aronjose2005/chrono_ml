import os
import subprocess

def make_video(agent='DQN', speed=10, fps=2):
    frame_dir = 'frames'
    output = f'videos/{agent}_speed_{speed}x.mp4'

    os.makedirs('videos', exist_ok=True)

    # 🔍 Glob pattern to match multiple frames for this agent and speed
    # Example: frames/agent_DQN_speed_10_frame_*.png
    frame_pattern = f"{frame_dir}/agent_{agent}_speed_{speed}_frame_*.png"

    command = [
        "ffmpeg",
        "-y",  # Overwrite output if it exists
        "-framerate", str(fps),
        "-pattern_type", "glob",
        "-i", frame_pattern,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output
    ]

    print(f"▶️ Running FFmpeg with pattern: {frame_pattern}")
    subprocess.run(command)
    print(f"✅ Video created at: {output}")

if __name__ == "__main__":
    make_video()

