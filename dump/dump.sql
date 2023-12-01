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
    number integer,
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
    search_field character varying(255),
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

COPY public."Episode" (id, number, video_msg_id, title_id) FROM stdin;
1	1	206	1
2	2	207	1
3	3	208	1
4	4	210	1
5	5	211	1
6	6	212	1
7	7	213	1
8	8	214	1
9	9	215	1
10	1	216	2
11	2	217	2
12	3	218	2
13	4	219	2
14	5	220	2
15	6	221	2
16	7	222	2
17	8	223	2
18	9	224	2
19	10	225	2
20	11	226	2
21	12	227	2
22	13	228	2
23	14	229	2
24	15	230	2
25	16	231	2
26	17	232	2
27	18	233	2
28	19	234	2
29	20	235	2
30	21	236	2
31	22	237	2
36	1	242	4
37	2	243	4
38	3	244	4
39	4	246	4
40	5	247	4
41	6	248	4
42	7	249	4
43	8	250	4
\.


--
-- Data for Name: Title; Type: TABLE DATA; Schema: public; Owner: animauntuser
--

COPY public."Title" (id, name, url, remote_path, description, image_url, match_episode, search_field, last_episode, last_update, complete) FROM stdin;
4	История знакомства опытной тебя и неопытного меня	https://animaunt.org/11602-istoriya-znakomstva-opytnoy-tebya-i-neopytnogo-menya.html	/home/video/mp4/История знакомства опытной тебя и неопытного меня | Keikenzumi na Kimi to Keiken Zero na Ore ga Otsukiai suru Hanashi	\N	https://animaunt.org/uploads/posts/2023-05/1684273143_istoriya-znakomstva-opytnoy-tebya-i-neopytnogo-menya.jpg	12	история знакомства опытной тебя и неопытного меня	8	2023-11-24 20:27:47	f
1	Низкоквалифицированный ниндзя	https://animaunt.org/11420-nizkokvalificirovannyy-nindzya.html	/home/video/mp4/Низкоквалифицированный ниндзя | Under Ninja	\N	https://animaunt.org/uploads/posts/2023-04/1681516812_nizkokvalificirovannyy-nindzya.jpg	12	низкоквалифицированный ниндзя	9	2023-11-30 21:53:14	f
2	Бродяга Кэнсин	https://animaunt.org/11364-brodyaga-kensin.html	/home/video/mp4/Бродяга Кэнсин | Rurouni Kenshin: Meiji Kenkaku Romantan	\N	https://animaunt.org/uploads/posts/2023-04/1680724446_brodyaga-kensin.jpg	24	бродяга кэнсин	22	2023-12-01 11:02:57	f
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
9b666ff89ee6
\.


--
-- Name: Episode_id_seq; Type: SEQUENCE SET; Schema: public; Owner: animauntuser
--

SELECT pg_catalog.setval('public."Episode_id_seq"', 43, true);


--
-- Name: Title_id_seq; Type: SEQUENCE SET; Schema: public; Owner: animauntuser
--

SELECT pg_catalog.setval('public."Title_id_seq"', 4, true);


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

