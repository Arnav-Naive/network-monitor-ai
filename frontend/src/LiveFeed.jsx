export default function LiveFeed({ liveRows }) {
  return (
    <div className="bg-gray-800 rounded-xl border border-gray-700 overflow-hidden mb-6">
      <div className="p-4 border-b border-gray-700 flex items-center gap-2">
        <span className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
        <h2 className="text-lg font-semibold">Live Feed</h2>
        <span className="text-gray-400 text-sm ml-auto">{liveRows.length} new rows</span>
      </div>
      <div className="overflow-y-auto max-h-48">
        <table className="w-full text-sm">
          <thead className="bg-gray-700 text-gray-300 sticky top-0">
            <tr>
              <th className="p-3 text-left">Time</th>
              <th className="p-3 text-left">Switch</th>
              <th className="p-3 text-left">CPU</th>
              <th className="p-3 text-left">Temp</th>
              <th className="p-3 text-left">Anomaly</th>
            </tr>
          </thead>
          <tbody>
            {liveRows.map((row, i) => (
              <tr key={i} className="border-t border-gray-700">
                <td className="p-3 text-gray-400">{row.timestamp}</td>
                <td className="p-3 text-green-400">{row.switch}</td>
                <td className={`p-3 ${row.cpu > 85 ? 'text-red-400 font-bold' : ''}`}>{row.cpu}%</td>
                <td className={`p-3 ${row.temperature > 78 ? 'text-red-400 font-bold' : ''}`}>{row.temperature}°C</td>
                <td className="p-3">
                  {row.anomalies
                    ? <span className="bg-yellow-900 text-yellow-300 px-2 py-1 rounded text-xs">{row.anomalies}</span>
                    : <span className="text-gray-500">Normal</span>}
                </td>
              </tr>
            ))}
            {liveRows.length === 0 && (
              <tr><td colSpan="5" className="p-4 text-center text-gray-500">Waiting for live data...</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  )
}