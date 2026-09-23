# Fabrica public rules

This repository is Fabrica's canonical public rule library. Its engineering rules can be shared across projects and given to coding agents.

Each rule explains an engineering expectation, when it applies, and how to check whether a change follows it. Start with one group, read its rules, and adopt the guidance that fits your project.

## How this fits with Code Rules

[Code Rules](https://github.com/fabricahq/code-rules) is the tool that imports, versions, and prepares rules for agents to read. This repository supplies a collection of rules that the tool can import.

Projects can combine this library with other public or private libraries. You can also write local rules, exclude imported rules, or replace them to fit your needs. These practices are choices for your project, not requirements for using Code Rules.

Giving an agent a rule does not guarantee compliance. Ask your agent to read the relevant rules before implementation and use them during review, alongside your tests and other checks.

## What's included

| Group | Rules | What it helps with |
| --- | --- | --- |
| [Code design](practices/code-design/) | 1 | Express operations as meaningful steps |
| [Performance](practices/performance/) | 1 | Remove repeated work from measured hot paths |
| [Testing](practices/testing/) | 6 | Choose tests by risk, test at the lowest layer, keep tests independent, test behavior, reproduce bugs, and cover boundary cases |
| [Go](techs/go/) | 4 | Explain contracts and preserve useful errors |
| [goose](techs/goose/) | 1 | Keep SQL migrations discoverable |
| [JavaScript](techs/javascript/) | 7 | Coordinate async work, use browser APIs efficiently, and keep paths analyzable |
| [Playwright](techs/playwright/) | 3 | Keep browser tests independent and use stable locators |
| [React](techs/react/) | 39 | Structure components, manage state, and avoid unnecessary work |
| [TanStack Query](techs/tanstack-query/) | 15 | Manage query keys, caching, mutations, and hydration |
| [TanStack Router](techs/tanstack-router/) | 18 | Structure routes, validate inputs, and coordinate data loading |
| [TypeScript](techs/typescript/) | 33 | Model data, preserve contracts, and keep code understandable |
| [Zustand](techs/zustand/) | 11 | Design stores, subscriptions, and persistence |

The 139 rules are independently selectable. A group's rules describe their own scope: some React rules apply only to Next.js or particular React APIs. Style preferences and performance techniques are choices to evaluate for your project, not universal requirements.

Practice groups apply across languages. Their TypeScript examples illustrate the ideas; they do not limit those practices to TypeScript projects.

The library contains source rules and group metadata:

```text
rule-library.yaml        Library format and license information
practices/               Practices that apply across technologies
  code-design/
  performance/
  testing/
techs/                   Guidance for a specific technology
  typescript/
```

Each group includes `_group.yaml` metadata and one Markdown file per rule. For format details, see [Rule and library format](https://code-rules.fabricahq.com/reference/rule-library-format/).

## Use the library

The library manifest (`rule-library.yaml`) and group metadata (`_group.yaml`) use YAML.

The first release, `v0.1.0`, must be published before the commands below work. Until then, the proposed library is available for review in this repository's pull requests.

After that release, [install Code Rules](https://code-rules.fabricahq.com/start-here/install/) and run these commands from your project's root:

```sh
code-rules project init
code-rules project add library fabrica \
  --repository https://github.com/fabricahq/.code-rules-public.git \
  --ref v0.1.0 \
  --groups practices/code-design
code-rules project sync
code-rules project check
```

This imports only the Code design group. In the proposed `v0.1.0` release, that group contains one rule: [Express operations as meaningful steps](practices/code-design/express-operations-as-meaningful-steps.md).

Open `.code-rules/generated/RULES.md` to read the generated guidance. Then connect it to your agent's project instructions using the [first-project walkthrough](https://code-rules.fabricahq.com/start-here/set-up-project/).

To select more groups, repeat `--groups` for each group ID when adding the source. Pin a published tag or full commit so your project adopts updates deliberately. For exclusions and replacements, see [Import rules](https://code-rules.fabricahq.com/guides/select-rules/).

## Propose a change

Open a pull request with the rule change and the problem it addresses. Keep each rule focused on one expectation, with examples, applicability, exceptions where needed, and a way to verify compliance.

Follow the [authoring rubric](https://code-rules.fabricahq.com/reference/rule-authoring/) and run this command from the library root:

```sh
code-rules library check
```

The command validates the library's format. Review the guidance itself as well: a rule should help someone make a better engineering decision.

Keep rule paths stable because projects use them to identify rules. Include source attribution and required notices when adapting others' work. Commit source rules here; Code Rules generates agent guidance in consuming projects.

Maintainers review changes through pull requests and publish version tags for approved releases. Existing release tags must not move. The first release follows review and an end-to-end import check.

## License and sources

The library uses the [MIT license](LICENSE.md), with copyright attributed to Fabrica Systems LLC. Some rules include material from mkosir, Vercel Labs, and Deckard Gerritsen, plus guidance informed by official documentation. Fabrica-specific rules are not included.

Rules adapted from third-party sources carry attribution in their metadata. [NOTICE.md](NOTICE.md) preserves the required third-party notices.
