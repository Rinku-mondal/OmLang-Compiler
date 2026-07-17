// Minimal Next.js pages router
import React, { useState } from 'react'

export default function Home() {
  const [source, setSource] = useState(`show "Hello, Om!"`)
  const [inputs, setInputs] = useState("")
  const [output, setOutput] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  async function compile() {
    setLoading(true)
    setError("")
    setOutput("")
    try {
      const res = await fetch((process.env.NEXT_PUBLIC_API_URL || "") + "/compile", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ source, inputs: inputs ? inputs.split(',').map(s => s.trim()) : [] }),
      })
      const data = await res.json()
      if (data.success) {
        setOutput(data.runtime_output || "(no output)")
      } else {
        setError(data.errors || "Unknown error")
      }
    } catch (e) {
      setError(String(e))
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: 20, fontFamily: 'Inter, Arial' }}>
      <h1>OmLang Web</h1>
      <p>Paste OmLang source below and press Compile. Provide comma-separated inputs if your program uses input().</p>
      <textarea value={source} onChange={e => setSource(e.target.value)} rows={10} cols={80} />
      <div style={{ marginTop: 10 }}>
        <input placeholder="comma-separated inputs" value={inputs} onChange={e => setInputs(e.target.value)} style={{ width: 400 }} />
      </div>
      <div style={{ marginTop: 10 }}>
        <button onClick={compile} disabled={loading}>{loading ? 'Compiling...' : 'Compile & Run'}</button>
      </div>
      <div style={{ marginTop: 20 }}>
        <h3>Output</h3>
        {error ? <pre style={{ color: 'red' }}>{error}</pre> : <pre>{output}</pre>}
      </div>
    </div>
  )
}
