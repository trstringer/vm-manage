CREATE TABLE public.virtual_machine
(
    vm_id   SERIAL          NOT NULL PRIMARY KEY,
    name    VARCHAR(256)    NOT NULL,
    size    VARCHAR(32)     NOT NULL
);
