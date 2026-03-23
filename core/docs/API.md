# API Reference

## Autenticação

Base: `/api/v1/accounts/`

- `POST /login/` - Autenticação via token.
- `POST /users/` - Cria usuário com perfil associado.
- `GET /me/` - Retorna usuário corrente.

## Clientes

Base: `/api/v1/customers/`

- `GET/POST /segments/`
- `GET/PUT/PATCH/DELETE /segments/{id}/`
- `GET/POST /customers/`
- `GET/PUT/PATCH/DELETE /customers/{id}/`
- `GET/POST /addresses/`
- `GET/PUT/PATCH/DELETE /addresses/{id}/`

Regras:
- Endereço principal único por cliente (`is_main`).

## Produtos

Base: `/api/v1/products/`

- `GET/POST /categories/`, `/suppliers/`, `/products/`
- `GET/PUT/PATCH/DELETE /categories/{id}/`, `/suppliers/{id}/`, `/products/{id}/`
- `GET /products/low_stock/` - produtos abaixo do nível de reposição.
- `POST /products/{id}/adjust_stock/` - ajuste de estoque em controller dedicado.

## Pedidos

Base: `/api/v1/orders/`

- `GET/POST /orders/`
- `GET/PUT/PATCH/DELETE /orders/{id}/`
- `GET/POST /payments/`
- `GET/PUT/PATCH/DELETE /payments/{id}/`

Regras:
- pedidos iniciam em `draft`.
- status permitidos via `SalesOrder.STATUS_TRANSITIONS`.
- `PaymentTransaction` aprovada define `order.status=paid`.

## Shipping

Base: `/api/v1/shipping/`

- `GET/POST /warehouses/`
- `GET/PUT/PATCH/DELETE /warehouses/{id}/`
- `GET/POST /shipments/`
- `GET/PUT/PATCH/DELETE /shipments/{id}/`

Regras:
- só é possível criar remessa para pedidos `confirmed` ou `paid`.
- item de remessa deve pertencer ao mesmo pedido.
