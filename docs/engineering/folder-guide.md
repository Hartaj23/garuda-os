# Folder Guide

## apps

User-facing applications. No business logic, AI reasoning or database logic.

## services

External system communication boundaries. Services do not make business decisions.

## packages

Reusable operating system capabilities and shared types. Packages must be independently testable and documented.

## agents

AI specialist implementation area for future approved sprints. No agent logic is implemented in Task 1.

## infrastructure

Docker, deployment, monitoring, observability and security infrastructure.

## scripts

Development utilities and validation scripts. Scripts must not contain permanent business logic.

## tests

Repository, integration, system, acceptance and architecture validation tests.

## docs

Architecture, engineering and sprint documentation.

