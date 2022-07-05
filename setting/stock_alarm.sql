-- public.bookmark definition

-- Drop table

-- DROP TABLE public.bookmark;

CREATE TABLE public.bookmark (
	chat_id varchar NOT NULL,
	name varchar NOT NULL,
	"date" timestamp NULL DEFAULT now()
);


-- public.high definition

-- Drop table

-- DROP TABLE public.high;

CREATE TABLE public.high (
	chat_id varchar NOT NULL,
	name varchar NOT NULL,
	price varchar NOT NULL,
	"date" timestamp NULL DEFAULT now(),
	idx serial4 NOT NULL,
	CONSTRAINT high_pk PRIMARY KEY (idx),
	CONSTRAINT high_un UNIQUE (chat_id, name)
);


-- public.lastupdate definition

-- Drop table

-- DROP TABLE public.lastupdate;

CREATE TABLE public.lastupdate (
	update_id int4 NOT NULL
);


-- public.low definition

-- Drop table

-- DROP TABLE public.low;

CREATE TABLE public.low (
	chat_id varchar NOT NULL,
	name varchar NOT NULL,
	price varchar NOT NULL,
	"date" timestamp NULL DEFAULT now(),
	idx serial4 NOT NULL,
	CONSTRAINT low_pk PRIMARY KEY (idx),
	CONSTRAINT low_un UNIQUE (chat_id, name)
);


-- public."member" definition

-- Drop table

-- DROP TABLE public."member";

CREATE TABLE public."member" (
	chat_id varchar NOT NULL,
	id varchar NULL,
	"date" timestamp NULL DEFAULT now(),
	name varchar NULL,
	CONSTRAINT member_pk PRIMARY KEY (chat_id)
);


-- public.stock definition

-- Drop table

-- DROP TABLE public.stock;

CREATE TABLE public.stock (
	name varchar(50) NULL,
	code varchar(6) NULL
);
