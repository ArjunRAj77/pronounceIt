# ProunceIt : Word Pronunciation Finder

**Word Pronunciation Finder** is a simple Streamlit web application that allows users to input or upload a list of words and retrieve their phonetic pronunciations in a tabular format. The app also provides an option to download the generated table as a CSV file.

## Features

- **Manual Input**: Enter a list of words (separated by commas or new lines) directly into the application.
- **CSV Upload**: Upload a CSV file with a column named `Word` to process a large number of words at once.
- **Pronunciation Table**: Displays words and their corresponding pronunciations in a clean table.
- **Downloadable CSV**: Export the table of results as a CSV file for offline use.

## How It Works

The application uses the [pronouncing](https://pypi.org/project/pronouncing/) library, which fetches pronunciations from the CMU Pronouncing Dictionary. If a word is not found in the dictionary, the app will display "No pronunciation found."

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/word-pronunciation-finder.git
   cd word-pronunciation-finder

