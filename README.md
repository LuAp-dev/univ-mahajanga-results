# 🚀 STRUCTURE COMPLÈTE - PROJET API + FRONTEND

## 📁 Architecture du Projet

```
univ-mahajanga-results/
├── 📁 backend-api/              # API Python FastAPI
│   ├── app/
│   │   ├── main.py              # Point d'entrée API
│   │   ├── database.py          # Connexion MySQL Laravel
│   │   ├── models/              # Modèles SQLAlchemy
│   │   │   ├── student.py       # Table etudiants
│   │   │   ├── result.py        # Table resultats_finaux
│   │   │   └── exam.py          # Tables examens, ecs, etc.
│   │   ├── routers/             # Endpoints API
│   │   │   ├── auth.py          # Authentification
│   │   │   └── students.py      # Résultats étudiants
│   │   └── schemas/             # Validation Pydantic
│   ├── requirements.txt
│   └── .env
├── 📁 frontend-web/             # Interface Étudiant
│   ├── index.html               # Page principale
│   ├── login.html               # Page connexion
│   ├── results.html             # Page résultats
│   ├── css/
│   │   └── style.css            # Styles
│   ├── js/
│   │   ├── api.js               # Client API
│   │   ├── auth.js              # Gestion auth
│   │   └── results.js           # Affichage résultats
│   └── assets/
└── 📁 docs/                     # Documentation
    ├── installation.md
    ├── api-endpoints.md
    └── user-guide.md
```

## 🎯 OBJECTIFS CLAIRS POUR LE STAGIAIRE

### Phase 1 : API Backend (6 semaines)
**Objectif :** Créer une API qui lit les données Laravel

✅ **Semaine 1-2 : Configuration Base**
- Connexion à la base MySQL Laravel
- Modèles SQLAlchemy pour tables existantes
- Endpoints de base fonctionnels

✅ **Semaine 3-4 : Authentification**
- Login par matricule
- JWT tokens
- Permissions (étudiant voit ses données uniquement)

✅ **Semaine 5-6 : Endpoints Résultats**
- Consultation résultats par étudiant
- Calcul statut (Admis/Redoublant/Exclus/Rattrapage)
- Moyennes et statistiques

### Phase 2 : Frontend Simple (4 semaines)
**Objectif :** Interface web pour consultation

✅ **Semaine 7-8 : Interface Base**
- Page de connexion
- Page d'affichage des résultats
- CSS responsive simple

✅ **Semaine 9-10 : Intégration API**
- Appels AJAX vers l'API
- Gestion authentification
- Affichage dynamique des données

### Phase 3 : Tests et Documentation (2 semaines)
✅ **Semaine 11-12 : Finalisation**
- Tests de l'API
- Documentation utilisateur
- Déploiement

## 🛠️ ÉTAPE 1 : API BACKEND

### Structure Minimale Backend

```python
# backend-api/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, students

app = FastAPI(title="Exam Results API", version="1.0.0")

# CORS pour le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # À restreindre en production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(students.router, prefix="/api/v1/students", tags=["students"])

@app.get("/")
def read_root():
    return {"message": "Exam Results API - Running"}
```

### Endpoints Essentiels

```python
# backend-api/app/routers/auth.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    matricule: str

@router.post("/login")
async def login(request: LoginRequest):
    # 1. Vérifier si étudiant existe dans DB
    # 2. Générer JWT token
    # 3. Retourner token + info étudiant
    return {
        "access_token": "jwt_token_here",
        "student": {
            "id": 123,
            "matricule": request.matricule,
            "nom": "CROLAS",
            "prenom": "Paul"
        }
    }

# backend-api/app/routers/students.py
@router.get("/{student_id}/results")
async def get_results(student_id: int):
    # 1. Récupérer résultats depuis resultats_finaux
    # 2. Joindre avec tables ecs, examens
    # 3. Calculer statut final
    # 4. Retourner données formatées
    return {
        "student": {...},
        "results": [...],
        "status": "Admis"  # ou Redoublant, Exclus, Rattrapage
    }
```

### Configuration .env

```env
# backend-api/.env
DATABASE_URL=mysql://username:password@localhost:3306/your_laravel_db
JWT_SECRET_KEY=your-super-secret-key
DEBUG=True
```

## 🎨 ÉTAPE 2 : FRONTEND SIMPLE

### Page de Connexion

```html
<!-- frontend-web/login.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Consultation Résultats - Université Mahajanga</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <div class="login-form">
            <h2>🎓 Consultation des Résultats</h2>
            <form id="loginForm">
                <input type="text" id="matricule" placeholder="Numéro matricule" required>
                <button type="submit">Se connecter</button>
            </form>
            <div id="error-message"></div>
        </div>
    </div>
    <script src="js/auth.js"></script>
</body>
</html>
```

### Page Résultats

```html
<!-- frontend-web/results.html -->
<!DOCTYPE html>
<html>
<head>
    <title>Mes Résultats</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>📊 Mes Résultats d'Examens</h1>
            <div id="student-info"></div>
        </header>
        
        <div class="status-card" id="status-card">
            <!-- Statut principal : Admis/Redoublant/etc. -->
        </div>
        
        <div class="results-table" id="results-table">
            <!-- Tableau des résultats par matière -->
        </div>
        
        <button onclick="logout()">Déconnexion</button>
    </div>
    
    <script src="js/api.js"></script>
    <script src="js/results.js"></script>
</body>
</html>
```

### JavaScript pour l'API

```javascript
// frontend-web/js/api.js
const API_BASE = 'http://localhost:8001/api/v1';

class ExamAPI {
    constructor() {
        this.token = localStorage.getItem('token');
    }
    
    async login(matricule) {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({matricule})
        });
        
        if (response.ok) {
            const data = await response.json();
            this.token = data.access_token;
            localStorage.setItem('token', this.token);
            localStorage.setItem('student', JSON.stringify(data.student));
            return data;
        }
        throw new Error('Connexion échouée');
    }
    
    async getResults(studentId) {
        const response = await fetch(`${API_BASE}/students/${studentId}/results`, {
            headers: {'Authorization': `Bearer ${this.token}`}
        });
        
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Erreur récupération résultats');
    }
}

// frontend-web/js/results.js
document.addEventListener('DOMContentLoaded', async () => {
    const api = new ExamAPI();
    const student = JSON.parse(localStorage.getItem('student'));
    
    if (!student) {
        window.location.href = 'login.html';
        return;
    }
    
    try {
        const results = await api.getResults(student.id);
        displayResults(results);
    } catch (error) {
        alert('Erreur: ' + error.message);
    }
});

function displayResults(data) {
    // Afficher info étudiant
    document.getElementById('student-info').innerHTML = `
        <h3>${data.student.prenom} ${data.student.nom}</h3>
        <p>Matricule: ${data.student.matricule}</p>
    `;
    
    // Afficher statut principal
    const statusCard = document.getElementById('status-card');
    const status = calculateOverallStatus(data.results);
    statusCard.innerHTML = `
        <h2 class="status-${status.toLowerCase()}">${status}</h2>
    `;
    
    // Afficher tableau résultats
    const tableHTML = `
        <table>
            <thead>
                <tr>
                    <th>Matière</th>
                    <th>Note</th>
                    <th>Statut</th>
                </tr>
            </thead>
            <tbody>
                ${data.results.map(r => `
                    <tr>
                        <td>${r.ec_nom}</td>
                        <td>${r.note}/20</td>
                        <td class="decision-${r.decision}">${r.decision}</td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;
    document.getElementById('results-table').innerHTML = tableHTML;
}

function calculateOverallStatus(results) {
    // Logique pour déterminer le statut global
    if (results.some(r => r.decision === 'exclus')) return 'EXCLUS';
    if (results.some(r => r.decision === 'redoublant')) return 'REDOUBLANT';
    if (results.some(r => r.decision === 'rattrapage')) return 'RATTRAPAGE';
    return 'ADMIS';
}
```

## 🎨 CSS Simple et Professionnel

```css
/* frontend-web/css/style.css */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}

.login-form {
    background: white;
    padding: 40px;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    text-align: center;
    margin-top: 100px;
}

.status-card {
    background: white;
    padding: 30px;
    border-radius: 10px;
    text-align: center;
    margin: 20px 0;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.status-admis { color: #28a745; }
.status-rattrapage { color: #ffc107; }
.status-redoublant { color: #fd7e14; }
.status-exclus { color: #dc3545; }

table {
    width: 100%;
    background: white;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

th, td {
    padding: 15px;
    text-align: left;
    border-bottom: 1px solid #eee;
}

th {
    background: #f8f9fa;
    font-weight: 600;
}

.decision-admis { 
    color: #28a745; 
    font-weight: bold;
}

.decision-rattrapage { 
    color: #ffc107; 
    font-weight: bold;
}

button {
    background: #667eea;
    color: white;
    border: none;
    padding: 12px 30px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 16px;
    transition: background 0.3s;
}

button:hover {
    background: #5a67d8;
}

input {
    width: 100%;
    padding: 15px;
    margin: 10px 0;
    border: 1px solid #ddd;
    border-radius: 5px;
    font-size: 16px;
}
```

## 📋 LIVRABLES POUR LE STAGIAIRE

### ✅ Livrable 1 (Semaine 6) : API Fonctionnelle
- [ ] Connexion à la base Laravel
- [ ] Authentification par matricule
- [ ] Endpoint de récupération résultats
- [ ] Calcul du statut (Admis/Redoublant/etc.)
- [ ] Documentation Swagger

### ✅ Livrable 2 (Semaine 10) : Frontend Complet
- [ ] Page de connexion sécurisée
- [ ] Page d'affichage des résultats
- [ ] Interface responsive
- [ ] Gestion des erreurs
- [ ] Déconnexion

### ✅ Livrable 3 (Semaine 12) : Projet Final
- [ ] Tests de l'API
- [ ] Documentation utilisateur
- [ ] Guide de déploiement
- [ ] Démonstration fonctionnelle

## 🚀 COMMANDES DE DÉMARRAGE

```bash
# 1. Backend API
cd backend-api
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate sur Windows
pip install fastapi uvicorn sqlalchemy pymysql python-jose python-dotenv
uvicorn app.main:app --reload --port 8001

# 2. Frontend (serveur simple)
cd frontend-web
python -m http.server 8080
# Ou utiliser Live Server dans VS Code

# 3. Accès
# API Documentation: http://localhost:8001/docs
# Frontend: http://localhost:8080
```

## 📊 CRITÈRES DE RÉUSSITE

| Critère | Poids | Objectif |
|---------|-------|----------|
| **API fonctionnelle** | 40% | Tous les endpoints marchent |
| **Frontend utilisable** | 30% | Interface claire et responsive |
| **Sécurité** | 15% | Authentification et permissions |
| **Documentation** | 10% | Guides clairs et complets |
| **Tests** | 5% | Tests de base fonctionnels |

**Note minimale pour validation :** 12/20
**Objectif d'excellence :** 16/20
