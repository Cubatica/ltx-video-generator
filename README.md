# LTX-2 Video Generator

A simple, user-friendly web interface for generating videos using the [LTX-2](https://github.com/Lightricks/LTX-2) video generation model. This application provides an intuitive Gradio UI for text-to-video and image-to-video generation.

## Features

- 🎬 **Text-to-Video Generation**: Generate videos from text prompts
- 🖼️ **Image-to-Video Generation**: Use an initial image to guide video generation
- 🎨 **Simple UI**: Clean, easy-to-use Gradio interface
- ⚙️ **Configurable Parameters**: Control resolution, frame count, seed, and more
- 📦 **Integrated Setup**: Built-in installation and model download helpers

## Quick Start

### Prerequisites

- Python 3.10 or higher
- CUDA-capable GPU (16GB+ VRAM recommended)
- 50GB+ free disk space for models

### Installation

1. **Clone this repository:**
```bash
git clone https://github.com/Cubatica/ltx-video-generator.git
cd ltx-video-generator
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Install LTX-2:**
   - Option A: Use the UI (recommended)
     - Run `python app.py`
     - Click "Install LTX-2" in the Setup Instructions section
   
   - Option B: Manual installation
     ```bash
     git clone https://github.com/Lightricks/LTX-2.git
     cd LTX-2
     # Install uv if not already installed
     pip install uv
     uv sync --frozen
     cd ..
     ```

4. **Download required models:**

Create a `models` directory and download the following files from [HuggingFace](https://huggingface.co/Lightricks/LTX-2):

**Main Model (choose one):**
- Recommended: `ltx-2-19b-distilled-fp8.safetensors` (smaller, faster)
- Alternative: `ltx-2-19b-distilled.safetensors` (higher quality, larger)

**Required Components:**
- `ltx-2-spatial-upscaler-x2-1.0.safetensors`
- `ltx-2-19b-distilled-lora-384.safetensors`

**Gemma Text Encoder:**
- Download all files from [google/gemma-3-12b-it-qat-q4_0-unquantized](https://huggingface.co/google/gemma-3-12b-it-qat-q4_0-unquantized)
- Place in `models/gemma-3-12b-it-qat-q4_0-unquantized/`

**Using huggingface-cli (easiest):**
```bash
# Install huggingface-cli if needed
pip install huggingface_hub

# Download models
huggingface-cli download Lightricks/LTX-2 ltx-2-19b-distilled-fp8.safetensors --local-dir models
huggingface-cli download Lightricks/LTX-2 ltx-2-spatial-upscaler-x2-1.0.safetensors --local-dir models
huggingface-cli download Lightricks/LTX-2 ltx-2-19b-distilled-lora-384.safetensors --local-dir models
huggingface-cli download google/gemma-3-12b-it-qat-q4_0-unquantized --local-dir models/gemma-3-12b-it-qat-q4_0-unquantized
```

### Running the Application

```bash
python app.py
```

Then open your browser to `http://localhost:7860`

## Usage

1. **Enter a prompt**: Describe the video you want to generate in detail
2. **(Optional) Upload an image**: Provide an initial frame to guide generation
3. **Adjust parameters**:
   - Seed: For reproducible results
   - Resolution: Width and height in pixels
   - Frames: Number of frames to generate
   - FPS: Frame rate of output video
   - Inference Steps: More steps = better quality but slower
4. **Click "Generate Video"**
5. **Wait**: Generation typically takes 5-15 minutes depending on parameters and GPU

## Tips for Best Results

### Writing Good Prompts

Focus on detailed, chronological descriptions:
- Start with the main action
- Add specific movements and gestures
- Describe appearances precisely
- Include background and environment details
- Specify camera angles and movements
- Describe lighting and colors
- Note any changes or events

Example:
```
A serene mountain lake at sunrise with mist rising from the water's surface. 
The camera slowly pans across the scene, revealing snow-capped peaks in the 
background. Golden sunlight gradually illuminates the landscape, creating 
reflections on the still water. A lone eagle soars across the frame from 
left to right.
```

### Performance Optimization

- **Use FP8 model**: Faster and uses less memory
- **Reduce frames**: Start with 121 frames for testing
- **Lower resolution**: Try 512x768 for faster generation
- **Fewer steps**: 20 steps is usually sufficient
- **Image conditioning**: Using an initial image can improve consistency

## Project Structure

```
ltx-video-generator/
├── app.py                 # Main application with Gradio UI
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore            # Git ignore rules
├── models/               # Model files (you need to download these)
│   ├── ltx-2-19b-distilled-fp8.safetensors
│   ├── ltx-2-spatial-upscaler-x2-1.0.safetensors
│   ├── ltx-2-19b-distilled-lora-384.safetensors
│   └── gemma-3-12b-it-qat-q4_0-unquantized/
├── outputs/              # Generated videos
└── LTX-2/               # LTX-2 repository (auto-installed)
```

## System Requirements

### Minimum
- GPU: NVIDIA GPU with 16GB VRAM
- RAM: 32GB
- Storage: 50GB free space
- CUDA: 11.8 or higher

### Recommended
- GPU: NVIDIA RTX 4090 or A100 (24GB+ VRAM)
- RAM: 64GB
- Storage: 100GB free space (SSD preferred)
- CUDA: 12.0 or higher

## Troubleshooting

### Out of Memory Errors
- Use the FP8 model variant
- Reduce resolution (try 512x512)
- Reduce number of frames (try 64)
- Close other applications

### Slow Generation
- Use FP8 model
- Reduce inference steps (20 is usually enough)
- Use distilled model for faster results

### Model Not Found
- Check that files are in the `models/` directory
- Verify file names match exactly
- Use "Check Model Files" button in the UI

### Installation Issues
- Ensure Python 3.10+ is installed
- Update pip: `pip install --upgrade pip`
- Install uv: `pip install uv`
- Check CUDA installation: `nvidia-smi`

## License

This project is a wrapper around the LTX-2 model. Please refer to the [LTX-2 repository](https://github.com/Lightricks/LTX-2) for model licensing information.

## Acknowledgments

- [Lightricks](https://www.lightricks.com/) for the LTX-2 model
- [Gradio](https://gradio.app/) for the UI framework

## Links

- **LTX-2 Repository**: https://github.com/Lightricks/LTX-2
- **LTX-2 Paper**: https://arxiv.org/abs/2601.03233
- **Model on HuggingFace**: https://huggingface.co/Lightricks/LTX-2
- **Official Demo**: https://app.ltx.studio/ltx-2-playground/i2v