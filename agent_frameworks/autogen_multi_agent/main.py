import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

import gradio as gr
from router import run_autogen_agents


def gradio_interface(message, _):
    return run_autogen_agents(message)


def launch_app():
    iface = gr.ChatInterface(fn=gradio_interface, title="AutoGen Copilot Multi-Agent")
    iface.launch()


if __name__ == "__main__":
    launch_app()
