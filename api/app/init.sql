-- create extension
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- grant usage to scitizen
GRANT USAGE ON SCHEMA cron TO scitizen;

-- create maintenance procedures
CREATE OR REPLACE PROCEDURE clean_failed_tasks() LANGUAGE SQL AS $$
UPDATE tasks
   SET active_task_state = 'EXITED',
       pid = NULL,
       scheduler_state = NULL,
       slot = NULL,
       slot_path = NULL,
       swap_size = NULL,
       state = 'FILES_DOWNLOADED'
WHERE (NOT exit_code = 0)
   OR (report_deadline_at < NOW())
$$;

CREATE OR REPLACE PROCEDURE clean_succeeded_tasks() LANGUAGE SQL AS $$
UPDATE tasks
   SET active_task_state = 'EXITED',
       fraction_done = 1,
       pid = NULL,
       scheduler_state = NULL,
       slot = NULL,
       slot_path = NULL,
       swap_size = NULL,
       state = 'FILES_UPLOADED'
 WHERE completed_at IS NOT NULL
   AND exit_code = 0
$$;

CREATE OR REPLACE PROCEDURE clean_cron() LANGUAGE SQL AS $$
DELETE FROM cron.job_run_details
 WHERE end_time < NOW() - INTERVAL '1 DAY'
$$;

-- cleanup old data every five minutes
SELECT cron.unschedule(jobid) FROM cron.job;
SELECT cron.schedule('*/5 * * * *', 'CALL clean_failed_tasks();');
SELECT cron.schedule('*/5 * * * *', 'CALL clean_succeeded_tasks();');

-- cleanup and vacuum every day
SELECT cron.schedule('0 0 * * *', 'CALL clean_cron();');
SELECT cron.schedule('0 0 * * *', 'VACUUM ANALYZE;');
