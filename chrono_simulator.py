# chrono_simulator.py

import os
import plotly.graph_objects as go
import plotly.io as pio
import subprocess

# Configure Plotly to export PNGs using Kaleido
pio.kaleido.scope.default_format = "png"

# --- Simulation Plot Generator ---
def create_figure(frame_num, agent='DQN'):
    fig = go.Figure()

    # Simulated values — replace with actual logic if needed
    x = list(range(frame_num + 1))
    y = [i ** 0.5 for i in x]

    fig.add_trace(go.Scatter(
        x=x,
        y=y,
        mode='lines+markers',
        name=f'{agent} Agent'
    ))

    fig.update_layout(
        title=f"{agent} - Frame {frame_num}",
        xaxis_title="Steps",
        yaxis_title="Reward or State",
        template="plotly_dark",
        width=700,
        height=500
    )

    return fig

# --- Save a single frame as PNG ---
def save_frame(fig, agent, speed, frame_num):
    os.makedirs("frames", exist_ok=True)
    frame_path = f"frames/agent_{agent}_speed_{speed}_frame_{frame_num}.png"
    pio.write_image(fig, frame_path)
    print(f"✅ Saved: {frame_path}")

# --- Run full simulation loop ---
def run_simulation(agent='DQN', speed=10, total_frames=30):
    print(f"\n🎮 Simulating {agent} with speed={speed}x for {total_frames} frames...\n")
    for frame_num in range(total_frames):
        fig = create_figure(frame_num, agent)
        save_frame(fig, agent, speed, frame_num)
    print(f"\n🎬 Done saving {total_frames} frames for {agent} at speed {speed}x.")

# --- Generate video from PNGs ---
def generate_video(agent='DQN', speed=10):
    os.makedirs("videos", exist_ok=True)
    pattern = f"frames/agent_{agent}_speed_{speed}_frame_*.png"
    output_path = f"videos/{agent}_speed_{speed}x.mp4"

    print(f"▶️ Running FFmpeg with pattern: {pattern}")

    cmd = [
        "ffmpeg",
        "-y",
        "-framerate", "2",  # 2 fps = 30 frames = 15 seconds
        "-pattern_type", "glob",
        "-i", pattern.replace('*', '[0-9]*'),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_path
    ]

    subprocess.run(cmd, check=True)
    print(f"✅ Video created at: {output_path}")

