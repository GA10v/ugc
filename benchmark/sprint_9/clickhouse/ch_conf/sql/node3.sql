CREATE DATABASE IF NOT EXISTS shard01;
CREATE DATABASE IF NOT EXISTS shard02;
CREATE DATABASE IF NOT EXISTS shard03;


CREATE TABLE IF NOT EXISTS shard02.reviews (
    user_id String,
    movie_id String,
    rating UInt64,
    event_time DateTime DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard01}/reviews', '{replica01}')
ORDER BY event_time;



CREATE TABLE IF NOT EXISTS shard01.reviews (
    user_id String,
    movie_id String,
    rating UInt64,
    event_time DateTime DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard02}/reviews', '{replica02}')
ORDER BY event_time;




CREATE TABLE IF NOT EXISTS default.reviews ON CLUSTER company_cluster (
    user_id String,
    movie_id String,
    rating UInt64,
    event_time DateTime DEFAULT now()
)
ENGINE = Distributed('company_cluster', '', reviews, rand());

