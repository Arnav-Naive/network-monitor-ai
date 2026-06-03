import { LineChart, Line, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function MetricsLineChart({ metrics }) {
  const data = [...metrics].reverse().slice(-20).map(m => ({
    time: m.timestamp ? m.timestamp.split('T')[1]?.slice(0,5) || m.timestamp.slice(-8,-3) : '',
    CPU: m.cpu_usage,
    Temp: m.temperature,
    Memory: m.memory_usage,
  }))

  return (
    <div className="bg-gray-800 rounded-xl p-5 border border-gray-700 mb-6">
      <h2 className="text-lg font-semibold mb-4">📊 CPU / Temp / Memory Trends</h2>
      <ResponsiveContainer width="100%" height={250}>
        <LineChart data={data}>
          <XAxis dataKey="time" stroke="#9ca3af" tick={{ fontSize: 11 }} />
          <YAxis stroke="#9ca3af" domain={[0, 100]} />
          <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
          <Legend />
          <Line type="monotone" dataKey="CPU" stroke="#ef4444" dot={false} strokeWidth={2} />
          <Line type="monotone" dataKey="Temp" stroke="#f97316" dot={false} strokeWidth={2} />
          <Line type="monotone" dataKey="Memory" stroke="#10b981" dot={false} strokeWidth={2} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}