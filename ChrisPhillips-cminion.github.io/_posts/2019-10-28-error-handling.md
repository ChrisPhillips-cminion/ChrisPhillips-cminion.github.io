---
layout: post
date: 2019-10-28 00:01:00
categories: APIConnect
title: "Developing APIs on API Connect - 106 - Error Handling"
author: ["NickCawood"]
draft: true
---
This article explains the basics of error handling in APIs in API Connect 2018.
<!--more-->



### Your API

-   Build and test your API.

-   In this example the API (v1.0.0)is as follows: a MAP policy to read
    in three input query parameters (an account\_id and a 2 target
    URLs), two INVOKE policies (to call the target URLs) and a
    GATEWAYSCRIPT policy (to format the response from the target URLs).

![](/images/image4.png)

![](/images/image5.png)

![](/images/image6.png)

![](/images/image7.png)

### Case 1: Stop-on-Error (OperationError)

-   The requirement here is to add a basic error handling function
    around the INVOKE policies. This example will show how to use the
    Stop-on-error feature of the INVOKE policy.


-   The first step is to activate the Catch functionality for the API:
    ensure the "Show catches" button is toggled to be on.

![](/images/image8.png)

-   Click on "catch" to enter the Catches of the API.

![](/images/image9.png)

-   The Catches can now be updated.

![](/images/image10.png)

-   Click on "+Catch" to add a catch to the API.

![](/images/image11.png)

-   Click on "search errors", then scroll through the drop-down list of
    errors. Select OperationError.

![](/images/image12.png)

![](/images/image13.png)

![](/images/image14.png)

-   Drag a GATEWAYSCRIPT policy to the catch, detailing the messages to
    be sent on error.

![](/images/image15.png)

-   Errors can be thrown in 2 ways. Either via the Stop-on-error
    function in an Invoke using a valid error, or using the THROW
    policy. In this section the focus is on Stop-on-error.

-   In the first INVOKE policy set the Stop-on-error function to be used
    with the OperationError already selected in the Catch created. Click
    on the first INVOKE policy.

![](/images/image16.png)

-   Scroll down the INVOKE policy. Click on Stop-on-error.

![](/images/image17.png)

-   Select OperationError from "search errors..." and Save the API.

![](/images/image18.png)

![](/images/image19.png)

-   Now re-publish.

-   Test the error API using working query inputs.

![](/images/image20.png)

-   A valid response is returned.

![](/images/image21.png)

-   Now test the error condition by inputting an invalid URL.

![](/images/image22.png)

-   The error condition is triggered.

![](/images/image23.png)

### Case 2: THROW policy (custom error condition)

-   The requirement here is still to add a basic error handling function
    around the INVOKE policies. This example will show how to use the
    THROW policy with a custom error condition to send an error without
    using the Stop-on-error feature.


-   First save v1.0.0 of the API as v2.0.0.

-   Add a new case to the Catch and create a custom error called
    "Invoke2Error" as the error condition.

![](/images/image24.png)

-   Drag a GATEWAYSCRIPT policy to the catch, detailing the messages to
    be sent on error.

![](/images/image25.png)

-   For an error to be caught by the catch an error must first be
    thrown, so add a THROW policy to the Assembly after the INVOKE. Use
    a SWITCH Policy to check for a non-200 code return from the INVOKE.

![](/images/image26.png)

![](/images/image27.png)

-   Edit the SWITCH cases. Click on "switch", and set a condition for
    the SWITCH by clicking on "edit condition".

![](/images/image28.png)

-   Set the condition to follow the SWITCH policy if the INVOKE does not
    return a 200, otherwise it will ignore the SWITCH policy.

![](/images/image29.png)

![](/images/image30.png)

-   Edit the THROW policy to throw the Invoke2Error.

![](/images/image31.png)

-   Note that by creating the custom error in the THROW policy the
    Invoke2Error condition will appear in the dropdown for the Catch
    cases.

![](/images/image32.png){width="3.45370406824147in"
height="3.700396981627297in"}

-   Finally set Stop-on-error in the second INVOKE policy but do not
    throw an error to Invoke2Error. Save the API.

![](/images/image33.png)

-   Now re-publish.

-   Test the error API using working query inputs.

![](/images/image34.png)

-   A valid response is returned.

![](/images/image35.png)

-   Now test the error condition by inputting an invalid URL.

![](/images/image36.png)

-   The error condition is triggered.

![](/images/image37.png)
