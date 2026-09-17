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

```
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
```

### Dataset

The project uses a synthetic professional user dataset containing:

- 100 professional user profiles
- 35 attributes
- 20 professions
- 5 profiles per profession

The dataset contains professional, demographic and profile-related information such as:

- Profession
- Skills
- Career goals
- Professional summary
- Personality information
- Location
- Industry
- Experience
- Work preferences
- Technology preferences

### Important Note

The user profiles and feedback datasets included in this repository are **synthetic datasets created for project development and demonstration purposes**.

They do not represent real users or real professional networking activity.

---

### NLP Processing

TF-IDF is used to convert profile text into numerical feature vectors.

The implementation uses:

- English stop-word removal
- Maximum vocabulary size of 500 features
- Unigram and bigram features

Cosine Similarity is then calculated between the TF-IDF representations.

The resulting similarity matrix contains pairwise similarity values for all 100 users.

Matrix size:

`100 × 100`

### Feedback Evaluation

A separate synthetic feedback dataset containing **500 interactions** was generated to demonstrate the feedback and adaptive-weighting workflow.

### Feedback Dataset

| Metric | Value |
|---|---:|
| Total interactions | 500 |
| Unique users   | 100 |
| Interactions per user   | 5 |
| Accepted | 130 |
| Rejected | 370 |
| Acceptance Rate | 26.0% |
| Rejection Rate | 74.0% |
| Average Compatibility | 25.93236% |

Because this dataset is synthetically generated, these values should be interpreted as evaluation results from the project setup rather than real-world user behavior.

### Baseline vs Adaptive Recommendations

For user `U001`:

### Baseline Configuration
```
Text Similarity    0.50
MBTI               0.20
Skills             0.15
Location           0.10
Experience         0.05
```

Average compatibility of the Top 5 recommendations:

`49.34%`

### Adaptive Configuration

After feedback-based rule adjustment:

```
Text Similarity    0.55
MBTI               0.20
Skills             0.15
Location           0.05
Experience         0.05
```

Average compatibility of the Top 5 recommendations:

`50.94%`

### Performance Change

`+1.60 percentage points`

This represents an improvement in the average compatibility score of the evaluated Top 5 recommendations for U001.

It should not be interpreted as classification accuracy or real-world recommendation accuracy.

---

### Streamlit Application

The project includes a Streamlit application that provides an interactive interface for the recommendation system.

Users can:

1. Select a professional profile
2. View profile information
3. Generate recommendations
4. View the Top 5 recommendations
5. View compatibility scores
6. View recommendation explanations
7. View compatibility breakdowns
8. View personalized recommendation weights
9. Accept recommendations
10. Reject recommendations
11. View feedback confirmation
12. View system performance information

The Streamlit interface acts as the front end, while the recommendation logic is implemented separately in `recommendation_engine.py`.

---

### Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- TF-IDF
- Cosine Similarity
- Matplotlib
- Faker
- Streamlit
- Jupyter Notebook
  
### Project Structure
```
professional-network-recommendation-system/
│
├── README.md
├── professional_network_recommendation.ipynb
├── recommendation_engine.py
├── app.py
│
├── users.csv
├── users_cleaned.csv
├── similarity_matrix.csv
├── feedback_training.csv
├── feedback_detailed.csv
│
├── requirements.txt
├── .gitignore
│
├── screenshots/
│   ├── dataset_validation.png
│   ├── similarity_matrix.png
│   ├── top5_recommendations.png
│   ├── compatibility_breakdown.png
│   ├── feedback.png
│   └── streamlit_app.png
│
└── PROFESSIONAL_NETWORK_RECOMMENDATION_SYSTEM_REPORT.pdf
```

---

### File Description

`professional_network_recommendation.ipynb`

Contains data generation, validation, NLP processing, similarity calculation, compatibility scoring, recommendation development, feedback analysis and evaluation.

`recommendation_engine.py`

Contains the core hybrid recommendation engine, score calculation, recommendation explanations, adaptive weighting and feedback evaluation logic.

`app.py`

Contains the Streamlit-based interactive user interface.

`users.csv`

Synthetic professional user profile dataset.

`users_cleaned.csv`

Cleaned version of the user profile dataset.

`similarity_matrix.csv`

100 × 100 profile similarity matrix generated using TF-IDF and Cosine Similarity.

`feedback_training.csv`

Synthetic 500-record feedback dataset used to demonstrate and evaluate the feedback workflow.

`feedback_detailed.csv`

Stores feedback generated through application interactions.

`requirements.txt`

Python dependencies required to run the project.

---

### Installation

Clone the repository:

[git clone](https://github.com/monahanumanthu/professional-network-recommendation-system.git)

Move into the project directory:

`cd professional-network-recommendation-system`

Install the dependencies:

`pip install -r requirements.txt`

---

### Run the Streamlit Application

Run:

`streamlit run app.py`

If the command is not recognized, use:

`python -m streamlit run app.py`

The application will open in your browser at:

`http://localhost:8501`

### Limitations

- The feedback dataset used for evaluation is synthetic rather than collected from a large real-world user base.
- The adaptive weighting mechanism currently uses rule-based adjustment.
- TF-IDF and Cosine Similarity provide useful text similarity but may not capture deeper semantic meaning.
- The MBTI compatibility component uses a predefined compatibility matrix.
- The current system does not use a database for persistent production-scale feedback storage.

---

### Future Improvements

Possible future improvements include:

1. Transformer-based sentence embeddings
2. Advanced learning-to-rank recommendation algorithms
3. Larger real-world feedback datasets
4. Database-backed feedback storage
5. User authentication
6. Cloud deployment
7. Real-time recommendation updates
8. More advanced personalization
9. Continuous online learning
10. Integration with professional networking platforms

---

### Key Learning

This project helped me understand how multiple recommendation signals can be combined into a single hybrid recommendation framework.

It provided practical experience with:

- NLP
- TF-IDF
- Cosine Similarity
- Recommendation systems
- Hybrid scoring
- Explainable recommendations
- Feedback-based personalization
- Data analysis
- Streamlit application development

---

### Conclusion

The Intelligent Hybrid Professional Network Recommendation System combines NLP-based profile similarity, MBTI compatibility, skill matching, location matching and experience matching into a unified compatibility score.

The system generates Top 5 recommendations, provides explanations and compatibility breakdowns, and supports Accept/Reject feedback through an interactive Streamlit application.

For the evaluated U001 example, the average compatibility of the Top 5 recommendations increased from **49.34% using baseline weights to 50.94% using adaptive weights, representing a change of +1.60 percentage points**.

The project demonstrates how NLP, hybrid recommendation, explainability, feedback-based personalization and interactive application development can be brought together into a single recommendation system.

### Disclaimer

This project is an educational and portfolio project.

The user profiles and feedback datasets are synthetic and are intended only for demonstration and evaluation.

The recommendation scores should not be interpreted as professional, personality or career advice.
