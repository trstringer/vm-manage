CREATE TABLE public.virtual_machine
(
    vm_id   SERIAL          NOT NULL PRIMARY KEY,
    name    VARCHAR(256)    NOT NULL,
    size    VARCHAR(32)     NOT NULL
);

CREATE TABLE public.virtual_machine_event
(
    vm_id           INT             NOT NULL
        REFERENCES public.virtual_machine (vm_id),
    log_datetime    TIMESTAMP       NOT NULL,
    unit            VARCHAR(256)    NOT NULL,
    message         TEXT            NOT NULL
);
