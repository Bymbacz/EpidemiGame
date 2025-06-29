// frontend/src/App.tsx

import React, { useState } from 'react'

type Team = { name: string; boats: number; cash: number }

type GameState = {
  turn: number
  fish_population: number
  teams: Team[]
  game_id?: string
}

export default function App() {
  const [state, setState] = useState<GameState | null>(null)
  const [socket, setSocket] = useState<WebSocket | null>(null)
  const [started, setStarted] = useState(false)

  // Start game: POST to backend, then open WebSocket immediately
  const startGame = async () => {
    // 1) Start new game
    const res = await fetch('http://localhost:8000/game/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({}) // default teams
    })
    const data: GameState = await res.json()
    setState(data)
    setStarted(true)

    // 2) Open WebSocket connection
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
        <button
          onClick={startGame}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
        >
          Start Game
        </button>
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

        <div className="mb-4">
          <span className="font-semibold">Fish Population:</span>{' '}
          {state.fish_population.toFixed(2)}
        </div>

        <div className="mb-4">
          <h2 className="font-semibold">Teams</h2>
          <ul className="list-disc list-inside">
            {state.teams.map((team) => (
              <li key={team.name}>
                {team.name}: Boats {team.boats}, Cash ${team.cash.toFixed(2)}
              </li>
            ))}
          </ul>
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
