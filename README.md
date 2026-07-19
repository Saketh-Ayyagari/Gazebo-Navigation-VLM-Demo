# Embodied AI Semantic Navigation

> An embodied AI system that autonomously explores unknown environments, constructs a spatial representation using Visual SLAM, and performs natural-language navigation through Vision-Language Models (VLMs).

---

## Overview

Robots operating in real-world environments often have **no prior knowledge of their surroundings**. While modern Visual SLAM systems enable robots to localize themselves and build maps, they primarily produce **geometric representations** of the environment rather than **semantic understanding**.

This project investigates how geometric mapping and modern Vision-Language Models (VLMs) can be combined to enable **high-level reasoning and navigation** in previously unseen environments.

Rather than asking a robot to navigate using manually specified coordinates, this project explores navigation using natural language instructions such as:

> "Go to the desk."

> "Find the kitchen."

> "Navigate to the room with the couch."

The robot must first explore, build a map, understand the environment, and then ground semantic concepts to physical locations.

---

# Motivation

Traditional robotics pipelines separate:

- Mapping
- Localization
- Navigation
- Semantic understanding

Recent Vision-Language Models demonstrate remarkable semantic reasoning capabilities, but they typically lack an explicit understanding of robot localization and world geometry.

This project explores how these two worlds can be integrated into a single embodied AI system.

---

# Research Question

**How can an embodied robot navigate an unknown environment using natural language without access to a pre-existing map?**

More specifically:

- How can Visual SLAM provide spatial context for a Vision-Language Model?
- How can semantic concepts be grounded to physical locations?
- How should a robot reason about unexplored environments?
- What information should be provided to a VLM to enable effective navigation?

---

# Project Objectives

## Phase 1 — Mapping & Localization

- Build a simulated robot using ROS 2 and Gazebo.
- Generate an online map using RTAB-Map.
- Perform localization in unknown environments.

Deliverable:

- Autonomous mapping of an unseen environment.

---

## Phase 2 — Semantic Understanding

Extract semantic information from the explored environment.

Potential examples include:

- Chairs
- Tables
- Doors
- Hallways
- Desks
- Offices

Deliverable:

- Semantic map aligned with the geometric map.

---

## Phase 3 — Natural Language Navigation

Use a Vision-Language Model to interpret commands such as:

- "Go to the chair."
- "Navigate to the office."
- "Find the kitchen."

The VLM must identify the appropriate destination and convert it into a navigable goal.

Deliverable:

- Language-grounded navigation.

---

## Phase 4 — Embodied Reasoning

Investigate how robots should reason when:

- the destination has not yet been observed,
- multiple candidate locations exist,
- the environment is only partially explored.

---

# Experimental Goals

This repository is intended to support experiments investigating the interaction between mapping, perception, and language.

Potential experiments include:

### Mapping

- Map quality across different environments
- Loop closure performance
- Exploration efficiency

### Perception

- Different camera configurations
- Feature-rich vs feature-poor environments
- Lighting conditions
- Dynamic obstacles

### Semantic Navigation

- Goal grounding accuracy
- Navigation success rate
- Effect of incomplete maps
- VLM reasoning performance

---

# Technologies

## Robotics

- ROS 2
- Gazebo
- Nav2
- RTAB-Map

## Computer Vision

- OpenCV

## AI

- Vision-Language Models (future integration)

## Programming

- Python
- C++

# Current Progress

- [x] Robot simulation
- [x] Camera integration
- [ ] RTAB-Map integration 
- [ ] Autonomous exploration
- [ ] Occupancy map generation
- [ ] Semantic scene extraction
- [ ] VLM interface
- [ ] Goal grounding
- [ ] Navigation
- [ ] Evaluation framework


# Inspiration

This project is inspired by recent advances in:

- Embodied AI
- Vision-Language Models
- Semantic Mapping
- Autonomous Navigation
- Simultaneous Localization and Mapping (SLAM)

The long-term goal is to investigate how modern foundation models can enhance robot autonomy by combining semantic reasoning with traditional robotics pipelines.
