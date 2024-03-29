#!/usr/bin/env bash

function k8s {
    name="$1"
    k8s_dir="$2"

    k8s_obj="$k8s_dir/$name.yml"

    kubectl delete -f "$k8s_obj" || true
    kubectl apply -f "$k8s_obj"
}

function uninstall_k8s {
    name="$1"
    k8s_dir="$2"

    k8s_obj="$k8s_dir/$name.yml"

    kubectl delete -f "$k8s_obj"
}
################################################################################
function openfaas {
    name="$1"
    k8s_dir="$2"

    values="$k8s_dir/openfaas/$name.yml"

    kubectl create namespace openfaas || true
    kubectl create namespace openfaas-fn || true
    helm upgrade openfaas --install openfaas/openfaas --namespace openfaas -f "$values" --version v12.0.2
}

function uninstall_openfaas {
    name="$1"

    helm uninstall openfaas --namespace openfaas
}
################################################################################

function fission {
    name="$1"
    k8s_dir="$2"

    values="$k8s_dir/fission/$name.yml"

    kubectl create namespace fission || true
    kubectl create -k "github.com/fission/fission/crds/v1?ref=v1.18.0" || true

    helm upgrade fission fission-charts/fission-all --install --version v1.18.0 --namespace fission -f "$values"
}

function uninstall_fission {
    name="$1"

    kubectl delete -k "github.com/fission/fission/crds/v1?ref=v1.18.0"
    helm uninstall fission --namespace fission
}
################################################################################
function kafka {
    name="$1"
    k8s_dir="$2"

    values_kafka="$k8s_dir/kafka/$name.yml"
    
    kubectl create namespace kafka || true
    helm upgrade --install kafka bitnami/kafka --namespace kafka -f "$values_kafka" --version v21.3.1
}

function uninstall_kafka {
    name="$1"

    helm uninstall kafka --namespace kafka
}
################################################################################

script_dir="$(dirname "$0")"
env_file="$script_dir/.env"
k8s_dir="$script_dir/k8s"

name="$1"

# Load env
export $(cat "$env_file" | xargs)

set -xeo pipefail

while getopts 'kKoOfFn:' c
do
  # echo "Processing $c : OPTIND is $OPTIND"
  case $c in
    n) name="$OPTARG" ;;
    k) kafka "$name" "$k8s_dir" ;;
    K) uninstall_kafka "$name" ;;
    o) openfaas "$name" "$k8s_dir" && k8s "openfaas-$name" "$k8s_dir" ;;
    O) uninstall_openfaas "$name" && uninstall_k8s "openfaas-$name" "$k8s_dir" ;;
    f) fission "$name" "$k8s_dir" && k8s "fission-$name" "$k8s_dir" ;;
    F) uninstall_fission "$name" && uninstall_k8s "fission-$name" "$k8s_dir" ;;
    *) 
        echo "USAGE -n LAYER_NAME"
        echo "-k/-K\tinstall/uninstall kafka"
        echo "-o/-O\tinstall/uninstall Openfaas"
        echo "-f/-F\tinstall/uninstall Fission"
        ;;
  esac
done
