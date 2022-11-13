export const getEnvValue = (name) => (
    window._env_?.[name] ?? process.env[name]
)
