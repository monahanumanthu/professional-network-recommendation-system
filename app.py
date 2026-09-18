import streamlit as st
import pandas as pd
import recommendation_engine as re
from datetime import datetime

# Page Configuration

st.set_page_config(
    page_title="Professional Network Recommendation System",
    page_icon="🤝",
    layout="wide"
)

# Load the Dataset

@st.cache_data
def load_users():

    return pd.read_csv("users.csv")

users_df = load_users()

# Load Similarity Matrix

@st.cache_data
def load_similarity_matrix():

    similarity_df = pd.read_csv(
        "similarity_matrix.csv",
        index_col=0
    )

    return similarity_df.to_numpy(dtype=float)

similarity_matrix = load_similarity_matrix()

# feedback-saving functio

def save_feedback(
    user_id,
    matched_user_id,
    action,
    recommendation
):

    feedback_file = r"feedback_detailed.csv"

    feedback_record = {
        "User_ID": user_id,
        "Recommended_User": matched_user_id,
        "Compatibility": recommendation["Compatibility (%)"],
        "Feedback": action,
        "Updated_Compatibility": recommendation["Compatibility (%)"]
    }

    try:

        feedback_df = pd.read_csv(
            feedback_file
        )

    except FileNotFoundError:

        feedback_df = pd.DataFrame(
            columns=[
                "User_ID",
                "Recommended_User",
                "Compatibility",
                "Feedback",
                "Updated_Compatibility"
            ]
        )

    feedback_df = pd.concat(
        [
            feedback_df,
            pd.DataFrame([feedback_record])
        ],
        ignore_index=True
    )

    feedback_df.to_csv(
        feedback_file,
        index=False
    )

    return True

# Create User Index

user_index = {
    user_id: idx
    for idx, user_id in enumerate(users_df["User_ID"])
}

# Store recommendations between Streamlit reruns

if "recommendations" not in st.session_state:
    st.session_state.recommendations = None

if "feedback_message" not in st.session_state:
    st.session_state.feedback_message = None
    
if "learned_weights" not in st.session_state:
    st.session_state.learned_weights = None

    
# Application Title

st.title("🤝 Professional Network Recommendation System")

st.write(
    "A hybrid professional network recommendation system that identifies "
    "potentially compatible users using profile similarity, skills, "
    "personality, location, experience, and career goals."
)

# User Selection

st.subheader("Select a User")

selected_user = st.selectbox(
    "Choose a User ID",
    users_df["User_ID"].tolist()
)

# Display Selected User Profile

user = users_df[
    users_df["User_ID"] == selected_user
].iloc[0]

st.subheader("User Profile")

st.write("**Name:**", user["Name"])

st.write(
    "**Profession:**",
    user["Profession"]
)

st.write(
    "**Industry:**",
    user["Industry"]
)

st.write(
    "**City:**",
    user["City"]
)

st.write(
    "**Experience:**",
    user["Experience_Years"]
)

st.write(
    "**MBTI:**",
    user["MBTI"]
)

st.write(
    "**Career Goal:**",
    user["Career_Goal"]
)

st.write(
    "**Skills:**",
    user["Skills"]
)

# ==========================================
# RECOMMENDATION BUTTON
# ==========================================

if st.button(
    "🔍 Generate Recommendations",
    type="primary"
):

    learned_weights = re.learn_user_weights(
        selected_user
    )

    st.session_state.learned_weights = learned_weights

    st.session_state.recommendations = (
        re.recommend_hybrid_users(
            selected_user,
            users_df,
            similarity_matrix,
            user_index,
            top_n=5,
            weights=learned_weights
        )
    )

    st.session_state.feedback_message = None


# ==========================================
# DISPLAY PERSONALIZED WEIGHTS
# ==========================================

if st.session_state.learned_weights is not None:

    with st.expander(
        "View Personalized Recommendation Weights"
    ):

        st.write(
            "The system adjusts these weights based on "
            "your previous feedback."
        )

        weights = st.session_state.learned_weights

        st.write(
            f"Text Similarity: {weights['text']:.2f}"
        )

        st.write(
            f"MBTI: {weights['mbti']:.2f}"
        )

        st.write(
            f"Skills: {weights['skills']:.2f}"
        )

        st.write(
            f"Location: {weights['location']:.2f}"
        )

        st.write(
            f"Experience: {weights['experience']:.2f}"
        )
        


# ==========================================
# DISPLAY RECOMMENDATIONS
# ==========================================

if st.session_state.recommendations is not None:

    recommendations = st.session_state.recommendations

    st.subheader(
        "Top 5 Professional Recommendations"
    )

    for _, recommendation in recommendations.iterrows():

        st.markdown(
            f"### 👤 {recommendation['Name']}"
        )

        # Professional details - line by line

        st.write(
            "**User ID:**",
            recommendation["User_ID"]
        )

        st.write(
            "**Profession:**",
            recommendation["Profession"]
        )

        st.write(
            "**Industry:**",
            recommendation["Industry"]
        )

        st.write(
            "**City:**",
            recommendation["City"]
        )

        st.write(
            "**Career Goal:**",
            recommendation["Career_Goal"]
        )

        st.write(
            "**Skills:**",
            recommendation["Skills"]
        )

        st.metric(
            "Compatibility",
            f"{recommendation['Compatibility (%)']:.2f}%"
        )

        st.info(
            f"💡 **Why this recommendation?** "
            f"{recommendation['Reason']}"
        )

        # ==========================================
        # COMPATIBILITY BREAKDOWN
        # ==========================================

        with st.expander(
            "View Compatibility Breakdown"
        ):

            st.write(
                "**Text Similarity:**",
                f"{recommendation['Text Similarity (%)']:.2f}%"
            )

            st.write(
                "**MBTI Compatibility:**",
                f"{recommendation['MBTI Compatibility (%)']:.2f}%"
            )

            st.write(
                "**Skill Match:**",
                f"{recommendation['Skill Match (%)']:.2f}%"
            )

            st.write(
                "**Location Match:**",
                f"{recommendation['Location Match (%)']:.2f}%"
            )

            st.write(
                "**Experience Match:**",
                f"{recommendation['Experience Match (%)']:.2f}%"
            )

        # ==========================================
        # FEEDBACK BUTTONS
        # ==========================================

        button_col1, button_col2 = st.columns(2)

        with button_col1:

            if st.button(
                "👍 Accept",
                key=f"accept_{selected_user}_{recommendation['User_ID']}"
            ):

                save_feedback(
                    selected_user,
                    recommendation["User_ID"],
                    1,
                    recommendation
                )

                st.session_state.feedback_message = (
                    f"Recommendation for "
                    f"{recommendation['Name']} "
                    f"was accepted!"
                )

                st.rerun()

        with button_col2:

            if st.button(
                "👎 Reject",
                key=f"reject_{selected_user}_{recommendation['User_ID']}"
            ):

                save_feedback(
                    selected_user,
                    recommendation["User_ID"],
                    0,
                    recommendation
                )

                st.session_state.feedback_message = (
                    f"Recommendation for "
                    f"{recommendation['Name']} "
                    f"was rejected."
                )

                st.rerun()

        st.divider()


# ==========================================
# FEEDBACK MESSAGE
# ==========================================

if st.session_state.feedback_message:

    st.success(
        st.session_state.feedback_message
    )

    
# ==========================================
# SYSTEM PERFORMANCE
# ==========================================

evaluation = re.evaluate_feedback_performance()

if evaluation is not None:

    st.subheader("📊 System Performance")

    st.write(
        "**Total Feedback:**",
        evaluation["Total Feedback"]
    )

    st.write(
        "**Accepted:**",
        evaluation["Accepted"]
    )

    st.write(
        "**Rejected:**",
        evaluation["Rejected"]
    )

    st.write(
        "**Acceptance Rate:**",
        f"{evaluation['Acceptance Rate (%)']:.2f}%"
    )

    st.write(
        "**Rejection Rate:**",
        f"{evaluation['Rejection Rate (%)']:.2f}%"
    )

    st.write(
        "**Average Compatibility:**",
        f"{evaluation['Average Compatibility (%)']:.2f}%"
    )

else:

    st.info(
        "No valid feedback data available yet."
    )

