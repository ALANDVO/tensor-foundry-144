import { useState, useEffect } from "react"

interface HealthResponse {
  status: string
  service: string
  version: string
}

interface ConfigModel {
  default_mode: string | null
  hide_status: boolean
  quiet_startup: boolean
  map_enabled: boolean
  map_chars: number
}

interface ModeInfo {
  modes: string[]
  descriptions: Record<string, string>
}

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null)
  const [config, setConfig] = useState<ConfigModel | null>(null)
  const [modes, setModes] = useState<ModeInfo | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchAll = async () => {
      try {
        setLoading(true)
        const [healthRes, configRes, modesRes] = await Promise.all([
          fetch("/health").then(r => r.json()),
          fetch("/api/config").then(r => r.json()),
          fetch("/api/modes").then(r => r.json()),
        ])
        setHealth(healthRes)
        setConfig(configRes)
        setModes(modesRes)
        setError(null)
      } catch (e) {
        setError("Failed to connect to backend")
      } finally {
        setLoading(false)
      }
    }
    fetchAll()
  }, [])

  const handleModeChange = async (mode: string) => {
    if (!config) return
    try {
      const res = await fetch("/api/config", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ...config, default_mode: mode }),
      })
      const updated = await res.json()
      setConfig(updated)
    } catch (e) {
      setError("Failed to update mode")
    }
  }

  if (loading) return <div>Loading...</div>
  if (error) return <div style={{ color: "red" }}>{error}</div>

  return (
    <div style={{ padding: "2rem", fontFamily: "system-ui, sans-serif", maxWidth: "600px", margin: "0 auto" }}>
      <h1>Tensor Foundry 144</h1>
      <p><em>Makes your AI agent think like the laziest senior dev in the room.</em></p>

      <section style={{ marginTop: "2rem" }}>
        <h2>Health Check</h2>
        {health && (
          <pre style={{ background: "#f5f5f5", padding: "1rem", borderRadius: "4px" }}>
            {JSON.stringify(health, null, 2)}
          </pre>
        )}
      </section>

      <section style={{ marginTop: "2rem" }}>
        <h2>Configuration</h2>
        {config && (
          <pre style={{ background: "#f5f5f5", padding: "1rem", borderRadius: "4px" }}>
            {JSON.stringify(config, null, 2)}
          </pre>
        )}
      </section>

      <section style={{ marginTop: "2rem" }}>
        <h2>Mode Selector</h2>
        {modes && (
          <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
            {modes.modes.map(mode => (
              <button
                key={mode}
                onClick={() => handleModeChange(mode)}
                disabled={config?.default_mode === mode}
                style={{
                  padding: "0.5rem 1rem",
                  border: config?.default_mode === mode ? "2px solid #007bff" : "1px solid #ccc",
                  background: config?.default_mode === mode ? "#007bff" : "white",
                  color: config?.default_mode === mode ? "white" : "black",
                  borderRadius: "4px",
                  cursor: config?.default_mode === mode ? "default" : "pointer",
                }}
              >
                {mode} — {modes.descriptions[mode]}
              </button>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}

export default App
