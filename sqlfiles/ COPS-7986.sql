--liquibase formatted sql
--changeset kaustab:COPS-7986 runOnChange:true

update CaptureCycleConfiguration set cycle_close_schedule_value = "0 0 6 * * *", time_modified = now();
