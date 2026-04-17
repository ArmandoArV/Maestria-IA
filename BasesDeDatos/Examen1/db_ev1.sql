--
-- PostgreSQL database dump
--

-- Dumped from database version 14.17 (Homebrew)
-- Dumped by pg_dump version 14.17 (Homebrew)

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
-- Name: actores; Type: TABLE; Schema: public; Owner: tomasjackson
--

CREATE TABLE public.actores (
    id integer NOT NULL,
    anombre character varying(100) NOT NULL
);


ALTER TABLE public.actores OWNER TO tomasjackson;

--
-- Name: actores_id_seq; Type: SEQUENCE; Schema: public; Owner: tomasjackson
--

CREATE SEQUENCE public.actores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actores_id_seq OWNER TO tomasjackson;

--
-- Name: actores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tomasjackson
--

ALTER SEQUENCE public.actores_id_seq OWNED BY public.actores.id;


--
-- Name: actuo_en; Type: TABLE; Schema: public; Owner: tomasjackson
--

CREATE TABLE public.actuo_en (
    id_actor integer NOT NULL,
    id_pelicula integer NOT NULL
);


ALTER TABLE public.actuo_en OWNER TO tomasjackson;

--
-- Name: peliculas; Type: TABLE; Schema: public; Owner: tomasjackson
--

CREATE TABLE public.peliculas (
    id integer NOT NULL,
    pnombre character varying(100) NOT NULL,
    "año" integer NOT NULL,
    categoria character varying(50) NOT NULL,
    calificacion numeric NOT NULL,
    pdirector character varying(100) NOT NULL
);


ALTER TABLE public.peliculas OWNER TO tomasjackson;

--
-- Name: peliculas_id_seq; Type: SEQUENCE; Schema: public; Owner: tomasjackson
--

CREATE SEQUENCE public.peliculas_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.peliculas_id_seq OWNER TO tomasjackson;

--
-- Name: peliculas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tomasjackson
--

ALTER SEQUENCE public.peliculas_id_seq OWNED BY public.peliculas.id;


--
-- Name: actores id; Type: DEFAULT; Schema: public; Owner: tomasjackson
--

ALTER TABLE ONLY public.actores ALTER COLUMN id SET DEFAULT nextval('public.actores_id_seq'::regclass);


--
-- Name: peliculas id; Type: DEFAULT; Schema: public; Owner: tomasjackson
--

ALTER TABLE ONLY public.peliculas ALTER COLUMN id SET DEFAULT nextval('public.peliculas_id_seq'::regclass);


--
-- Data for Name: actores; Type: TABLE DATA; Schema: public; Owner: tomasjackson
--

COPY public.actores (id, anombre) FROM stdin;
1	Leonardo DiCaprio
2	Matthew McConaughey
3	Daniel Radcliffe
4	Jessica Chastain
5	Tom Hanks
6	Scarlett Johansson
7	Meryl Streep
8	Brad Pitt
\.


--
-- Data for Name: actuo_en; Type: TABLE DATA; Schema: public; Owner: tomasjackson
--

COPY public.actuo_en (id_actor, id_pelicula) FROM stdin;
1	2
2	1
4	1
3	3
1	5
5	6
6	7
8	8
7	8
6	5
\.


--
-- Data for Name: peliculas; Type: TABLE DATA; Schema: public; Owner: tomasjackson
--

COPY public.peliculas (id, pnombre, "año", categoria, calificacion, pdirector) FROM stdin;
1	Interstellar	2014	SciFi	8.6	C. Nolan
2	The Revenant	2015	Drama	8.1	A. Iñárritu
3	Harry Potter	2011	Fantasy	8.1	D. Yates
4	The Theory of Everything	2014	Biography	7.7	J. Marsh
5	Inception	2010	Adventure	8.8	C. Nolan
6	Forrest Gump	1994	Drama	8.8	R. Zemeckis
7	Lost in Translation	2003	Drama	7.8	S. Coppola
8	Fight Club	1999	Drama	8.8	D. Fincher
\.


--
-- Name: actores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tomasjackson
--

SELECT pg_catalog.setval('public.actores_id_seq', 1, false);


--
-- Name: peliculas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tomasjackson
--

SELECT pg_catalog.setval('public.peliculas_id_seq', 1, false);


--
-- Name: actores actores_pkey; Type: CONSTRAINT; Schema: public; Owner: tomasjackson
--

ALTER TABLE ONLY public.actores
    ADD CONSTRAINT actores_pkey PRIMARY KEY (id);


--
-- Name: peliculas peliculas_pkey; Type: CONSTRAINT; Schema: public; Owner: tomasjackson
--

ALTER TABLE ONLY public.peliculas
    ADD CONSTRAINT peliculas_pkey PRIMARY KEY (id);


--
-- Name: actuo_en actuo_en_id_actor_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tomasjackson
--

ALTER TABLE ONLY public.actuo_en
    ADD CONSTRAINT actuo_en_id_actor_fkey FOREIGN KEY (id_actor) REFERENCES public.actores(id);


--
-- Name: actuo_en actuo_en_id_pelicula_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tomasjackson
--

ALTER TABLE ONLY public.actuo_en
    ADD CONSTRAINT actuo_en_id_pelicula_fkey FOREIGN KEY (id_pelicula) REFERENCES public.peliculas(id);


--
-- PostgreSQL database dump complete
--

