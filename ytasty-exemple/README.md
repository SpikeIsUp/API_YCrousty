# Ytasty Crousty — API (point de départ)

FastAPI + PostgreSQL + SQLAlchemy, géré avec uv.
Contient uniquement la route `GET /health`. Le reste est à construire
sur le même modèle.

## Lancer le projet

```bash
docker compose up --build
```

- API : http://localhost:8000/health
- Swagger : http://localhost:8000/docs

Sans Docker :

```bash
uv sync
uv run uvicorn app.main:app --reload
```

## Arborescence

```
app/
├── main.py                  crée l'app et branche les routers
├── common/
│   └── errors.py            messages et exceptions partagés
├── core/
│   ├── config.py            variables d'environnement
│   └── database.py          engine SQLAlchemy + get_db()
└── modules/
    └── health/
        ├── router.py        reçoit le HTTP
        ├── service.py       décide
        └── schemas.py       forme des données
```

Un module = un dossier. Pour ajouter une fonctionnalité, on copie le
dossier `health/`, on le renomme, et on branche son router dans `main.py`.

Dès qu'un module parle à la base, il gagne deux fichiers :
`models.py` (les tables) et `repository.py` (les requêtes SQLAlchemy).
`health/` n'en a pas besoin puisqu'il ne lit rien en base.

## Le chemin d'une requête

```
router.py   →   service.py   →   repository.py
reçoit          décide           interroge la base
```

- `router.py` : l'URL, le code HTTP, la validation d'entrée. Zéro règle métier.
- `service.py` : les règles (« un produit indisponible ne peut pas être
  commandé »). Ne fait jamais de SQL.
- `repository.py` : les requêtes SQLAlchemy. Le seul fichier qui parle à la base.

## Modules à ajouter

`auth/`, `users/`, `restaurants/`, `products/`, `orders/`.
