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
modal_weak = read_sentiment_files('/Users/thomasharshman/LoughranMcDonald_ModalWeak.csv')       # Load weak modal words
modal_strong = read_sentiment_files('/Users/thomasharshman/LoughranMcDonald_ModalStrong.csv')   # Load strong modal words
litigious = read_sentiment_files('/Users/thomasharshman/LoughranMcDonald_Litigious.csv')        # Load litigious words
uncertainty = read_sentiment_files('/Users/thomasharshman/LoughranMcDonald_Uncertainty.csv')    # Load uncertainty words

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
    weak_count = sum(word in modal_weak for word in words)          # Count weak modal words
    strong_count = sum(word in modal_strong for word in words)      # Count strong modal words
    litigious_count = sum(word in litigious for word in words)      # Count litigious words
    uncertainty_count = sum(word in uncertainty for word in words)  # Count uncertainty words

    if positive_count > negative_count:                             # Compare positive and negative word counts
        if strong_count > weak_count:                               # Compare strong and weak word counts
            sentiment = "Strong Positive"

    elif negative_count > positive_count:                           # Compare negative and positive word counts
        if weak_count > strong_count:                               # Compare weak and strong word counts
            sentiment = "Strong Negative"

    else:
        sentiment = "Neutral"
        
    if litigious_count >= 1:
        sentiment = "Check the legal background on this"
        
    if uncertainty_count >= 1:
        sentiment = "Seems to be some uncertantiy in this stock"                                       # Neutral sentiment
        
    return sentiment, positive_count, negative_count, strong_count, \
        weak_count, litigious_count, uncertainty_count

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file using PDFMiner.
    
    Args:
        pdf_path (str): Path to a PDF file.
        
    Returns:
        str: Extracted text from PDF file.
        
    """
    text =  extract_text(pdf_path)                                  # Extract text from PDF file
    return text                                                     # Return extracted text

pdf_file_path = "/Users/thomasharshman/PycharmProjects/pythonProject/data/Apple 's market value ends above $3.0 trillion for first time.pdf"
text = extract_text_from_pdf(pdf_file_path)                         # Extract text from PDF file

sentiment, positive_count, negative_count, strong_count, weak_count, litigious_count, uncertainty_count = analyze_sentiment(text) # Analyze sentiment
print(f"The sentiment is: {sentiment}")                             # Print sentiment
print(f"Positive word count: {positive_count}")                     # Print positive word count
print(f"Negative word count: {negative_count}")                     # Print negative word count
print(f'Positive to negative ratio: {positive_count/negative_count}') # Print positive to negative ratio
print(f"Strong word count: {strong_count}")                         # Print strong word count
print(f"Weak word count: {weak_count}")                             # Print weak word count
print(f'Strong to weak ratio: {strong_count/weak_count}')           # Print strong to weak ratio
print(f"Litigious word count: {litigious_count}")                   # Print litigious word count
print(f"Uncertainty word count: {uncertainty_count}")               # Print uncertainty word count
