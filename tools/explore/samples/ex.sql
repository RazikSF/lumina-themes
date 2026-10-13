-- Moyenne par classe, au-dessus de 10
SELECT c.nom AS classe,
       ROUND(AVG(n.valeur), 2) AS moyenne,
       COUNT(*) AS copies
FROM notes AS n
JOIN eleves AS e ON e.id = n.eleve_id
JOIN classes AS c ON c.id = e.classe_id
WHERE n.trimestre = 1 AND n.valeur IS NOT NULL
GROUP BY c.nom
HAVING AVG(n.valeur) > 10
ORDER BY moyenne DESC;
