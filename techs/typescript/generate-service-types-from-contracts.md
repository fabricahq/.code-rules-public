---
title: "Generate Service Types From Contracts"
whenToRead: "Before defining or reviewing TypeScript types for an API, database, schema, or message contract."
impact: "HIGH"
impactDescription: "prevents manually maintained service types from drifting away from source contracts"
tags: "typescript, codegen, api, contracts, generated-types"

attribution:
  - url: "https://github.com/mkosir/typescript-style-guide/blob/86bebd58a987e23277dba02028c0ee2d6ffb5073/website/src/pages/index.mdx"
    description: "Underlying TypeScript Style Guide material; required notice is retained in NOTICE.md."
---

## Generate Service Types From Contracts

Documentation becomes outdated the moment it's written, and worse than no documentation is wrong documentation. The same applies to types when describing the modules your app interacts with, such as APIs, messaging protocols and databases.

For external services, such as REST, GraphQL, and MQ it's crucial to generate types from their contracts, whether they use Swagger, schemas, or other sources (e.g. [openapi-ts](https://github.com/drwpow/openapi-typescript), [graphql-config](https://github.com/kamilkisiela/graphql-config)). Avoid manually declaring and maintaining types, as they can easily fall out of sync.

As an exception, only manually declare types when no options are available, such as when there is no documentation for the service, data cannot be fetched to retrieve a contract, or the database cannot be accessed to infer types.
