# auto-label-api-sample
The api sample for auto label.

## environment

```bash
conda create -n toby python=3.11
source activate toby
pip install -r requirements.txt
```

## docker running

```bash
# for build image
docker build -f docker/Dockerfile -t auto-label-api .
docker build -f docker/Dockerfile -t auto-label-api:v1 .
# for runing
docker run auto-label-api arg1 arg2
```

## docker compose

```bash
# for start
docker-compose -f docker/docker-compose.yml up --build
# for down
docker-compose -f docker/docker-compose.yml down

docker-compose -f docker/docker-compose.yml up
```

## run backend

```bash
python app.py -m b
```

## run client for test

```bash
python app.py -m c
```



