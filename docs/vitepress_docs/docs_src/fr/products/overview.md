---
description: 'Découvrez la suite Open Ticket AI : un classifieur sur site (on-prem), une API hébergée, un générateur de données synthétiques et des modèles publics pour automatiser votre flux de travail de tickets de support.'
pageClass: full-page
---
# Aperçu des produits

Utilisez cette page pour voir ce qui est disponible aujourd'hui, ce qui est hébergé par nous, et ce qui est à venir.
**Open Ticket AI** est le produit phare sur site (on-prem) ; les **modèles** et les **API** sont des modules complémentaires optionnels.

## En un coup d'œil

<Table>
    <Row>
      <C header>Produit</C>
      <C header>Description</C>
      <C header>Statut</C>
      <C header>Liens</C>
    </Row>
    <Row>
      <C><strong>Open Ticket AI (Sur site/Produit principal)</strong></C>
      <C>Classifieur de tickets local et open-source (files d'attente & priorité) intégré via des pipelines/adaptateurs.</C>
      <C>✅ Disponible</C>
      <C><Link to="/">Aperçu</Link></C>
    </Row>
    <Row>
      <C><strong>API de prédiction hébergée (allemand)</strong></C>
      <C>API HTTP pour classifier la file d'attente & la priorité en utilisant notre modèle de base public allemand (hébergé par nous).</C>
      <C>✅ Gratuit pour le moment</C>
      <C><Link to="/products/prediction-api/overview">Documentation de l'API</Link></C>
    </Row>
    <Row>
      <C><strong>Modèles de base publics (allemand)</strong></C>
      <C>Modèles de base pour file d'attente/priorité publiés sur Hugging Face pour les utilisateurs sans leurs propres données.</C>
      <C>✅ Disponible</C>
      <C>Voir les liens dans la <Link to="/products/prediction-api/overview">Documentation de l'API</Link></C>
    </Row>
    <Row>
      <C><strong>Générateur de données synthétiques</strong></C>
      <C>Outil Python pour créer des jeux de données de tickets synthétiques multilingues ; licence LGPL prévue.</C>
      <C>✅ Disponible</C>
      <C><Link to="/products/synthetic-data/synthetic-data-generation">Générateur</Link></C>
    </Row>
    <Row>
      <C><strong>Jeux de données de tickets (v5, v4, v3)</strong></C>
      <C>Jeux de données synthétiques créés avec notre générateur (focus EN/DE en v5/v4 ; plus de langues en v3).</C>
      <C>✅ Disponible</C>
      <C><Link to="/products/synthetic-data/ticket-dataset">Jeu de données</Link></C>
    </Row>
    <Row>
      <C><strong>Modèle de prédiction anglais</strong></C>
      <C>Modèle de base pour file d'attente/priorité en anglais.</C>
      <C>🚧 Bientôt disponible</C>
      <C>(sera ajouté ici)</C>
    </Row>
    <Row>
      <C><strong>Langues & attributs supplémentaires</strong></C>
      <C>Modèles pour d'autres langues ; prédictions pour les étiquettes, l'assigné ; première réponse optionnelle.</C>
      <C>🧭 En exploration</C>
      <C>(feuille de route)</C>
    </Row>
    <Row>
      <C><strong>Interface utilisateur web pour le générateur de données</strong></C>
      <C>Interface utilisateur dans le navigateur pour le générateur, destinée aux utilisateurs non techniques.</C>
      <C>🧭 En exploration</C>
      <C>(feuille de route)</C>
    </Row>
</Table>

> **Note sur la tarification :** L'**API de prédiction allemande** hébergée est actuellement gratuite. Si la demande augmente trop les coûts d'infrastructure, nous pourrions introduire des limites de taux ou une tarification. **Open Ticket AI** sur site (on-prem) reste open-source et local.

---

## Open Ticket AI (Sur site/Produit principal)

- S'exécute localement ; s'intègre avec Znuny/OTRS/OTOBO via des adaptateurs.
- Classifie la **File d'attente** & la **Priorité** des tickets entrants ; architecture de pipeline extensible.
- Se combine bien avec notre **Générateur de données synthétiques** pour un démarrage à froid ou l'équilibrage des classes.

**En savoir plus :**
[Aperçu](../index.md)

---

## API de prédiction hébergée & Modèles de base publics (allemand)

- Pour les équipes **sans leurs propres données** pour qui les **files d'attente/priorités de base** conviennent raisonnablement.
- Utilisez le modèle **allemand** via notre API hébergée (**gratuit pour le moment**).
- Les modèles sont **publics sur Hugging Face** ; vous pouvez également les auto-héberger ou les affiner.

**Commencez ici :** [API de prédiction](./prediction-api/overview.md)

---

## Générateur de données synthétiques

- Outil Python pour créer des jeux de données de tickets réalistes et étiquetés (sujet, corps, file d'attente, priorité, type, étiquettes, langue, première réponse).
- Publication sous licence **LGPL** prévue ; envoyez un e-mail pour un accès ou des modifications : **sales@softoft.de**.

**Détails :** [Génération de données synthétiques](./synthetic-data/synthetic-data-generation.md)

---

## Jeux de données de tickets

- Plusieurs versions disponibles :
    - **v5 / v4 :** EN & DE, les plus volumineux et diversifiés.
    - **v3 :** plus de langues (par ex., FR/ES/PT), plus petits.
- Idéal pour le bootstrapping, le benchmarking et les expérimentations multilingues.

**Parcourir :** [Tickets de support client multilingues](./synthetic-data/ticket-dataset.md)

---

## Feuille de route

- Modèle de base **anglais** pour file d'attente/priorité (hébergé & téléchargeable).
- Modèles optionnels pour d'**autres langues**.
- Attributs supplémentaires : **étiquettes**, **assigné**, et génération de **première réponse**.
- Prototype précoce d'une **interface web** pour le générateur de données.

---

## FAQ

**L'API fait-elle partie d'Open Ticket AI ?**
Non. **Open Ticket AI** s'exécute localement. L'**API de prédiction** est un service hébergé distinct qui utilise nos modèles publics.

**Puis-je utiliser ma propre taxonomie ?**
Oui. Entraînez un modèle localement avec vos données, ou demandez-nous de générer des données synthétiques qui reflètent vos files d'attente/priorités.

**Support & Services ?**
Nous proposons des abonnements de support et des intégrations personnalisées. Contactez **sales@softoft.de**.