module.exports = {
  root: true,
  env: {
    commonjs: true,
    es2020: true,
    node: true,
  },
  extends: [
    'airbnb-base',
  ],
  parserOptions: {
    ecmaVersion: 11,
  },
  rules: {
    'import/no-extraneous-dependencies': 'off',
    'jsx-a11y/control-has-associated-label': 'off',
    'func-names': 'off',
    'no-console': 'off',
    'no-param-reassign': 'off',
    'no-underscore-dangle': 'off',
    'no-continue': 'off',
    'no-var': 'off',
    'no-restricted-syntax': 'off',
    'no-prototype-builtins': 'off',
    'guard-for-in': 'off',
  },
};
