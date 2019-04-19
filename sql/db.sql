-- Table: public.users2

-- DROP TABLE public.users2;

CREATE TABLE public.users2
(
    id integer NOT NULL DEFAULT nextval('users2_id_seq'::regclass),
    name text COLLATE pg_catalog."default",
    photo text COLLATE pg_catalog."default",
    surname text COLLATE pg_catalog."default",
    status text COLLATE pg_catalog."default",
    encoding text COLLATE pg_catalog."default",
    CONSTRAINT users2_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.users2
    OWNER to test_user;