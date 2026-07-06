/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  docs: [
    'intro',
    {
      type: 'category', label: 'Development',
      items: [
        'development/index',
        'development/product-specification',
        'development/architecture-specification',
        'development/ontology-reference',
        'development/tooling-architecture',
        'development/test-strategy',
        'development/alpha-scope',
        'development/landscape-note',
        'development/acceptance-gate',
        {
          type: 'category', label: 'Analysis',
          collapsed: true,
          items: [
            'development/analysis/index',
            'development/analysis/base-context',
            'development/analysis/concept-mapping-briefing-analysis',
            'development/analysis/processkit-v1-rfc-analysis',
            'development/analysis/okf-compatibility-analysis',
            'development/analysis/processkit-v1-start-assessment',
          ],
        },
      ],
    },
    {
      type: 'category', label: 'Getting Started', collapsed: false,
      items: [
        'getting-started/overview',
        'getting-started/installing',
        'getting-started/first-entity',
      ],
    },
    {
      type: 'category', label: 'Primitives',
      items: [
        'primitives/overview',
        'primitives/format',
        'primitives/state-machines',
        'primitives/relationships',
        {
          type: 'category', label: 'Reference',
          collapsed: true,
          items: [
            'primitives/workitem',
            'primitives/logentry',
            'primitives/decisionrecord',
            'primitives/artifact',
            'primitives/note',
            'primitives/actor',
            'primitives/role',
            'primitives/binding',
            'primitives/scope',
            'primitives/discussion',
            'primitives/gate',
            'primitives/migration',
            'primitives/schedule',
            'primitives/constraint',
            'primitives/category',
            'primitives/cross-reference',
            'primitives/context-entity',
            'primitives/process-entity',
            'primitives/statemachine',
          ],
        },
      ],
    },
    {
      type: 'category', label: 'Skills',
      items: [
        'skills/overview',
        'skills/format',
        'skills/hierarchy',
        {
          type: 'category', label: 'Catalog',
          items: [
            'skills/catalog/process',
            'skills/catalog/language',
            'skills/catalog/framework',
            'skills/catalog/architecture',
            'skills/catalog/api',
            'skills/catalog/infrastructure',
            'skills/catalog/database',
            'skills/catalog/data',
            'skills/catalog/ai-ml',
            'skills/catalog/security',
            'skills/catalog/observability',
            'skills/catalog/performance',
            'skills/catalog/design',
          ],
        },
      ],
    },
    {
      type: 'category', label: 'Packages',
      items: [
        'packages/overview',
        'packages/minimal',
        'packages/managed',
        'packages/software',
        'packages/research',
        'packages/product',
      ],
    },
    {
      type: 'category', label: 'Processes',
      items: [
        'processes/overview',
      ],
    },
    {
      type: 'category', label: 'MCP Servers',
      items: [
        'mcp-servers/overview',
        'mcp-servers/harness-compatibility',
      ],
    },
    {
      type: 'category', label: 'Reference',
      items: [
        'reference/apiversion-policy',
        'reference/id-formats',
        'reference/migration',
        'reference/privacy',
        'reference/v2-contracts',
      ],
    },
  ],
};

export default sidebars;
