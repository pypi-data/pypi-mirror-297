# SAP Business One - Python Service Layer Sales wrapper

This package provides a base wrapper for accessing the SAP
service layer in Python for sales objects.

## Installation

```shell
$ python -m pip install sbo-service-sales
```

## Helpful Examples

```
def read_sales_order_by_po_and_shipto(sbo: service, po, shipto):
    filter = f"(NumAtCard eq '{po}') and (ShipToCode eq '{shipto}')"

    return read_sales_order_with_filter(sbo, filter)


def so_exists_by_cust_po(sbo: service, customer, po_number):
    filter = f'(CardCode eq \'{customer}\') and (NumAtCard eq \'{po_number}\')'

    response = read_sales_order_with_filter(sbo, filter)

    return response['success']
```
