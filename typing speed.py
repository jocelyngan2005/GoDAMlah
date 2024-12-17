import time
import difflib

def speed_writing_test(test_phrase, accuracy_threshold=0.9):
    word_count = len(test_phrase.split())
    
    while True:
        response = input('Enter yes when you are ready: ')
        if response.lower() == 'yes':
            break
    
    print(f"Type the following phrase: {test_phrase}")
    t0 = time.time()
    user_input = input()
    t1 = time.time()
    
    # Calculate accuracy
    matcher = difflib.SequenceMatcher(None, test_phrase.lower(), user_input.lower())
    accuracy = matcher.ratio()
    
    # Time and speed calculations
    time_taken = t1 - t0
    words_per_minute = (word_count / time_taken) * 60
    
    # Authentication check
    if accuracy < accuracy_threshold:
        print("Authentication Failed")
    else:
        print("Authentication Successful")
    
    # Detailed results
    print(f"Words per Minute: {words_per_minute:.2f}")
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(f"Time Taken: {time_taken:.2f} seconds")

# Example usage
test_phrase = 'python is my favourite language'
speed_writing_test(test_phrase)