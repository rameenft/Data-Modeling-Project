# MentorMenteeSystem

## MentorMenteeSystem

The Mentor-Mentee System is the core mechanism for connecting individuals on the platform, facilitating shared human experiences through a two-sided matching market. It aims to pair users seeking support (mentees) with those who have successfully navigated similar challenges (mentors), leveraging AI to ensure high-quality, empathetic connections while preventing mentor burnout.

### Key Concepts

*   **Two-sided Matching Market:** A system where both mentors and mentees must accept a proposed match, optimizing for mutual satisfaction and engagement rather than strict stability.
*   **Mentor Capacity Management:** Proactive measures, such as hard limits on active mentees, designed to prevent volunteer fatigue and ensure mentors can provide quality support.
*   **Affect Trajectory:** The longitudinal tracking of a user's emotional state over multiple sessions, used to assess the effectiveness of a mentor-mentee relationship and inform future matching.
*   **Hybrid Matching:** A multi-stage approach combining fast, semantic similarity search with slower, LLM-powered re-ranking and explanation generation to provide transparent and relevant match suggestions.
*   **Cold Start Problem:** The challenge of effectively matching new users who lack historical interaction data, often addressed through structured onboarding or demographic fallbacks.
*   **Functional Empathy:** The AI's ability to generate responses and facilitate interactions that are *perceived* as empathetic by human users, crucial for establishing trust and rapport in sensitive contexts.

### How It Works

The system begins with **Experience Capture** where users articulate their lived experiences. Recognizing the difficulty of typing sensitive narratives, the platform priorit