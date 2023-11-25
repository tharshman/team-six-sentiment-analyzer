from pdfminer.high_level import extract_text

def read_sentiment_files(file_path):
    """Load sentiment words from a CSV file.
    
    Args:
        file_path (str): Path to the CSV file.
        
    Returns:
        set: A set of words.
        
    """
    with open(file_path, 'r') as file:                      # Open the file
        return set(word.strip().lower() for word in file)   # Return a set of words


positive_words = read_sentiment_files('/Users/thomasharshman/LoughranMcDonald_Positive.csv')    # Load positive words
negative_words = read_sentiment_files('/Users/thomasharshman/LoughranMcDonald_Negative.csv')    # Load negative words

def analyze_sentiment(text):
    """Analyze the sentiment of the given text using bag-of-words approach.
    
    Args:
        text (str): Text to analyze.
        
    Returns:
        tuple: A tuple containing:
            str: Sentiment of the text.
            int: Number of positive words.
            int: Number of negative words.
            
    """
    
    words = text.lower().split()                                    # Tokenize the text

    positive_count = sum(word in positive_words for word in words)  # Count positive words
    negative_count = sum(word in negative_words for word in words)  # Count negative words

    if positive_count > negative_count:                             # Determine overall sentiment
        sentiment = "Positive"
    elif negative_count > positive_count:                           # Determine overall sentiment
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return sentiment, positive_count, negative_count                # Return sentiment and word counts
    
def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file using PDFMiner.
    
    Args:
        pdf_path (str): Path to a PDF file.
        
    Returns:
        str: Extracted text from PDF file.
        
    """
    text =  extract_text(pdf_path)                                  # Extract text from PDF file
    return text                                                     # Return extracted text

pdf_file_path = "/Users/thomasharshman/PycharmProjects/pythonProject/data/Apple keeps iPhone shipments steady despite 2023 turmoil.pdf"
text = extract_text_from_pdf(pdf_file_path)                         # Extract text from PDF file

sentiment, positive_count, negative_count = analyze_sentiment(text) # Analyze sentiment
print(f"The sentiment is: {sentiment}")                             # Print sentiment
print(f"Positive word count: {positive_count}")                     # Print positive word count
print(f"Negative word count: {negative_count}")                     # Print negative word count   
