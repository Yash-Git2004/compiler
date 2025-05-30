// Import ESLint configurations and plugins
import js from '@eslint/js'                              // ESLint’s base JavaScript rules
import globals from 'globals'                            // Common global variables (e.g., for browser environments)
import reactHooks from 'eslint-plugin-react-hooks'       // Plugin for enforcing React Hooks rules
import reactRefresh from 'eslint-plugin-react-refresh'   // Plugin to support React Fast Refresh

export default [
  { ignores: ['dist'] },
  {
    files: ['**/*.{js,jsx}'],
    languageOptions: {
      ecmaVersion: 2020,
      globals: globals.browser,
      parserOptions: {
        ecmaVersion: 'latest',
        ecmaFeatures: { jsx: true },
        sourceType: 'module',
      },
    },
    plugins: {
      'react-hooks': reactHooks,
      'react-refresh': reactRefresh,
    },
    rules: {
      ...js.configs.recommended.rules,
      ...reactHooks.configs.recommended.rules,
      'no-unused-vars': ['error', { varsIgnorePattern: '^[A-Z_]' }],
      'react-refresh/only-export-components': [
        'warn',
        { allowConstantExport: true },
      ],
    },
  },
]
