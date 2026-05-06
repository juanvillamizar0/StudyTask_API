\# Mapa de Endpoints - StudyTask API



\## Descripción General



Este documento presenta el mapa de endpoints de la API StudyTask.  

La API permite gestionar estudiantes, asignaturas y tareas académicas mediante operaciones Find, Update, Create y Kill, usando persistencia en archivos CSV.



\---



\## Endpoints Generales



| Método | Endpoint | Descripción |

|---|---|---|

| GET | / | Muestra la información general del proyecto |

| GET | /health | Verifica que la API esté funcionando correctamente |



\---



\## Endpoints de Estudiantes



| Método | Endpoint | Operación | Descripción |

|---|---|---|---|

| POST | /students | Create | Crea un nuevo estudiante |

| GET | /students | Find | Consulta todos los estudiantes |

| GET | /students/{student\_id} | Find | Busca un estudiante por ID |

| PUT | /students/{student\_id} | Update | Actualiza un estudiante existente |

| DELETE | /students/{student\_id} | Kill | Marca un estudiante como inactivo |

| GET | /students/filter/semester/{semester} | Find | Filtra estudiantes por semestre |

| GET | /students/filter/active/{is\_active} | Find | Filtra estudiantes activos o inactivos |

| GET | /students/search/email/{email} | Find | Busca estudiantes por correo electrónico |



\---



\## Endpoints de Asignaturas



| Método | Endpoint | Operación | Descripción |

|---|---|---|---|

| POST | /subjects | Create | Crea una nueva asignatura |

| GET | /subjects | Find | Consulta todas las asignaturas |

| GET | /subjects/{subject\_id} | Find | Busca una asignatura por ID |

| PUT | /subjects/{subject\_id} | Update | Actualiza una asignatura existente |

| DELETE | /subjects/{subject\_id} | Kill | Marca una asignatura como inactiva |

| GET | /subjects/filter/credits/{credits} | Find | Filtra asignaturas por número de créditos |

| GET | /subjects/filter/active/{is\_active} | Find | Filtra asignaturas activas o inactivas |

| GET | /subjects/search/name/{name} | Find | Busca asignaturas por nombre |



\---



\## Endpoints de Tareas



| Método | Endpoint | Operación | Descripción |

|---|---|---|---|

| POST | /tasks | Create | Crea una nueva tarea académica |

| GET | /tasks | Find | Consulta todas las tareas |

| GET | /tasks/{task\_id} | Find | Busca una tarea por ID |

| PUT | /tasks/{task\_id} | Update | Actualiza una tarea existente |

| DELETE | /tasks/{task\_id} | Kill | Marca una tarea como inactiva |

| GET | /tasks/filter/status/{status} | Find | Filtra tareas por estado |

| GET | /tasks/filter/active/{is\_active} | Find | Filtra tareas activas o inactivas |

| GET | /tasks/search/title/{title} | Find | Busca tareas por título |



\---



\## Manejo de Histórico



La eliminación no borra físicamente los registros del archivo CSV.  

En su lugar, el sistema cambia el campo `is\_active` a `false`.



Esto permite conservar histórico de estudiantes, asignaturas y tareas, mostrando registros activos e inactivos cuando sea necesario.



\---



\## Manejo de Excepciones



La API utiliza `HTTPException` para responder adecuadamente cuando:



\- Se intenta crear un registro que ya existe.

\- Se busca un registro inexistente.

\- Se intenta actualizar un registro con un ID que no coincide.

\- Se intenta crear una tarea con estudiante o asignatura inexistente.

\- No se encuentran resultados en filtros o búsquedas.

