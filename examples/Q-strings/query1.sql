/* query1.sql */
SELECT
  Symbol,
  Number,
  Mass,
  Abundance
FROM 'https://raw.githubusercontent.com/liquidcarbon/chembiodata/main/isotopes.csv'
WHERE Mass::INT = {x}