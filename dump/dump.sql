--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1 (Debian 16.1-1.pgdg120+1)
-- Dumped by pg_dump version 16.1 (Debian 16.1-1.pgdg120+1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: Episode; Type: TABLE; Schema: public; Owner: animauntuser
--

CREATE TABLE public."Episode" (
    id integer NOT NULL,
    number double precision,
    view_number character varying(31),
    caption character varying(63),
    video_msg_id character varying(255),
    title_id integer
);


ALTER TABLE public."Episode" OWNER TO animauntuser;

--
-- Name: Episode_id_seq; Type: SEQUENCE; Schema: public; Owner: animauntuser
--

CREATE SEQUENCE public."Episode_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Episode_id_seq" OWNER TO animauntuser;

--
-- Name: Episode_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: animauntuser
--

ALTER SEQUENCE public."Episode_id_seq" OWNED BY public."Episode".id;


--
-- Name: Title; Type: TABLE; Schema: public; Owner: animauntuser
--

CREATE TABLE public."Title" (
    id integer NOT NULL,
    name character varying(255),
    url character varying(255),
    remote_path character varying(255),
    description text,
    image_url text,
    match_episode character varying(255),
    last_episode double precision,
    last_update timestamp without time zone,
    complete boolean
);


ALTER TABLE public."Title" OWNER TO animauntuser;

--
-- Name: Title_id_seq; Type: SEQUENCE; Schema: public; Owner: animauntuser
--

CREATE SEQUENCE public."Title_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."Title_id_seq" OWNER TO animauntuser;

--
-- Name: Title_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: animauntuser
--

ALTER SEQUENCE public."Title_id_seq" OWNED BY public."Title".id;


--
-- Name: User; Type: TABLE; Schema: public; Owner: animauntuser
--

CREATE TABLE public."User" (
    id integer NOT NULL,
    email character varying(255),
    hashed_password character varying(255),
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    is_verified boolean NOT NULL
);


ALTER TABLE public."User" OWNER TO animauntuser;

--
-- Name: User_id_seq; Type: SEQUENCE; Schema: public; Owner: animauntuser
--

CREATE SEQUENCE public."User_id_seq"
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public."User_id_seq" OWNER TO animauntuser;

--
-- Name: User_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: animauntuser
--

ALTER SEQUENCE public."User_id_seq" OWNED BY public."User".id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: animauntuser
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO animauntuser;

--
-- Name: Episode id; Type: DEFAULT; Schema: public; Owner: animauntuser
--

ALTER TABLE ONLY public."Episode" ALTER COLUMN id SET DEFAULT nextval('public."Episode_id_seq"'::regclass);


--
-- Name: Title id; Type: DEFAULT; Schema: public; Owner: animauntuser
--

ALTER TABLE ONLY public."Title" ALTER COLUMN id SET DEFAULT nextval('public."Title_id_seq"'::regclass);


--
-- Name: User id; Type: DEFAULT; Schema: public; Owner: animauntuser
--

ALTER TABLE ONLY public."User" ALTER COLUMN id SET DEFAULT nextval('public."User_id_seq"'::regclass);


--
-- Data for Name: Episode; Type: TABLE DATA; Schema: public; Owner: animauntuser
--

COPY public."Episode" (id, number, view_number, caption, video_msg_id, title_id) FROM stdin;
102	1	1	1 серия	388	17
103	2	2	2 серия	389	17
104	3	3	3 серия	390	17
105	4	4	4 серия	391	17
106	5	5	5 серия	392	17
107	6	6	6 серия	393	17
108	7	7	7 серия	394	17
109	8	8	8 серия	395	17
110	8.5	8.5	8.5 серия	396	17
111	9	9	9 серия	397	17
112	10	10	10 серия	398	17
113	11	11	11 серия	399	17
114	12	12	12 серия	400	17
115	1.1	1. 1ч	1 серия 1 часть	401	18
116	1.2	1. 2ч	1 серия 2 часть	402	18
117	1.3	1. 3ч	1 серия 3 часть	403	18
118	2.1	2. 1ч	2 серия 1 часть	404	18
119	2.2	2. 2ч	2 серия 2 часть	405	18
120	3.1	3. 1ч	3 серия 1 часть	406	18
122	3.3	3. 3ч	3 серия 3 часть	408	18
123	4.1	4. 1ч	4 серия 1 часть	409	18
124	4.2	4. 2ч	4 серия 2 часть	410	18
125	4.3	4. 3ч	4 серия 3 часть	411	18
126	5.1	5. 1ч	5 серия 1 часть	412	18
127	5.2	5. 2ч	5 серия 2 часть	413	18
128	5.3	5. 3ч	5 серия 3 часть	414	18
129	6.1	6. 1ч	6 серия 1 часть	415	18
130	6.2	6. 2ч	6 серия 2 часть	416	18
131	6.3	6. 3ч	6 серия 3 часть	417	18
132	7.1	7. 1ч	7 серия 1 часть	418	18
133	7.2	7. 2ч	7 серия 2 часть	419	18
134	7.3	7. 3ч	7 серия 3 часть	420	18
135	8.1	8. 1ч	8 серия 1 часть	421	18
136	8.2	8. 2ч	8 серия 2 часть	422	18
137	8.3	8. 3ч	8 серия 3 часть	423	18
121	3.2	3. 2ч	3 серия 2 часть	424	18
138	1	1	1 серия	425	19
139	2	2	2 серия	426	19
140	3	3	3 серия	427	19
141	4	4	4 серия	428	19
142	5	5	5 серия	429	19
143	-1	сп 1	Спешл 1	431	19
144	-2	сп 2	Спешл 2	432	19
145	6	6	6 серия	433	19
146	7	7	7 серия	434	19
147	8	8	8 серия	435	19
148	9	9	9 серия	436	19
149	10	10	10 серия	438	19
150	11	11	11 серия	439	19
151	12	12	12 серия	440	19
152	13	13	13 серия	441	19
153	14	14	14 серия	442	19
154	15	15	15 серия	443	19
155	16	16	16 серия	445	19
156	17	17	17 серия	446	19
157	18	18	18 серия	447	19
158	19	19	19 серия	448	19
\.


--
-- Data for Name: Title; Type: TABLE DATA; Schema: public; Owner: animauntuser
--

COPY public."Title" (id, name, url, remote_path, description, image_url, match_episode, last_episode, last_update, complete) FROM stdin;
18	Плутон	https://animaunt.org/11510-pluton.html	Плутон | Pluto	В далеком будущем вместо обыкновенных следователей действительно сложные дела поручают вести роботам. Это не почти что цельнометаллические рыцари в технологичных доспехах из «Робокопа»: детектив по имени Гезихт очень даже похож на человека, но сознание его все же вполне искусственное. Ему предстоит выяснить, что на самом деле произошло во время цепочки убийств, жертвами которых становились наиболее сильные и мощные роботы и люди своего времени. Намного сложнее дело начинает выглядеть, когда среди подозреваемых не оказывается человеческих существ.	https://animaunt.org/uploads/posts/2023-04/1682019596_pluton.jpg	8	8.3	2023-10-28 11:04:16	t
17	Папаши-дружбаны	https://animaunt.org/10968-papashi-druzhbany.html	Папаши-дружбаны | Buddy Daddies	Папаши-дружбаныСюжет японского аниме «Папаши-дружбаны» в жанре комедийной повседневности от режиссёра Ёсиюки Асаи разворачивается в нашей реальности, в обыденной повседневности.Главными героями являются двое взрослых мужчин. У них весьма интересная профессия, которая им, на первый взгляд, не совсем подходит. Мужчины, которых зовут Кадзуки Курусу и Рэйем Сувой, работают профессиональными нянями, которые присматривают за маленькими сорванцами, когда их родители заняты. Главные герои настолько безупречно выполняют поручения по уходу за детьми, что никто даже не думает, что всё это лишь прикрытие для их основного рода деятельности. Кадзуки Курусу и Рэй Сува – это профессиональные киллеры, и именно такая работа приносит им основной доход	https://animaunt.org/uploads/posts/2022-12/1670182431_poster-53.jpg	12	12	2023-03-31 20:36:41	t
19	Магическая битва 2	https://animaunt.org/11141-magicheskaya-bitva-2.html	Магическая битва 2 | Jujutsu Kaisen 2nd Season	Главному герою второго сезона «Магической битвы» Юдзи Итадори предстоит столкнуться с множеством трудностей. Вот ещё странности, перед смертью любимый дедушка героя наказал ему защищать людей, не жалея на то сил. Парень на всю жизнь запомнил эти слова, хотя и не стал придавать им особого значения.   Главный герой не замечает, как постепенно его мысли начинают опутывать оккультные науки, хотя когда-то он был многообещающим спортсменом. Юноша занимался атлектикой и подавал большие надежды, однако в самый последний момент отказался от участия в команде. Друзья Юдзи тоже увлекаются магическими «науками» и чёрной магией, например, они учатся призывать духов умерших «по приколу» – подростки не слишком верят в происходящее	https://animaunt.org/uploads/posts/2023-02/1675952950_mag-bitva-2.jpg	23	19	2023-11-30 19:46:45	f
\.


--
-- Data for Name: User; Type: TABLE DATA; Schema: public; Owner: animauntuser
--

COPY public."User" (id, email, hashed_password, is_active, is_superuser, is_verified) FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: animauntuser
--

COPY public.alembic_version (version_num) FROM stdin;
e826240cfc66
\.


--
-- Name: Episode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: animauntuser
--

SELECT pg_catalog.setval('public."Episode_id_seq"', 158, true);


--
-- Name: Title_id_seq; Type: SEQUENCE SET; Schema: public; Owner: animauntuser
--

SELECT pg_catalog.setval('public."Title_id_seq"', 19, true);


--
-- Name: User_id_seq; Type: SEQUENCE SET; Schema: public; Owner: animauntuser
--

SELECT pg_catalog.setval('public."User_id_seq"', 1, false);


--
-- Name: Episode Episode_pkey; Type: CONSTRAINT; Schema: public; Owner: animauntuser
--

ALTER TABLE ONLY public."Episode"
    ADD CONSTRAINT "Episode_pkey" PRIMARY KEY (id);


--
-- Name: Title Title_pkey; Type: CONSTRAINT; Schema: public; Owner: animauntuser
--

ALTER TABLE ONLY public."Title"
    ADD CONSTRAINT "Title_pkey" PRIMARY KEY (id);


--
-- Name: User User_email_key; Type: CONSTRAINT; Schema: public; Owner: animauntuser
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_email_key" UNIQUE (email);


--
-- Name: User User_pkey; Type: CONSTRAINT; Schema: public; Owner: animauntuser
--

ALTER TABLE ONLY public."User"
    ADD CONSTRAINT "User_pkey" PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: animauntuser
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: Episode Episode_title_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: animauntuser
--

ALTER TABLE ONLY public."Episode"
    ADD CONSTRAINT "Episode_title_id_fkey" FOREIGN KEY (title_id) REFERENCES public."Title"(id);


--
-- PostgreSQL database dump complete
--

