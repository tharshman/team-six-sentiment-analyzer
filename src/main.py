"""Sentiment Analysis using Bag-of-Words approach."""

# Imports
import os
import shutil
import zipfile
import tempfile
import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from pdfminer.high_level import extract_text


def read_sentiment_files(file_path: str) -> set[str]:
    """Load sentiment words from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        set: A set of words.
    """
    with open(file_path, "r") as file:  # Open the file
        return set(word.strip().lower() for word in file)  # Return a set of words


def tokenize_text(document_text: str, exclude_stop_words: bool = True) -> list[str]:
    """Tokenize the given text.

    Args:
        document_text (str): Text to tokenize.
        exclude_stop_words (bool): Whether to exclude stop words or not.

    Returns:
        list: A list of words.
    """
    corpus = document_text.lower()
    tokens = word_tokenize(corpus)  # Tokenize the text
    if not exclude_stop_words:
        return tokens

    return [t for t in tokens if t not in stop_words]


def analyze_sentiment(document_text: str) -> float:
    """Analyze the sentiment of the given text using bag-of-words approach.

    Args:
        document_text (str): Text to analyze.

    Returns:
        tuple: A tuple containing:
            str: Sentiment of the text.
            int: Number of positive words.
            int: Number of negative words.
    """

    words = tokenize_text(document_text, global_exclude_stop_words)  # Tokenize the text
    word_cnt = len(words)  # Count the number of words

    positive_cnt = sum(word in positive_words for word in words)  # Count positive words
    negative_cnt = sum(word in negative_words for word in words)  # Count negative words

    sentiment_score = (positive_cnt - negative_cnt) / word_cnt

    return sentiment_score


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file using PDFMiner.

    Args:
        pdf_path (str): Path to a PDF file.

    Returns:
        str: Extracted text from PDF file.

    """
    document_text = extract_text(pdf_path)  # Extract text from PDF file
    return document_text  # Return extracted text


def process_zip(file_path: str, scores: dict) -> None:
    """Process a zip file and return a list of files in it.

    Args:
        file_path (str): Path to a zip file.
        scores (dict): Dictionary to store the scores.

    Returns:
        None
    """
    zip_file_name = os.path.basename(file_path).replace(os.path.extsep + "zip", "")
    stock_symbol = os.path.splitext(zip_file_name)[0]
    extracted_path = os.path.join(temp_dir, stock_symbol)

    score_list = []
    with zipfile.ZipFile(file_path, "r") as zip_archive:  # Open the zip file
        zip_archive.extractall(extracted_path)  # Extract all files

        for pdf_file in os.listdir(extracted_path):
            if pdf_file.endswith(".pdf"):
                pdf_file_path = os.path.join(extracted_path, pdf_file)
                text = extract_text_from_pdf(pdf_file_path)

                sentiment_score = analyze_sentiment(text)
                score_list.append(sentiment_score)

    # Calculate average sentiment score
    scores[stock_symbol] = sum(score_list) / len(score_list)


if __name__ == "__main__":
    # Load stopwords
    print("Loading stopwords...")
    nltk.download("stopwords")
    stop_words = stopwords.words("english")
    global_exclude_stop_words = False

    # Create a temporary directory
    print("Setup directories...")
    temp_dir = tempfile.mkdtemp()
    current_file = __file__
    current_dir = os.path.dirname(current_file)
    data_path = os.path.join(current_dir, "..", "data")
    lmcd_file_path = os.path.join(data_path, "loughran_mcdonald")
    portfolio_file_path = os.path.join(data_path, "portfolio")

    # Load sentiment words
    print("Loading sentiment words...")
    word_file = os.path.join(lmcd_file_path, "LoughranMcDonald_Positive.csv")
    positive_words = read_sentiment_files(word_file)  # Load positive words
    word_file = os.path.join(lmcd_file_path, "LoughranMcDonald_Negative.csv")
    negative_words = read_sentiment_files(word_file)  # Load negative words

    # Generate a dictionary representing the DOW 30 stocks
    dow_30 = {
        "AAPL": "Apple Inc.",
        "AMGN": "Amgen Inc.",
        "AXP": "American Express Company",
        "BA": "Boeing Company",
        "CAT": "Caterpillar Inc.",
        "CRM": "Salesforce Inc.",
        "CSCO": "Cisco Systems, Inc.",
        "CVX": "Chevron Corporation",
        "DIS": "Walt Disney Company",
        "DOW": "Dow Inc.",
        "GS": "Goldman Sachs Group Inc.",
        "HD": "Home Depot Inc.",
        "HON": "Honeywell International Inc.",
        "IBM": "International Business Machines Corporation",
        "INTC": "Intel Corporation",
        "JNJ": "Johnson & Johnson",
        "JPM": "JPMorgan Chase & Co.",
        "KO": "Coca-Cola Company",
        "MCD": "McDonald's Corporation",
        "MMM": "3M Company",
        "MRK": "Merck & Co., Inc.",
        "MSFT": "Microsoft Corporation",
        "NKE": "Nike, Inc.",
        "PG": "Procter & Gamble Company",
        "TRV": "Travelers Companies Inc.",
        "UNH": "UnitedHealth Group Incorporated",
        "V": "Visa Inc.",
        "VZ": "Verizon Communications Inc.",
        "WBA": "Walgreens Boots Alliance, Inc.",
        "WMT": "Walmart Inc."
    }

    # Initialize score dictionary
    print("Initializing score dictionary...")
    score_dict = {}

    # Extract text from PDF file
    print("Extracting zip files and reading text from PDF files...")
    zip_files = os.listdir(data_path)
    for zip_file in zip_files:
        if zip_file.lower().endswith(".zip"):
            stock_symbol = os.path.splitext(zip_file)[0]
            zip_file_path = os.path.join(data_path, zip_file)
            print(f"Processing documents for {dow_30[stock_symbol]}...")
            process_zip(zip_file_path, score_dict)

    # Print sentiment scores
    print("Top 5 Stocks based on sentiment scores:")
    df = pd.DataFrame.from_dict(score_dict, orient="index", columns=["Sentiment Score"])
    df = df.sort_values(by="Sentiment Score", ascending=False)
    df_top5 = df.head(5)
    print(df_top5)

    # Save df_top5 to a CSV file
    print("Saving top 5 stocks to a CSV file...")
    df_export = pd.DataFrame(index=df_top5.index, columns=["NAME", "AMOUNT_INVESTED"])
    df_export["NAME"] = df_top5.index.map(dow_30)
    df_export["AMOUNT_INVESTED"] = 200000
    df_export.to_csv(os.path.join(portfolio_file_path, "sentiment_portfolio.csv"),
                     index=True, header=True, index_label="TICKER")

    # Clean up temp folder
    print("Cleaning up...")
    shutil.rmtree(temp_dir)

    print("Please open process_portfolio.ipynb to continue.")
