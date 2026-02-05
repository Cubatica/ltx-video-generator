#!/bin/bash

# Installation script for LTX-2 Video Generator
# This script helps automate the setup process

set -e  # Exit on error

echo "================================================"
echo "LTX-2 Video Generator - Installation Script"
echo "================================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
required_version="3.10"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo -e "${RED}Error: Python 3.10 or higher is required. Found: $python_version${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Python $python_version${NC}"
echo ""

# Check CUDA
echo "Checking CUDA availability..."
if command -v nvidia-smi &> /dev/null; then
    echo -e "${GREEN}✓ NVIDIA GPU detected${NC}"
    nvidia-smi --query-gpu=name,memory.total --format=csv,noheader
else
    echo -e "${YELLOW}⚠ Warning: nvidia-smi not found. GPU may not be available.${NC}"
fi
echo ""

# Create directories
echo "Creating directories..."
mkdir -p models
mkdir -p outputs
echo -e "${GREEN}✓ Created models/ and outputs/ directories${NC}"
echo ""

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt
echo -e "${GREEN}✓ Python dependencies installed${NC}"
echo ""

# Clone LTX-2 repository
echo "Installing LTX-2 framework..."
if [ ! -d "LTX-2" ]; then
    git clone https://github.com/Lightricks/LTX-2.git
    echo -e "${GREEN}✓ LTX-2 repository cloned${NC}"
else
    echo -e "${YELLOW}LTX-2 directory already exists, skipping clone${NC}"
fi
echo ""

# Install LTX-2 dependencies
echo "Installing LTX-2 dependencies..."
cd LTX-2

# Check if uv is available
if command -v uv &> /dev/null; then
    echo "Using uv for installation..."
    uv sync --frozen
else
    echo "uv not found, installing with pip..."
    pip3 install uv
    uv sync --frozen
fi

cd ..
echo -e "${GREEN}✓ LTX-2 dependencies installed${NC}"
echo ""

# Check for model files
echo "Checking for model files..."
models_found=0

if [ -f "models/ltx-2-19b-distilled-fp8.safetensors" ] || \
   [ -f "models/ltx-2-19b-distilled.safetensors" ] || \
   [ -f "models/ltx-2-19b-dev.safetensors" ] || \
   [ -f "models/ltx-2-19b-dev-fp8.safetensors" ]; then
    echo -e "${GREEN}✓ Model checkpoint found${NC}"
    ((models_found++))
else
    echo -e "${YELLOW}✗ Model checkpoint not found${NC}"
fi

if [ -f "models/ltx-2-spatial-upscaler-x2-1.0.safetensors" ]; then
    echo -e "${GREEN}✓ Spatial upscaler found${NC}"
    ((models_found++))
else
    echo -e "${YELLOW}✗ Spatial upscaler not found${NC}"
fi

if [ -f "models/ltx-2-19b-distilled-lora-384.safetensors" ]; then
    echo -e "${GREEN}✓ Distilled LoRA found${NC}"
    ((models_found++))
else
    echo -e "${YELLOW}✗ Distilled LoRA not found${NC}"
fi

if [ -d "models/gemma-3-12b-it-qat-q4_0-unquantized" ]; then
    echo -e "${GREEN}✓ Gemma text encoder found${NC}"
    ((models_found++))
else
    echo -e "${YELLOW}✗ Gemma text encoder not found${NC}"
fi

echo ""

if [ $models_found -eq 4 ]; then
    echo -e "${GREEN}All model files found!${NC}"
else
    echo -e "${YELLOW}Some model files are missing.${NC}"
    echo ""
    echo "To download models, run:"
    echo ""
    echo "  pip install huggingface_hub"
    echo ""
    echo "  # Main model (FP8 - recommended)"
    echo "  huggingface-cli download Lightricks/LTX-2 ltx-2-19b-distilled-fp8.safetensors --local-dir models"
    echo ""
    echo "  # Spatial upscaler"
    echo "  huggingface-cli download Lightricks/LTX-2 ltx-2-spatial-upscaler-x2-1.0.safetensors --local-dir models"
    echo ""
    echo "  # Distilled LoRA"
    echo "  huggingface-cli download Lightricks/LTX-2 ltx-2-19b-distilled-lora-384.safetensors --local-dir models"
    echo ""
    echo "  # Gemma text encoder"
    echo "  huggingface-cli download google/gemma-3-12b-it-qat-q4_0-unquantized --local-dir models/gemma-3-12b-it-qat-q4_0-unquantized"
    echo ""
fi

echo "================================================"
echo "Installation complete!"
echo "================================================"
echo ""
echo "To start the application, run:"
echo "  python3 app.py"
echo ""
echo "Then open your browser to http://localhost:7860"
echo ""
echo "For detailed usage instructions, see USAGE.md"
echo "================================================"
