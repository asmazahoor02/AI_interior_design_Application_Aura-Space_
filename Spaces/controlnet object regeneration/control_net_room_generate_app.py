# --- Gradio Interface Definition ---
import gradio as gr
from regenerate import on_upload_image, handle_generate_button
with gr.Blocks() as demo:


    gr.Markdown(
        """
        # Interior Design AI: Regenerate Mode
        Upload an image, select objects to regenerate, and provide prompts.
        """
    )

    with gr.Row():
        with gr.Column():
            input_image_component = gr.Image(
                type="pil",
                label="Upload an image of your room (PNG/JPG)",
                sources=["upload"],
                height=300,
                interactive=True # Allow direct image upload
            )


            gr.Markdown("---")
            gr.Markdown("### Prompts & Seed")
            positive_prompt_textbox = gr.Textbox(
                label="Enter prompt",
                placeholder="a photograph of a room, interior design, 4k, high resolution",
                interactive=False
            )


            gr.Markdown("---")
            # gr.Markdown("### Regeneration Options")
            # # This replaces the st.expander and st.write explanation
            # gr.Markdown("This mode allows you to choose which objects you want to re-generate in the image. "
            #             "Use the selection dropdown to add or remove objects. If you are ready, press the generate button"
            #             " to generate the image, which can take up to 30 seconds. If you want to improve the generated image, click"
            #             " the 'move image to input' button.")

            regenerate_objects_checkboxes = gr.CheckboxGroup(
                label="Choose which concepts you want to regenerate in the image",
                choices=[], # Populated after image processing
                interactive=False
            )


            generate_button = gr.Button("Generate Output", interactive=False)

        with gr.Column():
            output_image_display = gr.Image(type="pil", label="Output Image", height=400)


    # --- Event Listeners ---

    # When an image is uploaded or the "Process Image" button is clicked
    input_image_component.upload(
        fn=on_upload_image,
        inputs=[input_image_component],
        outputs=[
            input_image_component,
            regenerate_objects_checkboxes,
            positive_prompt_textbox,
            generate_button # Now correctly matched in outputs and function signature
        ]
    )

    generate_button.click(
        fn=handle_generate_button,
        inputs=[
            positive_prompt_textbox,
            regenerate_objects_checkboxes, # This passes the list of selected RGB tuples
        ],
        outputs=[output_image_display] # Removed the second output
    )

demo.launch(debug=True)