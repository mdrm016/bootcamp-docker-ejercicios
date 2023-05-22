CREATE TABLE public.persona
(
    id        bigserial PRIMARY KEY,
    documento varchar(50),
    nombre    varchar(100),
    apellido  varchar(100),
    ciudad    varchar(100),
    direccion varchar(100),
    telefono  varchar(20),
    email     varchar(30)
);


INSERT INTO public.persona (documento, nombre, apellido, ciudad, direccion, telefono, email) VALUES ('1234567', 'Alberto', 'Gomez', 'Asunción', 'Tte. fariña c/ mexico 156', '021456789', 'albet123@gmail.com');
INSERT INTO public.persona (documento, nombre, apellido, ciudad, direccion, telefono, email) VALUES ('6789452', 'Maria', 'Giménez', 'Fernando de la Mora', 'Colón 456', '0981444666', 'mgimenez25@gmail.com');
INSERT INTO public.persona (documento, nombre, apellido, ciudad, direccion, telefono, email) VALUES ('5222222', 'Juan', 'Pereira', 'San Lorenzo', 'Ruta II km 13', '0986541236', 'pereira5463@gmail.com');

