import gradio as gr
from project.main_agent import run_agent


def respond(message: str, history: list):
    response = run_agent(message)
    history = history + [[message, response]]
    return history, history


with gr.Blocks() as demo:
    gr.Markdown("# Emergency Response Guide Agent (Demo)")
    gr.Markdown(
        "This demo provides educational emergency guidance only. "
        "It is **not** a substitute for professional medical or emergency services."
    )

    chat = gr.Chatbot(label="Conversation")
    msg = gr.Textbox(label="Your message")
    clear = gr.Button("Clear")

    msg.submit(respond, [msg, chat], [chat, chat])
    clear.click(lambda: ([], []), None, [chat, chat])

if __name__ == "__main__":
    demo.launch()
