import { useState, useEffect } from 'react'

interface RestTimerProps {
  duration: number // в секундах
  onComplete?: () => void
  autoStart?: boolean
}

export default function RestTimer({ duration, onComplete, autoStart = false }: RestTimerProps) {
  const [remaining, setRemaining] = useState(duration)
  const [isActive, setIsActive] = useState(autoStart)
  const [isCompleted, setIsCompleted] = useState(false)

  useEffect(() => {
    if (isActive && remaining > 0) {
      const timer = setInterval(() => {
        setRemaining((prev) => {
          if (prev <= 1) {
            setIsActive(false)
            setIsCompleted(true)
            if (onComplete) {
              onComplete()
            }
            return 0
          }
          return prev - 1
        })
      }, 1000)

      return () => clearInterval(timer)
    }
  }, [isActive, remaining, onComplete])

  // Автозапуск при изменении duration и autoStart
  useEffect(() => {
    if (autoStart && !isActive && !isCompleted && remaining === duration) {
      setIsActive(true)
    }
  }, [autoStart, duration])

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60)
    const secs = seconds % 60
    return `${mins}:${secs.toString().padStart(2, '0')}`
  }

  const handleStart = () => {
    setIsActive(true)
    setIsCompleted(false)
    setRemaining(duration)
  }

  const handleStop = () => {
    setIsActive(false)
  }

  const handleReset = () => {
    setIsActive(false)
    setIsCompleted(false)
    setRemaining(duration)
  }

  if (duration === 0) {
    return null
  }

  return (
    <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
      <div className="flex items-center justify-between mb-2">
        <span className="text-sm font-medium text-blue-900">Отдых</span>
        {isCompleted && (
          <span className="text-xs text-green-600 font-medium">✓ Завершено</span>
        )}
      </div>
      
      <div className="text-2xl font-bold text-blue-600 mb-2">
        {formatTime(remaining)}
      </div>

      <div className="flex gap-2">
        {!isActive && !isCompleted && (
          <button
            onClick={handleStart}
            className="px-3 py-1 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
          >
            Начать отдых
          </button>
        )}
        {isActive && (
          <button
            onClick={handleStop}
            className="px-3 py-1 text-sm bg-gray-600 text-white rounded hover:bg-gray-700"
          >
            Пауза
          </button>
        )}
        {isCompleted && (
          <button
            onClick={handleReset}
            className="px-3 py-1 text-sm bg-gray-200 text-gray-700 rounded hover:bg-gray-300"
          >
            Сбросить
          </button>
        )}
      </div>
    </div>
  )
}

