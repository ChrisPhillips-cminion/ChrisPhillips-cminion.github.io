---
layout: post
date: 2019-07-24 06:00:00
categories: DataPower
title: "High Level Migration Overview to the DataPower X2 Appliance [by  R George Inness]"
image: https://developer.ibm.com/apiconnect/wp-content/uploads/sites/23/2018/03/Screen-Shot-2018-03-16-at-3.07.06-PM.png
---
*This is a guest post by R George Inness*

![](https://developer.ibm.com/apiconnect/wp-content/uploads/sites/23/2018/03/Screen-Shot-2018-03-16-at-3.07.06-PM.png)
*Image taken from ibm.com*

### Introduction

Your company has just bought DataPower X2 appliances and you have been assigned to lead the effort to migrate from the current appliances to the new X2s and you are looking for some direction on how to put together a high-level plan.  This article will give you an overview on how to plan and execute the migration with some key pointers on what to look for and possible gotchas.  It will not be a detailed step by step on how to do the migration.  

The IBM recommended methodology to migrate the appliance configuration between appliances is the Secure Backup and Restore feature.  This feature moves all of the configuration information to the new appliance except the content of the Hardware Security Module (HSM) if one is installed and being used.  The Secure Backup and Restore feature can be compared to the process of moving to a newer iPhone using iTunes.  

The major assumptions in this article are:

1.	You and your team have a detailed understanding on DataPower setup and configuration and have used Secure Backup and Restore.  If your team does not have the skills, we recommend working with your sales team to engage a DataPower Business Partner or IBM Lab Services to put together a proposal for the migration.
2.	Your company is doing a like for like migration where the services on the existing DataPowers will not be changed.  An example is moving domains around and consolidating the usage of the appliances.  This methodology supports downsizing the number of appliances that maintain the same usage where your team.  
3.	If your company is downsizing the number of DataPower appliances, your team has done a performance study to ensure the number of appliances being migrated perform as needed.
4.	Your team has the skills necessary to do the appliance migration.  If your team does not have skills, we recommend working with your sales team to engage a DataPower Business Partner or IBM Lab Services to put together a Statement of Work for the migration.
5.	Your current appliances are running v7.6.0.8 or higher.  If they are not, it is recommended that you install and test on either v7.6.0.latest or v2018.40.1.latest in all of your environments then do the appliance migration.  Upgrading firmware and then immediately doing an appliance migration is not recommended because if there are issues, it will be harder to debug.

There are three recommended high-level phases for the X2 migration:  **Inventory, Planning, and Execution** that should map into your company’s methodology for IT projects.  The **Inventory** phase is the gathering of information on your current appliances like the firmware version, what licenses the appliances have and other information required to do the migration.  The **Planning** phase is reviewing the inventory information gathered along with the time estimates to do the specific tasks during the migration.  The **Execution** phase is when your team is doing the appliance migration.

The key requirements for a successful migration are:

1.	The current appliances are running version 7.6.0.8 or higher as this is the minimum firmware level that the X2 appliances support.
2.	Your company has purchased the appropriate DataPower modules for the new appliances.
3.	The firmware version and licenses must be the same on the current and new appliances.
4.	Replacing the appliances in stages, starting at the lowest level like development before migrating production.
5.	When replacing two or more appliances in a High Availability environment, it is recommended that you replace one at a time.  You can run the different appliance types as long as they have the same firmware version and licenses.

### Inventory Phase

You will need to gather the following information from all of the source appliances:
*	Determine what version of the firmware the appliances are running by running the CLI command `show version`.
*	Determine what modules are installed on the current, appliances by running the CLI command `show licenses`.  If the license output contains HSM, do the following steps
  * Run the CLI command `show hsm-keys`
  * If the command returns keys, mark the HSM as being used.  Otherwise, it is not being used.
* Determine whether or not Secure Backup is enabled on the by running the CLI command `show system`.

### Planning Phase

Review the Inventory details gathered in the previous phase then use the details to put together a plan.  From the inventory gathered,  

**Determine the version to install on the X2s.**
* This information can be found in the `show version` output.  

**Determine if Secure Backup is enabled on the current appliances.**
* On the show system output, review the backup mode field and make sure it is set to secure.  If backup mode is set to normal, open a support ticket to get a scrypt3 file to enable secure restore.

**Determine what licenses to install on the new appliances.**
* Make sure you are entitled to the correct modules for the new X2 appliances based upon what you have installed on the current, appliances.
  * If the current, appliance is a XI52, you will need the Integration module.
  * If the current, appliance is a XB62, you will need the B2B module.
  * If the current, appliance’s `show license` output has TIBCO-EMS, you will need the TIBCO-EMS module.
  * If the current, appliance’s `show license` output has AppOpt, you will need the Application Optimization module
  * If the current, appliance’s `show license` output has B2B, you need the B2B module.
  * If the current, appliance’s `show license` output contains all of the following:  DataGlue, SQL-ODBC, DCO and IMS, you will need the integration module.
  * If the new appliance needs the B2B module and your company did not purchase the Integration Module, open a Support Ticket for further assistance.

**Determine next steps if the current, appliance has an HSM installed.**
* If an HSM is installed in the current, appliance, and has keys installed in it, make sure that the private keys are available to be used on the new appliance.  If they are not, update the keys on the current, appliance and use the updated private keys.

The following time estimates are for each summary step of the migration.  With the estimated testing of each new appliance after the Secure Restore has completed.

* 1 hour -> Prepare the new appliance with the matching firmware and install the modules.
* 1 hour -> Secure backup of the current, appliance
* 1 hour -> Secure restore on the new appliance
* Optional if the appliance has a HSM:  4 hours -> Initialize and populate the HSM with the private keys.
* 1 hour -> Unrack the current, appliance and rack and cable the new appliance.
* 2 hours -> Validate the new appliance and turn traffic back on to it.

In planning the replacement schedule, it is recommended that you do not replacement more than one appliance a night in a particular environment like Performance or Production.  It is acceptable to run in a mixed mode in terms of hardware as long as they are running the same firmware and licenses.

### Execution Phase

Two days before migrating an appliance, open up a Support Ticket on the current, appliance and indicate that this is a place holder for an appliance migration that will happen at the planned time.  This will entitle the Support Ticket so there will not be any delay in going through the entitlement check.

When you migrate between the appliances of different generations using Secure Backup and Restore, the only difference in the restore process is specifying the source appliance type in the **Backup appliance model** field.  Use the machine type model from the table below.  The field is case sensitive.  The following tables are the appliance models.




<table border="1"><tr><th>Product Name</th><th>Machine type model</th></tr>
<tr><td rowspan="4">DataPower Gateway (IDG)	844152X</td></tr>
	<tr><td>844153X</td></tr>
	<tr><td>843652X</td></tr>
	<tr><td>843653X</td></tr>
<tr><td>DataPower Gateway Virtual Edition</td><td>5725T09</td></tr>
<tr><td>DataPower Integration Appliance (XI52</td><td>719942X</td></tr>
<tr><td>DataPower B2B Appliance (XB62)</td><td>719962X</td></tr>
<tr><td>DataPower Service Gateway (XG45)</td><td>719832X</td></tr>
</table>

Key Tips for restoring on the new appliance.

* Set the date and time on the new appliance.
* Validate the secure restore files because running it by selecting `On` in the **Only validate the backup** radio button.  If it succeeds, select `Off` and run the secure restore.
* Make sure the backupmanifest.xml does not have a different file extension like “.txt” because some browsers will change the file extension.
* Make sure the Key/Cert for the restore is up and running.
