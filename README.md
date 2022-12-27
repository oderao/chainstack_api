# chainstack_api
A simple API Server to perform CRUD operations on News Resource Platform

Features

1.Identity and Access Management 

2.Quota and Rate Limiting for API Request

3.Error Logging for Errors



API Server is built with Django and Django Rest Framework

Users are of two types `Platform User` `Platform Administrator`

Platform Users can create,list and delete resources on the platform

Platform Administrator can create and delete users,create and delete all resources on the platform

Authentication is handled via django rest framework TokenAuthentication

Quota management is handled programatically via API Request Tables

Error Logging  is managed programatically by the Error Log Table

API Documentation can be found here
https://documenter.getpostman.com/view/15534284/2s8Z6x1sYQ#b78c903f-8701-420a-ad2e-cc459402feb8



