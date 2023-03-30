set -ex

rm -fr specs || true

fission spec init
# Inference
fission env create --spec \
    --image ghcr.io/ertis-research/tensorflow-env:v0.0.6 \
    --builder ghcr.io/ertis-research/tensorflow-builder:v0.0.6 \
    --name tensorflow --poolsize=0 --version=3
fission fn create --spec --name cloud --env tensorflow --src 'inference/*' \
    --entrypoint '__init__.main' --executortype newdeploy --configmap inference \
    --minscale=1 --maxscale=20 \
    --minmemory=1024 --maxmemory=1024 \
    --mincpu=1000 --maxcpu=1000
fission ht create --spec --url=/cloud --function=cloud --name=cloud --namespace=default --method=POST

# Funnel
fission env create --spec \
    --image fission/python-env-3.10 \
    --builder fission/python-builder-3.10 \
    --name python --poolsize=0 --version=3
fission fn create --spec --name funnel-cloud-output --env python --src 'funnel/*' \
    --entrypoint '__init__.main' --executortype newdeploy --configmap inference \
    --minscale=1 --maxscale=10
fission ht create --spec --url=/funnel-cloud-output --function=funnel-cloud-output --name=funnel-cloud-output --namespace=default --method=POST
