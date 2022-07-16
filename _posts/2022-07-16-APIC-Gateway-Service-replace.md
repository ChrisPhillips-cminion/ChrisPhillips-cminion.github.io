---
layout: post
categories: APIConnect
date: 2022-07-16 00:14:00
title: Replacing an API Gateway Service in a provider org
---

Sometimes a client configures multiple provider orgs to share a single Gateway Service and then later on decides to change their mind. However this requires modifying every single API. This script will replace the currently configured gateway service for all APIs in a provider org and replace it with a new gateway service.

<!--more-->

```bash
#############################################################
# This script will add replace an API Gateways Service in
# for all APIs in a Porg
#
#############################################################

user=chris
password=Igash1sa
porg=ads
realm=provider/default-idp-2
platform_api_url=platform-api-cp4i.mycluster.eu-gb.containers.appdomain.cloud
gwsname=api-gateway-service2 # name not title of the gatewaysevice that you want to move all APIs in the porg to. this needs pre adding to the catalogs
clientsecret=d37729d0-6d48-4f94-8383-2bcfbdb92a53 # To get this please create a new registration object
clientid=968f1911-9025-4d28-9b13-8c73e20d5767  # To get this please create a new registration object

echo "-------------------"
echo " GetToken"
echo "-------------------"
access_token=$(curl -s "https://$platform_api_url/api/token" \
  -H 'Content-Type: application/json' \
	-H 'Accept: application/json' \
  --data-raw "{\"username\":\"$user\",\"password\":\"$password\",\"realm\":\"$realm\",\"client_id\":\"$clientid\",\"client_secret\":\"$clientsecret\",\"grant_type\":\"password\"}" \
  --compressed \
  --insecure | jq -r .access_token)
echo "-------------------"
echo " Get catalog list from all pOrgs"
echo "-------------------"
catalog_list=$(curl -s "https://$platform_api_url/api/catalogs" \
  -H "Authorization: Bearer $access_token" \
	-H 'Accept: application/json' \
  --compressed \
  --insecure | jq -r .results[].id)
echo $catalog_list
for i in  $catalog_list ; do
	echo
	echo "-------------------"
	echo " Entering Catalog - ($i)"
	echo "-------------------"
	echo
	echo "-------------------"
	echo "   Getting Products from Catalog ($i)"
	echo "-------------------"
	product_list=$(curl -s "https://$platform_api_url/api/catalogs/$porg/$i/products?fields=id" \
  -H "authorization: Bearer $access_token" \
	-H 'Accept: application/json' \
  --compressed \
  --insecure | jq -r .results[].id)
	# echo $product_list
	echo
	echo "-------------------"
	echo "   Get configured-gateway-services  in  catalog ($i)"
	echo "-------------------"
	urlCGWS=$(curl -s "https://$platform_api_url/api/catalogs/$porg/$i/configured-gateway-services/$gwsname" \
		-H "Authorization: Bearer $access_token " \
		-H 'Accept: application/json' \
		-H 'Content-Type: application/json' \
		--compressed \
		--insecure | jq -r .url)
	gwsList2=$(echo $urlCGWS | sed -e s/^/\"/ | sed -e s/\ /\",\"/g | sed -e s/$/\"/)
	for prod in  $product_list ; do
		echo
		echo "-------------------"
		echo "   Adding GWSs ($gwsList2) to Prod ($prod) in catalog ($i)"
		echo "-------------------"
		addProd=$(curl -s -q "https://$platform_api_url/api/catalogs/$porg/$i/products/$prod" \
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
