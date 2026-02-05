# LTX-2 Video Generator - Usage Guide

## Overview

This guide provides detailed instructions for using the LTX-2 Video Generator application.

## Setup Process

### 1. System Requirements Check

Before starting, ensure your system meets these requirements:
- NVIDIA GPU with 16GB+ VRAM (24GB recommended)
- CUDA 11.8 or higher
- 32GB+ RAM
- 50GB+ free disk space

Check your GPU:
```bash
nvidia-smi
```

### 2. Installation Steps

#### Step 1: Clone and Install Dependencies
```bash
git clone https://github.com/Cubatica/ltx-video-generator.git
cd ltx-video-generator
pip install -r requirements.txt
```

#### Step 2: Install LTX-2 Framework

**Option A - Using the UI (Easiest):**
1. Run `python app.py`
2. Navigate to `http://localhost:7860`
3. Expand "Setup Instructions"
4. Click "Install LTX-2"
5. Wait for installation to complete

**Option B - Manual Installation:**
```bash
git clone https://github.com/Lightricks/LTX-2.git
cd LTX-2
pip install uv
uv sync --frozen
cd ..
```

#### Step 3: Download Models

Create a `models` directory if it doesn't exist:
```bash
mkdir -p models
```

**Using huggingface-cli (Recommended):**
```bash
pip install huggingface_hub

# Download main model (FP8 version - faster, less memory)
huggingface-cli download Lightricks/LTX-2 \
  ltx-2-19b-distilled-fp8.safetensors \
  --local-dir models

# Download spatial upscaler
huggingface-cli download Lightricks/LTX-2 \
  ltx-2-spatial-upscaler-x2-1.0.safetensors \
  --local-dir models

# Download distilled LoRA
huggingface-cli download Lightricks/LTX-2 \
  ltx-2-19b-distilled-lora-384.safetensors \
  --local-dir models

# Download Gemma text encoder
huggingface-cli download google/gemma-3-12b-it-qat-q4_0-unquantized \
  --local-dir models/gemma-3-12b-it-qat-q4_0-unquantized
```

**Manual Download:**
Visit these URLs and download to the `models/` directory:
- https://huggingface.co/Lightricks/LTX-2/resolve/main/ltx-2-19b-distilled-fp8.safetensors
- https://huggingface.co/Lightricks/LTX-2/resolve/main/ltx-2-spatial-upscaler-x2-1.0.safetensors
- https://huggingface.co/Lightricks/LTX-2/resolve/main/ltx-2-19b-distilled-lora-384.safetensors

For Gemma, download all files from:
- https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-unquantized

## Using the Application

### Starting the Application

```bash
python app.py
```

The application will:
1. Create `models/` and `outputs/` directories if they don't exist
2. Start the Gradio web server
3. Display a URL (usually `http://localhost:7860`)

Open the URL in your web browser.

### Verification

Before generating videos, verify your setup:

1. Expand "Setup Instructions" in the UI
2. Click "Check Model Files"
3. Verify all required models are detected:
   - ✓ Checkpoint: Found
   - ✓ Spatial Upsampler: Found
   - ✓ Distilled LoRA: Found
   - ✓ Gemma Text Encoder: Found

## Generation Parameters

### Prompt
The most important parameter. Write detailed, chronological descriptions.

**Good Example:**
```
A serene mountain lake at sunrise with mist rising from the water's surface. 
The camera slowly pans across the scene from left to right, revealing snow-capped 
peaks in the background. Golden sunlight gradually illuminates the landscape, 
creating shimmering reflections on the still water. A lone eagle soars across 
the frame, gliding gracefully through the morning air.
```

**Bad Example:**
```
Nice mountain scene
```

### Initial Image (Optional)
Upload an image to use as the first frame. The model will animate from this image.

- Recommended size: 768x512 or 512x768
- Format: JPG or PNG
- The image will guide the generation

### Seed
- Integer value for reproducibility
- Same seed + same parameters = same video
- Use random values (e.g., 42, 123, 456) to explore variations

### Resolution

**Width x Height:**
- Low: 512x512 (faster, less detail)
- Medium: 768x512 (recommended, good balance)
- High: 1024x576 (slower, more detail)

**Tips:**
- Start with 768x512 for testing
- Higher resolution needs more VRAM
- The upsampler will 2x the resolution in stage 2

### Number of Frames
- Minimum: 25 (1 second at 25 FPS)
- Recommended: 121 (about 5 seconds)
- Maximum: 257 (about 10 seconds)

**More frames = longer generation time**

### FPS (Frames Per Second)
- 12-15: Cinematic, slower motion
- 24-25: Standard video (recommended)
- 30: Smooth, fast motion

### Inference Steps
- Minimum: 8 (fastest, lower quality)
- Recommended: 20 (good balance)
- Maximum: 50 (best quality, slowest)

**More steps = better quality but slower generation**

## Generation Process

1. Enter your prompt
2. (Optional) Upload initial image
3. Adjust parameters
4. Click "Generate Video"
5. Wait 5-15 minutes (depending on parameters)
6. Video appears in the output section

## Estimated Generation Times

On NVIDIA RTX 4090:
- 512x512, 121 frames, 20 steps: ~5 minutes
- 768x512, 121 frames, 20 steps: ~8 minutes
- 1024x576, 121 frames, 20 steps: ~12 minutes

On NVIDIA RTX 3090:
- 512x512, 121 frames, 20 steps: ~8 minutes
- 768x512, 121 frames, 20 steps: ~12 minutes
- 1024x576, 121 frames, 20 steps: ~18 minutes

## Tips for Best Results

### Prompt Writing
1. **Start with the main action**: "A woman walks down a beach"
2. **Add details**: "wearing a flowing white dress"
3. **Describe movement**: "her hair gently blowing in the breeze"
4. **Set the scene**: "at sunset with orange and pink skies"
5. **Camera work**: "the camera follows from behind"
6. **Atmosphere**: "peaceful and serene atmosphere"

### Image Conditioning
- Use high-quality images
- Match the aspect ratio to your target resolution
- The first frame will closely match your image
- Subsequent frames will animate naturally from it

### Performance
- Use FP8 model for faster generation
- Start with lower settings, then increase
- Close other GPU applications
- Monitor VRAM usage with `nvidia-smi`

## Common Issues

### Out of Memory
- Reduce resolution (try 512x512)
- Reduce number of frames (try 64)
- Use FP8 model
- Close other applications
- Restart the application

### Slow Generation
- This is normal! Video generation is compute-intensive
- Use FP8 model for faster results
- Reduce inference steps to 15-20
- Reduce resolution

### Poor Quality Results
- Increase inference steps to 30-40
- Write more detailed prompts
- Try different seeds
- Use higher resolution

### Model Not Found
- Verify files are in `models/` directory
- Check file names match exactly (case-sensitive)
- Click "Check Model Files" in the UI
- Re-download if files are corrupted

## Advanced Usage

### Batch Generation
Generate multiple variations by changing the seed:
1. Generate with seed 42
2. Generate with seed 123
3. Generate with seed 456
4. Compare results

### Progressive Refinement
1. Start with low settings (512x512, 64 frames, 15 steps)
2. Test your prompt
3. Increase resolution (768x512)
4. Increase frames (121)
5. Increase steps (25-30)

### Using Generated Videos
Output videos are saved in the `outputs/` directory with names like:
- `output_42.mp4` (where 42 is the seed)

You can:
- Download them from the UI
- Find them in the `outputs/` folder
- Use them in video editors
- Share them online

## Troubleshooting

### Application Won't Start
```bash
# Check Python version (need 3.10+)
python --version

# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check for port conflicts
lsof -i :7860
```

### CUDA Errors
```bash
# Check CUDA is available
python -c "import torch; print(torch.cuda.is_available())"

# Check CUDA version
nvcc --version

# Update PyTorch for your CUDA version
pip install torch --upgrade
```

### Import Errors
```bash
# Make sure LTX-2 is installed
cd LTX-2
uv sync --frozen
cd ..

# Or use pip
pip install -e LTX-2/packages/ltx-core
pip install -e LTX-2/packages/ltx-pipelines
```

## Support

For issues with:
- **This application**: Open an issue at https://github.com/Cubatica/ltx-video-generator/issues
- **LTX-2 model**: Visit https://github.com/Lightricks/LTX-2
- **Model behavior**: Check the LTX-2 Discord at https://discord.gg/ltxplatform

## Examples

### Example 1: Nature Scene
```
Prompt: A majestic waterfall cascading down moss-covered rocks in a lush forest. 
Sunlight filters through the canopy above, creating dappled light patterns on the 
water. The camera slowly zooms in on the waterfall, revealing the intricate details 
of water droplets and mist. Birds occasionally fly through the frame. The sound of 
rushing water fills the peaceful atmosphere.

Settings:
- Resolution: 768x512
- Frames: 121
- FPS: 25
- Steps: 25
- Seed: 42
```

### Example 2: Urban Scene
```
Prompt: A busy intersection in Tokyo at night with neon signs illuminating the wet 
pavement. People cross the street holding colorful umbrellas as light rain falls. 
The camera is positioned at street level, capturing the reflection of lights in 
puddles. Cars pass by with their headlights creating light trails. The scene is 
vibrant and energetic with a cyberpunk aesthetic.

Settings:
- Resolution: 768x512
- Frames: 121
- FPS: 30
- Steps: 20
- Seed: 789
```

### Example 3: Portrait with Image Conditioning
```
Initial Image: Upload a portrait photo
Prompt: The person smiles warmly and turns their head slightly to the right. 
Their eyes light up with joy. Soft natural lighting illuminates their face. 
The background is slightly blurred with bokeh effect. A gentle breeze causes 
their hair to move subtly. The mood is warm and inviting.

Settings:
- Resolution: 512x768 (portrait)
- Frames: 97
- FPS: 25
- Steps: 25
- Seed: 555
```

## File Locations

```
ltx-video-generator/
├── app.py                    # Main application
├── models/                   # Model files (you download these)
│   ├── ltx-2-19b-distilled-fp8.safetensors
│   ├── ltx-2-spatial-upscaler-x2-1.0.safetensors
│   ├── ltx-2-19b-distilled-lora-384.safetensors
│   └── gemma-3-12b-it-qat-q4_0-unquantized/
├── outputs/                  # Generated videos
│   └── output_*.mp4
└── LTX-2/                   # LTX-2 framework (auto-installed)
```

## Performance Optimization

### For Best Performance:
1. Use FP8 model: `ltx-2-19b-distilled-fp8.safetensors`
2. Set `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`
3. Close unnecessary applications
4. Use recommended settings: 768x512, 121 frames, 20 steps

### For Best Quality:
1. Use non-FP8 model: `ltx-2-19b-distilled.safetensors`
2. Increase inference steps to 30-40
3. Use higher resolution: 1024x576
4. Write detailed, descriptive prompts

### For Experimentation:
1. Use FP8 model for speed
2. Start with 512x512, 64 frames, 15 steps
3. Test different prompts quickly
4. Increase settings for final renders
