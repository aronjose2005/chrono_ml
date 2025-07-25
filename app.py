# app.py

from chrono_simulator import run_simulation, generate_video

if __name__ == "__main__":
    agent = "DQN"
    speed = 10
    total_frames = 30

    run_simulation(agent=agent, speed=speed, total_frames=total_frames)
    generate_video(agent=agent, speed=speed)

