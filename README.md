# Mapas Estelares com Python

Como eu não sou um astrônomo profissional, adaptei o código a seguir para um uso mais dinâmico, você pode consultar o projeto original em: [How to Use Python to Create Custom Star Maps for Your Next Stargazing Journey](https://levelup.gitconnected.com/how-to-use-python-to-create-custom-star-maps-for-your-next-stargazing-journey-9908b421f30e)

## Installation

```
pip install -r requirements.txt
```

## Warnings

Para a versão do package [tzwhere](https://github.com/pegler/pytzwhere), submeti a pull request [#64](https://github.com/pegler/pytzwhere/pull/64). Pois há um bug na construção do array do numpy no método construtor principal, a solução deixei a seguir, se o problema persistir:

```python
    for tzname, poly in pgen:
            self.timezoneNamesToPolygons[tzname].append(poly)
        for tzname, polys in self.timezoneNamesToPolygons.items():
            self.timezoneNamesToPolygons[tzname] = WRAP(polys, dtype='object') # <- adicionar o tipo do objeto

            if forceTZ:
                self.unprepTimezoneNamesToPolygons[tzname] = WRAP(polys)
```

## How to Use

```python
from starmap import StarMap

generator = StarMap(when = '2024-01-27 21:00') # setado em São Luís, por padrão

generator.star_map(
    location = 'São Luís, Maranhão, Brasil', 
    chart_size = 10, max_star_size = 150, show = True
)

generator = StarMap(when = '2024-01-27 09:00', lat = 35.5074466, long = 139.1104488) # setando em Tóquio, Japão às 9 horas da manhã

generator.star_map(
    location = 'Tóquio, Japão', chart_size = 10, max_star_size = 150, show = True, daylight = True # configurando o modo para luz do dia
)

```

## Results

![](images/São%20Luís%2C%20Maranhão%2C%20Brasil_20240127_2100.png)

![](images/Tokyo,%20Japão_20240127_0900.png)

## To-Do

- [ ] Download Images Bytes
- [ ] WebApp (aguardar nova versão do tzwhere)
