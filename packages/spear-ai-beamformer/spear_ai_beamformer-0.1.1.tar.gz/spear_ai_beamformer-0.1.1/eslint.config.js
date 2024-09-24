import { baseEslintConfig, prettierConfig } from "@spear-ai/eslint-config";

const eslintConfig = [
  {
    ignores: [
      ".coverage_reports",
      ".mypy_cache",
      ".pytest_cache",
      ".ruff_cache",
      ".venv",
      "node_modules",
    ],
  },
  ...baseEslintConfig,
  prettierConfig,
];

export default eslintConfig;
