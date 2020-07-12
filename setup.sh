service postgresql start
su - postgres bash -c "psql < ./backend/setup.sql"
su - postgres bash -c "psql bookshelf < ./backend/books.psql"