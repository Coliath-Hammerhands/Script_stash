```bash
helm install -f my-values.yaml k8s-mediaserver ./k8s-mediaserver-operator/helm-charts/k8s-mediaserver/
helm upgrade -f my-values.yaml k8s-mediaserver ./k8s-mediaserver-operator/helm-charts/k8s-mediaserver/
```



# Storage

The PVC needs something to bind to. I used [storage.yml](./storage.yml).

my command from documents
```bash
helm install -f Script_stash/Kubernetes/media_server/my-values.yaml k8s-mediaserver k8s-mediaserver-operator/helm-charts/k8s-mediaserver/
helm upgrade -f Script_stash/Kubernetes/media_server/my-values.yaml k8s-mediaserver k8s-mediaserver-operator/helm-charts/k8s-mediaserver/
```

```
helm uninstall k8s-mediaserver
```


THE PAIN WAS TOO DEEP AND I GAVE UP