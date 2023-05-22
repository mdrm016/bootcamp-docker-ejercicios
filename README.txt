Se solicita ejecutar 3 contenedores que corresponde a partes de una aplicación web.

1. Levantar una BD en postgres
- Crear el Dockerfile
- Usar la imagen oficial de postgres
- Copiar el script de BD en la raiz del contenedor
- Crear la imagen con el siguiente comando
	docker build -t bootcamp_ej1_bd:0.0.1 .
- Crear el contenerdor con el siguiente comando
	docker run -p 5433:5432 --name bootcamp-ej1-db -e POSTGRES_PASSWORD=postgres -d bootcamp_ej1_bd:0.0.1
- Conectarse al contenedor de Modo Interactivo
	docker exec -it <ID_CONTENEDOR> bash
- Restaurar la BD con el script copiado con los siguientes comandos
	psql -U postgres -c "create database app;"
	psql -U postgres -d app -f script_db.sql
- Salir del modo iterativo con "exit"

2. Levantar un API REST [Backend]
- Crear el Dockerfile en la raiz del proyecto backend
- Usar la imagen oficial de python:3.8
- Copiar el directorio backend en "/home"
- Establecer un directorio de trabajo por ejemplo "/home/backend"
- Restaurar las dependencias -> pip install -r requirements.txt
- Ejecutar el Process Main -> CMD [ "gunicorn", "-b :5000", "app:app" ]
- Exponer el contenedor en el puerto 5000 -> EXPOSE 5000
- Crear la imagen con el siguiente comando
	docker build -t bootcamp_ej2_backend:0.0.1 .
- Crear el contenedor con el siguiente comando
	-> Obtener la ip de nuestra maquina y reemplazar por <IP_HOST>
	docker run --rm -p 5000:5000 --name bootcamp-ej2-backend -e SQLALCHEMY_DATABASE_URI=postgresql://postgres:postgres@<IP_HOST>:5433/app -d bootcamp_ej2_backend:0.0.1


3. Levantar el Frontend
- Crear la imagen a partir del dockerfile proveído
	-> Obtener la ip de nuestra maquina y reemplazar por <IP_HOST>
	docker build -t bootcamp_ej3_frontend:0.0.1 --build-arg BACKEND_URL=http://<IP_HOST>:5000/api .
- Crear el contenedor
	docker run --rm -p 8080:80 --name bootcamp-ej3-frontend -d bootcamp_ej3_frontend:0.0.1
- Acceder a la aplicacion con test:test
- Analizar los pasos del dockerfile


