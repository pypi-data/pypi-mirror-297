# borsaAPI

Bu Python kütüphanesi, Google App Engine üzerinde barındırılan bir API'den BIST hisse verilerini çekmek için kullanılabilir.

## Kullanım

```python
from borsaAPI import get_hisse_verisi

# Hisse verisini çek
df = get_hisse_verisi('THYAO')
print(df)


