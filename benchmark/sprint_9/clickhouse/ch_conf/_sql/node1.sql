CREATE DATABASE IF NOT EXISTS shard01;
CREATE DATABASE IF NOT EXISTS shard02;
CREATE DATABASE IF NOT EXISTS shard03;


CREATE TABLE IF NOT EXISTS shard01.views (
    user_id String,
    movie_id String,
    event UInt64,
    event_time DateTime DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard01}/views', '{replica01}')
ORDER BY event_time;

CREATE TABLE IF NOT EXISTS shard01.bookmarks (
    user_id String,
    bookmarks Array(String),
    event_time DateTime DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard01}/bookmarks', '{replica01}')
ORDER BY event_time;

CREATE TABLE IF NOT EXISTS shard01.ratings (
    movie_id String,
    likes Array(String),
    dislikes Array(String),
    rating Float32,
    event_time DateTime DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard01}/ratings', '{replica01}')
ORDER BY event_time;

CREATE TABLE IF NOT EXISTS shard01.reviews (
    user_id String,
    movie_id String,
    review String,
    movie_rating UInt64,
    likes Array(String),
    dislikes Array(String),
    review_rating Float32,
    event_time DateTime DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard01}/reviews', '{replica01}')
ORDER BY event_time;




CREATE TABLE IF NOT EXISTS shard03.views (
    user_id String,
    movie_id String,
    event UInt64,
    event_time DateTime DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard02}/views', '{replica02}')
ORDER BY event_time;

CREATE TABLE IF NOT EXISTS shard03.bookmarks (
    user_id String,
    bookmarks Array(String),
    event_time DateTime DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard02}/bookmarks', '{replica02}')
ORDER BY event_time;

CREATE TABLE IF NOT EXISTS shard03.ratings (
    movie_id String,
    likes Array(String),
    dislikes Array(String),
    rating Float32,
    event_time DateTime DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard02}/ratings', '{replica02}')
ORDER BY event_time;

CREATE TABLE IF NOT EXISTS shard03.reviews (
    user_id String,
    movie_id String,
    review String,
    movie_rating UInt64,
    likes Array(String),
    dislikes Array(String),
    review_rating Float32,
    event_time DateTime DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard02}/reviews', '{replica02}')
ORDER BY event_time;


CREATE TABLE IF NOT EXISTS default.views (
    user_id String,
    movie_id String,
    event UInt64,
    event_time DateTime DEFAULT now()
)
ENGINE = Distributed('company_cluster', '', views, rand());

CREATE TABLE IF NOT EXISTS default.bookmarks (
    user_id String,
    bookmarks Array(String),
    event_time DateTime DEFAULT now()
)
ENGINE = Distributed('company_cluster', '', bookmarks, rand());

CREATE TABLE IF NOT EXISTS default.ratings (
    movie_id String,
    likes Array(String),
    dislikes Array(String),
    rating Float32,
    event_time DateTime DEFAULT now()
)
ENGINE = Distributed('company_cluster', '', ratings, rand());

CREATE TABLE IF NOT EXISTS default.reviews (
    user_id String,
    movie_id String,
    review String,
    movie_rating UInt64,
    likes Array(String),
    dislikes Array(String),
    review_rating Float32,
    event_time DateTime DEFAULT now()
)
ENGINE = Distributed('company_cluster', '', reviews, rand());