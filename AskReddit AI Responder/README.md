# Askreddit AI Auto-Responder

### A one-off script that uses the PRAW Reddit API wrapper to webscrape Askreddit and answer questions using ChatGPT via OpenAI's API.

*Note: Deprecated thanks to Reddit's new API terms*

## Usage:
1. Replace API username, password, and key info with valid values.
    - *Optional: Review and edit blacklist*
    - *Note: Set posting=True (line 15) to publish response, otherwise response is only printed to CLI*
2. Execute the script.
3. Enter how many posts to evaluate when prompted.
    - *Note: If the post does not meet standards listed in blacklist, the post will be skipped without adding another to evaluate.*
4. For every suitable post evaluated, ChatGPT will answer the question and print or publish its response.

## Note:
- This is a one-off script made for fun so I'm not entirely satified with it and I don't expect you to be either. Such as:
    - Lazy handling for OpenAI request overflow error (sleep timer after every OpenAI API request)
    - Filtering for suitable Reddit posts could be so much better
    - Prepare ChatGPT prompt better than adding block of text before every inquiry.
    - And much more, just take a look!
