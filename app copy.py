import streamlit as st
from recipe_module.recommend_recipe import load_recipes, search_recipes

# Load recipes
filename = "bbc_recipes_ingredients.txt"
recipes = load_recipes(filename)

# User input for ingredients
user_input = st.text_input("Enter ingredients (comma-separated):", "")

if user_input:
    ingredients = [ingredient.strip() for ingredient in user_input.split(",")]
    matching = search_recipes(recipes, ingredients)

    if matching:
        st.subheader(f"✅ {len(matching)} Recipes Found")

        # Initialize session state for tracking current recipe index
        if "current_recipe_idx" not in st.session_state:
            st.session_state.current_recipe_idx = 0

        # Get current recipe to display
        current_idx = st.session_state.current_recipe_idx
        current_recipe = matching[current_idx]

        # Display recipe in a bordered container
        st.markdown(
            f"""
            <div style="border: 2px solid #ccc; padding: 15px; border-radius: 10px; background-color: #f9f9f9;">
                <h3><a href="{current_recipe['link']}" target="_blank">{current_recipe['title']}</a></h3>
                <h4>Ingredients:</h4>
                <ul>
                    {''.join(f'<li>{ingredient}</li>' for ingredient in current_recipe['ingredients'])}
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Navigation buttons
        col1, col2, col3 = st.columns([1, 2, 1])

        with col1:
            if st.button("⬅ Previous") and st.session_state.current_recipe_idx > 0:
                st.session_state.current_recipe_idx -= 1

        with col3:
            if st.button("Next ➡") and st.session_state.current_recipe_idx < len(matching) - 1:
                st.session_state.current_recipe_idx += 1

        # Show current recipe index
        st.write(f"Recipe {current_idx + 1} of {len(matching)}")

    else:
        st.warning("❌ No recipes found with those ingredients.")
