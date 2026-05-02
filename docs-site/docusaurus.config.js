import {themes as prismThemes} from 'prism-react-renderer';

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'processkit',
  tagline: 'Primitives, skills, and process templates for AI-assisted work environments — a projectious.work project',
  favicon: 'img/favicon.ico',
  url: 'https://projectious-work.github.io',
  baseUrl: '/processkit/',
  organizationName: 'projectious-work',
  projectName: 'processkit',
  onBrokenLinks: 'warn',
  i18n: { defaultLocale: 'en', locales: ['en'] },
  markdown: {
    format: 'detect',
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },
  presets: [['classic', {
    docs: {
      sidebarPath: './sidebars.js',
      editUrl: 'https://github.com/projectious-work/processkit/tree/main/docs-site/',
      // Exclude any private/ subtrees from the published docs build.
      // This is the processkit convention: any directory named `private/`
      // anywhere under `context/` is user-private and must not be published.
      // Projects that build their own docs site should carry this same rule.
      exclude: ['**/private/**'],
    },
    blog: false,
    theme: { customCss: './src/css/custom.css' },
  }]],
  themeConfig: {
    colorMode: { defaultMode: 'dark', respectPrefersColorScheme: true },
    navbar: {
      title: 'processkit',
      items: [
        { type: 'docSidebar', sidebarId: 'docs', position: 'left', label: 'Docs' },
        { href: 'https://github.com/projectious-work/aibox', label: 'aibox', position: 'right' },
        { href: 'https://github.com/projectious-work/processkit', label: 'GitHub', position: 'right' },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        { title: 'Docs', items: [
          { label: 'Getting Started', to: '/docs/getting-started/overview' },
          { label: 'Primitives', to: '/docs/primitives/overview' },
          { label: 'Skills', to: '/docs/skills/overview' },
          { label: 'Packages', to: '/docs/packages/overview' },
        ]},
        { title: 'Ecosystem', items: [
          { label: 'aibox', href: 'https://github.com/projectious-work/aibox' },
          { label: 'aibox docs', href: 'https://projectious-work.github.io/aibox/' },
        ]},
        { title: 'Project', items: [
          { label: 'GitHub', href: 'https://github.com/projectious-work/processkit' },
          { label: 'Releases', href: 'https://github.com/projectious-work/processkit/releases' },
        ]},
      ],
      copyright: `\u00a9 ${new Date().getFullYear()} projectious.work`,
    },
    prism: { theme: prismThemes.github, darkTheme: prismThemes.dracula },
  },
};

export default config;
