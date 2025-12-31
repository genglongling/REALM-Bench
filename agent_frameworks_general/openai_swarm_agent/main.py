import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))

import gradio as gr
from router import SwarmRouter

def gradio_interface(message, history):
    router = SwarmRouter()
    agent_response = router.process_query(message)
    return agent_response

def launch_app():
    iface = gr.ChatInterface(fn=gradio_interface, title="OpenAI Swarms Agent")
    iface.launch()

if __name__ == "__main__":
    launch_app() 