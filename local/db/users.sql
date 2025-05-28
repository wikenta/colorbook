--схемы: coloring, cartoons, files

CREATE ROLE color_admin LOGIN PASSWORD 'PASSWORD';
GRANT CONNECT ON DATABASE color TO color_admin;
ALTER SCHEMA public OWNER TO color_admin;
ALTER SCHEMA cartoons OWNER TO color_admin;
ALTER SCHEMA coloring OWNER TO color_admin;
ALTER SCHEMA files OWNER TO color_admin;
GRANT ALL PRIVILEGES ON DATABASE color TO color_admin;
GRANT ALL ON SCHEMA public, cartoons, coloring, files TO color_admin;
GRANT ALL ON ALL TABLES IN SCHEMA public, cartoons, coloring, files TO color_admin;

CREATE ROLE color_reader LOGIN PASSWORD 'PASSWORD';
GRANT CONNECT ON DATABASE color TO color_reader;
GRANT USAGE ON SCHEMA public, cartoons, coloring, files TO color_reader;
GRANT SELECT ON ALL TABLES IN SCHEMA public, cartoons, coloring, files TO color_reader;
ALTER DEFAULT PRIVILEGES IN SCHEMA public, cartoons, coloring, files GRANT SELECT ON TABLES TO color_reader;
