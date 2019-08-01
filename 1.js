{
  attempts: 180,
  changed: false,
  module_results: {
    cmd: /usr/bin / oc get node--selector = -o json - n
    default,
    results: [{
      apiVersion: v1,
      items: [{
        apiVersion: v1,
        kind: Node,
        metadata: {
          annotations: {
            volumes.kubernetes.io / controller - managed - attach - detach: true
          },
          creationTimestamp: 2019 - 07 - 29 T21: 56: 25 Z,
          labels: {
            beta.kubernetes.io / arch: amd64,
            beta.kubernetes.io / os: linux,
            kubernetes.io / hostname: banana.phillips11.cf
          },
          name: banana.phillips11.cf,
          namespace: ,
          resourceVersion: 4609,
          selfLink: /api/v1 / nodes / banana.phillips11.cf,
          uid: b5fce2d4 - b24b - 11e9 - 8 bd5 - 00e04 c68524f
        },
        spec: {},
        status: {
          addresses: [{
            address: 10.200 .0 .12,
            type: InternalIP
          }, {
            address: banana.phillips11.cf,
            type: Hostname
          }],
          allocatable: {
            cpu: 8,
            hugepages - 1 Gi: 0,
            hugepages - 2 Mi: 0,
            memory: 32278736 Ki,
            pods: 250
          },
          capacity: {
            cpu: 8,
            hugepages - 1 Gi: 0,
            hugepages - 2 Mi: 0,
            memory: 32381136 Ki,
            pods: 250
          },
          conditions: [{
            lastHeartbeatTime: 2019 - 07 - 29 T22: 27: 38 Z,
            lastTransitionTime: 2019 - 07 - 29 T21: 56: 25 Z,
            message: kubelet has sufficient disk space available,
            reason: KubeletHasSufficientDisk,
            status: False,
            type: OutOfDisk
          }, {
            lastHeartbeatTime: 2019 - 07 - 29 T22: 27: 38 Z,
            lastTransitionTime: 2019 - 07 - 29 T21: 56: 25 Z,
            message: kubelet has sufficient memory available,
            reason: KubeletHasSufficientMemory,
            status: False,
            type: MemoryPressure
          }, {
            lastHeartbeatTime: 2019 - 07 - 29 T22: 27: 38 Z,
            lastTransitionTime: 2019 - 07 - 29 T21: 56: 25 Z,
            message: kubelet has no disk pressure,
            reason: KubeletHasNoDiskPressure,
            status: False,
            type: DiskPressure
          }, {
            lastHeartbeatTime: 2019 - 07 - 29 T22: 27: 38 Z,
            lastTransitionTime: 2019 - 07 - 29 T21: 56: 25 Z,
            message: kubelet has sufficient PID available,
            reason: KubeletHasSufficientPID,
            status: False,
            type: PIDPressure
          }, {
            lastHeartbeatTime: 2019 - 07 - 29 T22: 27: 38 Z,
            lastTransitionTime: 2019 - 07 - 29 T21: 56: 25 Z,
            message: runtime network not ready: NetworkReady = false reason: NetworkPluginNotReady message: docker: network plugin is not ready: cni config uninitialized,
            reason: KubeletNotReady,
            status: False,
            type: Ready
          }],
          daemonEndpoints: {
            kubeletEndpoint: {
              Port: 10250
            }
          },
          nodeInfo: {
            architecture: amd64,
            bootID: a8362430 - 556 f - 4 dcc - 9 c1b - 2 bf23dcf21ad,
            containerRuntimeVersion: docker1 .13 .1,
            kernelVersion: 5.1 .18 - 200. fc29.x86_64,
            kubeProxyVersion: v1 .10 .0 + d4cacc0,
            kubeletVersion: v1 .10 .0 + d4cacc0,
            machineID: 121 c7bd4ac504b11a824b913e541c06e,
            operatingSystem: linux,
            osImage: Fedora 29(Twenty Nine),
            systemUUID: fe933acc - 2 f8d - 11 b2 - a85c - 9e6 b63f15df6
          }
        }
      }, {
        apiVersion: v1,
        kind: Node,
        metadata: {
          annotations: {
            node.openshift.io / md5sum: 750 d932dc11c24e30370add98002d396,
            volumes.kubernetes.io / controller - managed - attach - detach: true
          },
          creationTimestamp: 2019 - 07 - 29 T21: 53: 23 Z,
          labels: {
            beta.kubernetes.io / arch: amd64,
            beta.kubernetes.io / os: linux,
            kubernetes.io / hostname: random.phillips11.cf,
            node - role.kubernetes.io / compute: true,
            node - role.kubernetes.io / infra: true,
            node - role.kubernetes.io / master: true
          },
          name: random.phillips11.cf,
          namespace: ,
          resourceVersion: 4622,
          selfLink: /api/v1 / nodes / random.phillips11.cf,
          uid: 4956 f60b - b24b - 11e9 - 8 bd5 - 00e04 c68524f
        },
        spec: {},
        status: {
          addresses: [{
            address: 10.200 .0 .17,
            type: InternalIP
          }, {
            address: random.phillips11.cf,
            type: Hostname
          }],
          allocatable: {
            cpu: 16,
            hugepages - 1 Gi: 0,
            hugepages - 2 Mi: 0,
            memory: 32845276 Ki,
            pods: 250
          },
          capacity: {
            cpu: 16,
            hugepages - 1 Gi: 0,
            hugepages - 2 Mi: 0,
            memory: 32947676 Ki,
            pods: 250
          },
          conditions: [{
            lastHeartbeatTime: 2019 - 07 - 29 T22: 27: 45 Z,
            lastTransitionTime: 2019 - 07 - 29 T21: 53: 23 Z,
            message: kubelet has sufficient disk space available,
            reason: KubeletHasSufficientDisk,
            status: False,
            type: OutOfDisk
          }, {
            lastHeartbeatTime: 2019 - 07 - 29 T22: 27: 45 Z,
            lastTransitionTime: 2019 - 07 - 29 T21: 53: 23 Z,
            message: kubelet has sufficient memory available,
            reason: KubeletHasSufficientMemory,
            status: False,
            type: MemoryPressure
          }, {
            lastHeartbeatTime: 2019 - 07 - 29 T22: 27: 45 Z,
            lastTransitionTime: 2019 - 07 - 29 T21: 53: 23 Z,
            message: kubelet has no disk pressure,
            reason: KubeletHasNoDiskPressure,
            status: False,
            type: DiskPressure
          }, {
            lastHeartbeatTime: 2019 - 07 - 29 T22: 27: 45 Z,
            lastTransitionTime: 2019 - 07 - 29 T21: 53: 23 Z,
            message: kubelet has sufficient PID available,
            reason: KubeletHasSufficientPID,
            status: False,
            type: PIDPressure
          }, {
            lastHeartbeatTime: 2019 - 07 - 29 T22: 27: 45 Z,
            lastTransitionTime: 2019 - 07 - 29 T21: 56: 33 Z,
            message: kubelet is posting ready status,
            reason: KubeletReady,
            status: True,
            type: Ready
          }],
          daemonEndpoints: {
            kubeletEndpoint: {
              Port: 10250
            }
          },
          images: [{
            names: [docker.io / openshift / origin - node @sha256: 170888 a5ffd34a25649367313ef4c8c3c379d762e0f227189fd14c2377ef3417, docker.io / openshift / origin - node: v3 .11],
            sizeBytes: 1173006907
          }, {
            names: [docker.io / openshift / origin - control - plane @sha256: e48b7433f6f123f92f2f3d14f5786620718babe883f865b7cf4deb4252fd1e49, docker.io / openshift / origin - control - plane: v3 .11],
            sizeBytes: 828832649
          }, {
            names: [docker.io / cockpit / kubernetes @sha256: f38c7b0d2b85989f058bf78c1759bec5b5d633f26651ea74753eac98f9e70c9b, docker.io / cockpit / kubernetes: latest],
            sizeBytes: 335808186
          }, {
            names: [docker.io / openshift / origin - pod @sha256: 0 c86f2d08bd25de3992182b171becbca048fb1868f1655798dc0b247acdf85da, docker.io / openshift / origin - pod: v3 .11, docker.io / openshift / origin - pod: v3 .11 .0],
            sizeBytes: 261540611
          }, {
            names: [quay.io / coreos / etcd @sha256: 43 fbc8a457aa0cb887da63d74a48659e13947cb74b96a53ba8f47abb6172a948, quay.io / coreos / etcd: v3 .2 .22],
            sizeBytes: 37269372
          }],
          nodeInfo: {
            architecture: amd64,
            bootID: e51035ca - 3 ba4 - 4 d93 - b7ee - 65 d3a4a4c018,
            containerRuntimeVersion: docker: 1.13 .1,
            kernelVersion: 5.1 .18 - 200. fc29.x86_64,
            kubeProxyVersion: v1 .10 .0 + d4cacc0,
            kubeletVersion: v1 .10 .0 + d4cacc0,
            machineID: 35 a97cef8e7e4fada6e8efe9ab0a6922,
            operatingSystem: linux,
            osImage: Fedora 29(Twenty Nine),
            systemUUID: 03 d502e0 - 045e-0524 - 8 a06 - b60700080009
          }
        }
      }, {
        apiVersion: v1,
        kind: Node,
        metadata: {
          annotations: {
            node.openshift.io / md5sum: 32 ae361b122c8a26a133736689eaf26e,
            volumes.kubernetes.io / controller - managed - attach - detach: true
          },
          creationTimestamp: 2019 - 07 - 29 T21: 56: 25 Z,
          labels: {
            beta.kubernetes.io / arch: amd64,
            beta.kubernetes.io / os: linux,
            kubernetes.io / hostname: randomstore.phillips11.cf,
            node - role.kubernetes.io / compute: true
          },
          name: randomstore.phillips11.cf,
          namespace: ,
          resourceVersion: 4618,
          selfLink: /api/v1 / nodes / randomstore.phillips11.cf,
          uid: b5f06a95 - b24b - 11e9 - 8 bd5 - 00e04 c68524f
        },
        spec: {},
        status: {
          addresses: [{
            address: 10.200 .0 .14,
            type: InternalIP
          }, {
            address: randomstore.phillips11.cf,
            type: Hostname
          }],
          allocatable: {
            cpu: 4,
            hugepages - 1 Gi: 0,
            hugepages - 2 Mi: 0,
            memory: 7713032 Ki,
            pods: 250
          },
          capacity: {
            cpu: 4,
            hugepages - 1 Gi: 0,
            hugepages - 2 Mi: 0,
            memory: 7815432 Ki,
            pods: 250
          },
          conditions: [{
            lastHeartbeatTime: 2019 - 07 - 29 T22: 27: 43 Z,
            lastTransitionTime: 2019 - 07 - 29 T21: 56: 25 Z,
            message: kubelet has sufficient disk space available,
            reason: KubeletHasSufficientDisk,
            status: False,
            type: OutOfDisk
          }, {
            lastHeartbeatTime: 2019 - 07 - 29 T22: 27: 43 Z,
            lastTransitionTime: 2019 - 07 - 29 T21: 56: 25 Z,
            message: kubelet has sufficient memory available,
            reason: KubeletHasSufficientMemory,
            status: False,
            type: MemoryPressure
          }, {
            lastHeartbeatTime: 2019 - 07 - 29 T22: 27: 43 Z,
            lastTransitionTime: 2019 - 07 - 29 T21: 56: 25 Z,
            message: kubelet has no disk pressure,
            reason: KubeletHasNoDiskPressure,
            status: False,
            type: DiskPressure
          }, {
            lastHeartbeatTime: 2019 - 07 - 29 T22: 27: 43 Z,
            lastTransitionTime: 2019 - 07 - 29 T21: 56: 25 Z,
            message: kubelet has sufficient PID available,
            reason: KubeletHasSufficientPID,
            status: False,
            type: PIDPressure
          }, {
            lastHeartbeatTime: 2019 - 07 - 29 T22: 27: 43 Z,
            lastTransitionTime: 2019 - 07 - 29 T21: 56: 50 Z,
            message: kubelet is posting ready status,
            reason: KubeletReady,
            status: True,
            type: Ready
          }],
          daemonEndpoints: {
            kubeletEndpoint: {
              Port: 10250
            }
          },
          images: [{
            names: [docker.io / openshift / origin - node @sha256: 170888 a5ffd34a25649367313ef4c8c3c379d762e0f227189fd14c2377ef3417, docker.io / openshift / origin - node: v3 .11],
            sizeBytes: 1173006907
          }, {
            names: [docker.io / rook / ceph @sha256: 15 ea6316e32053e807170d80cce42c34d6e952452087d4999dfd150dcbf1c728, docker.io / rook / ceph: master],
            sizeBytes: 920744489
          }, {
            names: [docker.io / ceph / ceph @sha256: 43 d62cfba07ef79b66068c53346be8e6fe2d21cf22c7ac3cdd967a188b4d5c7f, docker.io / ceph / ceph: v14 .2 .2 - 20190722],
            sizeBytes: 849090159
          }, {
            names: [registry.access.redhat.com / amqstreams - 1 / amqstreams10 - clusteroperator - openshift @sha256: ee3a689122ac473cfc71f46183ed7c8afc6351b151aa9db46c00ebd2da544803, registry.access.redhat.com / amqstreams - 1 / amqstreams10 - clusteroperator - openshift: 1.0 .0],
            sizeBytes: 427548108
          }, {
            names: [docker.io / openshift / origin - pod @sha256: 0 c86f2d08bd25de3992182b171becbca048fb1868f1655798dc0b247acdf85da, docker.io / openshift / origin - pod: v3 .11, docker.io / openshift / origin - pod: v3 .11 .0],
            sizeBytes: 261540611
          }, {
            names: [quay.io / coreos / kube - rbac - proxy @sha256: a578315f24e6fd01a65e187e4d1979678598a7d800d039ee5cfe4e11b0b1788d, quay.io / coreos / kube - rbac - proxy: v0 .3 .1],
            sizeBytes: 40160345
          }],
          nodeInfo: {
            architecture: amd64,
            bootID: ecad113b - 2 dd5 - 433 a - 85 c4 - 3 be66d702a0a,
            containerRuntimeVersion: docker1 .13 .1,
            kernelVersion: 5.1 .18 - 200. fc29.x86_64,
            kubeProxyVersion: v1 .10 .0 + d4cacc0,
            kubeletVersion: v1 .10 .0 + d4cacc0,
            machineID: f56cf4ae58134f8a91ce67da91550015,
            operatingSystem: linux,
            osImage: Fedora 29(Twenty Nine),
            systemUUID: 03000200 - 0400 - 0500 - 0006 - 000700080009
          }
        }
      }],
      kind: List,
      metadata: {
        resourceVersion: ,
        selfLink:
      }
    }],
    returncode: 0
  },
  state: list
}
