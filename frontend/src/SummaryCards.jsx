export default function SummaryCards({ metrics, switches }) {
  const total = metrics.length
  const anomalies = metrics.filter(m => m.anomalies && m.anomalies !== 'None').length
  const health = total > 0 ? Math.round(((total - anomalies) / total) * 100) : 0

  return (
    <div className="grid grid-cols-3 gap-4 mb-6">
      <div className="bg-gray-800 rounded-xl p-5 border-l-4 border-green-500">
        <p className="text-gray-400 text-xs uppercase font-semibold mb-1">Total Readings</p>
        <p className="text-4xl font-bold text-white">{total}</p>
      </div>
      <div className="bg-gray-800 rounded-xl p-5 border-l-4 border-red-500">
        <p className="text-gray-400 text-xs uppercase font-semibold mb-1">ML Anomalies</p>
        <p className="text-4xl font-bold text-white">{anomalies}</p>
      </div>
      <div className="bg-gray-800 rounded-xl p-5 border-l-4 border-blue-500">
        <p className="text-gray-400 text-xs uppercase font-semibold mb-1">System Health</p>
        <p className="text-4xl font-bold text-white">{health}%</p>
      </div>
    </div>
  )
}