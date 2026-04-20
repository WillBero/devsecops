# Rapport de sécurité

## Nombre de vulnérabilités par sévérité

- High : 4
- Medium : 11
- Low : 1


# Liste des corrections à apporter

## 1. Corrections critiques (HIGH)

### Flask

- **Problème :**
  - Version utilisée : `Flask==2.0.1`
  - Vulnérabilités :
    - Information Exposure (HIGH)
    - Cache contenant des données sensibles

- **Correction :**

```txt
Flask==3.1.3
```

### urllib3 *(dépendance indirecte via requests)*

- **Problème :**
  - Vulnérabilités HIGH :
    - Data amplification
    - Resource exhaustion

- **Correction** *(indirecte via requests ou pin direct)* :

```txt
urllib3==2.6.3
```

---

## 2. Corrections importantes (MEDIUM)

### Jinja2

- **Problème :**
  - XSS multiples
  - Template Injection

- **Correction :**

```txt
Jinja2==3.1.6
```

### Requests

- **Problème :**
  - Fuite d'informations sensibles
  - Gestion de fichiers temporaires insecure
  - Flux de contrôle incorrect

- **Correction :**

```txt
requests==2.33.0
```

### idna

- **Problème :**
  - Resource exhaustion

- **Correction :**

```txt
idna==3.7
```

---

## 3. Correction recommandée *(meilleure approche)*

Simplification du `requirements.txt` :

```txt
Flask==3.1.3
requests==2.33.0
```

> 👉 Les dépendances suivantes seront automatiquement résolues : `Jinja2`, `urllib3`, `idna`

---

## 4. Corrections Semgrep (SAST)

### 4.1 Mode debug activé

❌ **Mauvais :**

```python
app.run(debug=True)
```

✅ **Correct :**

```python
app.run(debug=False)
```

---

### 4.2 Injection de données utilisateur (XSS)

❌ **Mauvais :**

```python
user = request.args.get("user")
return f"Hello {user}"
```

✅ **Correct :**

```python
from markupsafe import escape

user = escape(request.args.get("user"))
return f"Hello {user}"
```

---

### 4.3 SQL Injection

❌ **Mauvais :**

```python
query = f"SELECT * FROM users WHERE id={user_id}"
```

✅ **Correct :**

```python
cursor.execute("SELECT * FROM users WHERE id=%s", (user_id,))
```

---

### 4.4 Command Injection

❌ **Mauvais :**

```python
os.system(user_input)
```

✅ **Correct :**

- Éviter l'exécution directe
- Valider strictement les entrées

---

### 4.5 Secret hardcodé

❌ **Mauvais :**

```python
app.secret_key = "123456"
```

✅ **Correct :**

```python
import os
app.secret_key = os.environ.get("SECRET_KEY")
```

---

## 5. Résultat attendu après correction

### Snyk

- ✅ 0 HIGH
- ✅ 0 CRITICAL
- ✅ Réduction significative des MEDIUM

### Semgrep

- ✅ 0 findings blocking
- ✅ Ou uniquement LOW non critiques

---

## 6. Plan d'action

1. Mettre à jour `requirements.txt`
2. Installer les dépendances localement :

```bash
pip install -r requirements.txt
```

3. Corriger `app.py`
4. Commit + push
5. Vérifier :
   - GitHub Actions
   - Code Scanning
   - Artifacts
