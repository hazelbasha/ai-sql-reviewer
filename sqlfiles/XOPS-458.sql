--liquibase formatted sql
--changeset basha:XOPS-458 runOnChange:true

Alter OrderInvoice add column reference_number2(varchar (25));

