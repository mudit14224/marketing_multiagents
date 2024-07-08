import gradio as gr
from main import run_crews


def run_agents(url, client, search_criteria):
    final_result = run_crews(url, client, search_criteria)
    return final_result

demo = gr.Interface(fn=run_agents, inputs=["textbox", "textbox", "textbox"], outputs="textbox")
    
demo.launch(share=True) 