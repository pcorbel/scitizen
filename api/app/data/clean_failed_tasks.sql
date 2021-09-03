UPDATE task
   SET active_task_state = 'EXITED',
       pid = NULL,
       scheduler_state = NULL,
       slot = NULL,
       slot_path = NULL,
       swap_size = NULL,
       state = 'FILES_DOWNLOADED'
WHERE (NOT exit_code = 0)
   OR (report_deadline_at < datetime('now'))
      ;
