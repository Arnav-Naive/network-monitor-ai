import { useState, useEffect } from "react"
import SummaryCards from "./SummaryCards"
import BandwidthChart from "./BandwidthChart"

function App() {
  const [switches, setSwitches] = useState([])
  const [metrics, setMetrics] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/switches/')
      .then(r => r.json())
      .then(data => setSwitches(data.results))

    fetch('/api/metrics/')
      .then(r => r.json())
      .then(data => {
        setMetrics(data.results)
        setLoading(false)
      })
  }, [])

  if (loading) return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center">
      <p className="text-white text-xl">Loading...</p>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold">🔧 Network Monitor AI</h1>
        <p className="text-gray-400 text-sm mt-1">AI-Powered Switch Monitoring — Tata Steel Internship</p>
      </div>

      {/* Summary Cards */}
      <SummaryCards metrics={metrics} switches={switches} />

      {/* Switch Cards */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        {switches.map(sw => (
          <div key={sw.id} className="bg-gray-800 rounded-xl p-5 border border-gray-700 hover:border-green-500 transition-colors">
            <div className="flex justify-between items-start">
              <h2 className="text-lg font-semibold text-green-400">{sw.name}</h2>
              <span className="text-xs bg-green-900 text-green-300 px-2 py-1 rounded-full">Active</span>
            </div>
            <p className="text-gray-400 text-sm mt-2">📍 {sw.location}</p>
            <p className="text-gray-500 text-xs mt-1">🌐 {sw.ip_address}:{sw.port}</p>
          </div>
        ))}
      </div>

      {/* Bandwidth Chart */}
      <BandwidthChart switches={switches} metrics={metrics} />

      {/* Metrics Table */}
      <div className="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden">
        <div className="p-4 border-b border-gray-700 flex justify-between items-center">
          <h2 className="text-lg font-semibold">Recent Metrics</h2>
          <span className="text-gray-400 text-sm">{metrics.length} readings</span>
        </div>
        <table className="w-full text-sm">
          <thead className="bg-gray-700 text-gray-300">
            <tr>
              <th className="p-3 text-left">Switch</th>
              <th className="p-3 text-left">CPU %</th>
              <th className="p-3 text-left">Memory %</th>
              <th className="p-3 text-left">Temp °C</th>
              <th className="p-3 text-left">Bandwidth</th>
              <th className="p-3 text-left">Anomaly</th>
            </tr>
          </thead>
          <tbody>
            {metrics.map(m => (
              <tr key={m.id} className="border-t border-gray-700 hover:bg-gray-750">
                <td className="p-3 text-green-400 font-medium">{m.switch_name}</td>
                <td className={`p-3 ${m.cpu_usage > 85 ? 'text-red-400 font-bold' : ''}`}>{m.cpu_usage}</td>
                <td className="p-3">{m.memory_usage}</td>
                <td className={`p-3 ${m.temperature > 78 ? 'text-red-400 font-bold' : ''}`}>{m.temperature}</td>
                <td className="p-3">{m.bandwidth}</td>
                <td className="p-3">
                  {m.anomalies && m.anomalies !== 'None'
                    ? m.anomalies.includes('ML DETECTED')
                      ? <span className="bg-yellow-900 text-yellow-300 px-2 py-1 rounded text-xs">{m.anomalies}</span>
                      : <span className="bg-red-900 text-red-300 px-2 py-1 rounded text-xs">{m.anomalies}</span>
                    : <span className="text-gray-500">None</span>
                  }
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default App