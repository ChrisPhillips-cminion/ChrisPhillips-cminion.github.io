---
layout: post
date: 2020-6-22 00:02:00
categories: APIConnect
title: "APIConnect v10  - DataPower Pods are not created after Gateway CR is applied"
---

When installing gateway pods this can fail stale webhooks are not cleaned up first.

<!--more-->
# Symptons

1. DataPower CR is applied but nothing happens.
2. The API connect Operator has an error message similar to

```
{"level":"error","ts":"2020-06-23T14:24:48.464Z","logger":"controller-runtime.controller","msg":"Reconciler error","controller":"gatewaycluster-controller","request":"apic/gwv5","error":"Internal error occurred: failed calling webhook \"datapowerservices.validator.datapower.ibm.com\": Post https://datapower-operator.apic.svc:443/validate-datapower-ibm-com-v1beta1-datapowerservice?timeout=2s: x509: certificate signed by unknown authority (possibly because of \"crypto/rsa: verification error\" while trying to verify candidate authority certificate \"datapower-operator-ca\")","stacktrace":"github.com/go-logr/zapr.(*zapLogger).Error\n\t/home/jenkins/go/pkg/mod/github.com/go-logr/zapr@v0.1.1/zapr.go:128\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).reconcileHandler\n\t/home/jenkins/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.5.2/pkg/internal/controller/controller.go:258\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).processNextWorkItem\n\t/home/jenkins/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.5.2/pkg/internal/controller/controller.go:232\nsigs.k8s.io/controller-runtime/pkg/internal/controller.(*Controller).worker\n\t/home/jenkins/go/pkg/mod/sigs.k8s.io/controller-runtime@v0.5.2/pkg/internal/controller/controller.go:211\nk8s.io/apimachinery/pkg/util/wait.JitterUntil.func1\n\t/home/jenkins/go/pkg/mod/k8s.io/apimachinery@v0.17.4/pkg/util/wait/wait.go:152\nk8s.io/apimachinery/pkg/util/wait.JitterUntil\n\t/home/jenkins/go/pkg/mod/k8s.io/apimachinery@v0.17.4/pkg/util/wait/wait.go:153\nk8s.io/apimachinery/pkg/util/wait.Until\n\t/home/jenkins/go/pkg/mod/k8s.io/apimachinery@v0.17.4/pkg/util/wait/wait.go:88"}
```

The actual error is
```
,"error":"Internal error occurred: failed calling webhook \"datapowerservices.validator.datapower.ibm.com\": Post https://datapower-operator.apic.svc:443/validate-datapower-ibm-com-v1beta1-datapowerservice?timeout=2s: x509: certificate signed by unknown authority (possibly because of \"crypto/rsa: verification error\" while trying to verify candidate authority certificate \"datapower-operator-ca\")"
```


This problems is caused by stale webhooks. The solotuion to this problem can be found here [https://ibm.github.io/datapower-operator-doc/troubleshooting/stale-webhooks](https://ibm.github.io/datapower-operator-doc/troubleshooting/stale-webhooks)

Then delete both the  datapower operator and apiconnect operator pod to force them to restart.

Now you will  need to remove the DataPower CR and apply it again.

DataPower should start deploying its pods.