UPDATE task
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
       ;
