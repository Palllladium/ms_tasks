DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_database WHERE datname = 'students_db') THEN
        CREATE DATABASE students_db;
    END IF;
END $$;

GRANT ALL PRIVILEGES ON DATABASE students_db TO admin;