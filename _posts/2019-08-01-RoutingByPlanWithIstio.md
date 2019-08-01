---
layout: post
date: 2019-08-01 09:00:00
categories: APIConnect
title: 'Using API Connect to allow Istio to route by plan'
image:  '/images/2019-08-01-istio.png'
tags: [ "Claudio Tag", "Tim Quigly"]
author: "Claudio Tag, Tim Quigly and Chris Phillips"
youtubeId: 53o15ESfpdM
---

API Connect allows an Application to subscribe to one plan for a product. This is traditionally used to determine which rate limit they are allowed to subscribe to. A couple of years ago Chris wrote an article on how to use this for plan variable to route to specific endpoints. []()  Istio provides the facility to route to different endpoints depending on header variables. This article shows how you can take the plan from a context variable and set it to a header to be picked up by Istio.

## What is a Service Mesh and Istio?
*Taken from a future publication*
In traditional applications, communication patterns are usually built into application code and service endpoint configuration is usually statically defined per environment.

As application componentisation grows and applications become more cloud-native, so does the number of components on the network. These components, often called services, typically expose APIs to be consumable by other services. Service-to-service communication in cloud native world is dramatically more complex than in traditional IT.

Therefore, there is a requirement for an additional infrastructure layer that helps manage communication between complex applications consisting of a large number of distinct services. Such a layer is usually called a service mesh.

It is important to note that a service mesh is not an overlay network. A service mesh simplifies and enhances how service communicate over the network provided by the underlying platform.

The aim of a service mesh is to abstract that complexity away from applications and their components, and to manage it at cloud-native infrastructure level. As such, a service mesh is a cloud-native infrastructure layer which handles communication between services, and allows reliable delivery of requests across services.

At a high level, a service mesh is responsible for:
* providing efficient communication between services,
* abstracting the mechanism for reliable request/response delivery from the application code,
* allowing management of services, independently from their number and growth rate,
* handling network failures,
* providing visibility and control of the service-to-service communication.

More specifically, typical functional requirements for a service mesh are:
* Service discovery
* Service registry
* Traffic management
* Traffic encryption
* Observability and traceability
* Authentication and authorisation
* Failure recovery

Often a service mesh also has more complex operational requirements, like A/B testing, canary rollouts, rate limiting, access control, and end-to-end encryption.
From a non-functional point of view, all these capabilities are available to applications and their components without impacting the application code, so that developers can leverage them without having to instrument their code.

Finally, a typical building block of cloud-native infrastructure is a container orchestration platform, as Kuberentes. For this reason, it is expected from a service mesh to be able to interact natively with Kubernetes controllers and resources, and to enhance their functionality, when it comes to service-to-service communication.


Istio ([https://istio.io](https://istio.io)) is one of the most popular technology implementations for a service mesh. Istio is a Kubernetes-compatible open platform for providing a uniform way to integrate microservices, manage traffic flow across microservices, enforce policies and aggregate telemetry data.
In short, Istio allows to connect, secure, control, and observe microservices running on Kubernetes.


## Writing the API and Product Logic
In order for this to work the keyword that Istio will look for will be the name as the name of the plan. Please note this is not the title.



### Product Sample

In the example below `plan1` will be picked up and sent to istio.

<button class="collapsible" id="yaml2">Click here for the example.</button>

<div class="content" id="yaml2data" markdown="1">

```yaml
plan1:
  rate-limits:
    default:
      value: 100/1minute
  title: PLAN1
  description: First Plan
  approval: false
```
</div>
Complete sample available at the end of the document

### API Sample

The API Logic is extract the plan value from the context variable, set it as a header and invoke the proxy. The core logic from the yaml is below.


<button class="collapsible" id="yaml3">Click here for the example.</button>

<div class="content" id="yaml3data" markdown="1">

```yaml
- set-variable:
    version: 1.0.0
    title: set-variable
    actions:
      - value: $(plan.name)
        set: message.headers.X-PLAN
- proxy:
    title: proxy
    version: 1.0.0
    verb: GET
    target-url: $(target-url)/theInfo
```
</div>

And a screenshoot from the UI.

![](/images/2019-06-07-assembly.png)

The complete sample is available at the end of this article.


## Istio configuration

<span style="float:left; margin-right:5px; margin-left:5px"> <img src="/images/2019-08-01-istio.png" /></span>

In your istio-enabled namespace, create a Kubernetes service, an Istio virtual service and two Istio destination rules, each pointing at the different Kubernetes deployments that you want to connect to.

The Kubernetes Service will have a label selector which we’ll use to point at the two deployments.
The K8s Service will look like this, where the label selector is `istio-plan`.

<button class="collapsible" id="yamlK8s-service.yaml">Click here for the K8s-service.yaml</button>

<div class="content" id="yamlK8s-service.yamldata" markdown="1">
```yaml
# Kubernetes Service
apiVersion: v1
kind: Service
metadata:
  name: istio-plan-routing-svc
  labels:
    istio: istio-plan-routing
spec:
  type: ClusterIP
  ports:
  - port: < Port number for the service >
    targetPort: < Target port number for the service >
    protocol: TCP
    name: http-istio
  selector:
    istio: istio-plan
```
</div>


The Istio Virtual Service will point at the K8s service, and in addition will:
- match the header in the API invocation, mapping the plan name, to the subset in the destination rules.
- weight the traffic distribution across the two deployments.  In this case 100% on one or the other.


<button class="collapsible" id="yamlvirtual-service.yaml">Click here for the virtual-service.yaml</button>

<div class="content" id="yamlvirtual-service.yamldata" markdown="1">
```yaml
# Virtual Service
apiVersion: networking.istio.io/v1alpha3
kind: VirtualService
metadata:
  name: istio-plan-routing-vs
spec:
  hosts:
  - "*"
  gateways:
  - < Istio Ingress Gateway >
  http:
  # Match sends ALL traffic with the PLAN1 header
  - match:
    - headers:
        X-PLAN:
          exact: PLAN1
    route:
    - destination:
        port:
          number: < Port number for the service >
        host: istio-plan-routing-svc
        subset: PLAN1
      weight: 100
    - destination:
        port:
          number: < Port number for the service >
        host: istio-plan-routing-svc
        subset: PLAN2
      weight: 0
    # Match sends ALL traffic with the PLAN2 header
  - match:
    - headers:
        X-PLAN:
          exact: PLAN2
    route:
    - destination:
        port:
          number: < Port number for the service >
        host: istio-plan-routing-svc
        subset: PLAN1
      weight: 0
    - destination:
        port:
          number: < Port number for the service >
        host: istio-plan-routing-svc
        subset: PLAN2
      weight: 100
```
</div>

The Destination Rules will:
- reference to the K8s service.
- create a subset pointing at one specific deployment.
- Enforce encryption policies. E.g. Mutual TLS.


<button class="collapsible" id="yamldestination-rules.yaml">Click here for the destination-rules.yaml.</button>

<div class="content" id="yamldestination-rules.yamldata" markdown="1">
```yaml
# Destination Rule 1
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: istio-plan-routing-dr1
spec:
  host: istio-plan-routing-svc
  subsets:
  - name: PLAN1
    labels:
      version: PLAN1
  trafficPolicy:
    tls:
      #mode: ISTIO_MUTUAL
      mode: < value to enable mutual TLS >

---
# Destination Rule 2
apiVersion: networking.istio.io/v1alpha3
kind: DestinationRule
metadata:
  name: istio-plan-routing-dr2
spec:
  host: istio-plan-routing-svc
  subsets:
  - name: PLAN2
    labels:
      version: PLAN2
  trafficPolicy:
    tls:
      #mode: ISTIO_MUTUAL
      mode: < value to enable mutual TLS >
```
</div>

For all of it to work, make sure to label your deployments with:
- the label for the K8s service to select them. E.g. `istio-plan` for both deployments.
- the destination rule's subset value. E.g. `PLAN1` for one deployment, and `PLAN2` for the other.





## Links
* Samples on GitHub (Coming)
* [Learn more about Istio](https://istio.io)


## Samples
### Product Sample

<button class="collapsible" id="yaml">Click here for the sample.</button>

<div class="content" id="yamldata" markdown="1">

```yaml

info:
  name: istoRoutingSample-product
  title: istoRoutingSample product
  version: 1.0.0
gateways:
  - datapower-gateway
plans:
  default-plan:
    rate-limits:
      default:
        value: 100/1hour
    title: Default Plan
    description: Default Plan
    approval: false
  plan1:
    rate-limits:
      default:
        value: 100/1minute
    title: PLAN1
    description: First Plan
    approval: false
  plan2:
    title: PLAN2
    description: Everything Else Plan
    approval: false
    rate-limits:
      default:
        value: 3/1minute
        hard-limit: true
    burst-limits: {}
apis:
  istoRoutingSample1.0.0:
    $ref: istoRoutingSample_1.0.0.yaml
visibility:
  view:
    type: public
    orgs: []
    enabled: true
  subscribe:
    type: authenticated
    orgs: []
    enabled: true
product: 1.0.0

```
</div>
### API Sample

<button class="collapsible" id="yaml4">Click here for the Sample.</button>

<div class="content" id="yaml4data" markdown="1">

```yaml
swagger: '2.0'
info:
  title: istoRoutingSample
  x-ibm-name: istoRoutingSample
  version: 1.0.0
schemes:
  - http
  - https
basePath: /IstoRoutingSample/v2
security:
  - clientID: []
securityDefinitions:
  clientID:
    type: apiKey
    in: header
    name: X-IBM-Client-Id
x-ibm-configuration:
  properties:
    target-url:
      value: 'https://ISTIOTargetHost0/simpleinfoapp/v1'
      description: URL of the proxy policy
      encoded: false
  cors:
    enabled: true
  gateway: datapower-gateway
  type: rest
  phase: realized
  enforced: true
  testable: true
  assembly:
    execute:
      - set-variable:
          version: 1.0.0
          title: set-variable
          actions:
            - value: $(plan.name)
              set: message.headers.X-PLAN
      - proxy:
          title: proxy
          version: 1.0.0
          verb: GET
          target-url: $(target-url)/theInfo
    catch:
      - errors: []
        execute: []
  application-authentication:
    certificate: false
definitions:
  env data model:
    type: object
    properties:
      inputVar:
        type: string
      targetEndPoint:
        type: string
      soapReqDest:
        type: string
paths:
  /theInfo:
    get:
      operationId: gettheInfo
      responses:
        '200':
          description: The operation was successful.
          schema:
            $ref: '#/definitions/env data model'
      produces:
        - application/json
      description: Retrieve theInfo
      parameters:
        - name: varName
          in: query
          type: string
          description: Name of the backend service
```
</div>

### Demo Video

{% include youtube.html id=page.youtubeId %}
