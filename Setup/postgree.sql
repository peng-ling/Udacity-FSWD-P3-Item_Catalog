CREATE DATABASE ITEMLIST;

CREATE ROLE cataloge WITH LOGIN PASSWORD 'A1See2D3See';


CREATE SCHEMA itemlist;

GRANT SELECT ON ALL TABLES IN SCHEMA itemlist TO cataloge;

GRANT INSERT ON ALL TABLES IN SCHEMA itemlist TO cataloge;

GRANT DELETE ON ALL TABLES IN SCHEMA itemlist TO cataloge;

GRANT UPDATE ON ALL TABLES IN SCHEMA itemlist TO cataloge;
--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: itemlist; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA itemlist;


ALTER SCHEMA itemlist OWNER TO postgres;

SET search_path = itemlist, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: category; Type: TABLE; Schema: itemlist; Owner: postgres; Tablespace:
--

CREATE TABLE category (
    name character varying(80) NOT NULL,
    id integer NOT NULL,
    user_id integer
);


ALTER TABLE itemlist.category OWNER TO postgres;

--
-- Name: category_id_seq; Type: SEQUENCE; Schema: itemlist; Owner: postgres
--

CREATE SEQUENCE category_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE itemlist.category_id_seq OWNER TO postgres;

--
-- Name: category_id_seq; Type: SEQUENCE OWNED BY; Schema: itemlist; Owner: postgres
--

ALTER SEQUENCE category_id_seq OWNED BY category.id;


--
-- Name: item; Type: TABLE; Schema: itemlist; Owner: postgres; Tablespace:
--

CREATE TABLE item (
    id integer NOT NULL,
    title character varying(250),
    description character varying(250),
    category_id integer,
    user_id integer
);


ALTER TABLE itemlist.item OWNER TO postgres;

--
-- Name: item_id_seq; Type: SEQUENCE; Schema: itemlist; Owner: postgres
--

CREATE SEQUENCE item_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE itemlist.item_id_seq OWNER TO postgres;

--
-- Name: item_id_seq; Type: SEQUENCE OWNED BY; Schema: itemlist; Owner: postgres
--

ALTER SEQUENCE item_id_seq OWNED BY item.id;


--
-- Name: user; Type: TABLE; Schema: itemlist; Owner: postgres; Tablespace:
--

CREATE TABLE "user" (
    id integer NOT NULL,
    username character varying(250),
    email character varying(250)
);


ALTER TABLE itemlist."user" OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: itemlist; Owner: postgres
--

CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE itemlist.user_id_seq OWNER TO postgres;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: itemlist; Owner: postgres
--

ALTER SEQUENCE user_id_seq OWNED BY "user".id;


--
-- Name: id; Type: DEFAULT; Schema: itemlist; Owner: postgres
--

ALTER TABLE ONLY category ALTER COLUMN id SET DEFAULT nextval('category_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: itemlist; Owner: postgres
--

ALTER TABLE ONLY item ALTER COLUMN id SET DEFAULT nextval('item_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: itemlist; Owner: postgres
--

ALTER TABLE ONLY "user" ALTER COLUMN id SET DEFAULT nextval('user_id_seq'::regclass);


--
-- Name: category_pkey; Type: CONSTRAINT; Schema: itemlist; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- Name: item_pkey; Type: CONSTRAINT; Schema: itemlist; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY item
    ADD CONSTRAINT item_pkey PRIMARY KEY (id);


--
-- Name: user_pkey; Type: CONSTRAINT; Schema: itemlist; Owner: postgres; Tablespace:
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: category_user_id_fkey; Type: FK CONSTRAINT; Schema: itemlist; Owner: postgres
--

ALTER TABLE ONLY category
    ADD CONSTRAINT category_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- Name: item_category_id_fkey; Type: FK CONSTRAINT; Schema: itemlist; Owner: postgres
--

ALTER TABLE ONLY item
    ADD CONSTRAINT item_category_id_fkey FOREIGN KEY (category_id) REFERENCES category(id);


--
-- Name: item_user_id_fkey; Type: FK CONSTRAINT; Schema: itemlist; Owner: postgres
--

ALTER TABLE ONLY item
    ADD CONSTRAINT item_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- PostgreSQL database dump complete
--
