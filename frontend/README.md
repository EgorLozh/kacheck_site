# Kacheck Frontend

React + TypeScript фронтенд приложения для отслеживания тренировок.

## Технологии

- React 18
- TypeScript
- Vite
- React Router
- TanStack Query (React Query)
- React Hook Form
- Zod (валидация)
- TailwindCSS
- Axios
- Recharts (графики)

## Установка

```bash
npm install
```

## Настройка

Создайте файл `.env` на основе `.env.example`:

```bash
cp .env.example .env
```

Переменные окружения:
- `VITE_PORT` - порт для фронтенда (по умолчанию 3000)
- `VITE_API_BASE_URL` - URL бэкенда (по умолчанию http://localhost:8000)

## Запуск в режиме разработки

```bash
npm run dev
```

Приложение будет доступно по адресу: http://localhost:3000 (или по порту, указанному в VITE_PORT)

## Сборка для production

```bash
npm run build
```

## Структура проекта

```
frontend/
├── src/
│   ├── components/     # React компоненты
│   │   └── layout/     # Layout компоненты (Header, Sidebar)
│   ├── contexts/       # React Contexts (AuthContext)
│   ├── pages/          # Страницы приложения
│   ├── services/       # API сервисы
│   ├── types/          # TypeScript типы
│   ├── App.tsx         # Главный компонент
│   └── main.tsx        # Точка входа
├── package.json
├── vite.config.ts
└── .env.example
```
