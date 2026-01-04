import { NavLink } from 'react-router-dom'

interface SidebarProps {
  isOpen: boolean
  onClose: () => void
}

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  return (
    <>
      {/* Desktop sidebar - always visible */}
      <aside className="hidden md:block w-64 bg-white shadow-sm min-h-screen">
        <nav className="p-4">
          <ul className="space-y-2">
            <li>
              <NavLink
                to="/dashboard"
                className={({ isActive }) =>
                  `block px-4 py-2 rounded-md ${
                    isActive
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`
                }
              >
                Дашборд
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/trainings"
                className={({ isActive }) =>
                  `block px-4 py-2 rounded-md ${
                    isActive
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`
                }
              >
                Тренировки
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/templates"
                className={({ isActive }) =>
                  `block px-4 py-2 rounded-md ${
                    isActive
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`
                }
              >
                Шаблоны
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/exercises"
                className={({ isActive }) =>
                  `block px-4 py-2 rounded-md ${
                    isActive
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`
                }
              >
                Упражнения
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/analytics"
                className={({ isActive }) =>
                  `block px-4 py-2 rounded-md ${
                    isActive
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`
                }
              >
                Аналитика
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/followers"
                className={({ isActive }) =>
                  `block px-4 py-2 rounded-md ${
                    isActive
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`
                }
              >
                Подписчики
              </NavLink>
            </li>
            <li>
              <NavLink
                to="/following"
                className={({ isActive }) =>
                  `block px-4 py-2 rounded-md ${
                    isActive
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`
                }
              >
                Подписки
              </NavLink>
            </li>
          </ul>
        </nav>
      </aside>

      {/* Mobile sidebar - drawer */}
      <aside
        className={`fixed top-0 left-0 z-50 h-full w-64 bg-white shadow-lg transform transition-transform duration-300 ease-in-out md:hidden ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="p-4">
          {/* Close button */}
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-gray-800">Меню</h2>
            <button
              onClick={onClose}
              className="p-2 rounded-md text-gray-600 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500"
              aria-label="Close menu"
            >
              <svg
                className="w-6 h-6"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>
          <nav>
            <ul className="space-y-2">
              <li>
                <NavLink
                  to="/dashboard"
                  onClick={onClose}
                  className={({ isActive }) =>
                    `block px-4 py-2 rounded-md ${
                      isActive
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`
                  }
                >
                  Дашборд
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/trainings"
                  onClick={onClose}
                  className={({ isActive }) =>
                    `block px-4 py-2 rounded-md ${
                      isActive
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`
                  }
                >
                  Тренировки
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/templates"
                  onClick={onClose}
                  className={({ isActive }) =>
                    `block px-4 py-2 rounded-md ${
                      isActive
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`
                  }
                >
                  Шаблоны
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/exercises"
                  onClick={onClose}
                  className={({ isActive }) =>
                    `block px-4 py-2 rounded-md ${
                      isActive
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`
                  }
                >
                  Упражнения
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/analytics"
                  onClick={onClose}
                  className={({ isActive }) =>
                    `block px-4 py-2 rounded-md ${
                      isActive
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`
                  }
                >
                  Аналитика
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/followers"
                  onClick={onClose}
                  className={({ isActive }) =>
                    `block px-4 py-2 rounded-md ${
                      isActive
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`
                  }
                >
                  Подписчики
                </NavLink>
              </li>
              <li>
                <NavLink
                  to="/following"
                  onClick={onClose}
                  className={({ isActive }) =>
                    `block px-4 py-2 rounded-md ${
                      isActive
                        ? 'bg-blue-100 text-blue-700'
                        : 'text-gray-700 hover:bg-gray-100'
                    }`
                  }
                >
                  Подписки
                </NavLink>
              </li>
            </ul>
          </nav>
        </div>
      </aside>
    </>
  )
}



