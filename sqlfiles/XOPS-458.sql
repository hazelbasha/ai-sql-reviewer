--liquibase formatted sql
--changeset basha:XOPS-458 runOnChange:true

Alter OrderItem add column price_v3(int);

