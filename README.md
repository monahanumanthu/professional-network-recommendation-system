# Intelligent Hybrid Professional Network Recommendation System

A hybrid professional network recommendation system that combines NLP-based profile similarity with personality, skill, location and experience compatibility to generate explainable professional recommendations.

## Overview

Professional networking platforms contain large amounts of user information, including professional interests, skills, career goals, personality characteristics, location and experience.

This project develops a recommendation system that combines these different signals into a unified compatibility score.

The system uses:

- TF-IDF and Cosine Similarity for profile text
- MBTI compatibility
- Skill matching
- Location matching
- Experience matching
- Weighted hybrid scoring
- Explainable recommendations
- Accept/Reject feedback
- Rule-based adaptive weighting
- Streamlit for interactive use

The system generates and ranks the **Top 5 professional recommendations** for a selected user.

---

## Problem Statement

Finding professionally compatible people can be difficult when profile information is considered using only one factor.

The objective of this project is to develop a Python-based recommendation system that combines multiple professional and profile-based attributes to identify potentially compatible users.

The system also provides explanations for recommendations and supports feedback-based adjustment of recommendation weights.

---

## Key Features

### 1. NLP-Based Profile Similarity

Profile information from multiple fields is combined into text and processed using TF-IDF.

The system uses:

- Profession
- Skills
- Career Goal
- Professional Summary
- About Me
- Interests
- Personality Traits
- Personal Values
- Favorite Tech Stack
- Preferred Industry

Cosine Similarity is then used to measure similarity between user profiles.

### 2. MBTI Compatibility

The system supports all 16 MBTI personality types through a predefined 16 × 16 compatibility matrix.

MBTI compatibility is used as one component of the overall recommendation score.

### 3. Skill Matching

The system compares the skills of two users and calculates a percentage-based skill compatibility score.

### 4. Location Matching

Users from the same city receive a higher location compatibility score than users from different cities.

### 5. Experience Matching

Experience compatibility is calculated based on the difference between users' experience levels.

### 6. Hybrid Recommendation Score

The final recommendation score combines five components:

| Component | Baseline Weight |
|---|---:|
| Text Similarity | 0.50 |
| MBTI Compatibility | 0.20 |
| Skill Matching | 0.15 |
| Location Matching | 0.10 |
| Experience Matching | 0.05 |

The candidates are ranked using the final compatibility score, and the Top 5 recommendations are returned.

### 7. Explainable Recommendations

The system provides reasons behind recommendations, including:

- Shared skills
- Same MBTI type
- Same industry
- Similar career goals
- Same city
- Similar experience level

It also provides a compatibility breakdown showing the contribution of each scoring component.

### 8. Feedback and Adaptive Weighting

Users can Accept or Reject recommendations through the Streamlit application.

The system uses a **rule-based adaptive weighting mechanism** to adjust recommendation weights based on observed feedback.

This demonstrates a feedback-driven personalization workflow.

---

## System Workflow

```text
Professional User Profiles
          ↓
Data Validation
          ↓
Profile Text Creation
          ↓
Text Preprocessing
          ↓
TF-IDF Vectorization
          ↓
Cosine Similarity
          ↓
┌─────────────────────────────┐
│ Compatibility Signals       │
│                             │
│ • Text Similarity           │
│ • MBTI Compatibility        │
│ • Skill Matching            │
│ • Location Matching         │
│ • Experience Matching       │
└─────────────────────────────┘
          ↓
Hybrid Compatibility Score
          ↓
Top-5 Recommendations
          ↓
Recommendation Explanations
          ↓
Accept / Reject Feedback
          ↓
Rule-Based Adaptive Weighting
          ↓
Updated Recommendation Scores
