"""# Gradio Function"""

# --- Gradio UI Event Handlers ---

import gradio as gr
from typing import Dict, Union, Tuple
from PIL import Image
from inpainting import load_and_preprocess_image, make_inpainting, get_mask, on_upload_image, handle_generate_button
import random
import numpy as np

"""# Gradio UI"""

with gr.Blocks() as demo:

    gr.Markdown(
        """
        # Interior Design AI: Inpainting Mode
        Upload an image, draw a mask over the area to inpaint, and provide prompts.
        """
    )

    with gr.Row():
        with gr.Column():
            input_image_component = gr.ImageEditor(
                label="Upload an image of your room (PNG/JPG)",
                sources=["upload"],
                height=300,
                interactive=True # Explicitly set interactive
            )
            gr.Markdown("---")
            gr.Markdown("### Prompts & Seed")
            positive_prompt_textbox = gr.Textbox(
                label="Positive prompt",
                placeholder="a photograph of a room, interior design, 4k, high resolution",
                interactive=False # Enabled after image upload
            )
            

            generate_button = gr.Button("Generate Output", interactive=False)

        with gr.Column():
            output_image_display = gr.Image(type="pil", label="Output Image", height=400)
    # --- Event Listeners ---

    # positive_prompt_textbox.change(update_positive_prompt_global, inputs=[positive_prompt_textbox])
    # negative_prompt_textbox.change(update_negative_prompt_global, inputs=[negative_prompt_textbox])
    input_image_component.upload(
        fn=on_upload_image,
        inputs=[input_image_component],
        outputs=[
            input_image_component,
            positive_prompt_textbox,
                
            generate_button,

            ]
        )

    generate_button.click(
        fn=handle_generate_button,
        inputs=[
            positive_prompt_textbox,
            # negative_prompt_textbox,
            # seed_slider,
            input_image_component, # ImageEditor output
        ],
        outputs=[output_image_display]
    )

    # move_to_input_btn.click(
    #     fn=move_output_to_input_for_ui,
    #     inputs=[output_image_display],
    #     outputs=[input_image_component]
    # )

if __name__ == "__main__":
    demo.launch(debug=True)