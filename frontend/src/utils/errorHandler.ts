/**
 * Formats error messages from FastAPI/Pydantic validation errors
 * Handles both string errors and array of validation errors
 * Always returns a string
 */
export function formatApiError(error: any): string {
  try {
    // Handle network errors or errors without response
    if (!error?.response) {
      if (error?.message && typeof error.message === 'string') {
        return error.message
      }
      return 'Произошла ошибка соединения. Проверьте подключение к интернету.'
    }

    if (!error.response.data) {
      return 'Произошла ошибка. Попробуйте позже.'
    }

    const detail = error.response.data.detail

    // Handle undefined or null detail
    if (!detail) {
      return 'Произошла ошибка. Попробуйте позже.'
    }

    // If detail is a string, return it directly
    if (typeof detail === 'string') {
      return detail
    }

    // If detail is an array (validation errors), format them
    if (Array.isArray(detail)) {
      if (detail.length === 0) {
        return 'Ошибка валидации данных'
      }

      const formattedErrors: string[] = []
      
      for (const err of detail) {
        if (!err || typeof err !== 'object') {
          continue
        }

        // Format field path (e.g., ["body", "email"] -> "email")
        let field = ''
        if (Array.isArray(err.loc)) {
          // Skip "body" or "query" prefix, get the actual field name
          const fieldPath = err.loc.slice(1)
          if (fieldPath.length > 0) {
            field = String(fieldPath[fieldPath.length - 1])
          }
        }
        
        // Map field names to Russian for better UX
        const fieldNames: Record<string, string> = {
          email: 'Email',
          username: 'Имя пользователя',
          password: 'Пароль',
          confirmPassword: 'Подтверждение пароля',
        }
        
        const fieldLabel = field ? (fieldNames[field] || field) : ''
        // Ensure message is always a string
        let message = 'Ошибка валидации'
        if (err.msg) {
          if (typeof err.msg === 'string') {
            message = err.msg
          } else if (typeof err.msg === 'object') {
            // If msg is an object, try to stringify it or use a default
            message = 'Ошибка валидации данных'
          }
        }
        
        const formatted = fieldLabel ? `${fieldLabel}: ${message}` : message
        formattedErrors.push(formatted)
      }
    
      return formattedErrors.length > 0 
        ? formattedErrors.join('; ') 
        : 'Ошибка валидации данных'
    }

    // If detail is an object (shouldn't happen with FastAPI, but handle it)
    if (typeof detail === 'object') {
      return 'Произошла ошибка валидации данных.'
    }

    // Fallback for other error formats
    return 'Произошла ошибка. Попробуйте позже.'
  } catch (e) {
    // If anything goes wrong, return a safe fallback message
    console.error('Error formatting API error:', e)
    return 'Произошла ошибка. Попробуйте позже.'
  }
}

