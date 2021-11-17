---
layout: post
date: 2021-11-12 00:13:00
categories: APIConnect
title: "Adding a new API Gateway to an existing estate."
---

Recently I have had two customers come to me saying they are adding new API Gateway Service and they need a way to expose all of their existing APIs on these Gateways.


<!--more-->

I "hacked together" the following shell script.  *As ever this is provided with no support as a proof of concept. *



```shell
#############################################################
# This script will add all API Gateways in a catalogs to the
# APIs published. This is useful when adding a new GW Service
# and all APis need to be migrated to it.
#
#############################################################

user=chris.phillips@uk.ibm.com
password=pass
porg="bf4c934d-b92c-4e8f-8d63-2ad5247f3622"
realm=provider/blue-pages
org_admin_url=devext-mgr-apimgr.event.ibm.com

echo "-------------------"
echo " GetToken"
echo "-------------------"
access_token=$(curl -s "https://$org_admin_url/api/token" \
  -H 'Content-Type: application/json' \
	-H 'Accept: application/json' \
  --data-raw "{\"username\":\"$user\",\"password\":\"$password\",\"realm\":\"$realm\",\"client_id\":\"6e47ebcd-58fa-4de0-ba5e-ada2c3689a45\",\"client_secret\":\"3cc36a4f-089d-475a-b317-b86171853f76\",\"grant_type\":\"password\"}" \
  --compressed \
  --insecure | jq -r .access_token)
#echo $access_token
	echo "-------------------"
	echo " Get catalog list from all pOrgs"
	echo "-------------------"
catalog_list=$(curl -s "https://$org_admin_url/api/catalogs" \
  -H "Authorization: Bearer $access_token" \
	-H 'Accept: application/json' \
  --compressed \
  --insecure | jq -r .results[].id)
echo $catalog_list
echo "-------------------"
echo " Get GW Services"
echo "-------------------"
gatewaysvc_list=$(curl -s "https://$org_admin_url/api/orgs/$porg/gateway-services" \
  -H "Authorization: Bearer $access_token" \
	-H 'Accept: application/json' \
  --compressed \
  --insecure | jq -r .results[].url)
echo $gatewaysvc_list
for i in  $catalog_list ; do
	echo
	echo "-------------------"
	echo " Entering Catalog - ($i)"
	echo "-------------------"
	echo
	echo "-------------------"
	echo "   Getting Products from Catalog ($i)"
	echo "-------------------"
	product_list=$(curl -s "https://$org_admin_url/api/catalogs/$porg/$i/products?fields=id" \
  -H "authorization: Bearer $access_token" \
	-H 'Accept: application/json' \
  --compressed \
  --insecure | jq -r .results[].id)
	# echo $product_list
	for gws in  $gatewaysvc_list ; do
		echo
		echo "-------------------"
		echo "   Add GW Service ($gws) to catalog ($i)"
		echo "-------------------"
		addGW=$(curl -s "https://$org_admin_url/api/catalogs/$porg/$i/configured-gateway-services" \
		  -H "Authorization: Bearer $access_token " \
			-H 'Accept: application/json' \
			-H 'Content-Type: application/json' \
		  --data-raw "{\"gateway_service_url\":\"$gws\"}" \
		  --compressed \
		  --insecure | tr -d '\n')
			if [ "$(echo $addGW | jq .status)" != "null" ] ; then
				if [ "$(echo $addGW | jq .status)" == "409" ] ; then
					echo "GW already added no action"
				else
					echo $addGW
			  fi
			fi
	done
	echo
	echo "-------------------"
	echo "   Get configured-gateway-services  in  catalog ($i)"
	echo "-------------------"
	urlCGWS=$(curl -s "https://$org_admin_url/api/catalogs/$porg/$i/configured-gateway-services" \
		-H "Authorization: Bearer $access_token " \
		-H 'Accept: application/json' \
		-H 'Content-Type: application/json' \
		--compressed \
		--insecure | jq -r .results[].url)
	gwsList2=$(echo $urlCGWS | sed -e s/^/\"/ | sed -e s/\ /\",\"/g | sed -e s/$/\"/)

	for prod in  $product_list ; do
		echo
		echo "-------------------"
		echo "   Adding GWSs ($gwsList2) to Prod ($prod) in catalog ($i)"
		echo "-------------------"
		addProd=$(curl -s -q "https://$org_admin_url/api/catalogs/$porg/$i/products/$prod" \
		-X 'PATCH' \
		-H 'Content-Type: application/json' \
		-H 'Accept: application/json' \
		-H "Authorization: Bearer $access_token" \
		--data-raw "{\"gateway_service_urls\":[$gwsList2]}" \
		--compressed \
		--insecure | tr -d '\n')
		if [ "$(echo $addProd | jq .status)" != "null" ] ; then
			if [ "$(echo $addProd | jq .status)" == "400" ] ; then
				if [[ "$(echo $addProd | jq .message)" == *"empty because the product contains only unenforced APIs"* ]] ; then
			 		echo "Unenforced API - no action required"
				else
					echo $addProd
				fi
			else
				echo $addProd
		  fi
		fi
	done
done
```
