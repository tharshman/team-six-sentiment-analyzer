"""Sentiment Analysis using Bag-of-Words approach."""

# Imports
import os
import shutil
import zipfile
import tempfile
import pandas as pd
from pdfminer.high_level import extract_text

temp_dir = tempfile.mkdtemp()


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


def process_zip(zip_file_path: str, scores: dict) -> None:
    """Process a zip file and return a list of files in it.

    Args:
        zip_file_path (str): Path to a zip file.
        scores (dict): Dictionary to store the scores.

    Returns:
        None
    """
    zip_file_name = os.path.basename(zip_file_path).replace(os.path.extsep + 'zip', '')
    extracted_path = os.path.join(temp_dir, zip_file_name)

    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:  # Open the zip file
        zip_file.extractall(extracted_path)  # Extract all files

    shutil.rmtree(extracted_path)


if __name__ == '__main__':
    current_file = __file__
    current_dir = os.path.dirname(current_file)
    data_path = os.path.join(current_dir, 'data')
    lmcd_file_path = os.path.join(current_dir, 'data', 'loughran_mcdonald')
    lmcd_file_path = os.path.abspath(lmcd_file_path)  # Optional: Converts to absolute path
    print(lmcd_file_path)

    # Load sentiment words
    word_file = os.path.join(lmcd_file_path, 'LoughranMcDonald_Positive.csv')
    positive_words = read_sentiment_files(word_file)  # Load positive words
    print(positive_words)

    word_file = os.path.join(lmcd_file_path, 'LoughranMcDonald_Negative.csv')
    negative_words = read_sentiment_files(word_file)  # Load negative words
    print(negative_words)

    score_dict = {}

    # Extract text from PDF file
    zip_files = os.listdir(data_path)
    for zip_file in zip_files:
        if zip_file.lower().endswith('.zip'):
            zip_file_path = os.path.join(data_path, zip_file)
            process_zip(zip_file_path, score_dict)

    print("Sentiment scores:")
    for zip_file_name, scores in score_dict.items():
        positive_count, negative_count, sentiment_score = scores
        print(f"File: {zip_file_name}")
        print(f"Sentiment score: {sentiment_score}")
        print(f"Positive word count: {positive_count}")
        print(f"Negative word count: {negative_count}")
        print("-" * 50)

        scores[zip_file_name] = (positive_count, negative_count, sentiment_score)