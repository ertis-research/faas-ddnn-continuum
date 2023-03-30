set -ex

rm -fr specs || true

fission spec init
# Inference
fission env create --spec \
    --image ghcr.io/ertis-research/tensorflow-env:v0.0.6 \
    --builder ghcr.io/ertis-research/tensorflow-builder:v0.0.6 \
    --name tensorflow --poolsize=3 \
    --minmemory=512 --maxmemory=512 \
    --mincpu=500 --maxcpu=500
fission fn create --spec --name cloud --env tensorflow --src 'inference/*' \
    --entrypoint '__init__.main' --configmap inference
fission ht create --spec --url=/cloud --function=cloud --name=cloud --namespace=default --method=POST

# Funnel
fission env create --spec \
    --image fission/python-env-3.10 \
    --builder fission/python-builder-3.10 \
    --name python --version=3
fission fn create --spec --name funnel-cloud-output --env python --src 'funnel/*' \
    --entrypoint '__init__.main' --configmap inference 
fission ht create --spec --url=/funnel-cloud-output --function=funnel-cloud-output --name=funnel-cloud-output --namespace=default --method=POST
