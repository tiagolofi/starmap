# Mapas Estelares com Python

Como eu não sou um astrônomo profissional, adaptei o código a seguir para um uso mais dinâmico, você pode consultar o projeto original em: [How to Use Python to Create Custom Star Maps for Your Next Stargazing Journey](https://levelup.gitconnected.com/how-to-use-python-to-create-custom-star-maps-for-your-next-stargazing-journey-9908b421f30e)

## Installation

```
pip install -r requirements.txt
```

## Warnings

Para a versão do package [tzwhere](https://github.com/pegler/pytzwhere), submeti a pull request [#64](https://github.com/pegler/pytzwhere/pull/64). Pois há um bug na construção do array do numpy no método construtor principal, a solução deixei a seguir, se o problema persistir:

```{python}
    for tzname, poly in pgen:
            self.timezoneNamesToPolygons[tzname].append(poly)
        for tzname, polys in self.timezoneNamesToPolygons.items():
            self.timezoneNamesToPolygons[tzname] = WRAP(polys, dtype='object') # <- adicionar o tipo do objeto

            if forceTZ:
                self.unprepTimezoneNamesToPolygons[tzname] = WRAP(polys)
```

## How to Use

```{python}
from starmap import StarMap

generator = StarMap(when = '2024-01-27 21:00')

generator.star_map(
    location = 'São Luís, Maranhão, Brasil', 
    chart_size = 10, max_star_size = 150, show = True
)

```

## Results

![](images/São Luís, Maranhão, Brasil_20240127_2100.png)

## To-Do

- [] Download Images Bytes
- [] WebApp
