# My own graphic library
Graphics library that render polygons without external frameworks

## Tools
Used tools during the development and testing:

### Right Triangle Calculator
https://www.calculator.net/right-triangle-calculator.html
### Pythagorean Theorem Calculator
https://www.calculator.net/pythagorean-theorem-calculator.html
### Low of sines Calculator
https://www.omnicalculator.com/math/law-of-sines
### Scientific Notation Converter
https://www.calculatorsoup.com/calculators/math/scientific-notation-converter.php
### Vector normal to plane Calculator
https://www.vcalc.com/wiki/vector-normal-to-a-plane
### Find normal vector to a plane
https://web.ma.utexas.edu/users/m408m/Display12-5-4.shtml


## TODO
* Que el cambio de posición de la cámara hacia una no sea estática hacia alguno de los puntos cardinales, sino hacia el ángulo de visión.
* Que el ratón se pueda mover sin límite hacia todos los angulos, y no solo ±180 grados.
* Renderizar solo los poligonos más cercanos a la cámara, ignorando los tapados por estos.
* Transformar todos los diccionarios del tipo {"x","y","z"} a objetos de la clase Point.
* Extrapolar el punto anterior a otras clases como Polygon, Line.
* Añadir Ctrl + F3
* Aplicar transformacion como la rotación y escala solo cuando estos parámetros cambian.
* El ángulo de visión está fijado a 45º devido a la manera en la que se obtienen los 3 puntos para conseguir le Vector Normal de los planos de la visión de la cámara.
* Si la cámara tiene las mismas coordenadas que una arista, crasea por la división de 0.