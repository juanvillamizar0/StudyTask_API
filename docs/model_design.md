# StudyTask API - Diseño de Modelos

## Idea del Proyecto

StudyTask API es un proyecto desarrollado con FastAPI para la materia Ingeniería Web.

El objetivo del sistema es permitir la gestión de tareas académicas mediante tres entidades principales:

- Estudiantes
- Asignaturas
- Tareas

El proyecto aplica la lógica FUCK trabajada en clase:

- Find: buscar registros
- Update: actualizar registros
- Create: crear registros
- Kill: eliminar registros

La información se almacena en archivos CSV, ya que para esta primera versión del proyecto no se permite el uso de bases de datos SQL.

---

## Modelo 1: Student

El modelo Student representa a un estudiante registrado en el sistema.

| Campo | Tipo de dato | Descripción |
|---|---|---|
| id | int | Identificador único del estudiante |
| name | str | Nombre completo del estudiante |
| email | EmailStr | Correo electrónico del estudiante con validación |
| semester | int | Semestre académico actual |

Ejemplo:

```json
{
  "id": 1,
  "name": "Juan Villamizar",
  "email": "juan@email.com",
  "semester": 9
}