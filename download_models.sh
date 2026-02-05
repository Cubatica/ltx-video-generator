#!/bin/bash

# Model download script for LTX-2 Video Generator
# Downloads all required models from HuggingFace

set -e

echo "================================================"
echo "LTX-2 Model Downloader"
echo "================================================"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check if huggingface_hub is installed
echo "Checking for huggingface-cli..."
if ! command -v huggingface-cli &> /dev/null; then
    echo "Installing huggingface_hub..."
    pip3 install huggingface_hub
fi
echo -e "${GREEN}✓ huggingface-cli available${NC}"
echo ""

# Create models directory
mkdir -p models

# Download models
echo "Downloading models..."
echo "This will download approximately 40GB of data."
echo ""

read -p "Continue? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Download cancelled."
    exit 0
fi

echo ""
echo "1/4 Downloading main model (FP8 version - ~8GB)..."
huggingface-cli download Lightricks/LTX-2 \
    ltx-2-19b-distilled-fp8.safetensors \
    --local-dir models
echo -e "${GREEN}✓ Model checkpoint downloaded${NC}"
echo ""

echo "2/4 Downloading spatial upscaler (~2GB)..."
huggingface-cli download Lightricks/LTX-2 \
    ltx-2-spatial-upscaler-x2-1.0.safetensors \
    --local-dir models
echo -e "${GREEN}✓ Spatial upscaler downloaded${NC}"
echo ""

echo "3/4 Downloading distilled LoRA (~2GB)..."
huggingface-cli download Lightricks/LTX-2 \
    ltx-2-19b-distilled-lora-384.safetensors \
    --local-dir models
echo -e "${GREEN}✓ Distilled LoRA downloaded${NC}"
echo ""

echo "4/4 Downloading Gemma text encoder (~28GB)..."
huggingface-cli download google/gemma-3-12b-it-qat-q4_0-unquantized \
    --local-dir models/gemma-3-12b-it-qat-q4_0-unquantized
echo -e "${GREEN}✓ Gemma text encoder downloaded${NC}"
echo ""

echo "================================================"
echo "All models downloaded successfully!"
echo "================================================"
echo ""
echo "Model files are in the models/ directory:"
ls -lh models/*.safetensors 2>/dev/null || true
echo ""
echo "You can now run the application:"
echo "  python3 app.py"
echo "================================================"
