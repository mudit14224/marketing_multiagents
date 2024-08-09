import gradio as gr
from main import run_crews, run_contact_search_crew


def run_agents(url, client, search_criteria):
    final_result = run_crews(url, client, search_criteria)
    return final_result

def run_contact_agents(client):
    json_result = run_contact_search_crew(client=client)
    return json_result


client_search = gr.Interface(fn=run_agents, inputs=["textbox", "textbox", "textbox"], outputs="textbox")
contact_search = gr.Interface(fn=run_contact_agents, inputs=["textbox"], outputs="textbox")

demo = gr.TabbedInterface([client_search, contact_search], ["Client Search Agent", "Contact Search Agent"])

if __name__ == '__main__':      
    demo.launch(server_name="0.0.0.0", server_port=7860) 