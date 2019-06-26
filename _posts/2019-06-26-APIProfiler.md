---
layout: post
date: 2019-06-26 01:00:00
categories: APIConnect
title: "APIC Profiler"
image: "https://asciinema.org/a/zSkEqXvfHSN8I6Sb2UgHI0LwW.svg"
---

I spend a lot of time at clients trying to debug their issues. It was suggested that it would help if we had a tool that could extract volumetrics out of the API Manager. This is not the transaction rate but the quantity of content.

APIC Profiler was created to do this job. The tool is run against an API Connect 2018 stack. Firstly it calls the Admin API to determine the number of provider orgs and other key details. Then the user can select which provider orgs to drill down into. If these require different credentials thats fine it prompts for each provider org.  If you want to automate the solution all parameters can be passed in on the cli.

The tool outputs in either markdown, yaml or json.

For a demo of the tool please take a look at the video below. A sample of the output is available at the end of this article.
[![asciicast](https://asciinema.org/a/zSkEqXvfHSN8I6Sb2UgHI0LwW.svg)](https://asciinema.org/a/zSkEqXvfHSN8I6Sb2UgHI0LwW)


To download and install the tool please go to [https://github.com/ChrisPhillips-cminion/APIConnect-Profiler](https://github.com/ChrisPhillips-cminion/APIConnect-Profiler)



## Sample default Output

--------------------------------------------------------------------------------------------------------

# Cloud Name = 'Cloud Admin'
-1 means an issue retreiving the data


--------------------------------------------------------------------------------------------------------

 Cloud Manager Details

|      NUMBER OF ORGS       | 19 |
|---------------------------|----|
| Number of Members         |  2 |
| Number of Member Invites  |  0 |
| Number of Oauth Providers |  0 |
| Number of User Registries |  7 |
| Number of Mail Servers    |  1 |

--------------------------------------------------------------------------------------------------------

 ## Number of Availability Zones 2
--------------------------------------------------------------------------------------------------------

|           NAME            | NUMBER OF V5C GWS | NUMBER OF API GWS | NUMBER OF PORTALS | NUMBER OF ANALYTICS |
|---------------------------|-------------------|-------------------|-------------------|---------------------|
| availability-zone-default |                 1 |                 2 |                 1 |                   1 |
| performance-testing       |                 1 |                 1 |                 0 |                   0 |
|                           |                   |                   |                   |                     |

--------------------------------------------------------------------------------------------------------

## Number of Provider Organizations to investigate 3
--------------------------------------------------------------------------------------------------------

|  NAME   |   | MEMBERS | MEMBERINVITES | DRAFTAPIS | AVG API SIZE | MAX API SIZE | DRAFTPRODUCTS | TLS PROFILES | OAUTH PROIVDERS | USER REGISTRIES | KEYSTORES | TRUSTSTORES | CATALOGS |
|---------|---|---------|---------------|-----------|--------------|--------------|---------------|--------------|-----------------|-----------------|-----------|-------------|----------|
| chrisp  |   |       2 |             0 |         5 |        43589 |        91159 |            28 |           13 |               2 |               8 |         0 |           0 |        3 |
| chrisp3 |   |       1 |             0 |         9 |       130794 |       941383 |             8 |           13 |               2 |               6 |         0 |           0 |        1 |
| chrisp2 |   |       1 |             0 |         0 |            0 |            0 |             0 |           10 |               0 |               4 |         0 |           0 |        1 |
|         |   |         |               |           |              |              |               |              |                 |                 |           |             |          |

--------------------------------------------------------------------------------------------------------

## 		 Number of catalogs investigated - 5
--------------------------------------------------------------------------------------------------------

|   ORG   |             CATALOG NAME             | MEMBERS | MEMBERINVITES | APIS | AVG API SIZE | MAX API SIZE | PRODUCTS | CONSUMERORGS | PORTAL | TLSPROFILES | OAUTHPROS | USERREGS | SPACES | APPS | SUBSCRIPTIONS | WEBHOOKS |
|---------|--------------------------------------|---------|---------------|------|--------------|--------------|----------|--------------|--------|-------------|-----------|----------|--------|------|---------------|----------|
|         |                                      |         |               |      |              |              |          |              |        |             |           |          |        |      |               |          |
| chrisp  | a6f7f15e-0290-40af-afb5-ab7ab998a484 |       2 |             0 |    0 |            0 |            0 |        0 |            0 | false  |           0 |         0 |        0 |      0 |    0 |             0 |        2 |
| chrisp  | Sandbox                              |       2 |             0 |    2 |        15355 |        25171 |        2 |            3 | true   |           1 |         0 |        0 |      0 |    1 |             0 |        2 |
| chrisp  | spacetes asdfa;dfauidh adfafd        |       2 |             0 |    3 |        29642 |        45289 |        1 |            0 | false  |           2 |         0 |        0 |      3 |    0 |             0 |        1 |
| chrisp3 | Sandbox                              |       1 |             0 |    0 |            0 |            0 |        0 |            1 | false  |           1 |         1 |        0 |      0 |    2 |             0 |        2 |
| chrisp2 | Sandbox                              |       1 |             0 |    0 |            0 |            0 |        0 |            0 | false  |           0 |         0 |        0 |      0 |    0 |             0 |        0 |

--------------------------------------------------------------------------------------------------------

## 		 Number of Webhooks investigated - 7
--------------------------------------------------------------------------------------------------------

|              WEBHOOK ID              |              ORGANIZATION              |                CATALOG                 |       STATE        | LEVEL |            TITLE            |        CREATED AT        |        UPDATED AT        |
|--------------------------------------|----------------------------------------|----------------------------------------|--------------------|-------|-----------------------------|--------------------------|--------------------------|
|                                      |                                        |                                        |                    |       |                             |                          |                          |
| 96daa6b3-81ed-448e-8c21-1994a08165ad | chrisp                                 | a6f7f15e-0290-40af-afb5-ab7ab998a484   | online_configured  | sync  | idg77v-v5c                  | 2019-04-26T10:43:03.193Z | 2019-06-03T22:57:06.048Z |
|                                      | (8643dbab-b431-4602-a083-8d8fa29d2f6e) | (a6f7f15e-0290-40af-afb5-ab7ab998a484) |                    |       |                             |                          |                          |
| d8d14f26-7a09-47db-8998-c0b5313bf944 | chrisp                                 | a6f7f15e-0290-40af-afb5-ab7ab998a484   | online_configured  | sync  | Performance Testing Gateway | 2019-04-26T10:43:45.085Z | 2019-04-29T16:06:35.458Z |
|                                      | (8643dbab-b431-4602-a083-8d8fa29d2f6e) | (a6f7f15e-0290-40af-afb5-ab7ab998a484) |                    |       |                             |                          |                          |
| 2bddcbbb-ac02-4d9b-98ce-898030d8b121 | chrisp                                 | Sandbox                                | online             | sync  | IBM Developer Portal        | 2019-04-24T11:12:10.119Z | 2019-06-26T08:48:16.042Z |
|                                      | (8643dbab-b431-4602-a083-8d8fa29d2f6e) | (bf4c0ec9-95c8-4e71-a2fd-fec37bbb79d1) |                    |       |                             |                          |                          |
| f510da41-d49e-4c97-9814-3f4beb493baf | chrisp                                 | Sandbox                                | offline_configured | sync  | idg77v-v5c                  | 2019-03-08T17:38:45.159Z | 2019-06-03T23:02:48.675Z |
|                                      | (8643dbab-b431-4602-a083-8d8fa29d2f6e) | (bf4c0ec9-95c8-4e71-a2fd-fec37bbb79d1) |                    |       |                             |                          |                          |
| 125a63ff-699c-4249-ba7b-9557eb9e09d5 | chrisp                                 | spacetes asdfa;dfauidh adfafd          | online_configured  | sync  | idg77v-v5c                  | 2019-04-24T11:55:47.721Z | 2019-06-03T22:57:14.197Z |
|                                      | (8643dbab-b431-4602-a083-8d8fa29d2f6e) | (42298b69-0edf-4cc3-83b4-232786976bbe) |                    |       |                             |                          |                          |
| f1d48c28-d420-4d01-ba70-4aea110323b4 | chrisp3                                | Sandbox                                | online_configured  | sync  | idg77v-v5c                  | 2019-03-25T08:59:25.592Z | 2019-06-03T22:57:32.700Z |
|                                      | (b7cc4351-6be1-4047-a645-b1cc01942c9a) | (6db92f5f-2f10-4d91-bd20-98427ff58f5c) |                    |       |                             |                          |                          |
| 7c16e811-dc9e-4897-873c-39798cc3a157 | chrisp3                                | Sandbox                                | online_configured  | sync  | Performance Testing Gateway | 2019-04-26T10:44:17.148Z | 2019-04-29T16:06:46.215Z |
|                                      | (b7cc4351-6be1-4047-a645-b1cc01942c9a) | (6db92f5f-2f10-4d91-bd20-98427ff58f5c) |                    |       |                             |                          |                          |
