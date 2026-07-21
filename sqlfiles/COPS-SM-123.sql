--liquibase formatted sql
--changeset basha:XYZOPS-8129 runOnChange:true

update TVMBEA set satus = 2001, time_modified = now(), amount = 32 where payment_reference_number = "ABC0123-859";

