--liquibase formatted sql
--changeset basha:XOPS-457 runOnChange:true

update OrderInvoice set status = 2001, time_modified = now(), amount = 32 where reference_number = 'ABC-123';

