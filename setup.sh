service postgresql start
su - postgres bash -c "psql < ./backend/setup.sql"
su - postgres bash -c "psql fyyur < ./backend/fyyur.psql"