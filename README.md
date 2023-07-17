# Functions as a Service for Distributed Deep Neural Network inference over the Cloud-to-Things continuum

> The use of serverless computing has been gaining popularity in recent years as
> an alternative to traditional Cloud computing. We explore the usability and
> developer experience of three popular open-source serverless platforms in the
> context of IoT: OpenFaaS, Fission, and OpenWhisk. We also discuss our
> experience developing a serverless and low-latency Distributed Deep Neural
> Network (DDNN) application. Our findings indicate that these serverless
> platforms are developer-friendly and reduce the time to market of
> applications, but require significant resources to operate and are not ideal
> for constrained devices. In addition, we archived a 55\% improvement compared
> to Kafka-ML's performance under load, a framework without dynamic scaling
> support, demonstrating the potential of serverless computing for low-latency
> applications.

<!--
## Citation

TBD
-->

## Project structure

This repository is organized into the following directories:

- [ddnn](ddnn): Contains Kubernetes objects, Helm values, and scripts used for
  the first benchmark, "Evaluating serverless platforms for DDNN inference over
  the Cloud-to-Things continuum".
- [ddnn2](ddnn2): Contains Kubernetes objects, Helm values, and scripts used for
  the second benchmark, "Reevaluating serverless platforms for DDNN inference:
  Removing the Edge".
- [docs](docs): Provides documentation, Helm values, and helper scripts for
  deploying various Kubernetes applications (in Spanish).
- [Fission](Fission): Includes example functions implemented in Fission
  serverless platform.
- [integration](integration): Demonstrates the integration of serverless
  platforms with Kafka-ML.
- [jupyter](jupyter): Contains Jupyter notebooks for benchmark analysis.
- [k6](k6): Provides Kubernetes objects and scripts for K6s load testing.
- [kafka-connector](kafka-connector): Contains the source code for the Kafka
  connector.
- [kafkaml](kafkaml): Includes TensorFlow MINST models for Kafka-ML DDNN
  training.
- [OpenFaaS](OpenFaaS): Includes example functions implemented in OpenFaaS
  serverless platform.
- [OpenWhisk](OpenWhisk): Includes example functions implemented in OpenWhisk
  serverless platform.
- [scripts](scripts): Contains helper scripts for working with Kafka.

## [License](LICENSE)

MIT License

Copyright (c) 2023 ERTIS Research Group
