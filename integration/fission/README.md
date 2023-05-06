Integration between Fission and Kafka-ML

# Usage

```sh
# Build the image
docker build -t inference-env .
# Create the environment
fission env create --image inference-env --name tensorflow --poolsize=0 --version=3
# Create the function
fission fn create --name example --env tensorflow --deployarchive 'model.h5' --executortype newdeploy
```
