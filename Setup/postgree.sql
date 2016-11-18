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




ALTER SCHEMA itemlist OWNER TO postgres;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner:
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = itemlist, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: category; Type: TABLE; Schema: itemlist; Owner: pgadmin; Tablespace:
--

CREATE TABLE category (
    name character varying(80) NOT NULL,
    id integer NOT NULL,
    user_id integer
);


ALTER TABLE itemlist.category OWNER TO pgadmin;

--
-- Name: item; Type: TABLE; Schema: itemlist; Owner: pgadmin; Tablespace:
--

CREATE TABLE item (
    id integer NOT NULL,
    title character varying(250),
    description character varying(250),
    category_id integer,
    user_id integer
);


ALTER TABLE itemlist.item OWNER TO pgadmin;

--
-- Name: user; Type: TABLE; Schema: itemlist; Owner: pgadmin; Tablespace:
--

CREATE TABLE "user" (
    id integer NOT NULL,
    username character varying(250),
    email character varying(250)
);


ALTER TABLE itemlist."user" OWNER TO pgadmin;

--
-- Name: category_pkey; Type: CONSTRAINT; Schema: itemlist; Owner: pgadmin; Tablespace:
--

ALTER TABLE ONLY category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- Name: item_pkey; Type: CONSTRAINT; Schema: itemlist; Owner: pgadmin; Tablespace:
--

ALTER TABLE ONLY item
    ADD CONSTRAINT item_pkey PRIMARY KEY (id);


--
-- Name: user_pkey; Type: CONSTRAINT; Schema: itemlist; Owner: pgadmin; Tablespace:
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: category_user_id_fkey; Type: FK CONSTRAINT; Schema: itemlist; Owner: pgadmin
--

ALTER TABLE ONLY category
    ADD CONSTRAINT category_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- Name: item_category_id_fkey; Type: FK CONSTRAINT; Schema: itemlist; Owner: pgadmin
--

ALTER TABLE ONLY item
    ADD CONSTRAINT item_category_id_fkey FOREIGN KEY (category_id) REFERENCES category(id);


--
-- Name: item_user_id_fkey; Type: FK CONSTRAINT; Schema: itemlist; Owner: pgadmin
--

ALTER TABLE ONLY item
    ADD CONSTRAINT item_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: category; Type: ACL; Schema: itemlist; Owner: pgadmin
--

REVOKE ALL ON TABLE category FROM PUBLIC;
REVOKE ALL ON TABLE category FROM pgadmin;
GRANT ALL ON TABLE category TO pgadmin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE category TO cataloge;


--
-- Name: item; Type: ACL; Schema: itemlist; Owner: pgadmin
--

REVOKE ALL ON TABLE item FROM PUBLIC;
REVOKE ALL ON TABLE item FROM pgadmin;
GRANT ALL ON TABLE item TO pgadmin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE item TO cataloge;


--
-- Name: user; Type: ACL; Schema: itemlist; Owner: pgadmin
--

REVOKE ALL ON TABLE "user" FROM PUBLIC;
REVOKE ALL ON TABLE "user" FROM pgadmin;
GRANT ALL ON TABLE "user" TO pgadmin;
GRANT SELECT,INSERT,DELETE,UPDATE ON TABLE "user" TO cataloge;

--
-- Name: Serialize; Type: VIEW; Schema: itemlist; Owner: pgadmin
--

CREATE VIEW "Serialize" AS
 SELECT i.id AS item_id,
    u.username,
    c.id AS category_id,
    c.name AS category_name,
    i.title AS item_title,
    i.description AS item_description,
    u.id AS user_id
   FROM (("user" u
     LEFT JOIN category c ON ((u.id = c.user_id)))
     LEFT JOIN item i ON ((i.category_id = c.id)));


ALTER TABLE itemlist."Serialize" OWNER TO pgadmin;

REVOKE ALL ON TABLE "Serialize" FROM PUBLIC;
REVOKE ALL ON TABLE "Serialize" FROM pgadmin;
GRANT ALL ON TABLE "Serialize" TO pgadmin;
GRANT SELECT ON TABLE "Serialize" TO cataloge;


--
-- PostgreSQL database dump complete
--
