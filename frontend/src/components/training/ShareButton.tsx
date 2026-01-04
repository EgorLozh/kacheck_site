import { useState } from 'react'
import { trainingService } from '../../services/training.service'
import type { Training } from '../../types'

interface ShareButtonProps {
  training: Training
  onUpdate?: (training: Training) => void
}

export default function ShareButton({ training, onUpdate }: ShareButtonProps) {
  const [loading, setLoading] = useState(false)
  const [copied, setCopied] = useState(false)

  const handleShare = async () => {
    try {
      setLoading(true)
      let updatedTraining: Training

      if (training.share_token) {
        // Already shared, copy link
        await copyToClipboard()
      } else {
        // Generate share token
        updatedTraining = await trainingService.shareTraining(training.id)
        await copyToClipboard(updatedTraining.share_token)
        onUpdate?.(updatedTraining)
      }
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Ошибка при создании ссылки')
    } finally {
      setLoading(false)
    }
  }

  const handleUnshare = async () => {
    if (!confirm('Отключить публичный доступ к тренировке?')) return

    try {
      setLoading(true)
      const updatedTraining = await trainingService.unshareTraining(training.id)
      onUpdate?.(updatedTraining)
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Ошибка при отключении доступа')
    } finally {
      setLoading(false)
    }
  }

  const copyToClipboard = async (token?: string | null) => {
    // Get share token from parameter or training object
    const shareTokenRaw = token ?? training.share_token
    if (!shareTokenRaw) return

    // Ensure shareToken is a string
    // If it's already a string, use it; otherwise convert to string explicitly
    const shareTokenStr: string = typeof shareTokenRaw === 'string' 
      ? shareTokenRaw 
      : String(shareTokenRaw)
    
    // Validate that we have a valid token string (not "[object Object]")
    if (shareTokenStr === '[object Object]' || shareTokenStr.length === 0) {
      console.error('Invalid share token format:', shareTokenRaw, typeof shareTokenRaw)
      alert('Ошибка: неверный формат токена для совместного доступа')
      return
    }
    
    const url = `${window.location.origin}/trainings/shared/${shareTokenStr}`
    try {
      await navigator.clipboard.writeText(url)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      // Fallback for older browsers
      const textArea = document.createElement('textarea')
      textArea.value = url
      document.body.appendChild(textArea)
      textArea.select()
      document.execCommand('copy')
      document.body.removeChild(textArea)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    }
  }

  if (training.share_token) {
    return (
      <div className="flex items-center gap-2">
        <button
          onClick={() => copyToClipboard()}
          disabled={loading}
          className="px-3 py-1 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
        >
          {copied ? '✓ Скопировано' : '📋 Копировать ссылку'}
        </button>
        <button
          onClick={handleUnshare}
          disabled={loading}
          className="px-3 py-1 text-sm bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 disabled:opacity-50"
        >
          Отключить
        </button>
      </div>
    )
  }

  return (
    <button
      onClick={handleShare}
      disabled={loading}
      className="px-3 py-1 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
    >
      {loading ? 'Создание...' : '🔗 Поделиться'}
    </button>
  )
}


