k# utils.py
import os
import plotly.io as pio
import plotly.graph_objects as go

def simulate(agent_name, speed, frame_count):
    os.makedirs("frames", exist_ok=True)
    for frame in range(frame_count):
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[i for i in range(10)],
            y=[(i * speed + frame) % 10 for i in range(10)],
            mode="lines+markers",
            name=f"{agent_name} - frame {frame}"
        ))
        fig.update_layout(
            title=f"{agent_name} | Speed: {speed}x | Frame: {frame}",
            xaxis_title="Time",
            yaxis_title="Value",
            width=700,
            height=500
        )
        path = f"frames/agent_{agent_name}_speed_{speed}_frame_{frame}.png"
        pio.write_image(fig, path)
        print(f"✅ Saved: {path}")

def generate_video(agent_name, speed):
    os.makedirs("videos", exist_ok=True)
    output_file = f"videos/{agent_name}_speed_{speed}x.mp4"
    command = (
        f"ffmpeg -framerate 2 -pattern_type glob "
        f"-i 'frames/agent_{agent_name}_speed_{speed}_frame_*.png' "
        f"-c:v libx264 -pix_fmt yuv420p {output_file} -y"
    )
    os.system(command)
    print(f"✅ Video created at: {output_file}")
    return output_file

def cleanup_frames():
    import glob
    for f in glob.glob("frames/*.png"):
        os.remove(f)
    print("🧹 All frame images deleted.")

