/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  docs: [
    'intro',
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
      ],
    },
    {
      type: 'category', label: 'Reference',
      items: [
        'reference/apiversion-policy',
        'reference/id-formats',
        'reference/migration',
        'reference/privacy',
      ],
    },
  ],
};

export default sidebars;
