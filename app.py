"""
LTX-2 Video Generator with Gradio UI

This application provides a simple UI for generating videos using the LTX-2 model.
It supports text-to-video and image-to-video generation.
"""

import os
import sys
import gradio as gr
from pathlib import Path
import subprocess
import shutil

# Configuration
MODELS_DIR = Path("models")
OUTPUTS_DIR = Path("outputs")
LTX2_REPO_DIR = Path("LTX-2")

# Create directories
MODELS_DIR.mkdir(exist_ok=True)
OUTPUTS_DIR.mkdir(exist_ok=True)


def check_ltx2_installation():
    """Check if LTX-2 repository is cloned and set up."""
    if not LTX2_REPO_DIR.exists():
        return False, "LTX-2 repository not found"
    
    # Check if packages are installed
    venv_path = LTX2_REPO_DIR / ".venv"
    if not venv_path.exists():
        return False, "LTX-2 environment not set up"
    
    return True, "LTX-2 is installed"


def install_ltx2():
    """Clone and set up LTX-2 repository."""
    try:
        if not LTX2_REPO_DIR.exists():
            print("Cloning LTX-2 repository...")
            subprocess.run([
                "git", "clone", 
                "https://github.com/Lightricks/LTX-2.git",
                str(LTX2_REPO_DIR)
            ], check=True)
        
        # Check if uv is installed, if not use pip
        if shutil.which("uv"):
            print("Setting up environment with uv...")
            subprocess.run(
                ["uv", "sync", "--frozen"],
                cwd=LTX2_REPO_DIR,
                check=True
            )
        else:
            print("UV not found. Please install dependencies manually.")
            print(f"cd {LTX2_REPO_DIR} && pip install -e packages/ltx-core -e packages/ltx-pipelines")
            
        return True, "LTX-2 installed successfully"
    except Exception as e:
        return False, f"Installation failed: {str(e)}"


def check_model_files():
    """Check which model files are present."""
    required_files = {
        "checkpoint": [
            "ltx-2-19b-dev-fp8.safetensors",
            "ltx-2-19b-dev.safetensors",
            "ltx-2-19b-distilled.safetensors",
            "ltx-2-19b-distilled-fp8.safetensors"
        ],
        "spatial_upsampler": ["ltx-2-spatial-upscaler-x2-1.0.safetensors"],
        "distilled_lora": ["ltx-2-19b-distilled-lora-384.safetensors"]
    }
    
    status = {}
    for category, files in required_files.items():
        found = []
        for file in files:
            file_path = MODELS_DIR / file
            if file_path.exists():
                found.append(file)
        status[category] = found
    
    return status


def get_model_download_info():
    """Get information about downloading required models."""
    info = """
    ## Required Model Files
    
    Download the following files from HuggingFace and place them in the 'models' directory:
    
    **Main Model (choose one):**
    - ltx-2-19b-distilled-fp8.safetensors (Recommended - smaller, faster)
      https://huggingface.co/Lightricks/LTX-2/resolve/main/ltx-2-19b-distilled-fp8.safetensors
    
    **Spatial Upsampler (Required):**
    - ltx-2-spatial-upscaler-x2-1.0.safetensors
      https://huggingface.co/Lightricks/LTX-2/resolve/main/ltx-2-spatial-upscaler-x2-1.0.safetensors
    
    **Distilled LoRA:**
    - ltx-2-19b-distilled-lora-384.safetensors
      https://huggingface.co/Lightricks/LTX-2/resolve/main/ltx-2-19b-distilled-lora-384.safetensors
    
    **Gemma Text Encoder:**
    Download all files from: https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-unquantized
    Place them in: models/gemma-3-12b-it-qat-q4_0-unquantized/
    
    Or use the huggingface-cli:
    ```
    huggingface-cli download Lightricks/LTX-2 ltx-2-19b-distilled-fp8.safetensors --local-dir models
    huggingface-cli download Lightricks/LTX-2 ltx-2-spatial-upscaler-x2-1.0.safetensors --local-dir models
    huggingface-cli download Lightricks/LTX-2 ltx-2-19b-distilled-lora-384.safetensors --local-dir models
    huggingface-cli download google/gemma-3-12b-it-qat-q4_0-unquantized --local-dir models/gemma-3-12b-it-qat-q4_0-unquantized
    ```
    """
    return info


def generate_video(prompt, initial_image, seed, width, height, num_frames, fps, num_steps):
    """Generate video using LTX-2 model."""
    try:
        # Check if LTX-2 is installed
        installed, msg = check_ltx2_installation()
        if not installed:
            return None, f"Error: {msg}. Please install LTX-2 first."
        
        # Check model files
        model_status = check_model_files()
        
        # Find checkpoint
        checkpoint = None
        if model_status["checkpoint"]:
            checkpoint = MODELS_DIR / model_status["checkpoint"][0]
        else:
            return None, "Error: No checkpoint file found. Please download a model checkpoint."
        
        # Check for spatial upsampler
        if not model_status["spatial_upsampler"]:
            return None, "Error: Spatial upsampler not found. Please download it."
        spatial_upsampler = MODELS_DIR / model_status["spatial_upsampler"][0]
        
        # Check for Gemma
        gemma_dir = MODELS_DIR / "gemma-3-12b-it-qat-q4_0-unquantized"
        if not gemma_dir.exists():
            return None, "Error: Gemma text encoder not found. Please download it."
        
        # Prepare output path
        output_path = OUTPUTS_DIR / f"output_{seed}.mp4"
        
        # Build command
        cmd = [
            sys.executable, "-m", "ltx_pipelines.ti2vid_two_stages",
            "--checkpoint-path", str(checkpoint),
            "--spatial-upsampler-path", str(spatial_upsampler),
            "--gemma-root", str(gemma_dir),
            "--prompt", prompt,
            "--output-path", str(output_path),
            "--seed", str(seed),
            "--width", str(width),
            "--height", str(height),
            "--num-frames", str(num_frames),
            "--frame-rate", str(fps),
            "--num-inference-steps", str(num_steps),
        ]
        
        # Add distilled LoRA if available
        if model_status["distilled_lora"]:
            distilled_lora = MODELS_DIR / model_status["distilled_lora"][0]
            cmd.extend(["--distilled-lora", str(distilled_lora), "0.8"])
        
        # Add initial image if provided
        if initial_image is not None:
            # Save the uploaded image
            image_path = OUTPUTS_DIR / f"input_{seed}.jpg"
            initial_image.save(str(image_path))
            cmd.extend(["--images", str(image_path), "0", "1.0"])
        
        # Add environment variable for FP8
        env = os.environ.copy()
        env["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
        
        # Check if using FP8 model
        if "fp8" in str(checkpoint):
            cmd.append("--enable-fp8")
        
        # Change to LTX-2 directory and run
        print(f"Running command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            cwd=LTX2_REPO_DIR,
            env=env,
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            error_msg = f"Generation failed:\n{result.stderr}\n{result.stdout}"
            print(error_msg)
            return None, error_msg
        
        if output_path.exists():
            return str(output_path), "Video generated successfully!"
        else:
            return None, "Error: Output video not created."
        
    except Exception as e:
        return None, f"Error: {str(e)}"


# Create Gradio interface
with gr.Blocks(title="LTX-2 Video Generator") as app:
    gr.Markdown("# LTX-2 Video Generator")
    gr.Markdown("Generate videos from text prompts and optional initial images using the LTX-2 model.")
    
    # Setup section
    with gr.Accordion("Setup Instructions", open=False):
        with gr.Row():
            with gr.Column():
                gr.Markdown(get_model_download_info())
                
                install_btn = gr.Button("Install LTX-2", variant="secondary")
                install_status = gr.Textbox(label="Installation Status", interactive=False)
                
                check_btn = gr.Button("Check Model Files", variant="secondary")
                model_status = gr.Textbox(label="Model Status", interactive=False, lines=5)
        
        def install_handler():
            success, msg = install_ltx2()
            return msg
        
        def check_handler():
            status = check_model_files()
            msg = "Model Files Status:\n\n"
            msg += f"Checkpoint: {', '.join(status['checkpoint']) if status['checkpoint'] else 'None found'}\n"
            msg += f"Spatial Upsampler: {', '.join(status['spatial_upsampler']) if status['spatial_upsampler'] else 'None found'}\n"
            msg += f"Distilled LoRA: {', '.join(status['distilled_lora']) if status['distilled_lora'] else 'None found'}\n"
            
            gemma_dir = MODELS_DIR / "gemma-3-12b-it-qat-q4_0-unquantized"
            msg += f"Gemma Text Encoder: {'Found' if gemma_dir.exists() else 'Not found'}\n"
            
            return msg
        
        install_btn.click(install_handler, outputs=install_status)
        check_btn.click(check_handler, outputs=model_status)
    
    # Generation interface
    with gr.Row():
        with gr.Column():
            prompt = gr.Textbox(
                label="Prompt",
                placeholder="A beautiful sunset over the ocean with waves gently rolling onto the shore...",
                lines=4
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
            
            generate_btn = gr.Button("Generate Video", variant="primary", size="lg")
        
        with gr.Column():
            output_video = gr.Video(label="Generated Video")
            status_text = gr.Textbox(label="Status", lines=3)
    
    generate_btn.click(
        fn=generate_video,
        inputs=[prompt, initial_image, seed, width, height, num_frames, fps, num_steps],
        outputs=[output_video, status_text]
    )
    
    # Examples
    gr.Examples(
        examples=[
            ["A serene landscape with mountains in the background and a lake in the foreground, with mist rising from the water at sunrise", None, 42, 768, 512, 121, 25, 20],
            ["A person walking down a busy city street at night with neon lights reflecting on wet pavement", None, 123, 768, 512, 121, 25, 20],
            ["Close-up of colorful flowers swaying gently in the breeze on a sunny day", None, 456, 768, 512, 121, 25, 20],
        ],
        inputs=[prompt, initial_image, seed, width, height, num_frames, fps, num_steps],
    )

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0", server_port=7860, share=False)
