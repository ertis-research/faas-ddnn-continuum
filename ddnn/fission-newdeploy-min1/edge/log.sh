set -ex

rm -fr specs || true

fission spec init
# Inference
fission env create --spec \
    --image ghcr.io/ertis-research/tensorflow-arm-env:v0.0.6 \
    --builder ghcr.io/ertis-research/tensorflow-arm-builder:v0.0.6 \
    --name tensorflow --poolsize=0 --version=3
fission fn create --spec --name edge --env tensorflow --src 'inference/*' \
    --entrypoint '__init__.main' --executortype newdeploy --configmap inference \
    --minscale=1 --maxscale=20 \
    --minmemory=512 --maxmemory=512 \
    --mincpu=500 --maxcpu=500
fission ht create --spec --url=/edge --function=edge --name=edge --namespace=default --method=POST

# Funnel
fission env create --spec \
    --image fission/python-env-3.10 \
    --builder fission/python-builder-3.10 \
    --name python --poolsize=0 --version=3

fission pkg create --spec --name funnel --env python --src 'funnel/*'

fission fn create --spec --name funnel-edge-output --env python --pkg funnel \
    --entrypoint '__init__.main' --executortype newdeploy --configmap inference \
    --minscale=1 --maxscale=10
fission ht create --spec --url=/funnel-edge-output --function=funnel-edge-output --name=funnel-edge-output --namespace=default --method=POST

fission fn create --spec --name funnel-fog-input --env python --pkg funnel \
    --entrypoint '__init__.main' --executortype newdeploy --configmap inference \
    --minscale=1 --maxscale=10
fission ht create --spec --url=/funnel-fog-input --function=funnel-fog-input --name=funnel-fog-input --namespace=default --method=POST
