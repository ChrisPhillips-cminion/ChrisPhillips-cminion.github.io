---
layout: post
date: 2019-09-06 01:00:00
categories: Kubernetes
title: "Accessing Custom Resource Definitions (CRD) without a code generator "
Location: "St Andrew's Church - Eastleigh"
---

Custom Resource Definitions are custom data types in Kubernetes. For a project I am working on (that will be posted soon i hope) I created three CRDs and read/write/update them from a Go Application.  The instructions on how to do this with out using a complex code generator was hard to find.

<!--more-->

First of all we need to create the `clientset` in order to communicate with the kubernetes.
```go
kubeconfig := "/Users/chris/.kube/config"
config, err := clientcmd.BuildConfigFromFlags("", kubeconfig)
if err != nil {
  panic(err.Error())
}
clientset, err := kubernetes.NewForConfig(config)
if err != nil {
  panic(err.Error())
}
```
The above code will only work from a client machine. There are numerious instructions on how to do it from inside of a container.

### Get

The sample code below acceses `v1` of my CRD  `nodescost`, that is part of group `cminion.com`.
```go
d, err := clientset.RESTClient().Get().AbsPath("apis/cminion.com/v1/nodescost").DoRaw()
if err != nil {
  panic(err.Error())
}
```

`d` is the json that is returned contain the object. I then unmarshall it to make it easier to work with.

```go
err = json.Unmarshal(d, &nodescost)
```

### Post

To POST uses a very simlar command. Firstly we Marshal the Object (`newItem`) and then we take the `byte[]` json and pass it in as a Body parameter.  If the JSON cannot be processed `b` contains the error. If there is a connectivity or Kubernetes issue `err` contains the error message. **Check Both.**

```go
json, err := json.Marshal(newItem)
if err != nil {
  panic(err.Error())
}
if b, err := clientset.RESTClient().Post().AbsPath("apis/cminion.com/v1/nodescost").Body(json).DoRaw(); err != nil {
  fmt.Println(string(b))
  panic(err.Error())
}
```

### Put


The only difference between POST and PUT apart from changing the verb in the command is to add `.Name()` with the Object Instance name. If the JSON cannot be processed `b` contains the error. If there is a connectivity or Kubernetes issue `err` contains the error message. **Check Both.**

```go
json, err := json.Marshal(updateItem)
if err != nil {
  panic(err.Error())
}
if b, err := clientset.RESTClient().Put().AbsPath("apis/cminion.com/v1/nodescost").Name(i).Body(json).DoRaw(); err != nil {
  fmt.Println(string(b))
  panic(err.Error())
}
```
