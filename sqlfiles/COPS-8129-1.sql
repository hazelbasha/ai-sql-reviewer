--liquibase formatted sql
--changeset kaustab:COPS-8129 runOnChange:true

update GatewayActivityLog set status = 2001, time_modified = now(), amount = 32 where payment_reference_number = "HRT09541880888-859";
