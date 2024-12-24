import streamlit as st
import pronouncing  # Install this library using 'pip install pronouncing'
import pandas as pd

def get_phonetic_spelling(word):
    """Fetches the phonetic spelling of a word in a human-readable format."""
    pronunciations = pronouncing.phones_for_word(word.lower())
    if not pronunciations:
        return "Phonetic spelling not found"
    
    # Simplify CMU phoneme notation into a readable phonetic spelling
    cmu_to_phonetic = {
        "AA": "ah", "AE": "a", "AH": "uh", "AO": "aw", "AW": "ow",
        "AY": "ai", "B": "b", "CH": "ch", "D": "d", "DH": "th",
        "EH": "e", "ER": "ur", "EY": "ay", "F": "f", "G": "g",
        "HH": "h", "IH": "i", "IY": "ee", "JH": "j", "K": "k",
        "L": "l", "M": "m", "N": "n", "NG": "ng", "OW": "oh",
        "OY": "oy", "P": "p", "R": "r", "S": "s", "SH": "sh",
        "T": "t", "TH": "th", "UH": "oo", "UW": "oo", "V": "v",
        "W": "w", "Y": "y", "Z": "z", "ZH": "zh"
    }

    # Custom replacements for better readability
    cluster_replacements = {
        "h y uw": "hyoo",
        "ah n": "uhn",
        "ah": "uh"
    }

    # Process the first available pronunciation
    pronunciation = pronunciations[0]
    phonemes = pronunciation.split()
    phonemes = [ph[:-1] if ph[-1].isdigit() else ph for ph in phonemes]  # Remove stress markers

    # Build the phonetic spelling
    phonetic_spelling = " ".join(cmu_to_phonetic.get(ph, ph.lower()) for ph in phonemes)
    
    # Apply custom replacements for clusters
    for cluster, replacement in cluster_replacements.items():
        phonetic_spelling = phonetic_spelling.replace(cluster, replacement)
    
    # Format the result (replace spaces with hyphens for readability)
    return phonetic_spelling.replace(" ", "-")

def main():
    st.title("PronounceIt - Phonetic spelling Generator")
    st.write("Provide a list of words (manual input or upload a CSV) to get their phonetic spellings in a table format.")
    
    # Input method selection
    input_method = st.radio("Choose input method:", ["Manual Input", "Upload CSV"])

    if input_method == "Manual Input":
        # Manual text input
        words_input = st.text_area("Enter words (separated by commas or new lines):")
        if st.button("Get Phonetic Spellings"):
            if words_input.strip():
                words = [word.strip() for word in words_input.replace("\n", ",").split(",")]
                generate_phonetic_table(words)
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
                    generate_phonetic_table(words)
            except Exception as e:
                st.error(f"An error occurred while processing the file: {e}")

def generate_phonetic_table(words):
    """Generates and displays the phonetic spelling table, with an option to download it as a .txt file."""
    phonetics = [{"Word": word, "Phonetic Spelling": get_phonetic_spelling(word)} for word in words]
    result_df = pd.DataFrame(phonetics)
    
    st.write("### Phonetic Spelling Table")
    st.table(result_df)  # Display table in Streamlit
    
    # Prepare the data for .txt download
    txt_content = "Word\tPhonetic Spelling\n"
    txt_content += "\n".join(f"{row['Word']}\t{row['Phonetic Spelling']}" for _, row in result_df.iterrows())
    
    # Provide download option for .txt
    st.download_button(
        label="Download Table as TXT",
        data=txt_content,
        file_name="phonetic_spelling_table.txt",
        mime="text/plain",
    )

if __name__ == "__main__":
    main()
