# 🏠 AURA-Space: AI-Based Interior Design Application
Generative AI | Computer Vision | Flutter | FastAPI

## Executive Summary

AURA-Space is an end-to-end AI platform that solves the challenge in interior design. Traditional AI often alters the entire room layout when asked for a small change. AURA-Space uses Semantic Segmentation and Multi-Conditioning ControlNets to provide surgical, pixel-perfect design edits while maintaining structural integrity.

## 📖 Table of Contents

1. [Project Structure](#project-structure)
2. [Mathedology](#mathedology)
3. [Data Pipeline & preprocessing](#data-pipeline-&-preprocessing)
4. [Object detection and Design Generation Pipeline](#object-detection-and-design-generation-pipeline)
5. [5 Main Core Modules of the Project](#5-main-core-modules-of-the-project)
6. [Mobile Application Flow](#mobile-application-flow)
7. [Technical Architecture](#technical-architecture)
8. [Tech Stack](#tech-stack)
9. [Setup & Installation](#setup--installation)
10. [Challenges & Limitations](#challenges-&-limitations)
11. [Academic Context](#academic-context)

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
      ├── Requirements.txt                  # Required Dependencies
      ├── LICENSE
      └── README.md

## Mathedology

In the Mathedology I followed a client-server architecture with Microservice architecture. Microservice architecture is used between the Flask API  and the model spaces, where each space works as a microcomponent. Request generated from the client side, which is the user interface of flutter mobile application, this request goes to the server, and in the server, it either goes to firebase or the AI model based on the request.
<img width="535" height="536" alt="image" src="https://github.com/user-attachments/assets/bb42e3c6-2266-47e8-a1ba-f99075cde243" />

## 📊 Data Pipeline & Preprocessing

Data piepline and preprocessing are cpmprised of image loading, resizing to maintain the aspoect ratio, Normalization to scale image values to (0,1). For data pipeline to finetuned model we implemented a data pipeline in which a dataset of 1505 images(5 categories rooms) are inserted through the following piepline.
1. **Depth Extraction:** Generating depth annotation images from the given images datasets for structural consistency.
2. **Automated Captioning:** Use Blip caption model to genmerate description for the interior datasets.
3. **Metadata Generation:** Create metadata.json file having triplet (image, depth map, and caption) save for the fine tunning of model.


## Object detection and Design Generation Pipeline

Design generation pipline isbased on computer vision and design generation process using AI and Gen Ai Models.
1. ***Semantic Segmentation:*** For the segmentation *Mask2Former* model used because of its state-of-the-art-performance which provide campabaility of universal segmentation.
   * **Inferenece Process:** Input image is preprocessed in the model to generate output of the class ID of detected objects in the image.
   *  **Object Identification and Mask Extraction:** After inference, there comes object identificationa nd mask extraction nference raw output with class labels and mask output in tensor format involves this step to map class ID (integers) with human-readable object names (e.g., “chair,” “bed”) using predefined functions in code, which are “map_color_rgb, and ade-palett.”
2. ***Design Generation:*** From semantic segmentation output images goes into desgin generation process.
   * **StableDiffusionInpaintPipeline:** segmented objects remove from another object or from the adjustment of the background.
   * **SatbaleDiffusionControlNetPipeline:** it is used to create a main model, which is the combination of all the encoders of Stable Diffusion and ControlNet, to use as input in image processing.


## 🧩 5 Main Core Modules of the Project

1. **Empty room generation** (empty_room_generation_app.py)
* Purpose: Furnishing an empty room with furniture based on prompt.
* How it works: makes use of ControlNet Depth and Segmentation in conjunction with Realistic Vision V5.1 to guarantee that furniture is positioned with 3D awareness while maintaining the integrity of walls and flooring.
* Testing Prompt: A minimalist bedroom with a platform bed, simple nightstands, and a large window, but without any curtains or wall art.
  <img width="1254" height="653" alt="image" src="https://github.com/user-attachments/assets/cac11094-1412-438d-8e80-7e06b5bf6137" />

2.  **Object Regeneration** (regenerate.py)
* Purpose: Replacing specific and selected objkects from image with another one.
* How it works: Leverages Mask2Former to identify 100+ object categories (ADE20K). It generates a precise inpainting mask for the selected object while preserving the room layout.
* Testing Prompt: Update the living room to a bohemian style. Replace the sofa with a comfortable, oversized velvet sofa in deep emerald green, add a distressed Persian rug, and hang macrame plant hangers beside the wall
  <img width="1419" height="741" alt="image" src="https://github.com/user-attachments/assets/f115864d-1a83-44f2-8975-5cf8b1b81911" />

3.  **Objects Recoloring** (recolor_object_app.py)
* Purpose: this space is used to change color of the user selected objects within an image.
* How it works: Employs LAB Color Space transformation. By isolating the Lightness and channel, we preserve original textures and shadows while injecting new color ($A, B$ channels).
* Testing Prompt: Recolor the sofa to a deep emerald green."
<img width="1092" height="580" alt="image" src="https://github.com/user-attachments/assets/e391c746-2efd-4c5e-a8af-b851163cbe82" />


4.  **Room Inpainting** (inpainting_app.py)
* Purpose: "Paint-to-Design" freehand editing.
* How it works: Features an interactive canvas where users brush areas for redesign. We apply FFT-based Gaussian Blurring to the mask edges to ensure a seamless "melt" between original and AI content.
* Testing Prompt: Remove the old brown sofa and replace it with a sleek, gray modular sectional.
<img width="1472" height="562" alt="image" src="https://github.com/user-attachments/assets/8b637fe8-7dd1-464c-bbd6-ebaf778b7853" />


 5. **ControlNet depth Generation:** (controlnet_depth_model_app.py) Generate a full interior design from an image of an empty room using detailed text prompts and 3 types of ControlNet Maps: segmentatio Map, canny edges, and depth Map. this Model is trained on our custom dataset.
    * Testing prompt: A high-quality photo of a modern, minimalist living room with a large window, light wooden flooring, a plush grey sofa, and a sleek glass coffee table.
<img width="1207" height="394" alt="image" src="https://github.com/user-attachments/assets/212a1707-f41e-4e7c-99fb-6e84668ed7ce" />
<img width="884" height="462" alt="image" src="https://github.com/user-attachments/assets/831e8c47-1439-42d2-bb18-c079d557d354" />

## Mobile Application Flow

 * The AuraSpace splash screen, which displays the app's branding and logo, marks the start of the user's journey. This first screen offers a smooth and eye-catching entrance.
<img width="375" height="610" alt="image" src="https://github.com/user-attachments/assets/75ffd319-ef52-4b36-8462-8f91971142d8" /> <img width="1139" height="794" alt="image" src="https://github.com/user-attachments/assets/9eab92f3-4970-4f6b-a18b-74c5f0a66096" />

 * Login and signup Screens
<img width="1033" height="736" alt="image" src="https://github.com/user-attachments/assets/6056991b-e123-4359-b39b-05e139e7dfeb" />

 * Main Menu and Feature Selection

   <img width="402" height="764" alt="image" src="https://github.com/user-attachments/assets/bcb34eff-c001-406a-b301-9773f95c4c3b" />

   
 * Empty room genearation Flow
   <img width="805" height="857" alt="image" src="https://github.com/user-attachments/assets/6a64ef80-206d-4934-98fe-d3ef9d9a9481" />

   
 * Object regenartion flow
<img width="719" height="817" alt="image" src="https://github.com/user-attachments/assets/ec559ed4-416e-4bef-9113-0813624de9cf" />
   
   
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

1. ##### Clone the repository:
       git clone [https://github.com/your-username/AURA-Space.git]([https://github.com/your-username/AURA-Space.git](https://github.com/asmazahoor02/AI_interior_design_Application_Aura-Space_.git))
2. ##### Environment setup:
       pip install torch diffusers transformers fastapi uvicorn opencv-python

## Challenges & Limitations

* **Negative Prompting:** Occasional issues with the model fully adhering to "negative prompts" (e.g., removing specific items like curtains).
* **Complex Scenes:** Potential accuracy drops in recoloring when a room is overcrowded with many overlapping objects.
* **Prompt Dependency:** The quality of the output is heavily reliant on precise prompt engineering by the user.

# 🎓 Academic Recognition

* Developed as a Final Year Project (FYP) at Sukkur IBA University (2025).
* Authors: Asma Zahoor & Aliza Imtiaz
* Supervisor: Ms. Sanam Fayaz
* Department: Computer Science & Software Engineering

* **Note:** the stable diffusion used in the project from stabilityai is wirthdrawed from the site, to run the spaces it is necessary to use another model instead of stabilityai/stablediffusionbase-2- version.

# 📫 Connect with the Developers
* Asma Zahoor - [LinkedIn](https://www.linkedin.com/in/asmazahoor/)
* Aliza Imtiaz - [LinkedIn](https://www.linkedin.com/in/alizaa-imtiaz-983b9a24a/)

