# 🏠 AURA-Space: AI-Based Interior Design Application
Generative AI | Computer Vision | Flutter | FastAPI

## Executive Summary
AURA-Space is an end-to-end AI platform that solves the "re-generation" challenge in interior design. Traditional AI often alters the entire room layout when asked for a small change; AURA-Space uses Semantic Segmentation and Multi-Conditioning ControlNets to provide surgical, pixel-perfect design edits while maintaining structural integrity.

## 📖 Table of Contents

1. [Project Structure](#project-structure)
2. [Data Pipeline & preprocessing](#data-pipeline-&-preprocessing)
3. [Core Modules](#core-modules)
4. [Problem Solving](#problem-solving)
5. [Technical Architecture](#technical-architecture)
6. [Tech Stack](#tech-stack)
7. [Setup & Installation](#setup--installation)
8. [Challenges & Limitations](#challenges-&-limitations)
9. [Academic Context](#academic-context)

## 📁 Project Structure
      AI_interior_design_Application_Aura-Space_/
      ├── Dataset/                             # some images from data which are used to train
      |   ├── images/                          # Original images
      │   ├── annotation/                      # annotated depth images
      │   ├── rename files.py/                 # rename image script (rename files.py)
      |   ├── depth map generator.py/          # py script to generat depth map image
      │   ├── Blip captioning.py/              # use blip model to captions images
      │   └── metadata.json                    # caption file of data
      ├── Spaces/                              # AI core spaces for design generation
      │   ├── controlnet depth generation/     #  fine tuned model to generate design from scratch (app.py)
      │   ├── Empty room generation/           # py scripts for empty room styling (app.py, color.py)
      │   ├── Room Inpainting/                 # space to inpaint object in image (inpainting.py, inpainting_app.py)
      │   ├── controlnet object regeneration/  # space to generate specific objects wihin image (colors.py, control_net_room_generate_app.py, regenerate.py)
      │   └── recolor_object_app.py/          # recolor space code file 
      │    
      ├── model/                              # trained modvl on Depth dataset
      │   ├── controlnet depth model/         # config.json or safetensors files of finetuned model
      │   └── fine_tunning_scrpt.py          # script to fine tune model
      ├── ui_fyp/                            # Mobile App UI and Api connection
      |   ├── lib/                           # dart source code
      │   └── pubspec.yaml                   # Flutter dependencies
      ├── Requirements.txt/                  # Required Dependencies
      ├── LICENSE
      └── README.md
## 📊 Data Pipeline & Preprocessing
To achieve high-quality results, we implemented a custom data pipeline:
1. **Depth Extraction:** Generating spatial maps for structural consistency.
2. **Automated Captioning:** Using Salesforce BLIP to generate natural language descriptions for interior datasets.
3. **Metadata Generation:** Creating metadata.json triplets (Image + Depth + Caption) for model fine-tuning.

## 🧩 Core Modules
1. **Empty Room Generation** (empty_room_generation_app.py)
* Purpose: Furnishing an empty architectural shell.
* How it works: Uses Realistic Vision V5.1 combined with ControlNet Depth and Segmentation to ensure furniture is placed in a 3D-aware manner while keeping walls and floors intact.
2.  **Semantic Object Regeneration** (regenerate.py)
* Purpose: Replacing specific furniture items via AI.
* How it works: Leverages Mask2Former to identify 100+ object categories (ADE20K). It generates a precise inpainting mask for the user-selected object, preserving the room's global context.
3.  **Texture-Preserving Recoloring** (recolor_object_app.py)
* Purpose: Non-destructive color changes for furniture and walls.
* How it works: Employs LAB Color Space transformation. By isolating the Lightness ($L$) channel, we preserve original textures and shadows while injecting new color ($A, B$ channels).
4.  **Manual Room Inpainting** (inpainting_app.py)
* Purpose: "Paint-to-Design" freehand editing.
* How it works: Features an interactive canvas where users brush areas for redesign. We apply FFT-based Gaussian Blurring to the mask edges to ensure a seamless "melt" between original and AI content.
 5. **Design from Scratch** ():  Generate a full interior design from an image of an empty room using detailed text prompts.
 6.  **Cloud Integration:** Firebase for user authentication and data storage; Hugging Face Spaces for hosting the AI model environments.

## Problem Solving
1. **Overcoming the Hallucination Problem**
   To ensure the AI respects room boundaries, we implemented Multi-Control Conditioning:
   * **Depth Anything Model:** Generates a 3D skeleton to prevent floating furniture.
   * **Canny Edge Detection:** Preserves architectural lines like windows and doors.
2. **Texture-Preserving Color Logic**
   * For the recoloring module, we avoided standard generation to prevent texture loss. By isolating the Lightness ($L$) channel in the LAB color space, the system changes the hue while maintaining the exact lighting and grain of the original material.
   
## Technical Architecture 
graph LR

    subgraph "Frontend Layer"
        F[Flutter Mobile App]
    end

    subgraph "API Gateway"
        API[FastAPI / Flask]
    end

    subgraph "AI Inference Engine (Hugging Face / Gradio)"
        SD[Stable Diffusion 1.5/2.0]
        CN[ControlNet Depth/Seg]
        M2F[Mask2Former Segmentation]
        DA[Depth Anything]
    end

    F -->|REST API / JSON| API
    API -->|Prompt & Image| SD
    SD -->|Generated Result| API
    API -->|Processed UI| F

## 🛠 Tech Stack

| Layer | Technology | Purpose |
| :--- | :--- | :--- |
| **Frontend** | **Flutter** | Cross-platform mobile UI for high-performance image manipulation. |
| **Backend** | **FastAPI / Flask** | High-concurrency API gateway for AI inference requests. |
| **AI Inference** | **Hugging Face / Gradio** | Distributed hosting for heavy diffusion models. |
| **Generative Models** | **Stable Diffusion v1.5/2.0** | Core engine for inpainting and text-to-image generation. |
| **Vision Models** | **Mask2Former / BLIP** | Semantic segmentation and automated image captioning. |

## 📦 Installation & Setup
#### Backend (AI Server)
1. ##### Clone the repository:
       git clone [https://github.com/your-username/AURA-Space.git](https://github.com/your-username/AURA-Space.git)
       cd AURA-Space/backend
2. ##### Environment setup:
       pip install torch diffusers transformers fastapi uvicorn opencv-python
3. ##### run server
       python controlnet_depth_model_app.py
#### Frontend (Mobile)
1. Install Flutter SDK.
2. Run the app:

     cd flutter_app
     flutter pub get
     flutter run

## Challenges & Limitations
* **Negative Prompting:** Occasional issues with the model fully adhering to "negative prompts" (e.g., removing specific items like curtains).
* **Complex Scenes:** Potential accuracy drops in recoloring when a room is overcrowded with many overlapping objects.
* **Prompt Dependency:** The quality of the output is heavily reliant on precise prompt engineering by the user.

# 🎓 Academic Recognition
* Developed as a Final Year Project (FYP) at Sukkur IBA University (2025).
* Authors: Asma Zahoor & Aliza Imtiaz
* Supervisor: Ms. Sanam Fayaz
* Department: Computer Science & Software Engineering

# 📫 Connect with the Developers
* Asma Zahoor - [LinkedIn](https://www.linkedin.com/in/asmazahoor/)
* Aliza Imtiaz - [LinkedIn](https://www.linkedin.com/in/alizaa-imtiaz-983b9a24a/)

