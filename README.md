# Relay Nostr em Python

Este projeto é uma implementação **simples** de um **Relay Nostr**, seguindo o protocolo definido pelo **NIP-01**.

## Funcionalidades

- [x] Servidor WebSocket
- [x] Recebimento de eventos (`EVENT`)
- [x] Validação de eventos (hash + assinatura)
- [x] Armazenamento em banco de dados (SQLite)
- [x] Subscriptions (`REQ`)
- [x] Filtros por `kinds`, `authors`, `since`, `until`
- [x] Broadcast de eventos em tempo real
- [x] Suporte a `EOSE` (End Of Stored Events)

## Como o Relay Funciona (visão geral)

1. Clientes se conectam via **WebSocket**
2. Enviam mensagens JSON (`EVENT` ou `REQ`)
3. O relay:
   - valida o evento (NIP-01)
   - salva no banco
   - distribui para subscribers
4. Subscriptions recebem:
   - eventos antigos do banco
   - eventos novos em tempo real
5. O relay envia `EOSE` ao finalizar os eventos armazenados

## 🗂 Estrutura do Projeto

```text
src/
├── main.py              # Entrypoint do servidor
├── config.py            # Configurações gerais
├── db.py                # Banco de dados e queries
├── nostr/
│   ├── crypto.py        # Hash, serialização e assinatura (NIP-01)
│   ├── filters.py       # Filtros Nostr
│   └── __init__.py
├── relay/
│   ├── handlers.py      # EVENT, REQ, CLOSE
│   ├── broadcast.py     # Envio de eventos para subscribers
│   ├── subscriptions.py # Gerenciamento de subscriptions
│   └── __init__.py
└── requirements.txt
```

Cada módulo possui **uma responsabilidade bem definida**, facilitando manutenção e evolução.

## Requisitos

* Python **3.14.2**
* Bibliotecas:

  * `websockets`
  * `ecdsa`

## Instalação

Clone o repositório:

```bash
git clone https://github.com/agiota-dev/py-relay.git
cd py-relay
```

Crie um ambiente virtual (opcional, recomendado):

```bash
python -m venv venv
source venv/bin/activate
```

Instale as dependências:

```bash
pip install -r src/requirements.txt
```

## Executando o Relay

```bash
python src/main.py
```

Você verá algo como:

```text
Relay rodando em ws://0.0.0.0:8863
```

O relay já estará pronto para receber conexões.

## Protocolo Suportado

### EVENT

Publica um evento no relay:

```json
["EVENT", { ...event }]
```

O relay:

* recalcula o `id`
* verifica a assinatura
* salva no banco
* responde com `OK`

### REQ

Cria uma subscription:

```json
["REQ", "sub_id", { "kinds": [1] }]
```

O relay:

* envia eventos antigos
* envia `EOSE`
* mantém a subscription ativa para eventos novos

### EOSE

```json
["EOSE", "sub_id"]
```

Indica o fim dos eventos armazenados.

## Segurança e Validação

* O relay **não confia no cliente**
* O `id` do evento é sempre recalculado
* A assinatura ECDSA (`secp256k1`) é verificada
* Eventos inválidos são rejeitados

## Aviso

Este projeto **não é pronto para produção**.
Ele foi feito com foco em:

* clareza
* aprendizado
* entendimento do protocolo Nostr

Use como base, não como solução final.

## Contribuições

Pull requests são bem-vindos!
Se tiver sugestões, ideias ou correções, fique à vontade para contribuir.
