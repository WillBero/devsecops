# Vulnerabilities Report

## High

### 1. SQL Injection
- Fichier : app.py
- Description : requête SQL non paramétrée
- Correction : utilisation de requêtes préparées

## Medium

### 2. Debug mode enabled
- Description : Flask en mode debug
- Correction : debug=False en production