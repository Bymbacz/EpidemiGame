// frontend/src/App.tsx

import React, { useState } from 'react'

type Team = { name: string; boats: number; cash: number }

type GameState = {
  turn: number
  ocean_fish_population: number
  sea_fish_population: number
  teams: Team[]
  game_id?: string
}

export default function App() {
  const [state, setState] = useState<GameState | null>(null)
  const [socket, setSocket] = useState<WebSocket | null>(null)
  const [started, setStarted] = useState(false)

  // New state for form fields
  const [startingSeaFish, setStartingSeaFish] = useState(1000)
  const [startingOceanFish, setStartingOceanFish] = useState(2000)
  const [seaFishCapacity, setSeaFishCapacity] = useState(2000)
  const [oceanFishCapacity, setOceanFishCapacity] = useState(2000)
  const [startingCash, setStartingCash] = useState(1000)

  // Start game: POST to backend, then open WebSocket immediately
  const startGame = async () => {
    const res = await fetch('http://localhost:8000/game/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        starting_sea_fish: startingSeaFish,
        starting_ocean_fish: startingOceanFish,
        sea_fish_capacity: seaFishCapacity,
        ocean_fish_capacity: oceanFishCapacity,
        starting_cash: startingCash,
      })
    })
    const data: GameState = await res.json()
    setState(data)
    setStarted(true)

    const ws = new WebSocket('ws://localhost:8000/ws/game')
    ws.onopen = () => console.log('WebSocket connected')
    ws.onmessage = (e) => {
      const updated: GameState = JSON.parse(e.data)
      setState(updated)
    }
    ws.onclose = () => console.log('WebSocket disconnected')
    setSocket(ws)
  }

  // Send end_turn action over WebSocket
  const endTurn = () => {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify({ action: 'end_turn' }))
    }
  }

  // Initial screen with Start button
  if (!started) {
    return (
      <div className="flex items-center justify-center h-full bg-gray-200">
        <form
          className="bg-white p-6 rounded shadow space-y-4"
          onSubmit={e => {
            e.preventDefault()
            startGame()
          }}
        >
          <div>
            <label className="block font-semibold mb-1">
              Starting Sea Fish
            </label>
            <input
              type="number"
              min={0}
              value={startingSeaFish}
              onChange={e => setStartingSeaFish(Number(e.target.value))}
              className="border rounded px-2 py-1 w-full"
            />
          </div>
          <div>
            <label className="block font-semibold mb-1">
              Sea Fish Capacity
            </label>
            <input
              type="number"
              min={0}
              value={seaFishCapacity}
              onChange={e => setSeaFishCapacity(Number(e.target.value))}
              className="border rounded px-2 py-1 w-full"
            />
          </div>
          <div>
            <label className="block font-semibold mb-1">
              Starting Ocean Fish
            </label>
            <input
              type="number"
              min={0}
              value={startingOceanFish}
              onChange={e => setStartingOceanFish(Number(e.target.value))}
              className="border rounded px-2 py-1 w-full"
            />
          </div>
          <div>
            <label className="block font-semibold mb-1">
              Ocean Fish Capacity
            </label>
            <input
              type="number"
              min={0}
              value={oceanFishCapacity}
              onChange={e => setOceanFishCapacity(Number(e.target.value))}
              className="border rounded px-2 py-1 w-full"
            />
          </div>
          <div>
            <label className="block font-semibold mb-1">
              Starting Cash per Team
            </label>
            <input
              type="number"
              min={0}
              value={startingCash}
              onChange={e => setStartingCash(Number(e.target.value))}
              className="border rounded px-2 py-1 w-full"
            />
          </div>
          <button
            type="submit"
            className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 w-full"
          >
            Start Game
          </button>
        </form>
      </div>
    )
  }

  // Loading state
  if (!state) {
    return (
      <div className="flex items-center justify-center h-full bg-gray-200">
        Loading…
      </div>
    )
  }

  // Main game view
  return (
    <div className="h-full bg-gray-200 p-6 overflow-auto">
      <div className="max-w-xl mx-auto bg-white p-6 rounded shadow">
        <h1 className="text-2xl font-bold mb-4">EpidemiGame MVP</h1>

        <div className="mb-4">
          <span className="font-semibold">Turn:</span> {state.turn}
        </div>

        {/* Fish in the Ocean Statistics Pane */}
        <div className="mb-6 p-4 bg-blue-100 rounded shadow-inner">
          <h2 className="font-semibold text-lg mb-2">Fish in the Ocean</h2>
          <div>
            <span className="font-semibold">Population:</span> {state.ocean_fish_population.toFixed(2)}
          </div>
          <div>
            <span className="font-semibold">Population % of Capacity:</span>{" "}
            {((state.ocean_fish_population / oceanFishCapacity) * 100).toFixed(1)}%
          </div>
        </div>

        {/* Fish in the Sea Statistics Pane */}
        <div className="mb-6 p-4 bg-cyan-100 rounded shadow-inner">
          <h2 className="font-semibold text-lg mb-2">Fish in the Sea</h2>
          <div>
            <span className="font-semibold">Population:</span> {state.sea_fish_population.toFixed(2)}
          </div>
          <div>
            <span className="font-semibold">Population % of Capacity:</span>{" "}
            {((state.sea_fish_population / seaFishCapacity) * 100).toFixed(1)}%
          </div>
        </div>

        {/* Team Statistics Pane */}
        <div className="mb-6 p-4 bg-green-100 rounded shadow-inner">
          <h2 className="font-semibold text-lg mb-2">Team Statistics</h2>
          <table className="w-full text-left">
            <thead>
              <tr>
                <th className="pr-4">Team</th>
                <th className="pr-4">Boats</th>
                <th className="pr-4">Cash</th>
              </tr>
            </thead>
            <tbody>
              {state.teams.map((team) => (
                <tr key={team.name}>
                  <td className="pr-4">{team.name}</td>
                  <td className="pr-4">{team.boats}</td>
                  <td className="pr-4">${team.cash.toFixed(2)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        <button
          onClick={endTurn}
          disabled={state.turn >= 10}
          className="mt-4 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
        >
          End Turn
        </button>
      </div>
    </div>
  )
}
