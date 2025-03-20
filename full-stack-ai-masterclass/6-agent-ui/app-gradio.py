import gradio as gr
from agent import get_response_with_history

gr.ChatInterface(
    fn=get_response_with_history, 
    type="messages"
).launch()