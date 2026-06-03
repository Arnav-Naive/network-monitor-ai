import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function BandwidthChart({ switches, metrics }) {
  const data = switches.map(sw => {
    const latest = metrics.find(m => m.switch_name === sw.name)
    return {
      name: sw.name.replace(' Switch', '').replace(' 0', ' '),
      Bandwidth: latest?.bandwidth || 0,
      TX: latest?.tx_rate || 0,
      RX: latest?.rx_rate || 0,
    }
  })

  return (
    <div className="bg-gray-800 rounded-xl p-5 border border-gray-700 mb-6">
      <h2 className="text-lg font-semibold mb-4">📶 Per-Switch Bandwidth (Latest)</h2>
      <ResponsiveContainer width="100%" height={250}>
        <BarChart data={data}>
          <XAxis dataKey="name" stroke="#9ca3af" />
          <YAxis stroke="#9ca3af" />
          <Tooltip contentStyle={{ backgroundColor: '#1f2937', border: 'none' }} />
          <Legend />
          <Bar dataKey="Bandwidth" fill="#6366f1" radius={[4,4,0,0]} />
          <Bar dataKey="TX" fill="#10b981" radius={[4,4,0,0]} />
          <Bar dataKey="RX" fill="#f59e0b" radius={[4,4,0,0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}