---
layout: post
date: 2019-10-28 00:01:00
categories: APIConnect
title: API Error Handling in  API connect 2018
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

![](/images/image4.png){width="6.5in" height="2.6819444444444445in"}

![](/images/image5.png){width="6.5in" height="1.5375in"}

![](/images/image6.png){width="6.5in" height="1.6493055555555556in"}

![](/images/image7.png){width="6.5in" height="2.9430555555555555in"}

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

![](/images/image10.png){width="6.5in" height="2.6979166666666665in"}

-   Click on "+Catch" to add a catch to the API.

![](/images/image11.png){width="6.5in" height="2.722916666666667in"}

-   Click on "search errors", then scroll through the drop-down list of
    errors. Select OperationError.

![](/images/image12.png){width="6.5in" height="2.7215277777777778in"}

![](/images/image13.png){width="6.5in" height="2.675in"}

![](/images/image14.png){width="6.5in" height="2.654166666666667in"}

-   Drag a GATEWAYSCRIPT policy to the catch, detailing the messages to
    be sent on error.

![](/images/image15.png){width="6.5in" height="3.076388888888889in"}

-   Errors can be thrown in 2 ways. Either via the Stop-on-error
    function in an Invoke using a valid error, or using the THROW
    policy. In this section the focus is on Stop-on-error.

-   In the first INVOKE policy set the Stop-on-error function to be used
    with the OperationError already selected in the Catch created. Click
    on the first INVOKE policy.

![](/images/image16.png){width="6.5in" height="2.754861111111111in"}

-   Scroll down the INVOKE policy. Click on Stop-on-error.

![](/images/image17.png){width="6.5in" height="3.040277777777778in"}

-   Select OperationError from "search errors..." and Save the API.

![](/images/image18.png){width="6.5in" height="3.0909722222222222in"}

![](/images/image19.png){width="6.5in" height="3.04375in"}

-   Now re-publish.

-   Test the error API using working query inputs.

![](/images/image20.png){width="6.5in" height="3.595833333333333in"}

-   A valid response is returned.

![](/images/image21.png){width="6.5in" height="3.5819444444444444in"}

-   Now test the error condition by inputting an invalid URL.

![](/images/image22.png){width="6.5in" height="3.598611111111111in"}

-   The error condition is triggered.

![](/images/image23.png){width="6.5in" height="3.5625in"}

### Case 2: THROW policy (custom error condition)

-   The requirement here is still to add a basic error handling function
    around the INVOKE policies. This example will show how to use the
    THROW policy with a custom error condition to send an error without
    using the Stop-on-error feature.


-   First save v1.0.0 of the API as v2.0.0.

-   Add a new case to the Catch and create a custom error called
    "Invoke2Error" as the error condition.

![](/images/image24.png){width="6.5in" height="2.6979166666666665in"}

-   Drag a GATEWAYSCRIPT policy to the catch, detailing the messages to
    be sent on error.

![](/images/image25.png){width="6.5in" height="3.0694444444444446in"}

-   For an error to be caught by the catch an error must first be
    thrown, so add a THROW policy to the Assembly after the INVOKE. Use
    a SWITCH Policy to check for a non-200 code return from the INVOKE.

![](/images/image26.png){width="6.5in" height="2.7381944444444444in"}

![](/images/image27.png){width="6.5in" height="2.7375in"}

-   Edit the SWITCH cases. Click on "switch", and set a condition for
    the SWITCH by clicking on "edit condition".

![](/images/image28.png){width="6.5in" height="2.707638888888889in"}

-   Set the condition to follow the SWITCH policy if the INVOKE does not
    return a 200, otherwise it will ignore the SWITCH policy.

![](/images/image29.png){width="6.5in" height="2.897222222222222in"}

![](/images/image30.png){width="6.5in" height="2.6958333333333333in"}

-   Edit the THROW policy to throw the Invoke2Error.

![](/images/image31.png){width="6.5in" height="2.7020833333333334in"}

-   Note that by creating the custom error in the THROW policy the
    Invoke2Error condition will appear in the dropdown for the Catch
    cases.

![](/images/image32.png){width="3.45370406824147in"
height="3.700396981627297in"}

-   Finally set Stop-on-error in the second INVOKE policy but do not
    throw an error to Invoke2Error. Save the API.

![](/images/image33.png){width="6.5in" height="3.0722222222222224in"}

-   Now re-publish.

-   Test the error API using working query inputs.

![](/images/image34.png){width="6.5in" height="3.598611111111111in"}

-   A valid response is returned.

![](/images/image35.png){width="6.5in" height="3.5527777777777776in"}

-   Now test the error condition by inputting an invalid URL.

![](/images/image36.png){width="6.5in" height="3.6152777777777776in"}

-   The error condition is triggered.

![](/images/image37.png){width="6.5in" height="3.5236111111111112in"}
