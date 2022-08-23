DROP DATABASE IF EXISTS movies;
CREATE DATABASE movies;
\c movies

CREATE SCHEMA IF NOT EXISTS content;
ALTER SCHEMA content OWNER TO postgres;
SET search_path TO content, public;

BEGIN;

CREATE TYPE content.filmwork_person_role AS ENUM (
    'actor',
    'director',
    'writer'
);
ALTER TYPE content.filmwork_person_role OWNER TO postgres;

CREATE TYPE content.filmwork_type AS ENUM (
    'film',
    'series'
);
ALTER TYPE content.filmwork_type OWNER TO postgres;

SET default_tablespace = '';
SET default_table_access_method = heap;

CREATE TABLE content.filmwork (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    uuid uuid NOT NULL,
    title character varying(255) NOT NULL,
    plot text,
    creation_date date,
    certificate text,
    file_path text,
    rating double precision,
    type content.filmwork_type NOT NULL,
    is_removed boolean DEFAULT false NOT NULL
);


ALTER TABLE content.filmwork OWNER TO postgres;

CREATE TABLE content.filmwork_genre (
    id integer NOT NULL,
    filmwork_id uuid NOT NULL,
    genre_id uuid NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    is_removed boolean DEFAULT false NOT NULL
);
ALTER TABLE content.filmwork_genre OWNER TO postgres;

CREATE SEQUENCE content.filmwork_genre_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER TABLE content.filmwork_genre_id_seq OWNER TO postgres;
ALTER SEQUENCE content.filmwork_genre_id_seq OWNED BY content.filmwork_genre.id;

CREATE TABLE content.filmwork_person (
    id uuid NOT NULL,
    role content.filmwork_person_role NOT NULL,
    filmwork_id uuid NOT NULL,
    person_id uuid NOT NULL,
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    is_removed boolean DEFAULT false NOT NULL
);
ALTER TABLE content.filmwork_person OWNER TO postgres;

CREATE TABLE content.genre (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    uuid uuid NOT NULL,
    name text NOT NULL,
    description text NOT NULL,
    is_removed boolean DEFAULT false NOT NULL
);
ALTER TABLE content.genre OWNER TO postgres;

CREATE TABLE content.person (
    created timestamp with time zone NOT NULL,
    modified timestamp with time zone NOT NULL,
    uuid uuid NOT NULL,
    first_name varchar(255) NOT NULL,
    last_name varchar(255),
    is_removed boolean DEFAULT false NOT NULL
);
ALTER TABLE content.person OWNER TO postgres;

-- insert values

-- filmwork

COPY content.filmwork
FROM '/docker-entrypoint-initdb.d/csv/filmwork.csv'
DELIMITER ',' CSV HEADER;

-- filmwork_genre

COPY content.filmwork_genre
FROM '/docker-entrypoint-initdb.d/csv/filmwork_genre.csv'
DELIMITER ',' CSV HEADER;

-- filmwork_person

COPY content.filmwork_person
FROM '/docker-entrypoint-initdb.d/csv/filmwork_person.csv'
DELIMITER ',' CSV HEADER;

-- genre

COPY content.genre
FROM '/docker-entrypoint-initdb.d/csv/genre.csv'
DELIMITER ',' CSV HEADER;

-- person

COPY content.person
FROM '/docker-entrypoint-initdb.d/csv/person.csv'
DELIMITER ',' CSV HEADER;


-- create constraints

SELECT pg_catalog.setval('content.filmwork_genre_id_seq', 4462, true);

ALTER TABLE ONLY content.filmwork_genre
    ADD CONSTRAINT filmwork_genre_filmwork_id_genre_id_5de454eb_uniq UNIQUE (filmwork_id, genre_id);

ALTER TABLE ONLY content.filmwork_genre
    ADD CONSTRAINT filmwork_genre_pkey PRIMARY KEY (id);

ALTER TABLE ONLY content.filmwork_person
    ADD CONSTRAINT filmwork_person_person_id_filmwork_id_role_3e531424_uniq UNIQUE (person_id, filmwork_id, role);

ALTER TABLE ONLY content.filmwork_person
    ADD CONSTRAINT filmwork_person_pkey PRIMARY KEY (id);

ALTER TABLE ONLY content.filmwork
    ADD CONSTRAINT filmwork_pkey PRIMARY KEY (uuid);

ALTER TABLE ONLY content.genre
    ADD CONSTRAINT genre_name_key UNIQUE (name);

ALTER TABLE ONLY content.genre
    ADD CONSTRAINT genre_pkey PRIMARY KEY (uuid);

ALTER TABLE ONLY content.person
    ADD CONSTRAINT person_first_name_last_name_8fb75a42_uniq UNIQUE (first_name, last_name);

ALTER TABLE ONLY content.person
    ADD CONSTRAINT person_pkey PRIMARY KEY (uuid);

CREATE INDEX filmwork_genre_filmwork_id_e6bc4455 ON content.filmwork_genre USING btree (filmwork_id);

CREATE INDEX filmwork_genre_genre_id_b329aef2 ON content.filmwork_genre USING btree (genre_id);

CREATE INDEX filmwork_idx ON content.filmwork USING btree (title, creation_date);

CREATE INDEX filmwork_modifie_1a6953_idx ON content.filmwork USING btree (modified);

CREATE INDEX filmwork_person_filmwork_id_d9748b7a ON content.filmwork_person USING btree (filmwork_id);

CREATE INDEX filmwork_person_person_id_0aea76a5 ON content.filmwork_person USING btree (person_id);

CREATE INDEX genre_modifie_148664_idx ON content.genre USING btree (modified);

CREATE INDEX genre_name_4b473646_like ON content.genre USING btree (name text_pattern_ops);

CREATE INDEX person_modifie_471683_idx ON content.person USING btree (modified);

ALTER TABLE ONLY content.filmwork_genre
    ADD CONSTRAINT filmwork_genre_filmwork_id_e6bc4455_fk_filmwork_id FOREIGN KEY (filmwork_id) REFERENCES content.filmwork(uuid) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY content.filmwork_genre
    ADD CONSTRAINT filmwork_genre_genre_id_b329aef2_fk_genre_id FOREIGN KEY (genre_id) REFERENCES content.genre(uuid) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY content.filmwork_person
    ADD CONSTRAINT filmwork_person_filmwork_id_d9748b7a_fk_filmwork_id FOREIGN KEY (filmwork_id) REFERENCES content.filmwork(uuid) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY content.filmwork_person
    ADD CONSTRAINT filmwork_person_person_id_0aea76a5_fk_person_id FOREIGN KEY (person_id) REFERENCES content.person(uuid) DEFERRABLE INITIALLY DEFERRED;
COMMIT;


-- auth database

DROP DATABASE IF EXISTS auth;
CREATE DATABASE auth;
\c auth

BEGIN;

CREATE TABLE public."UserRole" (
    id uuid NOT NULL,
    "userId" uuid,
    "roleId" uuid
);


ALTER TABLE public."UserRole" OWNER TO "postgres";

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO "postgres";

CREATE TABLE public.google_user (
    id uuid NOT NULL,
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL,
    email character varying NOT NULL,
    first_name character varying,
    last_name character varying,
    user_id uuid NOT NULL
);


ALTER TABLE public.google_user OWNER TO "postgres";

CREATE TABLE public.login_history_master (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    user_agent character varying NOT NULL,
    ip_addr character varying,
    "timestamp" timestamp without time zone NOT NULL,
    user_device_type text NOT NULL
)
PARTITION BY LIST (user_device_type);


ALTER TABLE public.login_history_master OWNER TO "postgres";

CREATE TABLE public.login_history_mobile (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    user_agent character varying NOT NULL,
    ip_addr character varying,
    "timestamp" timestamp without time zone NOT NULL,
    user_device_type text NOT NULL
);
ALTER TABLE ONLY public.login_history_master ATTACH PARTITION public.login_history_mobile FOR VALUES IN ('mobile');


ALTER TABLE public.login_history_mobile OWNER TO "postgres";

CREATE TABLE public.login_history_smart (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    user_agent character varying NOT NULL,
    ip_addr character varying,
    "timestamp" timestamp without time zone NOT NULL,
    user_device_type text NOT NULL
);
ALTER TABLE ONLY public.login_history_master ATTACH PARTITION public.login_history_smart FOR VALUES IN ('smart');


ALTER TABLE public.login_history_smart OWNER TO "postgres";

CREATE TABLE public.login_history_web (
    id uuid NOT NULL,
    user_id uuid NOT NULL,
    user_agent character varying NOT NULL,
    ip_addr character varying,
    "timestamp" timestamp without time zone NOT NULL,
    user_device_type text NOT NULL
);
ALTER TABLE ONLY public.login_history_master ATTACH PARTITION public.login_history_web FOR VALUES IN ('web');


ALTER TABLE public.login_history_web OWNER TO "postgres";

CREATE TABLE public.refresh_token (
    id uuid NOT NULL,
    token character varying NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.refresh_token OWNER TO "postgres";

CREATE TABLE public.role (
    id uuid NOT NULL,
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL,
    name character varying NOT NULL,
    permissions integer,
    "default" boolean
);


ALTER TABLE public.role OWNER TO "postgres";

CREATE TABLE public."user" (
    id uuid NOT NULL,
    created timestamp without time zone NOT NULL,
    updated timestamp without time zone NOT NULL,
    username character varying NOT NULL,
    password_hash character varying NOT NULL,
    first_name character varying,
    last_name character varying,
    email character varying,
    is_verified boolean,
    totp_secret character varying,
    is_active_2fa boolean
);


ALTER TABLE public."user" OWNER TO "postgres";

COPY public.alembic_version (version_num) FROM stdin;
ec1b9d5dd8d2
\.

COPY public.role (id, created, updated, name, permissions, "default") FROM stdin;
a61846cf-8882-4213-a471-f763000d114c	2022-01-23 14:05:32.084682	2022-01-23 14:05:32.084687	user	1	t
a79b94c0-d862-41d4-9f8d-1897309325e2	2022-01-23 14:05:32.084697	2022-01-23 14:05:32.084698	premium	3	f
1b6f37fa-7c90-4863-bf86-6a6aaa779880	2022-01-23 14:05:32.084706	2022-01-23 14:05:32.084708	superuser	7	f
\.

ALTER TABLE ONLY public."UserRole"
    ADD CONSTRAINT "UserRole_id_key" UNIQUE (id);

ALTER TABLE ONLY public."UserRole"
    ADD CONSTRAINT "UserRole_pkey" PRIMARY KEY (id);

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);

ALTER TABLE ONLY public.google_user
    ADD CONSTRAINT google_user_email_key UNIQUE (email);

ALTER TABLE ONLY public.google_user
    ADD CONSTRAINT google_user_id_key UNIQUE (id);

ALTER TABLE ONLY public.google_user
    ADD CONSTRAINT google_user_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.google_user
    ADD CONSTRAINT google_user_user_id_key UNIQUE (user_id);

ALTER TABLE ONLY public.login_history_master
    ADD CONSTRAINT login_history_master_pkey PRIMARY KEY (id, user_device_type);

ALTER TABLE ONLY public.login_history_mobile
    ADD CONSTRAINT login_history_mobile_pkey PRIMARY KEY (id, user_device_type);

ALTER TABLE ONLY public.login_history_smart
    ADD CONSTRAINT login_history_smart_pkey PRIMARY KEY (id, user_device_type);

ALTER TABLE ONLY public.login_history_web
    ADD CONSTRAINT login_history_web_pkey PRIMARY KEY (id, user_device_type);

ALTER TABLE ONLY public.refresh_token
    ADD CONSTRAINT refresh_token_id_key UNIQUE (id);

ALTER TABLE ONLY public.refresh_token
    ADD CONSTRAINT refresh_token_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.refresh_token
    ADD CONSTRAINT refresh_token_token_key UNIQUE (token);

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_id_key UNIQUE (id);

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_name_key UNIQUE (name);

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_id_key UNIQUE (id);

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);

ALTER INDEX public.login_history_master_pkey ATTACH PARTITION public.login_history_mobile_pkey;

ALTER INDEX public.login_history_master_pkey ATTACH PARTITION public.login_history_smart_pkey;

ALTER INDEX public.login_history_master_pkey ATTACH PARTITION public.login_history_web_pkey;

ALTER TABLE ONLY public."UserRole"
    ADD CONSTRAINT "UserRole_roleId_fkey" FOREIGN KEY ("roleId") REFERENCES public.role(id);

ALTER TABLE ONLY public."UserRole"
    ADD CONSTRAINT "UserRole_userId_fkey" FOREIGN KEY ("userId") REFERENCES public."user"(id);

ALTER TABLE ONLY public.google_user
    ADD CONSTRAINT google_user_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);

ALTER TABLE public.login_history_master
    ADD CONSTRAINT login_history_master_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);

ALTER TABLE ONLY public.refresh_token
    ADD CONSTRAINT refresh_token_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);
COMMIT;



-- auth database

DROP DATABASE IF EXISTS notifications;
CREATE DATABASE notifications;
\c notifications

BEGIN;

CREATE TABLE public.scheduled_notification (
    id uuid NOT NULL,
    schedule character varying(100) NOT NULL,
    template_id uuid NOT NULL,
    data json,
    enabled boolean DEFAULT true NOT NULL,
    last_update_time timestamp DEFAULT now() NOT NULL
);


ALTER TABLE public.scheduled_notification OWNER TO "postgres";

CREATE TABLE public.scheduled_notification_user (
    id uuid NOT NULL,
    scheduled_notification_id uuid NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.scheduled_notification_user OWNER TO "postgres";

CREATE TABLE public.template (
    id uuid NOT NULL,
    template_name character varying(100) NOT NULL,
    template_text text NOT NULL,
    send_via_email boolean NOT NULL DEFAULT TRUE,
    send_via_sms boolean NOT NULL DEFAULT FALSE
);


ALTER TABLE public.template OWNER TO "postgres";

COPY public.scheduled_notification (id, schedule, template_id, data, enabled) FROM stdin;
8a245a02-fdfe-49c7-8f5a-4590fb03ee50	M 1 18:00	2f987d44-5303-4b3c-aaba-4441e1cf8771	\N	t
60330fcc-a10f-4731-9ffa-605a938120e7	W 5 18:00	fce09a1d-ebd3-4174-ad99-9f4b232946cb	{"new_movie_ids": [ "59293411-08b7-4f49-8259-9d379952d62f", "5a769a49-9df1-4be0-bce9-a86904de115b", "fbcb0bba-d9f5-4013-82ae-0f87964e5b74", "897cc60e-0a29-4f71-b0b0-6e6b90853570", "d9f0654b-795b-4610-abf3-901a09a94e46" ]}	t
\.

COPY public.scheduled_notification_user (id, scheduled_notification_id, user_id) FROM stdin;
\.

COPY public.template (id, template_name, template_text) FROM stdin;
48bf294c-8efb-4181-82cd-fbcb628058e4	user_registered	<!DOCTYPE html>\n<html lang="en">\n<body>\n    <h1>Здравствуйте, {{username}}!</h1>\n    <p>\n        Мы рады приветствовать Вас на нашем сайте!\n    </p>\n</body>\n</html>\n
2f987d44-5303-4b3c-aaba-4441e1cf8771	user_month_statistics	<!DOCTYPE html>\n<html lang="en">\n<body>\n    <h1>Здравствуйте, {{username}}!</h1>\n    <p>\n        За последний месяц Вы посмотрели {{movies_count}} фильмов!\n    </p>\n    <p>\n        Из них {{detectives_count}} детективов.\n    </p>\n</body>\n</html>\n
fce09a1d-ebd3-4174-ad99-9f4b232946cb	last_week_new_movies	<!DOCTYPE html>\n<html lang="en">\n<body>\n    <h1>Здравствуйте, {{username}}!</h1>\n    <p>\n        Вот и вечер пятницы, бла-бла-бла! За последний месяц вышли новые фильмы:\n    </p>\n    {% for movie in movies %}\n        <p>{{ movie.title }}</p>\n    {% endfor %}\n</body>\n</html>\n
\.

ALTER TABLE ONLY public.scheduled_notification
    ADD CONSTRAINT scheduled_notification_pk PRIMARY KEY (id);

ALTER TABLE ONLY public.scheduled_notification_user
    ADD CONSTRAINT scheduled_notification_user_pk PRIMARY KEY (id);

ALTER TABLE ONLY public.template
    ADD CONSTRAINT template_pk PRIMARY KEY (id);

CREATE UNIQUE INDEX scheduled_notification_id_uindex ON public.scheduled_notification USING btree (id);

CREATE UNIQUE INDEX scheduled_notification_user_id_uindex ON public.scheduled_notification_user USING btree (id);

CREATE UNIQUE INDEX scheduled_notification_user_scheduled_notification_id_user_id_u ON public.scheduled_notification_user USING btree (scheduled_notification_id, user_id);

CREATE UNIQUE INDEX template_id_uindex ON public.template USING btree (id);

CREATE UNIQUE INDEX template_template_name_uindex ON public.template USING btree (template_name);

ALTER TABLE ONLY public.scheduled_notification
    ADD CONSTRAINT scheduled_notification_template_id_fk FOREIGN KEY (template_id) REFERENCES public.template(id) ON UPDATE CASCADE ON DELETE CASCADE;

ALTER TABLE ONLY public.scheduled_notification_user
    ADD CONSTRAINT scheduled_notification_user_scheduled_notification_id_fk FOREIGN KEY (scheduled_notification_id) REFERENCES public.scheduled_notification(id) ON UPDATE CASCADE ON DELETE CASCADE;
COMMIT;