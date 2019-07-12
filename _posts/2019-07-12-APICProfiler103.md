---
layout: post
date: 2019-07-12 06:00:00
categories: Misc
title: "API Connect Profiler new minor version v1.0.3 - DD"
---
Just a note to say that I have released the API Connect Profiler tool.

*This tool was created to extract non runtime statistics from an API Connect 2018 system and as a sample for how to call API Connects provider APIs. It is a self contained Go Application so once the binary is downloaded no additional files are needed. This must be run from a windows/linux/macos system that has https connectivity to the API Manager node.*

**Release Notes**
1. Added support for a version flag to return the version number
2. Fixed and issue with logging into the multiple provider orgs with different user creds
3. Pushed the code change that fixed the issue where it was using Title not Name when making requests.

https://github.com/ChrisPhillips-cminion/APIConnect-Profiler/releases/tag/v1.0.3

**TODO**
Tidy up the multi provider org code.
