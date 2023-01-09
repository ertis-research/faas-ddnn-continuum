# Commands used to generate `specs/`
fission spec init
# Create the environment
fission env create --spec \
 --name python-newdeploy \
 --image fission/python-env \
 --poolsize=0 \
 --version=3 \
 --builder fission/python-builder
# Create the function
fission fn create --spec \
 --name redis-glue-newdeploy \
 --env python-newdeploy \
 --src 'src/*' \
 --entrypoint 'main.main' \
 --executortype newdeploy \
 --minscale 0 --maxscale 3 \
 --configmap redis-glue
# Create the route
fission route create --spec \
 --method POST \
 --url /redis-glue-newdeploy \
 --function redis-glue-newdeploy
