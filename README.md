# Task Manager API

## Proyecto
El **Task Manager API** es un servicio web desarrollado con **FastAPI** que permite administrar tareas de manera eficiente. Su objetivo principal es ofrecer una solución escalable y confiable para el manejo de actividades, con funcionalidades como la creación, actualización, eliminación y seguimiento de tareas. Además, incluye automatización de procesos mediante *background jobs* y notificaciones integradas.

## Objetivos
- Crear una API RESTful para el manejo de tareas.
- Implementar un sistema de tareas con estados (pendiente, en progreso, completado).
- Integración de herramientas para automatización y comunicación.
- Establecer una base de datos persistente para almacenamiento estructurado.

## Herramientas Utilizadas
- **FastAPI**: Framework moderno para la creación de APIs con enfoque en velocidad y documentación.
- **APScheduler**: Para programar y ejecutar tareas en segundo plano.
- **aiosmtplib**: Manejo de correos electrónicos de manera asíncrona.
- **PostgreSQL**: Sistema de gestión de relaciones objetivas (ORM) para almacenamiento de datos.
- **uv**: Instalación y gestión de dependencias mediante CLI moderno.

## Base de Datos
El proyecto utiliza **PostgreSQL** como motor de base de datos, asegurando la integridad y escalabilidad de la información. Todas las operaciones de tareas (CRUD) se gestionan a través de consultas SQL optimizadas.

## Instalación
### Requisitos previos
1. Tener instalado **uv** en el sistema.
2. Python 3.8 o superior.

### Pasos de instalación
1. **Clonar el repositorio**:  
   ```bash
   git clone https://github.com/tu-usuario/task-manager-api.git
   cd task-manager-api
   ```

2. **Crear un entorno virtual** (usando `uv`):  
   ```bash
   uv create --python 3.9 --venv .
   ```

3. **Instalar dependencias**:  
   ```bash
   uv add fastapi uvicorn apscheduler aiosmtplib psycopg2-binary python-dotenv
   ```

4. **Configurar la base de datos**:  
   - Crear un archivo `.env` con las credenciales de PostgreSQL:  
     ```env
     DATABASE_URL=postgresql+psycopg2://usuario:contraseña@localhost:5432/task_manager
     ```

5. **Iniciar el servidor**:  
   ```bash
   uv run uvicorn main:app --reload
   ```

## Objetivos de Aprendizaje
1. **Background Jobs**:  
   - Uso de **APScheduler** para programar tareas recurrentes o diferidas (ej: envío de notificaciones de avance).  
   - Comprensión de las ventajas de la ejecución asíncrona en proyectos web.

2. **Pruebas Unitarias**:  
   - Desarrollo de pruebas con **pytest** para validar la funcionalidad de las rutas de la API y la lógica de negocio.  
   - Aseguro la calidad del código mediante la ejecución automatizada de casos de prueba.

3. **Autonomía y Escalabilidad**:  
   - Estructura modular del código para facilitar mantenimiento y escalabilidad futura.  
   - Implementación de buenas prácticas en diseño de APIs (RESTful, manejo de errores, documentación automática con **Swagger UI**).

## Notas Adicionales
- La API está diseñada para ser extensible, permitiendo añadir funcionalidades como autenticación, integración con third-party services o interfaces gráficas en el futuro.  
- Todos los scripts y configuraciones han sido probados en un entorno local, asegurando la reproducibilidad del proceso de instalación.  
- Para más detalles técnicos, contactar a [correo de contacto] o visitar el repositorio oficial.