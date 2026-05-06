\# StudyTask API



\## Descripción del Proyecto



StudyTask API es un proyecto desarrollado para la materia Ingeniería Web de la carrera Ingeniería de Sistemas y Computación.



El sistema consiste en una API construida con FastAPI que permite gestionar tareas académicas mediante tres modelos principales:



\- Estudiantes

\- Asignaturas

\- Tareas



La API implementa operaciones tipo FUCK:



\- Find: buscar registros

\- Update: actualizar registros

\- Create: crear registros

\- Kill: eliminar registros



La persistencia de datos se realiza mediante archivos CSV, ya que en esta primera versión no se permite el uso de bases de datos SQL.



\---



\## Objetivo del Proyecto



Desarrollar una API funcional que permita registrar, consultar, actualizar y eliminar información relacionada con estudiantes, asignaturas y tareas académicas, aplicando modelos Pydantic, lógica CRUD/FUCK y persistencia en archivos CSV.



\---



\## Tecnologías Utilizadas



\- Python

\- FastAPI

\- Pydantic

\- CSV

\- Pytest

\- Git

\- GitHub



\---



\## Modelos del Sistema



\### Student



Representa a un estudiante.



Campos:



\- id: identificador único

\- name: nombre del estudiante

\- email: correo electrónico validado

\- semester: semestre académico



\### Subject



Representa una asignatura.



Campos:



\- id: identificador único

\- name: nombre de la asignatura

\- credits: número de créditos

\- teacher: nombre del profesor



\### Task



Representa una tarea académica.



Campos:



\- id: identificador único

\- title: título de la tarea

\- description: descripción de la tarea

\- status: estado de la tarea

\- student\_id: estudiante asociado

\- subject\_id: asignatura asociada

\- due\_date: fecha opcional de entrega



\---



\## Endpoints Principales



\### Estudiantes



\- POST /students

\- GET /students

\- GET /students/{student\_id}

\- PUT /students/{student\_id}

\- DELETE /students/{student\_id}



\### Asignaturas



\- POST /subjects

\- GET /subjects

\- GET /subjects/{subject\_id}

\- PUT /subjects/{subject\_id}

\- DELETE /subjects/{subject\_id}



\### Tareas



\- POST /tasks

\- GET /tasks

\- GET /tasks/{task\_id}

\- PUT /tasks/{task\_id}

\- DELETE /tasks/{task\_id}



\---



\## Ejecución del Proyecto



Crear y activar entorno virtual:



```bash

python -m venv venv

venv\\Scripts\\activate

