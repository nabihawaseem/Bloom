import streamlit as st
from backend.query_generator import generate_query
from backend.google_cse import search_products
from food_waste.food import run_food_rescue_app
from backend.llm_helper import generate_quiz_questions, interpret_answers

# Set Streamlit page config
st.set_page_config(page_title="Eco-Friendly Hub", layout="wide")

# Sidebar Navigation Menu
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Eco Alternatives Finder", "Surplus Food Rescue", "Eco-Friendly Lifestyle Quiz"])

# === Page 1: Eco Alternatives Finder ===
if page == "Eco Alternatives Finder":
    st.title("🌿 Eco Alternatives Finder")
    st.markdown(
        """
        <style>
        .center-content {
            display: flex;
            justify-content: center;
            align-items: center;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Input Section
    st.header("🔍 Find Eco-Friendly Product Alternatives")
    st.markdown(
        """
        Enter the name of the product you are using, and we'll find eco-friendly alternatives for you!
        """
    )
    product_name = st.text_input("Enter a product name:")

    if st.button("Search for Alternatives", help="Click to search for eco-friendly alternatives"):
        if product_name:
            # Step 1: Generate the search query using Groke API
            st.markdown("#### Generating Search Query...")
            query = generate_query(product_name)
            st.write(f"**🔗 Generated Search Query:** `{query}`")

            # Step 2: Fetch product alternatives using Google CSE
            st.header("🌟 Search Results")
            products = search_products(query)

            # Step 3: Display the results in the Streamlit app
            if products:
                for product in products:
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        st.image(product["image_url"], width=120)
                    with col2:
                        st.write(f"**{product['product_name']}**")
                        st.write(f"[🔗 View Product]({product['link']})")
            else:
                st.warning("No products found. Please try a different query.")
        else:
            st.warning("Please enter a product name to search!")

# === Page 2: Surplus Food Rescue ===
elif page == "Surplus Food Rescue":
    # Call the function from food.py
    st.title("🍽️ Surplus Food Rescue")
    st.markdown(
        """
        Help fight food waste by rescuing surplus food near you. Use the map below to locate nearby restaurants and stores offering surplus food at discounted prices!
        """
    )
    run_food_rescue_app()

# === Page 3: Eco-Friendly Lifestyle Quiz ===
elif page == "Eco-Friendly Lifestyle Quiz":
    st.title("🧠 Eco-Friendly & Organic Lifestyle Quiz")
    st.markdown(
        """
        Take a short quiz to get personalized tips and recommendations for living an eco-friendlier life!
        """
    )

    # Quiz logic encapsulated in a function
    def render_quiz():
        # Step 1: User Input
        st.subheader("🌱 Describe Your Lifestyle Goals")
        st.markdown("What do you want to improve about your lifestyle?")
        user_focus = st.text_area(
            "",
            placeholder="E.g., I want to reduce plastic use, eat healthier, and switch to eco-friendly products.",
            height=120,
        )

        if st.button("Generate Quiz", help="Click to generate personalized quiz questions"):
            if user_focus:
                # Step 2: Generate Quiz Questions Using LLM
                st.markdown("#### Generating Quiz Questions...")
                quiz_questions = generate_quiz_questions(user_focus)
                st.session_state["quiz_questions"] = quiz_questions
                st.success("Quiz questions generated successfully!")
            else:
                st.warning("Please describe your lifestyle focus!")

        # Step 3: Display Quiz
        if "quiz_questions" in st.session_state:
            st.subheader("📋 Your Personalized Quiz")
            answers = {}
            for idx, question in enumerate(st.session_state["quiz_questions"]):
                question = question.lstrip("Q").split(")", 1)[-1].strip() 
                st.write(f"**Q{idx+1}:** {question}")
                answers[f"q{idx}"] = st.radio(
                    f"Answer for Q{idx+1}:", ["Never", "Rarely", "Sometimes", "Often", "Always"], key=f"q{idx}"
                )

            # Step 4: Submit Answers and Generate Recommendations
            if st.button("Get Results", help="Click to see personalized tips based on your quiz answers"):
                st.markdown("#### 🔄 Processing Your Results...")
                results = interpret_answers(answers, user_focus)
                st.subheader("🌟 Your Personalized Tips")
                for idx, tip in enumerate(results["tips"], start=1):
                    st.write(f"**Tip {idx}:** {tip}")

    render_quiz()
