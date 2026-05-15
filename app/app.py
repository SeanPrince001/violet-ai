import gradio as gr
from brain.chat import chat


def respond(message, history):
    reply = chat(message)
    return reply


interface = gr.ChatInterface(
    fn=respond,
    title="Violet",
    description="An elegant AI companion"
)

interface.launch()