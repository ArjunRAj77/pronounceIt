import streamlit as st
import pronouncing  # Install this library using 'pip install pronouncing'
import pandas as pd

def get_pronunciation(word):
    """Fetches the pronunciation of a word using the pronouncing library."""
    pronunciations = pronouncing.phones_for_word(word.lower())  # Convert to lowercase for consistency
    return pronunciations[0] if pronunciations else "No pronunciation found"

def main():
    st.title("Word Pronunciation Finder")
    st.write("Provide a list of words (manual input or upload a CSV) to get their pronunciations in a table format.")
    
    # Input method selection
    input_method = st.radio("Choose input method:", ["Manual Input", "Upload CSV"])

    if input_method == "Manual Input":
        # Manual text input
        words_input = st.text_area("Enter words (separated by commas or new lines):")
        if st.button("Get Pronunciations"):
            if words_input.strip():
                words = [word.strip() for word in words_input.replace("\n", ",").split(",")]
                generate_pronunciation_table(words)
            else:
                st.warning("Please provide a list of words.")
    
    elif input_method == "Upload CSV":
        # CSV upload
        uploaded_file = st.file_uploader("Upload a CSV file with a column named 'Word'", type=["csv"])
        if uploaded_file:
            try:
                df = pd.read_csv(uploaded_file)
                if "Word" not in df.columns:
                    st.error("The uploaded CSV must contain a column named 'Word'.")
                else:
                    words = df["Word"].tolist()
                    generate_pronunciation_table(words)
            except Exception as e:
                st.error(f"An error occurred while processing the file: {e}")

def generate_pronunciation_table(words):
    """Generates and displays the pronunciation table, with an option to download it."""
    pronunciations = [{"Word": word, "Pronunciation": get_pronunciation(word)} for word in words]
    result_df = pd.DataFrame(pronunciations)
    
    st.write("### Pronunciation Table")
    st.table(result_df)  # Display table in Streamlit
    
    # Provide download option
    csv = result_df.to_csv(index=False)
    st.download_button(
        label="Download Table as CSV",
        data=csv,
        file_name="pronunciation_table.csv",
        mime="text/csv",
    )

if __name__ == "__main__":
    main()
