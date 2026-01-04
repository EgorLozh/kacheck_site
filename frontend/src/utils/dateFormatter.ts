/**
 * Форматирует дату/время тренировки в формат "15.01.2024 14:30"
 */
export function formatTrainingName(dateTime: string): string {
  const date = new Date(dateTime)
  const day = date.getDate().toString().padStart(2, '0')
  const month = (date.getMonth() + 1).toString().padStart(2, '0')
  const year = date.getFullYear()
  const hours = date.getHours().toString().padStart(2, '0')
  const minutes = date.getMinutes().toString().padStart(2, '0')
  
  return `${day}.${month}.${year} ${hours}:${minutes}`
}


