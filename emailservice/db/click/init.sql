CREATE TABLE default.user_events (
    id           UUID DEFAULT generateUUIDv4(),
    user_id      UUID,
    movie_id     UUID,
    event        String,
    frame        Int32,
    event_time   DateTime('Europe/Moscow')
) ENGINE = MergeTree() ORDER BY id;
