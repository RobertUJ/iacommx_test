-- migrate:up
CREATE TABLE solicitudes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    identification VARCHAR(255) NOT NULL UNIQUE,
    age INT NOT NULL,
    magic_affinity VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    grimoire_type VARCHAR(50) NULL DEFAULT 'none',
    grimoire_description TEXT NULL DEFAULT 'none',
    clover_leaves INT NULL DEFAULT 0,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- migrate:down
DROP TABLE solicitudes;
