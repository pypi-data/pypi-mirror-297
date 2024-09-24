# Random generator

## Main

### Unique

```python
import random_generator
print(random_generator.unique_string(10))
```

### String

```python
import random_generator

print(random_generator.string(15))
```

### Number

```python
import random_generator

print(random_generator.number(15))
```

## Financial

### Credit card number

```python
from random_generator.financial import credit_card
print("Visa:", credit_card('Visa'))
print("MasterCard:", credit_card('MasterCard'))
print("American Express:", credit_card('American Express'))
```

### Iban generator

```python
from random_generator.financial import iban

print(iban('PL'))
print(iban('DE'))
```

## Network

### IP generator

```python
from random_generator.network import ip

print(ip()) # *.*.*.*
print(ip('192.168.*.*'))
```

### Mac address generator

```python
from random_generator.network import mac_address

print(mac_address()) # *:*:*:*:*:*
print(mac_address('e2:*:*:*:*:*'))
```

## Date

### Date generator (Y-m-d)

```python
from random_generator.date import date

print(date())
print(date('1980-01-01', 'Today')) # From, To
```

## Poland

### NIP
Polish NIP generator

```python
import random_generator.poland

print(random_generator.poland.nip())
```
### PESEL
Polish PESEL generator

```python
import random_generator.poland

print(random_generator.poland.pesel())
```

## Germany

### Vat number
German vat number generator

```python
import random_generator.germany

print(random_generator.germany.vat())
```