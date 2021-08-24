#!/usr/bin/env bash

# include pgcron config from main config
pgcron_conf=/docker-entrypoint-initdb.d/pgcron.conf
main_conf=/var/lib/postgresql/data/postgresql.conf
found=$(grep "include = '${pgcron_conf}'" ${main_conf})
if [ -z "$found" ]; then
  echo "include = '${pgcron_conf}'" >> ${main_conf}
fi
pg_ctl restart
