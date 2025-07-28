import streamlit as st
import requests

# Dictionary of top 20 currencies and their symbols
# Source: Most traded currencies by value
CURRENCIES = {
    "USD": "United States Dollar",
    "EUR": "Euro",
    "JPY": "Japanese Yen",
    "GBP": "British Pound Sterling",
    "AUD": "Australian Dollar",
    "CAD": "Canadian Dollar",
    "CHF": "Swiss Franc",
    "CNY": "Chinese Yuan",
    "SEK": "Swedish Krona",
    "NZD": "New Zealand Dollar",
    "MXN": "Mexican Peso",
    "SGD": "Singapore Dollar",
    "HKD": "Hong Kong Dollar",
    "NOK": "Norwegian Krone",
    "KRW": "South Korean Won",
    "TRY": "Turkish Lira",
    "INR": "Indian Rupee",
    "BRL": "Brazilian Real",
    "ZAR": "South African Rand",
    "PKR": "Pakistani Rupee",
}

# --- API Communication ---
def get_conversion_rate(base_currency: str, target_currency: str) -> float | None:
    """
    Fetches the conversion rate between two currencies from the ExchangeRate-API.

    Args:
        base_currency: The code for the base currency (e.g., "USD").
        target_currency: The code for the target currency (e.g., "EUR").

    Returns:
        The conversion rate as a float, or None if the API call fails.
    """
    # NOTE: This is a demo API key. For a real application, get your own free key from https://www.exchangerate-api.com
    api_key = "1bc301d0ddba6757da42822f"
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_currency}/{target_currency}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        data = response.json()
        if data.get("result") == "success":
            return data.get("conversion_rate")
        else:
            st.error(f"API Error: {data.get('error-type', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to the currency API: {e}")
        return None
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")
        return None

# --- Streamlit UI ---
st.set_page_config(page_title="Currency Converter", page_icon="💱", layout="centered")

# --- Header ---
st.title("💱 Currency Converter")
st.markdown("Convert between the world's top currencies in real-time. Select your base and target currencies, enter an amount, and see the result instantly.")

# --- Main Interface ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Conversion")
    base_currency_code = st.selectbox(
        "From Currency",
        options=list(CURRENCIES.keys()),
        format_func=lambda code: f"{code} - {CURRENCIES[code]}",
        index=0 # Default to USD
    )

    target_currency_code = st.selectbox(
        "To Currency",
        options=list(CURRENCIES.keys()),
        format_func=lambda code: f"{code} - {CURRENCIES[code]}",
        index=19 # Default to PKR
    )

    amount = st.number_input("Amount", min_value=0.01, value=1.00, step=1.00)

# --- Conversion Logic and Display ---
if st.button("Convert", use_container_width=True):
    if base_currency_code and target_currency_code and amount > 0:
        with st.spinner(f"Fetching exchange rate for {base_currency_code} to {target_currency_code}..."):
            rate = get_conversion_rate(base_currency_code, target_currency_code)

        if rate is not None:
            converted_amount = amount * rate
            with col2:
                st.subheader("Result")
                st.metric(label=f"{base_currency_code} to {target_currency_code}", value=f"{converted_amount:,.4f} {target_currency_code}")
                st.info(f"1 {base_currency_code} = {rate:,.4f} {target_currency_code}")
        else:
            st.error("Could not retrieve the conversion rate. Please try again.")

# --- Footer ---
st.markdown("---")
st.markdown(
    """
    <div style="text-align: center; color: grey;">
        <p>Powered by <a href="https://www.exchangerate-api.com" target="_blank">ExchangeRate-API.com</a></p>
    </div>
    """,
    unsafe_allow_html=True
)
