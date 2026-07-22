--liquibase formatted sql
--changeset basha:XOPS-456 runOnChange:true

Update OrderItem set price='1234',time_modfied=now();

