"""
Demo UI - Simplified version for testing the interface without requiring full model setup
"""

import gradio as gr
from pathlib import Path

def generate_video_demo(prompt, initial_image, seed, width, height, num_frames, fps, num_steps):
    """Demo function that simulates video generation"""
    status = f"""
    Demo Mode - Configuration:
    
    Prompt: {prompt[:100]}{'...' if len(prompt) > 100 else ''}
    Has initial image: {initial_image is not None}
    Seed: {seed}
    Resolution: {width}x{height}
    Frames: {num_frames}
    FPS: {fps}
    Inference Steps: {num_steps}
    
    In production mode, this would:
    1. Load the LTX-2 model
    2. Process your prompt with Gemma text encoder
    3. Generate video using TI2VidTwoStagesPipeline
    4. Save the output to outputs/ directory
    
    Expected generation time: 5-15 minutes depending on parameters
    """
    return None, status

# Create Gradio interface
with gr.Blocks(title="LTX-2 Video Generator - Demo") as demo:
    gr.Markdown("# LTX-2 Video Generator - Demo UI")
    gr.Markdown("This is a demo of the user interface. To use the actual video generation, see the full app.py")
    
    with gr.Row():
        with gr.Column():
            prompt = gr.Textbox(
                label="Prompt",
                placeholder="A beautiful sunset over the ocean with waves gently rolling onto the shore...",
                lines=4,
                value="A serene mountain lake at sunrise with mist rising from the water"
            )
            
            initial_image = gr.Image(
                label="Initial Image (Optional)",
                type="pil",
                sources=["upload"]
            )
            
            with gr.Row():
                seed = gr.Number(label="Seed", value=42, precision=0)
                num_steps = gr.Slider(
                    label="Inference Steps",
                    minimum=8,
                    maximum=50,
                    value=20,
                    step=1
                )
            
            with gr.Row():
                width = gr.Slider(label="Width", minimum=256, maximum=1024, value=768, step=64)
                height = gr.Slider(label="Height", minimum=256, maximum=1024, value=512, step=64)
            
            with gr.Row():
                num_frames = gr.Slider(
                    label="Number of Frames",
                    minimum=25,
                    maximum=257,
                    value=121,
                    step=8
                )
                fps = gr.Slider(label="FPS", minimum=12, maximum=30, value=25, step=1)
            
            generate_btn = gr.Button("Generate Video (Demo)", variant="primary", size="lg")
        
        with gr.Column():
            output_video = gr.Video(label="Generated Video (Demo)")
            status_text = gr.Textbox(label="Status", lines=10)
    
    generate_btn.click(
        fn=generate_video_demo,
        inputs=[prompt, initial_image, seed, width, height, num_frames, fps, num_steps],
        outputs=[output_video, status_text]
    )
    
    gr.Examples(
        examples=[
            ["A serene landscape with mountains in the background and a lake in the foreground", None, 42, 768, 512, 121, 25, 20],
            ["A person walking down a busy city street at night with neon lights", None, 123, 768, 512, 121, 25, 20],
            ["Close-up of colorful flowers swaying gently in the breeze", None, 456, 768, 512, 121, 25, 20],
        ],
        inputs=[prompt, initial_image, seed, width, height, num_frames, fps, num_steps],
    )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
