set -ex

rm -fr specs || true

fission spec init
# Inference
fission env create --spec \
    --image ghcr.io/ertis-research/tensorflow-env:v0.0.6 \
    --builder ghcr.io/ertis-research/tensorflow-builder:v0.0.6 \
    --name tensorflow --poolsize=0 --version=3
fission fn create --spec --name fog --env tensorflow --src 'inference/*' \
    --entrypoint '__init__.main' --executortype newdeploy --configmap inference \
    --minscale=1 --maxscale=20 \
    --minmemory=1024 --maxmemory=1024 \
    --mincpu=1000 --maxcpu=1000
fission ht create --spec --url=/fog --function=fog --name=fog --namespace=default --method=POST

# Funnel
fission env create --spec \
    --image fission/python-env-3.10 \
    --builder fission/python-builder-3.10 \
    --name python --poolsize=0 --version=3

fission pkg create --spec --name funnel --env python --src 'funnel/*'

fission fn create --spec --name funnel-fog-output --env python --pkg funnel \
    --entrypoint '__init__.main' --executortype newdeploy --configmap inference \
    --minscale=1 --maxscale=10
fission ht create --spec --url=/funnel-fog-output --function=funnel-fog-output --name=funnel-fog-output --namespace=default --method=POST

fission fn create --spec --name funnel-cloud-input --env python --pkg funnel \
    --entrypoint '__init__.main' --executortype newdeploy --configmap inference \
    --minscale=1 --maxscale=10
fission ht create --spec --url=/funnel-cloud-input --function=funnel-cloud-input --name=funnel-cloud-input --namespace=default --method=POST
