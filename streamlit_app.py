import os
import streamlit as st
import plotly.graph_objects as go
import plotly.io as pio

# Configure Kaleido for static image export
pio.kaleido.scope.default_format = "png"

# --- UI ---
st.title("🧠 Agent Simulation Visualizer")
agent = st.selectbox("Choose Agent", ["DQN", "A2C", "PPO"])
speed = st.slider("Simulation Speed", 1, 10, 5)
frame_num = st.slider("Frame Number", 1, 100, 10)

# --- Generate Plot ---
def create_figure(frame_num, agent='DQN'):
    x = list(range(frame_num + 1))
    y = [i ** 0.5 for i in x]  # Simulated metric

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode='lines+markers',
        name=f'{agent} Agent'
    ))
    fig.update_layout(
        title=f"{agent} - Frame {frame_num}",
        xaxis_title="Steps",
        yaxis_title="Reward or State",
        template="plotly_dark",
        width=800,
        height=500
    )
    return fig

fig = create_figure(frame_num, agent)
st.plotly_chart(fig)

# --- Optionally Save Frame ---
if st.button("📸 Save Frame as Image"):
    os.makedirs("frames", exist_ok=True)
    path = f"frames/agent_{agent}_speed_{speed}_frame_{frame_num}.png"
    pio.write_image(fig, path)
    st.success(f"Frame saved at `{path}` ✅")

