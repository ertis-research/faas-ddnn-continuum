# Commands used to generate `specs/`
# Create the environment
fission env create --spec \
 --name python \
 --image fission/python-env \
 --builder fission/python-builder
# Create the function
fission fn create --spec \
 --name redis-glue \
 --env python \
 --src 'src/*' \
 --entrypoint 'main.main' \
 --configmap redis-glue
# Create the route
fission route create --spec \
 --method POST \
 --url /redis-glue \
 --function redis-glue
