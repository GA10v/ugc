from enum import Enum


class EventEnum(str, Enum):
    views = 'views'
    rating = 'rating'


class ReviewReactionEnum(str, Enum):
    likes = 'likes'
    dislikes = 'dislikes'


class ReviewSortEnum(str, Enum):
    pub_date_asc = 'pub_date_asc'
    pub_date_desc = 'pub_date_desc'
    likes_count_asc = 'likes_count_asc'
    likes_count_desc = 'likes_count_desc'
    dislikes_count_asc = 'dislikes_count_asc'
    dislikes_count_desc = 'dislikes_count_desc'
    author_score_asc = 'author_score_asc'
    author_score_desc = 'author_score_desc'
