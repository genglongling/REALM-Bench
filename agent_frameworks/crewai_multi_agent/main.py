import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

import gradio as gr
from router import run_crewai

def gradio_interface(message, _):
    return run_crewai(message)

def launch_app():
    iface = gr.ChatInterface(fn=gradio_interface, title="CrewAI Copilot Multi-Agent")
    iface.launch()

if __name__ == "__main__":
    launch_app()
