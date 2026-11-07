import { describe, it, expect, vi, beforeEach } from "vitest"
import { render, screen, waitFor } from "@testing-library/react"
import App from "./App"

const fetchMock = vi.fn()
globalThis.fetch = fetchMock

describe("App", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("renders loading state initially", () => {
    fetchMock.mockImplementation(() => new Promise(() => {}))

    render(<App />)
    expect(screen.getByText("Loading...")).toBeInTheDocument()
  })

  it("renders health, config, and modes when fetch succeeds", async () => {
    const mockHealth = { status: "ok", service: "tensor-foundry-144", version: "0.1.0" }
    const mockConfig = {
      default_mode: "standard",
      hide_status: false,
      quiet_startup: false,
      map_enabled: true,
      map_chars: 2000,
    }
    const mockModes = {
      modes: ["off", "lite", "standard", "ultra"],
      descriptions: {
        off: "No Ponytail instructions injected",
        lite: "Minimal guidance - just the essentials",
        standard: "Balanced guidance for most tasks",
        ultra: "Maximum guidance - thorough analysis",
      },
    }

    fetchMock
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve(mockHealth) })
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve(mockConfig) })
      .mockResolvedValueOnce({ ok: true, json: () => Promise.resolve(mockModes) })

    render(<App />)

    await waitFor(() => {
      expect(screen.getByText("Health Check")).toBeInTheDocument()
      expect(screen.getByText("Configuration")).toBeInTheDocument()
      expect(screen.getByText("Mode Selector")).toBeInTheDocument()
    })

    await waitFor(() => {
      expect(screen.getByRole("button", { name: /off/i })).toBeInTheDocument()
      expect(screen.getByRole("button", { name: /lite/i })).toBeInTheDocument()
      expect(screen.getByRole("button", { name: /standard/i })).toBeInTheDocument()
      expect(screen.getByRole("button", { name: /ultra/i })).toBeInTheDocument()
    })
  })

  it("renders error when fetch fails", async () => {
    fetchMock.mockRejectedValue(new Error("Network error"))

    render(<App />)

    await waitFor(() => {
      expect(screen.getByText("Failed to connect to backend")).toBeInTheDocument()
    })
  })
})
