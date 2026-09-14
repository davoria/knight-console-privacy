# Audit de sécurité et de stabilité — Knight Console V1.8.5 PC test 3

Date de l'audit : 14 septembre 2026  
Auditeur : analyse automatisée Codex, environnement isolé local  
État : **audit de l'application bloqué faute de dépôt applicatif ; audit complet du dépôt fourni effectué**

## 1. Identification vérifiée

Le répertoire fourni est `/workspace/knight-console-privacy`. Il correspond au dépôt
`davoria/knight-console-privacy`, d'après `.git/FETCH_HEAD`, et non au dépôt de
l'application Knight Console.

| Élément | Valeur constatée |
|---|---|
| Branche au début de l'audit | `work` |
| Branche de rapport | `audit/v1.8.5-pc-test3` |
| Commit audité | `4adc6cd6860155b4bcfcd920b72685923bc0f9dc` |
| Sujet du commit | `Mise à jour de la politique pour la suppression automatique` |
| Version applicative vérifiable | aucune |
| Version demandée | V1.8.5 PC — test 3, **non disponible dans ce dépôt** |

L'historique complet ne contient que `README.md`, `index.html` et
`delete-account.html`. Aucun tag n'est présent. Aucun remote n'est configuré dans
`.git/config`; seule la provenance du dernier fetch subsiste dans
`.git/FETCH_HEAD`. `gh auth status` indique qu'aucune session GitHub n'est
disponible et toute connexion HTTPS à GitHub échoue avec `CONNECT tunnel failed,
response 403`. Il est donc impossible de découvrir ou récupérer honnêtement le
dépôt applicatif privé/public depuis cet environnement.

**Conséquence :** la présence de corrections postérieures à V1.8.5 PC test 3 ne
peut pas être établie. Ce rapport ne présente aucune conclusion de sécurité sur
l'application, Firebase ou Android qui ne soit étayée par un artefact local.

## 2. Périmètre effectivement examiné

### Présent et examiné

- les trois fichiers suivis et leurs six commits accessibles ;
- les deux pages HTML/CSS statiques, leurs liens, métadonnées et surfaces actives ;
- l'ensemble des objets et références Git locaux, y compris une recherche
  d'objets inaccessibles et de motifs de secrets ;
- la cohérence entre les déclarations de confidentialité et de suppression ;
- l'absence de JavaScript, ressources distantes et formulaires ;
- un test automatisé reproductible dans `tests/audit_privacy_site.py`.

### Absent, donc non testé

- sources PC et Android, HTML/JavaScript applicatif et lanceur Windows ;
- `package.json`, verrous de dépendances, scripts de compilation et workflows ;
- configuration Firebase, règles Firestore et index ;
- Cloud Functions ou serveur complet ;
- Firebase Emulator et jeux de comptes fictifs ;
- tests et deux audits applicatifs antérieurs ;
- APK, AAB, archives de livraison, signatures et empreinte attendue ;
- instance Firebase de test explicitement isolée et autorisée ;
- bundle exact de la V1.8.5 PC test 3 ou d'une correction ultérieure.

Il n'a été envoyé aucune requête à Firebase et aucun compte, donnée ou service de
production n'a été touché.

## 3. Résultats classés par gravité et preuve

### BLOQUANT — L'application demandée n'est pas auditable avec les artefacts fournis

**Niveau de preuve : reproduit.**

- **Emplacement :** racine du dépôt et historique Git.
- **Prérequis :** environnement remis à l'auditeur.
- **Scénario :** énumérer tous les fichiers suivis (`git ls-tree -r HEAD`), toutes
  les branches/tags et tous les chemins historiques. Seuls les trois fichiers du
  site de confidentialité apparaissent. Vérifier ensuite l'accès GitHub : aucun
  remote ni authentification, et le tunnel refuse GitHub.
- **Impact :** aucune tentative F12, aucun contrôle d'autorisation Firestore,
  aucune suppression de compte, aucun essai multi-utilisateur, aucune comparaison
  PC/Android ou source/bundle ne peut être exécuté. Affirmer que ces protections
  résistent constituerait une conclusion inventée.
- **Preuve minimale :** `git ls-tree -r --name-only HEAD` retourne seulement
  `README.md`, `delete-account.html`, `index.html`.
- **Correction de la situation d'audit :** fournir le clone du dépôt applicatif et
  ses sous-modules dans l'espace de travail, ainsi que les deux rapports précédents
  et les livrables. Fournir un projet Firebase Emulator sans données réelles. Il
  n'est pas nécessaire de fournir des secrets de production.
- **Test de non-régression :** avant reprise, archiver la sortie de
  `git remote -v`, `git status`, `git rev-parse HEAD`, `git describe --tags` et
  l'inventaire des artefacts ; rattacher chaque résultat au hash réellement testé.

### INFORMATION — Les garanties décrites par le site ne sont pas vérifiables ici

**Niveau de preuve : confirmé par analyse du code du site.**

- **Emplacement :** `index.html:24-80` et `delete-account.html:18-67`.
- **Prérequis :** aucun.
- **Scénario :** les pages affirment l'emploi de règles Firestore, une prévention
  des écrasements silencieux, une suppression automatique et un nettoyage de
  plusieurs familles de documents. Aucun code implémentant ces garanties ne se
  trouve dans le dépôt.
- **Impact :** risque documentaire : les utilisateurs peuvent se fier à des
  garanties que cet audit ne peut confirmer. Ce constat ne prouve pas que
  l'application est vulnérable.
- **Correction proposée :** lors de l'audit applicatif, relier chaque affirmation
  à une règle, une fonction et un test Emulator. Tester spécialement les échecs
  partiels de suppression et les sous-collections orphelines.
- **Test de non-régression :** une matrice exigence → code → test Emulator → résultat
  doit accompagner chaque livraison.

### INFORMATION — Surface active minimale du site statique

**Niveau de preuve : reproduit.**

- **Emplacement :** `index.html` et `delete-account.html`.
- **Prérequis :** ouverture locale des pages.
- **Scénario et preuve :** le test fourni confirme zéro balise `script`, zéro
  formulaire, zéro gestionnaire d'évènement HTML, zéro ressource HTTP(S) et
  uniquement des liens relatifs ou `mailto:` attendus.
- **Impact :** aucune surface DOM/Firebase applicative n'est exposée par ces deux
  pages. Cela ne dit rien de l'application PC.
- **Protection observée :** absence de moteur de rendu de contenu utilisateur,
  dépendance tierce ou script exécutable sur ce site.
- **Test de non-régression :** exécuter `python3 tests/audit_privacy_site.py`.

### HYPOTHÈSE — En-têtes HTTP de défense en profondeur non vérifiés

**Niveau de preuve : hypothèse restant à tester.**

- **Emplacement :** hébergement du site, absent du dépôt.
- **Prérequis :** URL de déploiement et accès réseau.
- **Scénario :** l'absence de configuration d'hébergement ne permet pas de vérifier
  CSP, `frame-ancestors`, `X-Content-Type-Options`, politique de référent ou HSTS.
- **Impact :** limité pour ces pages sans script ni saisie, mais le cadrage de la
  page ou une future régression active serait moins contenu.
- **Correction proposée :** définir les en-têtes sur l'hébergeur après validation
  de compatibilité ; ne pas ajouter une CSP en balise comme substitut complet aux
  en-têtes serveur.
- **Test de non-régression :** sur l'URL autorisée, capturer
  `curl -sS -D - -o /dev/null URL` et vérifier les en-têtes effectifs.

## 4. Contrôles applicatifs restant obligatoires

Ces contrôles ne sont pas des défauts confirmés. Ils constituent le protocole à
exécuter dès réception des artefacts manquants.

1. **Version et provenance :** comparer V1.8.5 PC test 3 aux tags/commits plus
   récents ; calculer SHA-256 des livrables ; construire depuis une copie propre.
2. **F12 et DOM :** tracer les appels de confiance client, appeler directement les
   fonctions cachées, modifier rôles et identifiants, et injecter des marqueurs
   inoffensifs dans chaque source de texte/URL/import. Une modification purement
   locale ne sera pas qualifiée de franchissement serveur.
3. **Firestore Emulator :** matrice déconnecté, sans Cloud, avec Cloud, MJ, Admin,
   suppression ; tester CRUD croisé, champs supplémentaires, types, tailles,
   immutabilité, campagnes séparées et requêtes réellement utilisées.
4. **Invitations :** rejeu, concurrence, changement de cible, attribution du
   propriétaire et consommation atomique du code.
5. **Fonctions privilégiées :** vérifier authentification, autorisation et
   validation à l'intérieur de chaque SDK Admin, puisque les règles Firestore ne
   s'y appliquent pas.
6. **Suppression :** réauthentification, anti-rejeu, deux requêtes simultanées,
   sous-collections, références, reprise après chaque point de panne et rejet de
   l'ancienne session. Vérifier l'export en le réimportant.
7. **Stabilité :** quota local, JSON invalide/ancien/volumineux, Unicode compté en
   octets, import transactionnel, changement de compte pendant les promesses,
   multi-onglets/appareils et restauration réelle des sauvegardes.
8. **Android :** manifeste fusionné du release, composants exportés, WebView et
   pont natif, navigation/fichiers, `debuggable`, Network Security Config,
   permissions et persistance lors d'une mise à jour.
9. **Distribution :** comparer source et bundle décompilé, certificat/signature,
   dépendances effectivement atteignables, secrets dans le dépôt **et tout son
   historique** sans jamais imprimer leurs valeurs.
10. **CI :** permissions minimales, actions épinglées par SHA, provenance des
    artefacts, séparation PR non fiable/secrets et absence de publication depuis
    du code non approuvé.

## 5. Architecture et organisation

Le dépôt présent est volontairement minimal. Pour trois fichiers, une
réorganisation importante n'est pas justifiée. La duplication du CSS entre les
deux pages est maintenable à cette échelle ; l'extraire modifierait la production,
ce qui est hors périmètre de cette mission.

L'organisation de **l'application** n'est pas évaluable : aucun de ses fichiers
n'est présent. À la reprise, l'audit devra notamment vérifier la séparation entre
UI, modèle local, synchronisation, couche Firebase, autorisation et migrations,
ainsi que la centralisation des validateurs et encodeurs de données.

## 6. Recherche de secrets et dépendances

Une recherche locale par noms et motifs usuels a été exécutée sur les fichiers
suivis et l'historique accessible. Aucun secret, clé privée, mot de passe de
signature, compte de service, jeton GitHub ou configuration Firebase n'a été
trouvé. Aucun gestionnaire de dépendances n'est présent. Ce résultat vaut
**uniquement pour ce dépôt minimal et son historique local**, pas pour Knight
Console ni pour les historiques distants inaccessibles.

## 7. Priorité de reprise

1. **P0 :** fournir le dépôt applicatif exact et identifier le commit/livrable
   V1.8.5 PC test 3 ainsi que les corrections ultérieures.
2. **P0 :** fournir règles, fonctions et configuration Emulator correspondant à la
   version réellement déployée, sans accès à la production.
3. **P0 :** fournir les deux audits précédents et reproduire leurs scénarios.
4. **P1 :** exécuter les matrices d'autorisation et de suppression avant toute
   analyse uniquement client.
5. **P1 :** éprouver pertes de données, concurrence et restauration.
6. **P1 :** comparer sources PC/Android et livrables signés.
7. **P2 :** auditer dépendances, CI et organisation, puis documenter les mesures de
   défense en profondeur.

## 8. Commandes reproductibles exécutées

```bash
pwd
find /workspace -maxdepth 3 -type d -name .git -print
find / -name AGENTS.md -print 2>/dev/null
git status --short --branch
git rev-parse HEAD
git log --oneline --decorate --all
git log --all --name-only --format= | sort -u
git ls-tree -r --name-only HEAD
git tag --list
git remote -v
git fsck --full --no-reflogs --unreachable
gh auth status
GIT_TERMINAL_PROMPT=0 git ls-remote https://github.com/davoria/knight-console.git HEAD
python3 tests/audit_privacy_site.py
git diff --check
```

La commande `ls-remote` échoue avant échange avec GitHub (`CONNECT tunnel failed,
response 403`). Cet échec est une limite d'environnement, non un résultat sur la
visibilité du dépôt supposé.
