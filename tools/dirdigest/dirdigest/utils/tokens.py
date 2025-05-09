# dirdigest/utils/tokens.py

# A very basic heuristic: average token length is around 4 characters for English text/code.
# This is a rough approximation and can vary significantly.
# For more accurate counts, a proper tokenizer (e.g., tiktoken for OpenAI) would be needed.
CHARS_PER_TOKEN_ESTIMATE = 4

def approximate_token_count(text: str) -> int:
    """
    Estimates the number of tokens in a given text based on character count.

    :param text: The text to analyze.
    :return: An approximate token count.
    """
    if not text:
        return 0
    return len(text) // CHARS_PER_TOKEN_ESTIMATE