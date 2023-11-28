"""Sentiment Analysis using Bag-of-Words approach."""

# Imports
import os
import shutil
import zipfile
import tempfile
import pandas as pd
from pdfminer.high_level import extract_text


def read_sentiment_files(file_path: str) -> set[str]:
    """Load sentiment words from a CSV file.

    Args:
        file_path (str): Path to the CSV file.

    Returns:
        set: A set of words.
    """
    with open(file_path, 'r') as file:  # Open the file
        return set(word.strip().lower() for word in file)  # Return a set of words


def analyze_sentiment(document_text: str) -> tuple[str, int, int, int, float]:
    """Analyze the sentiment of the given text using bag-of-words approach.

    Args:
        document_text (str): Text to analyze.

    Returns:
        tuple: A tuple containing:
            str: Sentiment of the text.
            int: Number of positive words.
            int: Number of negative words.
    """

    words = document_text.lower().split()  # Tokenize the text
    word_cnt: int = len(words)  # Count the number of words

    positive_cnt = sum(word in positive_words for word in words)  # Count positive words
    negative_cnt = sum(word in negative_words for word in words)  # Count negative words

    if positive_cnt > negative_cnt:  # Compare positive and negative word counts
        document_sentiment = "Positive"

    elif negative_cnt > positive_cnt:  # Compare negative and positive word counts
        document_sentiment = "Negative"

    else:
        document_sentiment = "Neutral"

    sentiment_score = (positive_cnt - negative_cnt) / word_cnt

    return document_sentiment, positive_cnt, negative_cnt, word_cnt, sentiment_score


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
    zip_file_name = os.path.basename(file_path).replace(os.path.extsep + 'zip', '')
    extracted_path = os.path.join(temp_dir, zip_file_name)

    score_list = []
    with zipfile.ZipFile(file_path, 'r') as zip_archive:  # Open the zip file
        zip_archive.extractall(extracted_path)  # Extract all files

        for pdf_file in os.listdir(extracted_path):
            if pdf_file.endswith(".pdf"):
                pdf_file_path = os.path.join(extracted_path, pdf_file)
                text = extract_text_from_pdf(pdf_file_path)
                sentiment, positive_count, negative_count, word_count, sentiment_score = analyze_sentiment(text)

                score_list.append(sentiment_score)

    # Calculate average sentiment score
    scores[zip_file_name] = sum(score_list) / len(score_list)

    shutil.rmtree(extracted_path)


if __name__ == '__main__':
    temp_dir = tempfile.mkdtemp()
    current_file = __file__
    current_dir = os.path.dirname(current_file)
    data_path = os.path.join(current_dir, '..', 'data')
    lmcd_file_path = os.path.join(data_path, 'loughran_mcdonald')
    lmcd_file_path = os.path.abspath(lmcd_file_path)  # Optional: Converts to absolute path

    # Load sentiment words
    word_file = os.path.join(lmcd_file_path, 'LoughranMcDonald_Positive.csv')
    positive_words = read_sentiment_files(word_file)  # Load positive words

    word_file = os.path.join(lmcd_file_path, 'LoughranMcDonald_Negative.csv')
    negative_words = read_sentiment_files(word_file)  # Load negative words

    score_dict = {}

    # Extract text from PDF file
    zip_files = os.listdir(data_path)
    for zip_file in zip_files:
        if zip_file.lower().endswith('.zip'):
            zip_file_path = os.path.join(data_path, zip_file)
            process_zip(zip_file_path, score_dict)

    print("Sentiment scores:")

    df = pd.DataFrame.from_dict(score_dict, orient='index', columns=['Sentiment Score'])
    df = df.sort_values(by='Sentiment Score', ascending=False)
    print(df.head(5))
