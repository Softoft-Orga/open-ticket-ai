---
description: 'Apprenez à évaluer les classifieurs de tickets IA sur des données réelles et déséquilibrées. Découvrez pourquoi l''exactitude est trompeuse et concentrez-vous sur les métriques qui comptent : la précision, le rappel et le score F1.'
---
# Évaluation des classifieurs IA sur des données de tickets réelles : les métriques qui comptent

## Introduction

Les données des tickets de support sont désordonnées et souvent fortement biaisées en faveur de quelques catégories communes. Par exemple,
80 % des tickets peuvent être étiquetés **« demande générale »**, ce qui rend les classifieurs biaisés en faveur de la classe majoritaire.
En pratique, le ML sur les données de tickets peut être utilisé pour :

- **La prédiction de la priorité** (par ex. signaler les problèmes urgents)
- **L'assignation à une file d'attente ou à une équipe** (par ex. envoyer les questions de facturation à la finance)
- **La classification de l'intention ou du sujet** (par ex. « demande de fonctionnalité » vs « rapport de bug »)

Ces cas d'usage montrent pourquoi l'évaluation est difficile : les jeux de données de tickets du monde réel sont multi-classe et
multi-étiquette, avec du texte bruyant et des **classes déséquilibrées**:contentReference[oaicite:0]{index=0}. Un
modèle naïf qui prédit toujours la classe majoritaire peut tout de même obtenir une exactitude élevée en ignorant les cas rares mais importants. Nous examinerons pourquoi l'exactitude seule est trompeuse et discuterons des métriques qui comptent vraiment.

## Pourquoi l'exactitude est trompeuse

L'**exactitude** (accuracy) est définie comme le total des prédictions correctes sur l'ensemble des prédictions :
$ \text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN} $
En termes de formule, exactitude = (TP + TN)/(tous les échantillons). Bien que
simple, l'exactitude échoue lamentablement sur les données déséquilibrées. Par exemple, si 80 % des tickets appartiennent à la classe A, un
classifieur simpliste qui prédit *toujours* A atteint une exactitude de 80 % par défaut – tout en ignorant complètement les 20 % restants des tickets. Dans les cas extrêmes (par ex. une répartition des classes de 99 % contre 1 %), prédire systématiquement la majorité donne une exactitude de 99 % malgré l'absence d'un réel apprentissage. En
bref, une exactitude élevée peut simplement refléter la distribution des classes, et non une performance réelle.

> « ... l'exactitude n'est plus une mesure appropriée [pour les jeux de données déséquilibrés], car elle ne fait pas de distinction entre le nombre d'exemples correctement classifiés des différentes classes. Par conséquent, elle peut conduire à des conclusions erronées ... ».

## Métriques fondamentales : Précision, Rappel, F1

Pour évaluer les classifieurs en situation de déséquilibre, nous nous appuyons sur la **précision, le rappel et le score F1**, qui se concentrent sur les erreurs dans les classes minoritaires. Celles-ci sont dérivées de la matrice de confusion, par exemple pour une classification binaire :

|                     | Prédit Positif      | Prédit Négatif      |
|---------------------|---------------------|---------------------|
| **Réel Positif**    | Vrai Positif (TP)   | Faux Négatif (FN)   |
| **Réel Négatif**    | Faux Positif (FP)   | Vrai Négatif (TN)   |

À partir de ces décomptes, nous définissons :

- **Précision** = TP / (TP + FP) – proportion de prédictions positives qui sont correctes :
- **Rappel** = TP / (TP + FN) – proportion de positifs réels qui ont été trouvés :
- **Score F1** = moyenne harmonique de la précision et du rappel :
  \[ \mathrm{F1} = \frac{2 \cdot \mathrm{TP}}{2 \cdot \mathrm{TP} + \mathrm{FP} + \mathrm{FN}}. \]

Chaque métrique met en évidence des erreurs différentes : la précision pénalise les fausses alarmes (FP), tandis que le rappel pénalise les omissions (FN). Le score F1 équilibre les deux. Pour être complet, notez que l'exactitude peut aussi s'écrire \( (TP + TN) / (TP+TN+FP+FN) \):contentReference[oaicite:8]{index=8}, mais sur des données déséquilibrées, elle masque les défaillances du modèle.

En pratique, la fonction `classification_report` de scikit-learn calcule ces métriques pour chaque classe. Par exemple :

rapporte la précision, le rappel, le score F1 (et le support) pour chaque classe de ticket.

## Moyennage Macro vs Micro

Pour les problèmes multi-classe, les métriques peuvent être moyennées de différentes manières. Le **moyennage micro** regroupe toutes les classes en additionnant les TP, FP, FN globaux, puis calcule les métriques – ce qui revient à pondérer par le support de chaque classe. Le **moyennage macro** calcule la métrique pour chaque classe séparément, puis prend la moyenne non pondérée. En d'autres termes, le moyennage macro traite toutes les classes de manière égale (les classes rares comptent autant que les classes communes), tandis que le micro favorise la performance sur les classes fréquentes. Utilisez le **moyennage macro** lorsque les classes minoritaires sont critiques (par ex. intercepter un ticket urgent rare), et le **moyennage micro** lorsque l'exactitude globale sur tous les tickets est plus importante.

| Moyennage | Comment c'est calculé                                        | Quand l'utiliser                                         |
|-----------|--------------------------------------------------------------|----------------------------------------------------------|
| **Micro** | Décomptes globaux de TP, FP, FN sur toutes les classes       | Donne la performance globale (favorise les grandes classes) |
| **Macro** | Moyenne de la métrique de chaque classe (chaque classe pondérée également) | Assure que les petites/rares classes comptent de manière égale |

## Défis du Multi-étiquette

Les tickets de support technique portent souvent plusieurs étiquettes à la fois (par ex. un ticket peut avoir à la fois une étiquette de **file d'attente** et de **priorité**). Dans les configurations multi-étiquette, des métriques supplémentaires s'appliquent :

*   **Exactitude du sous-ensemble** (Correspondance exacte) – fraction d'échantillons où *toutes* les étiquettes prédites correspondent exactement à l'ensemble des étiquettes réelles. C'est très strict : une seule mauvaise étiquette signifie un échec.
*   **Perte de Hamming** – la fraction de prédictions d'étiquettes individuelles qui sont incorrectes. La perte de Hamming est plus indulgente : chaque étiquette est jugée indépendamment. Une perte de Hamming plus faible (proche de 0) est meilleure.
*   **Perte de classement d'étiquette** – mesure combien de paires d'étiquettes sont incorrectement ordonnées par confiance. C'est pertinent lorsque le modèle produit des scores pour chaque étiquette, et que nous nous soucions du classement des étiquettes pour chaque ticket.

Scikit-learn fournit des fonctions comme `accuracy_score` (exactitude du sous-ensemble en mode multi-étiquette) et `hamming_loss`. En général, on choisit la métrique qui correspond aux besoins métier : la correspondance exacte si vous avez besoin que toutes les étiquettes soient correctes, ou la perte de Hamming/classement si une correction partielle est acceptable.

## La matrice de confusion en pratique

Une matrice de confusion est souvent le premier aperçu du comportement d'un classifieur. En Python, vous pouvez la calculer et l'afficher avec scikit-learn :

```python
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay

cm = confusion_matrix(y_test, y_pred, labels=classes)
print("Confusion Matrix:\n", cm)

# To visualize:
ConfusionMatrixDisplay(cm, display_labels=classes).plot()
```

Ici, `cm[i, j]` est le nombre de tickets dont la classe réelle est `i` mais qui ont été prédits comme étant de la classe `j`.
Lors de l'inspection d'une matrice de confusion (ou de sa carte de chaleur), recherchez :

*   **Cellules hors diagonale** – elles indiquent des erreurs de classification (quelles classes sont le plus souvent confondues).
*   **Faux positifs vs faux négatifs** – par ex. une somme de ligne élevée hors diagonale signifie que le modèle a fréquemment manqué cette classe réelle (beaucoup de FN) ; une somme de colonne élevée hors diagonale signifie de nombreuses prédictions incorrectes de cette classe (FP).
*   **Classes sous-représentées** – les classes avec peu d'exemples peuvent apparaître comme des lignes/colonnes presque vides, indiquant que le modèle les prédit rarement correctement.

Analyser correctement la matrice de confusion aide à cibler le nettoyage des données ou les ajustements du modèle pour des types de tickets spécifiques.

## Stratégie d'évaluation pour les systèmes de tickets réels

Construire un pipeline d'évaluation fiable nécessite plus que le simple choix des métriques :

*   **Données propres et étiquetées** : Assurez-vous que votre jeu de test est représentatif et correctement étiqueté. Supprimez les doublons ou les tickets mal étiquetés avant l'évaluation.
*   **Modèle de base vs Modèle affiné** : Comparez toujours votre modèle d'IA à des modèles de base simples (par ex. un prédicteur de classe majoritaire, ou des systèmes basés sur des règles de mots-clés). Mesurez les améliorations relatives en utilisant les métriques choisies.
*   **Réévaluation périodique** : Les tendances des tickets changent avec le temps (problèmes saisonniers, nouveaux produits). Prévoyez de ré-entraîner et de réévaluer le modèle régulièrement ou de le déclencher en cas de dérive des données (`data drift`).
*   **Communication avec les parties prenantes** : Traduisez les métriques en informations exploitables pour les parties prenantes non techniques. Par exemple, « Le rappel pour les tickets urgents est passé de 75 % à 85 %, ce qui signifie que nous interceptons automatiquement 10 % de problèmes à haute priorité en plus. » Utilisez des graphiques (par ex. des diagrammes à barres de la précision/rappel par classe) et soulignez l'impact métier (réponse plus rapide, réduction des arriérés).

## Conclusion

En résumé, **on ne peut pas améliorer ce que l'on ne mesure pas**. L'exactitude seule n'est pas suffisante pour des données de tickets complexes et déséquilibrées. À la place, suivez la précision, le rappel et le score F1 par classe (en utilisant les moyennes macro/micro appropriées), et envisagez des métriques multi-étiquette si vos tickets ont plusieurs annotations. Commencez à suivre les métriques dès le début de toute intégration d'IA afin que les gains (ou les problèmes) soient visibles. En se concentrant sur les bonnes métriques dès le premier jour, les équipes de support peuvent améliorer itérativement leurs classifieurs de tickets et fournir une automatisation plus fiable.

Vous voulez essayer ces idées sur vos propres données ? Découvrez la plateforme [Open Ticket AI Demo](https://open-ticket-ai.com) pour expérimenter avec de vrais jeux de données de tickets et des outils d'évaluation intégrés.