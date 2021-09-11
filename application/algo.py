from datetime import datetime 
from models import Card 

review_interval_easy = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
review_interval_med = [0, 1, 1, 1, 2, 2, 3, 4, 6, ]

def next_review(last_reviewed_date, review_interval):
    # scenarios: 
    # - no last reviewed date, meaning new card, review date is today
    # - last reviewed date + review interval < today then review
    # - last reviewed date + review interval = today then review
    # - last reviewed date + review interval = no review

    # need to take into account the number of reviews, how to incorporate 
    # when you're on the easy track and switch to the medium or hard track 
    # consider Anki or SuperMemo algorithm
    pass
