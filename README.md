# airflow-nlp

## Deploy Test stack

```
docker-compose -f docker-compose.dev.yaml config | docker stack deploy airflow-nlp --compose-file -
```

## Remove test env

```
docker stack rm airflow-nlp
```

