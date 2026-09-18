import pandas as pd
import numpy as np

# ==========================================
# HYBRID RECOMMENDATION WEIGHTS
# ==========================================

WEIGHTS = {

    "text": 0.50,

    "mbti": 0.20,

    "skills": 0.15,

    "location": 0.10,

    "experience": 0.05

}


MBTI_TYPES = [

    "INTJ","INTP","ENTJ","ENTP",

    "INFJ","INFP","ENFJ","ENFP",

    "ISTJ","ISFJ","ESTJ","ESFJ",

    "ISTP","ISFP","ESTP","ESFP"

]


MBTI_COMPATIBILITY = {}

for mbti1 in MBTI_TYPES:

    MBTI_COMPATIBILITY[mbti1] = {}

    for mbti2 in MBTI_TYPES:

        score = 40

        if mbti1 == mbti2:
            score = 100

        else:

            if mbti1[0] == mbti2[0]:
                score += 20

            if mbti1[1] == mbti2[1]:
                score += 15

            if mbti1[2] == mbti2[2]:
                score += 15

            if mbti1[3] == mbti2[3]:
                score += 10

        MBTI_COMPATIBILITY[mbti1][mbti2] = score

# MBTI score

def calculate_mbti_score(user1, user2):

    return MBTI_COMPATIBILITY[user1][user2]



# ==========================================
# SKILL MATCHING SCORE
# ==========================================

def calculate_skill_score(skills1, skills2):
    """
    Calculates skill similarity score (0-100)
    based on common skills.
    """

    skills1 = {
        skill.strip().lower()
        for skill in skills1.split(",")
    }

    skills2 = {
        skill.strip().lower()
        for skill in skills2.split(",")
    }

    common = skills1.intersection(skills2)

    maximum = max(len(skills1), len(skills2))

    if maximum == 0:
        return 0

    return (len(common) / maximum) * 100


# ==========================================
# LOCATION MATCHING SCORE
# ==========================================

def calculate_location_score(city1, city2):

    if city1.strip().lower() == city2.strip().lower():
        return 100

    return 0


# ==========================================
# EXPERIENCE MATCHING SCORE
# ==========================================

def calculate_experience_score(exp1, exp2):

    difference = abs(exp1 - exp2)

    if difference == 0:
        return 100

    elif difference == 1:
        return 90

    elif difference == 2:
        return 80

    elif difference == 3:
        return 70

    elif difference == 4:
        return 60

    return 50


# ==========================================
# COMMON SKILLS
# ==========================================

def get_common_skills(skills1, skills2):

    s1 = {skill.strip().lower() for skill in skills1.split(",") if skill.strip()}
    s2 = {skill.strip().lower() for skill in skills2.split(",") if skill.strip()}

    return sorted(s1.intersection(s2))

def generate_reason(user1, user2):

    reasons = []

    # Common Skills
    common_skills = get_common_skills(
        user1["Skills"],
        user2["Skills"]
    )

    if common_skills:
        reasons.append(
            f"Shared skills: {', '.join(common_skills[:3])}"
        )

    # MBTI
    if user1["MBTI"] == user2["MBTI"]:
        reasons.append(
            f"Same MBTI ({user1['MBTI']})"
        )

    # Industry
    if user1["Industry"] == user2["Industry"]:
        reasons.append(
            f"Same industry ({user1['Industry']})"
        )

    # Career Goal
    if user1["Career_Goal"] == user2["Career_Goal"]:
        reasons.append(
            "Similar career goals"
        )

    # City
    if user1["City"] == user2["City"]:
        reasons.append(
            f"Located in {user1['City']}"
        )

    # Experience
    difference = abs(
        user1["Experience_Years"] -
        user2["Experience_Years"]
    )

    if difference <= 2:
        reasons.append(
            "Similar experience level"
        )

    if len(reasons) == 0:
        return "General profile similarity"

    return "; ".join(reasons)


# ==========================================
# SCORE BREAKDOWN
# ==========================================

def calculate_score_breakdown(
    source_index,
    target_index,
    users_df,
    similarity_matrix,
    weights=WEIGHTS
):
    """
    Calculate individual compatibility components
    and the final weighted compatibility score.
    """

    if not np.isclose(sum(weights.values()), 1.0):
        raise ValueError(
            "Recommendation weights must sum to 1.0"
        )

    user1 = users_df.iloc[source_index]
    user2 = users_df.iloc[target_index]

    # Text similarity
    text_score = (
        similarity_matrix[source_index][target_index]
        * 100
    )

    # MBTI compatibility
    mbti_score = calculate_mbti_score(
        user1["MBTI"],
        user2["MBTI"]
    )

    # Skill compatibility
    skill_score = calculate_skill_score(
        user1["Skills"],
        user2["Skills"]
    )

    # Location compatibility
    location_score = calculate_location_score(
        user1["City"],
        user2["City"]
    )

    # Experience compatibility
    experience_score = calculate_experience_score(
        user1["Experience_Years"],
        user2["Experience_Years"]
    )

    # Final weighted score
    total_score = (
        weights["text"] * text_score +
        weights["mbti"] * mbti_score +
        weights["skills"] * skill_score +
        weights["location"] * location_score +
        weights["experience"] * experience_score
    )

    return {
        "text_score": round(float(text_score), 2),
        "mbti_score": round(float(mbti_score), 2),
        "skill_score": round(float(skill_score), 2),
        "location_score": round(float(location_score), 2),
        "experience_score": round(float(experience_score), 2),
        "total_score": round(float(total_score), 2)
    }

    
# ==========================================
# HYBRID RECOMMENDATION ENGINE
# ==========================================

def recommend_hybrid_users(
    user_id,
    users_df,
    similarity_matrix,
    user_index,
    top_n=5,
    weights=WEIGHTS
):

    if user_id not in user_index:
        raise ValueError(f"User ID '{user_id}' not found.")

    source_index = user_index[user_id]

    recommendations = []

    for target_index in range(len(users_df)):

        if target_index == source_index:
            continue


        breakdown = calculate_score_breakdown(
                source_index,
                target_index,
                users_df,
                similarity_matrix,
                weights
        )

        user = users_df.iloc[target_index]

        reason = generate_reason(
            users_df.iloc[source_index],
            user
        )

        recommendations.append({

            "User_ID": user["User_ID"],

            "Name": user["Name"],

            "Profession": user["Profession"],

            "Industry": user["Industry"],

            "City": user["City"],

            "Skills": user["Skills"],

            "Career_Goal": user["Career_Goal"],

            "Text Similarity (%)": breakdown["text_score"],

            "MBTI Compatibility (%)": breakdown["mbti_score"],

            "Skill Match (%)": breakdown["skill_score"],

            "Location Match (%)": breakdown["location_score"],

            "Experience Match (%)": breakdown["experience_score"],

            "Compatibility (%)": breakdown["total_score"],

            "Reason": reason

        })

    recommendations = sorted(
        recommendations,
        key=lambda x: x["Compatibility (%)"],
        reverse=True
    )

    return pd.DataFrame(recommendations[:top_n])


# ==========================================
# ADAPTIVE WEIGHT LEARNING
# ==========================================

def learn_user_weights(
    user_id,
    feedback_file=r"feedback_detailed.csv"
):

    default_weights = {
        "text": 0.50,
        "mbti": 0.20,
        "skills": 0.15,
        "location": 0.10,
        "experience": 0.05
    }

    try:
        feedback_df = pd.read_csv(
            feedback_file
        )

    except (
        FileNotFoundError,
        pd.errors.EmptyDataError
    ):
        return default_weights

    required_columns = [
        "User_ID",
        "Recommended_User",
        "Compatibility",
        "Feedback",
        "Updated_Compatibility"
    ]

    if not all(
        column in feedback_df.columns
        for column in required_columns
    ):
        return default_weights

    user_feedback = feedback_df[
        feedback_df["User_ID"].astype(str)
        == str(user_id)
    ].copy()

    if user_feedback.empty:
        return default_weights

    user_feedback["Feedback"] = pd.to_numeric(
        user_feedback["Feedback"],
        errors="coerce"
    )

    user_feedback = user_feedback[
        user_feedback["Feedback"].isin([0, 1])
    ].copy()

    if user_feedback.empty:
        return default_weights

    accepted = int(
        (user_feedback["Feedback"] == 1).sum()
    )

    rejected = int(
        (user_feedback["Feedback"] == 0).sum()
    )

    if accepted > rejected:

        learned_weights = {
            "text": 0.55,
            "mbti": 0.20,
            "skills": 0.15,
            "location": 0.05,
            "experience": 0.05
        }

    elif rejected > accepted:

        learned_weights = {
            "text": 0.40,
            "mbti": 0.20,
            "skills": 0.20,
            "location": 0.10,
            "experience": 0.10
        }

    else:

        learned_weights = default_weights

    return learned_weights

    
# ==========================================
# FEEDBACK PERFORMANCE EVALUATION
# ==========================================


def evaluate_feedback_performance(
    feedback_file=r"feedback_detailed.csv"
):

    try:

        feedback_df = pd.read_csv(
            feedback_file
        )

    except (
        FileNotFoundError,
        pd.errors.EmptyDataError
    ):

        return None

    required_columns = [
        "User_ID",
        "Recommended_User",
        "Compatibility",
        "Feedback",
        "Updated_Compatibility"
    ]

    if not all(
        column in feedback_df.columns
        for column in required_columns
    ):

        return None

    feedback_df["Feedback"] = pd.to_numeric(
        feedback_df["Feedback"],
        errors="coerce"
    )

    feedback_df["Compatibility"] = pd.to_numeric(
        feedback_df["Compatibility"],
        errors="coerce"
    )

    # Keep only valid feedback
    feedback_df = feedback_df[
        feedback_df["Feedback"].isin([0, 1])
    ].copy()

    if feedback_df.empty:

        return None

    total_feedback = len(
        feedback_df
    )

    accepted = int(
        (feedback_df["Feedback"] == 1).sum()
    )

    rejected = int(
        (feedback_df["Feedback"] == 0).sum()
    )

    acceptance_rate = (
        accepted / total_feedback
    ) * 100

    rejection_rate = (
        rejected / total_feedback
    ) * 100

    average_compatibility = (
        feedback_df["Compatibility"].mean()
    )

    return {

        "Total Feedback": total_feedback,

        "Accepted": accepted,

        "Rejected": rejected,

        "Acceptance Rate (%)": round(
            acceptance_rate,
            2
        ),

        "Rejection Rate (%)": round(
            rejection_rate,
            2
        ),

        "Average Compatibility (%)": round(
            average_compatibility,
            2
        )
     }


if __name__ == "__main__":

    print(calculate_mbti_score("INTJ", "INTP"))

    print(calculate_mbti_score("INTJ", "INTJ"))

    print(
    calculate_skill_score(
        "Python, SQL, Machine Learning",
        "Python, SQL, TensorFlow"
        )
    ) 
    print(
    calculate_location_score(
        "Hyderabad",
        "Hyderabad"
        )
    )

    print(
    calculate_location_score(
        "Hyderabad",
        "Bangalore"
        )
    ) 
    print(calculate_experience_score(5,5))
    print(calculate_experience_score(5,6))
    print(calculate_experience_score(5,10))

    users_df = pd.read_csv("users.csv")

    similarity_df = pd.read_csv(
    "similarity_matrix.csv",
    index_col=0
    )

    similarity_matrix = similarity_df.to_numpy(dtype=float)

    print(similarity_df.head())
    print(similarity_df.shape)
    print(similarity_df.dtypes)

    print(type(similarity_matrix))
    print(type(similarity_matrix[0][0]))

    user_index = {
        user_id: idx
        for idx, user_id in enumerate(users_df["User_ID"])
    }

    
    recommendations = recommend_hybrid_users(
        "U001",
        users_df,
        similarity_matrix,
        user_index,
        top_n=5,
        weights=WEIGHTS
    )
    recommendations = recommend_hybrid_users(
    "U050",
    users_df,
    similarity_matrix,
    user_index
    )
    recommendations = recommend_hybrid_users(
    "U100",
    users_df,
    similarity_matrix,
    user_index
    )
    
    learned_weights = learn_user_weights("U001")

    print("\nLearned Weights for U001:")
    print(learned_weights)

    print(
        "Weight Sum:",
        sum(learned_weights.values())
    )
    print(recommendations)




