# school-holiday-notification
I keep finding out that school holiday program enrolments are open too late, once there are limited slots still available.

So this is a quick little lambda function written in Python to pull down the page, look for whether the unstructured <h1> string has changed, and notifies me using Pushover if it has.
