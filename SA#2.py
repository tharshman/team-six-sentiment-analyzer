"""Sentiment Analysis using Bag-of-Words approach."""

# Imports
import os
import zipfile
from pdfminer.high_level import extract_text


def read_sentiment_files(file_path: str) -> set[str]:
    """Load sentiment words from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        set: A set of words.
    """
    with open(file_path, 'r') as file:                      # Open the file
        return set(word.strip().lower() for word in file)   # Return a set of words


def analyze_sentiment(document_text: str) -> tuple[str, int, int, int, int, int, int]:
    """Analyze the sentiment of the given text using bag-of-words approach.
    
    Args:
        document_text (str): Text to analyze.
        
    Returns:
        tuple: A tuple containing:
            str: Sentiment of the text.
            int: Number of positive words.
            int: Number of negative words.
    """
    
    words = document_text.lower().split()                           # Tokenize the text

    positive_cnt = sum(word in positive_words for word in words)  # Count positive words
    negative_cnt = sum(word in negative_words for word in words)  # Count negative words
    weak_cnt = sum(word in modal_weak for word in words)          # Count weak modal words
    strong_cnt = sum(word in modal_strong for word in words)      # Count strong modal words
    litigious_cnt = sum(word in litigious for word in words)      # Count litigious words
    uncertainty_cnt = sum(word in uncertainty for word in words)  # Count uncertainty words

    document_sentiment = "Neutral"                                           # Default sentiment
    if positive_cnt > negative_cnt:                             # Compare positive and negative word counts
        if strong_cnt > weak_cnt:                               # Compare strong and weak word counts
            document_sentiment = "Strong Positive"

    elif negative_cnt > positive_cnt:                           # Compare negative and positive word counts
        if weak_cnt > strong_cnt:                               # Compare weak and strong word counts
            document_sentiment = "Strong Negative"

    else:
        document_sentiment = "Neutral"
        
    if litigious_cnt >= 1:
        document_sentiment = "Check the legal background on this"
        
    if uncertainty_cnt >= 1:
        document_sentiment = "Seems to be some uncertainty in this stock"   # Neutral sentiment
        
    return document_sentiment, positive_cnt, negative_cnt, strong_cnt, \
        weak_cnt, litigious_cnt, uncertainty_cnt


def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract text from PDF file using PDFMiner.
    
    Args:
        pdf_path (str): Path to a PDF file.
        
    Returns:
        str: Extracted text from PDF file.
        
    """
    document_text = extract_text(pdf_path)                                  # Extract text from PDF file
    return document_text                                                    # Return extracted text


def process_zip(zip_file_path: str) -> None:
    """Process a zip file and return a list of files in it.

    Args:
        zip_file_path (str): Path to a zip file.

    Returns:
        None
    """
    with zipfile.ZipFile(zip_file_path, 'r') as zip_file:                    # Open the zip file
        tmp_path = os.path.join(os.path.dirname(zip_file_path), 'temp')                         # Temporary path
        zip_file.extractall(tmp_path)                                               # Extract all files
        for pdf_file in os.listdir(tmp_path):
            if pdf_file.endswith(".pdf"):
                pdf_file_path = os.path.join("temp", pdf_file)
                text = extract_text_from_pdf(pdf_file_path)
                sentiment, positive_count, negative_count, strong_count, weak_count, \
                    litigious_count, uncertainty_count = analyze_sentiment(text)

                if weak_count == 0:
                    weak_count = 1

                print(f"File: {pdf_file}")  # Print file name
                print(f"The sentiment is: {sentiment}")  # Print sentiment
                print(f"Positive word count: {positive_count}")  # Print positive word count
                print(f"Negative word count: {negative_count}")
                print(f'Positive to negative ratio: {positive_count / negative_count}')
                print(f"Strong word count: {strong_count}")
                print(f"Weak word count: {weak_count}")
                print(f'Strong to weak ratio: {strong_count / weak_count}')
                print(f"Litigious word count: {litigious_count}")
                print(f"Uncertainty word count: {uncertainty_count}")
                print("=" * 50)  # Print a separator

    for pdf_file in os.listdir(tmp_path):
        print(f"Removing temporary file: {pdf_file}")
        os.remove(pdf_file)


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

    word_file = os.path.join(lmcd_file_path, 'LoughranMcDonald_Negative.csv')
    negative_words = read_sentiment_files(word_file)  # Load negative words

    word_file = os.path.join(lmcd_file_path, 'LoughranMcDonald_ModalWeak.csv')
    modal_weak = read_sentiment_files(word_file)  # Load weak modal words

    word_file = os.path.join(lmcd_file_path, 'LoughranMcDonald_ModalStrong.csv')
    modal_strong = read_sentiment_files(word_file)  # Load strong modal words

    word_file = os.path.join(lmcd_file_path, 'LoughranMcDonald_Litigious.csv')
    litigious = read_sentiment_files(word_file)  # Load litigious words

    word_file = os.path.join(lmcd_file_path, 'LoughranMcDonald_Uncertainty.csv')
    uncertainty = read_sentiment_files(word_file)  # Load uncertainty words

    # Extract text from PDF file
    apple_zip = os.path.join(data_path, 'AAPL.zip')
    process_zip(apple_zip)

