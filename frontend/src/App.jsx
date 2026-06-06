import { useState, useEffect, useRef } from "react"
import SummaryCards from "./SummaryCards"
import BandwidthChart from "./BandwidthChart"
import MetricsLineChart from "./MetricsLineChart"
import LiveFeed from "./LiveFeed"

const API_BASE = import.meta.env.VITE_API_URL || ''
const BACKEND_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

function App() {
  const [switches, setSwitches] = useState([])
  const [filterType, setFilterType] = useState('all')
  const [dateRange, setDateRange] = useState('24h')
  const [switchFilter, setSwitchFilter] = useState('all')
  const [metrics, setMetrics] = useState([])
  const [liveRows, setLiveRows] = useState([])
  const [loading, setLoading] = useState(true)
  const filteredMetrics = metrics.filter(m => {
    // Anomaly filter
    if (filterType === 'anomalies' && (!m.anomalies || m.anomalies === 'None')) return false
    if (filterType === 'normal' && m.anomalies && m.anomalies !== 'None') return false
    
    // Switch filter
    if (switchFilter !== 'all' && m.switch_name !== switchFilter) return false
    
    // Date range filter
    if (dateRange !== 'all') {
      const hours = dateRange === '1h' ? 1 : dateRange === '24h' ? 24 : 168
      const cutoff = new Date(Date.now() - hours * 60 * 60 * 1000)
      const metricTime = new Date(m.timestamp)
      if (metricTime < cutoff) return false
    }
    
    return true
  })
  const wsRef = useRef(null)

  useEffect(() => {
    fetch(`${API_BASE}/api/switches/`)
      .then(r => r.json())
      .then(data => setSwitches(data.results))

    fetch(`${API_BASE}/api/metrics/`)
      .then(r => r.json())
      .then(data => {
        setMetrics(data.results)
        setLoading(false)
      })

    // WebSocket
    const wsUrl = import.meta.env.VITE_API_URL
      ? `wss://network-monitor-ai.onrender.com/ws/metrics/`
      : `ws://localhost:8000/ws/metrics/`

    const ws = new WebSocket(wsUrl)

    wsRef.current = ws

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      setLiveRows(prev => [data, ...prev].slice(0, 20))
    }

    ws.onclose = () => {
      console.log('WebSocket disconnected')
    }

    return () => ws.close()
  }, [])

  if (loading) return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center">
      <p className="text-white text-xl">Loading...</p>
    </div>
  )

  return (
    <div className="min-h-screen bg-gray-900 text-white p-6">
      {/* Header */}
      <div className="mb-6 flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">🔧 Network Monitor AI</h1>
          <p className="text-gray-400 text-sm mt-1">AI-Powered Switch Monitoring — Tata Steel Internship</p>
        </div>
        <div className="flex gap-3">
          <a href={`${BACKEND_URL}/alerts/`} target="_blank"
            className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg text-sm font-semibold transition-colors">
            🚨 Alert History
          </a>
          <a href={`${BACKEND_URL}/export/`} target="_blank"
            className="bg-green-600 hover:bg-green-700 px-4 py-2 rounded-lg text-sm font-semibold transition-colors">
            ⬇ Export CSV
          </a>
        </div>
      </div>

      {/* Filter Bar */}
      <div className="bg-gray-800 rounded-xl p-4 border border-gray-700 mb-6 flex flex-wrap gap-6 items-center">
        
        {/* Time Range */}
        <div className="flex items-center gap-2">
          <span className="text-gray-400 text-sm font-semibold">Time:</span>
          {['1h', '24h', '7d', 'all'].map(r => (
            <button key={r} onClick={() => setDateRange(r)}
              className={`px-3 py-1 rounded-full text-xs font-semibold transition-colors
                ${dateRange === r ? 'bg-green-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'}`}>
              {r === '1h' ? 'Last 1h' : r === '24h' ? 'Last 24h' : r === '7d' ? 'Last 7d' : 'All Time'}
            </button>
          ))}
        </div>

        {/* Anomaly Filter */}
        <div className="flex items-center gap-2">
          <span className="text-gray-400 text-sm font-semibold">Show:</span>
          {[['all','All'], ['anomalies','Anomalies'], ['normal','Normal']].map(([val, label]) => (
            <button key={val} onClick={() => setFilterType(val)}
              className={`px-3 py-1 rounded-full text-xs font-semibold transition-colors
                ${filterType === val
                  ? val === 'anomalies' ? 'bg-red-600 text-white'
                  : val === 'normal' ? 'bg-blue-600 text-white'
                  : 'bg-green-600 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'}`}>
              {label}
            </button>
          ))}
        </div>

        {/* Switch Filter */}
        <div className="flex items-center gap-2">
          <span className="text-gray-400 text-sm font-semibold">Switch:</span>
          <button onClick={() => setSwitchFilter('all')}
            className={`px-3 py-1 rounded-full text-xs font-semibold transition-colors
              ${switchFilter === 'all' ? 'bg-green-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'}`}>
            All
          </button>
          {switches.map(sw => (
            <button key={sw.id} onClick={() => setSwitchFilter(sw.name)}
              className={`px-3 py-1 rounded-full text-xs font-semibold transition-colors
                ${switchFilter === sw.name ? 'bg-green-600 text-white' : 'bg-gray-700 text-gray-300 hover:bg-gray-600'}`}>
              {sw.name.replace(' Switch', '').replace(' 0', ' ')}
            </button>
          ))}
        </div>

        {/* Results count */}
        <div className="ml-auto text-gray-400 text-sm">
          {filteredMetrics.length} results
        </div>
      </div>


      {/* Summary Cards */}
      <SummaryCards metrics={filteredMetrics} switches={switches} />

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

      {/* Charts */}
      <div className="grid grid-cols-2 gap-6 mb-6">
        <MetricsLineChart metrics={filteredMetrics} />
        <BandwidthChart switches={switches} metrics={filteredMetrics} />
      </div>

      {/* Live Feed */}
      <LiveFeed liveRows={liveRows} />

      {/* Metrics Table */}
      <div className="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden">
        <div className="p-4 border-b border-gray-700 flex justify-between items-center">
          <h2 className="text-lg font-semibold">Recent Metrics</h2>
          <span className="text-gray-400 text-sm">{filteredMetrics.length} readings</span>
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
            {filteredMetrics.map(m => (
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