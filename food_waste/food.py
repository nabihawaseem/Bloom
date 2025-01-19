import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

# Function to run the Surplus Food Rescue App
def run_food_rescue_app():
    # Initialize geolocator
    geolocator = Nominatim(user_agent="surplus_food_app")

    # Constants for CSV files
    FOOD_WASTE_FOLDER = "food_waste"
    PREDEFINED_DATA_FILE = f"{FOOD_WASTE_FOLDER}/predefined_offers.csv"
    USER_DATA_FILE = f"{FOOD_WASTE_FOLDER}/user_offers.csv"

    # Load predefined data
    try:
        predefined_data = pd.read_csv(PREDEFINED_DATA_FILE)
    except FileNotFoundError:
        predefined_data = pd.DataFrame(columns=["name", "address", "food", "price", "magic_hours", "latitude", "longitude"])

    # Load user-submitted data
    try:
        user_data = pd.read_csv(USER_DATA_FILE)
    except FileNotFoundError:
        user_data = pd.DataFrame(columns=["name", "address", "food", "price", "magic_hours", "latitude", "longitude"])

    # Combine all data
    all_data = pd.concat([predefined_data, user_data], ignore_index=True)

    # Sidebar filters
    st.sidebar.header("Filters")
    food_type = st.sidebar.selectbox("Food Type", options=["All"] + list(all_data["food"].unique()))
    if food_type != "All":
        all_data = all_data[all_data["food"].str.contains(food_type, case=False)]

    # Main section: Map and list of offers
    st.title("Surplus Food Rescue App")
    st.write("Find and rescue surplus food near you. Help fight food waste!")

    # Display map with all offers
    m = folium.Map(location=[40.7128, -74.0060], zoom_start=13)
    for _, row in all_data.iterrows():
        if not pd.isnull(row["latitude"]) and not pd.isnull(row["longitude"]):
            folium.Marker(
                [row["latitude"], row["longitude"]],
                popup=f"{row['name']} - {row['food']} ({row['price']})\n{row['magic_hours']}"
            ).add_to(m)

    st_folium(m, width=700, height=500)

    # Display list of offers
    st.write("Available Options:")
    st.dataframe(all_data[["name", "address", "food", "price", "magic_hours"]])

    # Section: Add a new surplus food offer
    st.header("Add a Surplus Food Offer")
    with st.form("food_offer_form", clear_on_submit=True):
        name = st.text_input("Restaurant/Store Name")
        address = st.text_input("Address")
        food = st.text_input("Food Items (e.g., Vegan Salads, Desserts)")
        price = st.text_input("Price (e.g., $5)")
        magic_hours = st.text_input("Magic Hours (e.g., 6:00 PM - 8:00 PM)")
        latitude = None
        longitude = None

        submit = st.form_submit_button("Add Offer")

        if submit:
            # Geocode the address to get latitude and longitude
            try:
                location = geolocator.geocode(address)
                if location:
                    latitude = location.latitude
                    longitude = location.longitude
                else:
                    st.warning("Could not locate the address. Please check the address and try again.")
            except Exception as e:
                st.error(f"Error during geocoding: {e}")

            if latitude and longitude:
                # Save the new offer
                new_offer = {
                    "name": name,
                    "address": address,
                    "food": food,
                    "price": price,
                    "magic_hours": magic_hours,
                    "latitude": latitude,
                    "longitude": longitude
                }
                # Save to CSV
                new_offer_df = pd.DataFrame([new_offer])
                new_offer_df.to_csv(USER_DATA_FILE, mode='a', index=False, header=not pd.read_csv(USER_DATA_FILE).shape[0])
                st.success("Food offer added successfully!")
