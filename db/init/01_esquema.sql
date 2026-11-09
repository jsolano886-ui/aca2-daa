CREATE TABLE clientes (id SERIAL PRIMARY KEY, nombre VARCHAR(80) NOT NULL, municipio VARCHAR(40) NOT NULL);
CREATE TABLE productos (sku VARCHAR(12) PRIMARY KEY, nombre VARCHAR(80) NOT NULL,
                        precio INT NOT NULL CHECK (precio > 0), stock INT NOT NULL CHECK (stock >= 0));
CREATE TABLE pedidos (id SERIAL PRIMARY KEY, cliente_id INT NOT NULL REFERENCES clientes(id),
                      total INT NOT NULL, creado TIMESTAMPTZ NOT NULL DEFAULT now());
CREATE TABLE pedido_items (pedido_id INT REFERENCES pedidos(id) ON DELETE CASCADE,
                           sku VARCHAR(12) REFERENCES productos(sku), cantidad INT NOT NULL CHECK (cantidad > 0),
                           precio INT NOT NULL, PRIMARY KEY (pedido_id, sku));
