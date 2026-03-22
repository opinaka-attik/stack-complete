-- Créé automatiquement au premier démarrage de PostgreSQL

CREATE TABLE IF NOT EXISTS users (
    id         SERIAL PRIMARY KEY,
    name       VARCHAR(100) NOT NULL,
    email      VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Données de démonstration
INSERT INTO users (name, email) VALUES
    ('Alice Dupont', 'alice@example.com'),
    ('Bob Martin',   'bob@example.com')
ON CONFLICT DO NOTHING;