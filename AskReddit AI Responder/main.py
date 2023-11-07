from time import sleep
import praw
import openai

openai.api_key = "OPENAI_API_KEY" # OpenAI key

reddit = praw.Reddit(  # creates Reddit instance
    client_id="ID",
    client_secret="SECRET",
    password="PASSWORD",
    user_agent="AGENT",
    username="USERNAME",
)

posting = False # True = publish comment to post, False = do not publish comment to post
reddit.read_only = False # sets read-only option to false (can comment/post)

blacklist = ["what", "pickup", "pick-up"] # list of words to avoid in reddit title (will skip post entirely)

sub = "askreddit" # subreddit used
lim = int(input("Posts to evaluate: ")) # prompts user for # of posts to evaluate


def setter(old_title):  # when called, returns reddit title with limiting factors
    return ("In a casual manner (as if talking on the internet) "
            "please answer the following question in 10 to 15 words: " + old_title)


subreddit = reddit.subreddit(sub)  # what subreddit is used
hot_subreddit = subreddit.hot(limit=lim)  # chooses the hot category

for post in hot_subreddit:  # parses through n posts in the subreddit
    title_list = post.title.lower().split()
    check = any(_ in blacklist for _ in title_list)
    if check:
        lim += 1
        continue
    else:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # what model is used, use GPT 3.5 'Turbo'
            messages=[
                {"role": "system", "content": ""},
                {"role": "user", "content": setter(post.title)}
            ]
        )

        gpt_response = completion.choices[0].message.content
        response_list = gpt_response.lower().split()

        if "ai" in response_list: # Evades "sorry, I'm an AI..." type exceptions
            sleep(20)  # timer to evade early quit from OpenAI for too many requests
            continue
        else:
            print(post.title)
            print(completion.choices[0].message.content)  # (should) print GPT response
            if posting:
                post.reply(gpt_response) # publishes ChatGPT response/comment to post
            sleep(20)  # timer to evade early quit from OpenAI for too many requests
            continue
