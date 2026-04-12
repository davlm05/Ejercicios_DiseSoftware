# Git Flow - Ejercicio 6: Lanchas Sin Permisos

## Estrategia de branching

```
main
 └── ejercicio-6-lanchas-sin-permisos        (branch del ejercicio)
      ├── feature/tours-service               (microservicio de tours)
      ├── feature/guides-service              (microservicio de guias)
      ├── feature/frontend-lanchas            (React + Tailwind)
      ├── feature/scripts-docs                (scripts dev/prod + CLAUDE.md)
      └── feature/readme-lanchas              (README + GIT_FLOW)
```

## Flujo

1. Desde `main` se creo `ejercicio-6-lanchas-sin-permisos`
2. Desde el branch del ejercicio se crearon feature branches independientes
3. Cada feature se mergeo al branch del ejercicio con `--no-ff` (merge commit visible)
4. Al finalizar, el branch del ejercicio se mergea a `main`

## Commits por feature

- `feature/tours-service` — microservicio Micronaut REST para tours en lancha (puerto 8081)
- `feature/guides-service` — microservicio Micronaut REST para guias locales (puerto 8082)
- `feature/frontend-lanchas` — frontend React + Tailwind consumiendo ambos servicios
- `feature/scripts-docs` — scripts individuales dev/prod y CLAUDE.md
- `feature/readme-lanchas` — README con instrucciones y GIT_FLOW.md
