import streamlit as st
import pandas as pd
import math

def convert_units(value, from_unit, to_unit, category):
    conversion_factors = {
        "Length": {
            "Meter": 1, "Kilometer": 0.001, "Centimeter": 100, "Millimeter": 1000, "Inch": 39.3701,
            "Foot": 3.28084, "Yard": 1.09361, "Mile": 0.000621371
        },
        "Weight": {
            "Kilogram": 1, "Gram": 1000, "Milligram": 1000000, "Pound": 2.20462, "Ounce": 35.274
        },
        "Volume": {
            "Liter": 1, "Milliliter": 1000, "Gallon": 0.264172, "Quart": 1.05669, "Cup": 4.22675,
            "Fluid Ounce": 33.814
        },
        "Temperature": {
            "Celsius": {"Celsius": lambda x: x, 
                       "Fahrenheit": lambda x: (x * 9/5) + 32, 
                       "Kelvin": lambda x: x + 273.15},
            "Fahrenheit": {"Celsius": lambda x: (x - 32) * 5/9, 
                          "Fahrenheit": lambda x: x, 
                          "Kelvin": lambda x: (x - 32) * 5/9 + 273.15},
            "Kelvin": {"Celsius": lambda x: x - 273.15, 
                      "Fahrenheit": lambda x: (x - 273.15) * 9/5 + 32, 
                      "Kelvin": lambda x: x}
        }
    }
    
    if category == "Temperature":
        return conversion_factors[category][from_unit][to_unit](value)
    
    return value * (conversion_factors[category][to_unit] / conversion_factors[category][from_unit])

def format_result(value, precision=4):
    if math.isclose(value, int(value), abs_tol=1e-9):
        return str(int(value))
    else:
        return f"{value:.{precision}f}"

# Streamlit UI
st.set_page_config(
    page_title="Universal Unit Converter",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600&family=Orbitron:wght@400;500;600&display=swap');
        
        * {font-family: 'Poppins', sans-serif;}
        
        .stApp {
            background-color: #121212;
            color: #e0e0e0;
        }
        
        .main-header {
            font-family: 'Orbitron', sans-serif;
            text-align: center;
            color: #00ffff;
            margin-bottom: 2rem;
            text-shadow: 0 5px 10px rgba(0, 255, 255, 0.7);
            font-weight: 600;
            letter-spacing: 2px;
        }
        
        .card {
            background-color: #1e1e1e;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px #00ffff;
            border: 1px solid #333;
        }
        
        .result-card {
            background: linear-gradient(135deg, #222222 0%, #111111 100%);
            color: #00ffaa;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 0 30px rgba(0, 255, 170, 0.3);
            text-align: center;
            margin-top: 20px;
            border: 1px solid #00ffaa;
        }
        
        .category-btn {
            background-color: #333;
            border: 1px solid #555;
            color: white;
            border-radius: 5px;
            transition: all 0.3s ease;
        }
        
        .category-btn:hover {
            background-color: #444;
            border-color: #00ffff;
        }
        
        .history-table {
            margin-top: 20px;
        }
        
        /* Button styling */
        .stButton>button {
            background-color: #212121;
            color: #00ffff;
            border: 1px solid #00ffff;
            border-radius: 5px;
            padding: 8px 16px;
            font-weight: 500;
            width: 100%;
            transition: all 0.3s ease;
            text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
        }
        
        .stButton>button:hover {
            background-color: #212121;
            color: #121212;
            border-color: #00ffff;
            box-shadow: 0 0 15px rgba(0, 255, 255, 0.5);
        }
        
        /* Convert button specific */
        [data-testid="stHorizontalBlock"] > div:nth-child(1) [data-testid="baseButton-secondary"] {
            background-color: #212121;
            color: #00ffaa;
            border: 1px solid #00ffaa;
            text-shadow: 0 0 10px rgba(0, 255, 170, 0.3);
        }
        
        [data-testid="stHorizontalBlock"] > div:nth-child(1) [data-testid="baseButton-secondary"]:hover {
            background-color: #00ffaa;
            color: #121212;
            box-shadow: 0 0 15px rgba(0, 255, 170, 0.5);
            border-color: #00ffff;
        }
        
        /* Input field styling */
        .stSelectbox>div>div, .stNumberInput>div>div {
            background-color: #292929;
            border: 1px solid #444;
            border-radius: 5px;
            color: white;
        }
        
        /* For info/success/warning/error boxes */
        .stAlert {
            background-color: rgba(0, 255, 255, 0.05);
            border: 1px solid rgba(0, 255, 255, 0.2);
            color: #e0e0e0;
        }
        
        /* DataFrame styling */
        [data-testid="stDataFrame"] {
            background-color: #1e1e1e;
            border: 1px solid #333;
            border-radius: 5px;
            padding: 10px;
        }
        
        [data-testid="stDataFrame"] th {
            background-color: #252525;
            color: #00ffff !important;
            font-weight: 600;
        }
        
        [data-testid="stDataFrame"] td {
            color: #e0e0e0 !important;
        }
        
        /* Separator lines */
        hr {
            border-color: #333;
        }
        
        /* Glowing text for results */
        .result-value {
            color: #00ffaa;
            font-weight: bold;
            font-family: 'Orbitron', sans-serif;
            font-size: 1.8rem;
            text-shadow: 0 0 15px rgba(0, 255, 170, 0.6);
            letter-spacing: 1px;
        }
        
        /* Subheaders */
        h2, h3, .stSubheader {
            color: #e0e0e0 !important;
            text-shadow: 0 0 10px rgba(0, 255, 255, 0.3);
            font-weight: 500;
            letter-spacing: 1px;
        }
        
        /* Text content */
        p, .stMarkdown {
            color: #e0e0e0;
            text-shadow: 0 0 1px rgba(255, 255, 255, 0.1);
        }
        
        /* Info bullets */
        .stMarkdown ul li, .stMarkdown ol li {
            color: #e0e0e0;
            margin-bottom: 5px;
        }
        
        /* Footer styling */
        .footer {
            text-align: center;
            margin-top: 30px;
            color: #888;
            font-size: 0.8rem;
            text-shadow: 0 0 5px rgba(0, 255, 255, 0.2);
            letter-spacing: 2px;
        }
        
        /* Improve sidebar styling */
        .css-6qob1r {
            background-color: #161616 !important;
            border-right: 1px solid #333 !important;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for conversion history
if 'history' not in st.session_state:
    st.session_state.history = []

# Header
st.markdown('<h1 class="main-header">✨ UNIVERSAL UNIT CONVERTER</h1>', unsafe_allow_html=True)

# Main layout
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    
    # Category selection with custom buttons
    st.subheader("📊 Select Category")
    
    categories = ["Length", "Weight", "Volume", "Temperature"]
    category_cols = st.columns(len(categories))
    
    category = st.session_state.get('category', 'Length')
    
    for i, cat in enumerate(categories):
        with category_cols[i]:
            if st.button(f"{cat}", key=f"btn_{cat}", help=f"Convert {cat.lower()} units"):
                category = cat
                st.session_state.category = cat
    
    # Unit options dictionary
    unit_options = {
        "Length": ["Meter", "Kilometer", "Centimeter", "Millimeter", "Inch", "Foot", "Yard", "Mile"],
        "Weight": ["Kilogram", "Gram", "Milligram", "Pound", "Ounce"],
        "Volume": ["Liter", "Milliliter", "Gallon", "Quart", "Cup", "Fluid Ounce"],
        "Temperature": ["Celsius", "Fahrenheit", "Kelvin"]
    }
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.subheader("🔄 Convert Units")
    
    # Input columns
    input_col1, input_col2 = st.columns(2)
    
    with input_col1:
        value = st.number_input("Enter value:", value=1.0, format="%.6f", step=0.1)
        from_unit = st.selectbox("From Unit:", unit_options[category])
    
    with input_col2:
        st.write("##")  # Spacer for alignment
        to_unit = st.selectbox("To Unit:", unit_options[category])
    
    # Swap button
    if st.button("↔️ Swap Units"):
        temp = from_unit
        from_unit = to_unit
        to_unit = temp
    
    # Convert button
    convert_cols = st.columns([2, 1])
    with convert_cols[0]:
        convert_button = st.button("🔄 Convert", use_container_width=True)
    
    if convert_button:
        try:
            result = convert_units(value, from_unit, to_unit, category)
            formatted_result = format_result(result)
            
            # Save to history
            st.session_state.history.append({
                "Category": category,
                "Value": value,
                "From": from_unit,
                "To": to_unit,
                "Result": formatted_result
            })
            
            # Display result
            st.markdown(f"""
                <div class="result-card">
                    <p>Result:</p>
                    <h2 class="result-value">{value} {from_unit} = {formatted_result} {to_unit}</h2>
                </div>
            """, unsafe_allow_html=True)
            
        except Exception as e:
            st.error(f"Conversion error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Unit information card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📚 Unit Information")
    
    unit_info = {
        "Length": "Length is a measure of distance. Common units include meters, feet, and miles.",
        "Weight": "Weight measures the heaviness of an object. Common units include kilograms, grams, and pounds.",
        "Volume": "Volume measures the amount of space occupied by a substance. Common units include liters, gallons, and cups.",
        "Temperature": "Temperature measures the degree of heat. Common scales include Celsius, Fahrenheit, and Kelvin."
    }
    
    st.info(unit_info[category])
    
    # Common conversions
    st.subheader("✨ Common Conversions")
    
    common_conversions = {
        "Length": [
            {"from": "Meter", "to": "Feet", "ratio": "1 meter = 3.28084 feet"},
            {"from": "Kilometer", "to": "Mile", "ratio": "1 kilometer = 0.621371 miles"},
            {"from": "Inch", "to": "Centimeter", "ratio": "1 inch = 2.54 centimeters"}
        ],
        "Weight": [
            {"from": "Kilogram", "to": "Pound", "ratio": "1 kilogram = 2.20462 pounds"},
            {"from": "Ounce", "to": "Gram", "ratio": "1 ounce = 28.3495 grams"}
        ],
        "Volume": [
            {"from": "Liter", "to": "Gallon", "ratio": "1 liter = 0.264172 gallons"},
            {"from": "Cup", "to": "Milliliter", "ratio": "1 cup = 236.588 milliliters"}
        ],
        "Temperature": [
            {"from": "Celsius", "to": "Fahrenheit", "ratio": "0°C = 32°F, 100°C = 212°F"},
            {"from": "Celsius", "to": "Kelvin", "ratio": "0°C = 273.15K"}
        ]
    }
    
    for conv in common_conversions[category]:
        st.write(f"• {conv['ratio']}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Conversion History
if st.session_state.history:
    st.markdown('<div class="card history-table">', unsafe_allow_html=True)
    st.subheader("📜 Conversion History")
    
    history_df = pd.DataFrame(st.session_state.history)
    st.dataframe(history_df, use_container_width=True)
    
    if st.button("Clear History"):
        st.session_state.history = []
        st.experimental_rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class="footer">
    <p>MADE WITH 💻 | UNIVERSAL UNIT CONVERTER | © 2025</p>
</div>
""", unsafe_allow_html=True)