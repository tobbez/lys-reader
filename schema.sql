DROP TABLE IF EXISTS lysr_feed_tag_assoc;
DROP TABLE IF EXISTS lysr_feed_tag;
DROP TABLE IF EXISTS lysr_feed_entry_status;
DROP TABLE IF EXISTS lysr_feed_entry;
DROP TABLE IF EXISTS lysr_user_feed;
DROP TABLE IF EXISTS lysr_feed;
DROP TABLE IF EXISTS lysr_user_settings;
DROP TABLE IF EXISTS lysr_user;


CREATE TABLE lysr_user (
	id BIGSERIAL PRIMARY KEY,
	email VARCHAR(255) UNIQUE,
	password VARCHAR(60)
);

CREATE TABLE lysr_user_settings (
	id BIGSERIAL PRIMARY KEY,
	"user" BIGINT NOT NULL REFERENCES lysr_user (id) ON DELETE CASCADE
);

CREATE TABLE lysr_feed (
	id BIGSERIAL PRIMARY KEY,
	url TEXT UNIQUE,
	last_check TIMESTAMP NOT NULL DEFAULT '-infinity',
	last_update TIMESTAMP NOT NULL DEFAULT '-infinity',
	update_interval INTERVAL NOT NULL DEFAULT '10m'
);

CREATE TABLE lysr_user_feed (
	id BIGSERIAL PRIMARY KEY,
	"user" BIGINT NOT NULL REFERENCES lysr_user (id) ON DELETE CASCADE,
	feed BIGINT NOT NULL REFERENCES lysr_feed (id) ON DELETE CASCADE,
	name TEXT NOT NULL
);

CREATE TABLE lysr_feed_entry (
	id BIGSERIAL PRIMARY KEY,
	feed BIGINT NOT NULL REFERENCES lysr_feed (id) ON DELETE CASCADE,
	title TEXT NOT NULL,
	guid TEXT NOT NULL,
	content TEXT NOT NULL
);

CREATE TABLE lysr_feed_entry_status (
	id BIGSERIAL PRIMARY KEY,
	"user" BIGINT NOT NULL REFERENCES lysr_user (id) ON DELETE CASCADE,
	feed_entry BIGINT NOT NULL REFERENCES lysr_feed_entry (id) ON DELETE CASCADE,
	read BOOLEAN,
	starred BOOLEAN
);


-- tags
CREATE TABLE lysr_feed_tag (
	id BIGSERIAL PRIMARY KEY,
	name TEXT
);

CREATE TABLE lysr_feed_tag_assoc (
	id BIGSERIAL PRIMARY KEY,
	tag BIGINT REFERENCES lysr_feed_tag (id) ON DELETE CASCADE,
	"user" BIGINT NOT NULL REFERENCES lysr_user (id) ON DELETE CASCADE,
	feed BIGINT REFERENCES lysr_user_feed (id) ON DELETE CASCADE
);
-- /tags
