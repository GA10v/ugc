CREATE DATABASE IF NOT EXISTS shard01;
CREATE DATABASE IF NOT EXISTS shard02;
CREATE DATABASE IF NOT EXISTS shard03;


CREATE TABLE IF NOT EXISTS shard02.views (
    user_id String,
    movie_id String,
    event UInt64,
    event_time DateTime DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard01}/views', '{replica01}')
ORDER BY event_time;

CREATE TABLE IF NOT EXISTS shard01.views (
    user_id String,
    movie_id String,
    event UInt64,
    event_time DateTime DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard02}/views', '{replica02}')
ORDER BY event_time;

CREATE TABLE IF NOT EXISTS shard02.rating (
    user_id String,
    movie_id String,
    event UInt64,
    event_time DateTime DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard01}/rating', '{replica01}')
ORDER BY event_time;

CREATE TABLE IF NOT EXISTS shard01.rating (
    user_id String,
    movie_id String,
    event UInt64,
    event_time DateTime DEFAULT now()
)
ENGINE = ReplicatedMergeTree('/clickhouse/tables/{shard02}/rating', '{replica02}')
ORDER BY event_time;

CREATE TABLE IF NOT EXISTS default.views (
    user_id String,
    movie_id String,
    event UInt64,
    event_time DateTime DEFAULT now()
)
ENGINE = Distributed('company_cluster', '', views, rand());

CREATE TABLE IF NOT EXISTS default.rating (
    user_id String,
    movie_id String,
    event UInt64,
    event_time DateTime DEFAULT now()
)
ENGINE = Distributed('company_cluster', '', rating, rand());