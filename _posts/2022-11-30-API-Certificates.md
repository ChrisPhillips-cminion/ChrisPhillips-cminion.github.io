---
layout: post
date: 2022-10-19 02:01:00
categories: DataPower
title: "Global disabling of Certificate Expiry validation"
author: [  "RGeorgeInness", "ChrisPhillips" ]
draft: true
---

API Connect has a number of certificates. I have been asked by a couple of clients what happens when individual certs expire. This table goes through the certificates and what the impact on them expiring is.
<!--more-->
|---|---|---|---|
| Component	| Cert Name	| MTLS Client, MTLS Server, TLS or Signer	| Description |
Analytics	a7s-ai-endpoint	MTLS Server	MTLS Server certficate for the analytics ingestion endpoint
Analytics	a7s-ca	Signer	Signer for all Analytics certificates
Analytics	a7s-client	MTLS Server	MTLS Server endpoint for the analytics data endpont
Analytics	a7s-server	TLS	Endpoint used to secure communications inside of A7s
API Manager	a7s-cl-client	MTLS Clent	MTLS  Client endpoint to secure communication with Analytics dataendpoint
API Manager	a7s-ing-client	MTLS Clent	MTLS  Client endpoint to secure communication with Analytics Ingestion
API Manager	event-gateway-management-client	MTLS Clent	MTLS  Client endpoint to secure communication with Event Gateway
API Manager	gw-dr-client	MTLS Clent	MTLS  Client endpoint to secure communication with the Datapower Director
API Manager	mgmt-70c12077-postgres	TLS 	Postgress
API Manager	mgmt-70c12077-postgres-pgbouncer	TLS 	Postgress
API Manager	mgmt-admin	TLS 	Used to expose the  Cloud manager UI
API Manager	mgmt-api-manager	TLS 	Used to expose the Api manager UI
API Manager	mgmt-ca	Signer	Signer for all management certificates
API Manager	mgmt-client	TLS 	??
API Manager	mgmt-consumer-api	TLS 	Used to expose the Consumer Rest Interface
API Manager	mgmt-db-client-apicuser	TLS 	Postgress
API Manager	mgmt-db-client-pgbouncer	TLS 	Postgress
API Manager	mgmt-db-client-postgres	TLS 	Postgress
API Manager	mgmt-db-client-primaryuser	TLS 	Postgress
API Manager	mgmt-db-client-replicator	TLS 	Postgress
API Manager	mgmt-natscluster-mgmt	TLS 	Nats Cluster
API Manager	mgmt-platform-api	TLS 	Used to expose the Provider Rest Interface
API Manager	mgmt-server	TLS 	??
API Manager	postgres-operator	TLS	Postgress
API Manager	ptl-adm-client	MTLS Clent	MTLS  Client endpoint to secure communication with the Portal Director
Gateway	gw-gateway	TLS	??
Gateway	gw-gateway-manager	MTLS Server	MTLS Server endpoint for the  Gateway Director endpont
Gateway	gw-peer	TLS 	Certificate used to communicate between peers
Gateway	gw-svc	TLS 	??
General	ingress-ca	Signer	Parent Signer
Portal	ptl-ca	Signer	Portal Signer
Portal	ptl-client	MTLS Clent	??
Portal	ptl-portal-director	MTLS Server	MTLS Server endpoint for the  Portal Director endpont
Portal	ptl-portal-web	TLS	Used to expose the Dev Portal sites
Portal	ptl-server	TLS	??
