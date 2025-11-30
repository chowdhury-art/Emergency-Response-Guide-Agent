# Emergency Response Guide Agent

A multi‑agent safety assistant that gives clear, step‑by‑step, location‑aware emergency guidance (medical issues, fires, earthquakes, floods, storms) using a Planner → Worker → Evaluator workflow, tools, and session memory, deployed on Hugging Face.

## Features

- Planner → Worker → Evaluator multi‑agent architecture  
- Simple tools for protocols, local emergency numbers, and alerts  
- Session memory for region and recent context  
- Gradio web UI for easy interaction

## How it works

- **PlannerAgent** classifies the situation (type + severity) and decides which tools to use.  
- **WorkerAgent** calls tools and builds numbered safety steps and warnings.  
- **EvaluatorAgent** adds disclaimers, checks safety, and formats the final answer.

## Run locally

