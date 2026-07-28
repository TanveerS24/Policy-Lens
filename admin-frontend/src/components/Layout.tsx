import React, { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  FileText, 
  FileCheck,
  Users, 
  ClipboardList, 
  Bell,
  Settings, 
  LogOut,
  Menu,
  X
} from 'lucide-react'
import { useAuthStore, AdminUser } from '../stores/authStore'
import { ToastContainer } from './Toast'
import { useToast } from '../hooks/useToast'

interface LayoutProps {
  children: React.ReactNode
}

const navigation = [
  { name: 'Dashboard', href: '/', icon: LayoutDashboard },
  { name: 'Schemes', href: '/schemes', icon: FileText },
  { name: 'Review Requests', href: '/review-requests', icon: FileCheck },
  { name: 'Users', href: '/users', icon: Users },
  { name: 'Audit Logs', href: '/audit-logs', icon: ClipboardList },
  { name: 'Notify Users', href: '/notify-users', icon: Bell },
  { name: 'Settings', href: '/settings', icon: Settings },
]

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const location = useLocation()
  const { user, logout } = useAuthStore()
  const { toasts, removeToast, success: toastSuccess, error: toastError, warning: toastWarning, info: toastInfo } = useToast()

  // Listen for toast events from child components
  React.useEffect(() => {
    const handleToast = (e: CustomEvent) => {
      const { type, message } = e.detail
      switch (type) {
        case 'success': toastSuccess(message); break
        case 'error': toastError(message); break
        case 'warning': toastWarning(message); break
        case 'info': toastInfo(message); break
      }
    }
    document.addEventListener('toast', handleToast as EventListener)
    return () => document.removeEventListener('toast', handleToast as EventListener)
  }, [toastSuccess, toastError, toastWarning, toastInfo])

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Mobile sidebar */}
      {sidebarOpen && (
        <div className="fixed inset-0 z-50 lg:hidden">
          <div 
            className="fixed inset-0 bg-gray-900/50" 
            onClick={() => setSidebarOpen(false)} 
          />
          <div className="fixed inset-y-0 left-0 w-64 bg-white shadow-lg">
            <SidebarContent 
              navigation={navigation} 
              location={location} 
              user={user}
              onLogout={logout}
              onClose={() => setSidebarOpen(false)}
            />
          </div>
        </div>
      )}

      {/* Desktop sidebar */}
      <div className="hidden lg:fixed lg:inset-y-0 lg:z-50 lg:flex lg:w-72 lg:flex-col">
        <div className="flex grow flex-col gap-y-5 overflow-y-auto border-r border-gray-200 bg-white px-6 pb-4">
          <SidebarContent 
            navigation={navigation} 
            location={location} 
            user={user}
            onLogout={logout}
          />
        </div>
      </div>

      {/* Main content */}
      <ToastContainer toasts={toasts} onRemove={removeToast} />

      <div className="lg:pl-72">
        <div className="sticky top-0 z-40 flex h-16 shrink-0 items-center gap-x-4 border-b border-gray-200 bg-white px-4 shadow-sm sm:gap-x-6 sm:px-6 lg:px-8">
          <button
            type="button"
            className="-m-2.5 p-2.5 text-gray-700 lg:hidden"
            onClick={() => setSidebarOpen(true)}
          >
            <Menu className="h-6 w-6" />
          </button>

          <div className="flex flex-1 gap-x-4 self-stretch lg:gap-x-6">
            <div className="flex flex-1 items-center justify-end gap-x-4 lg:gap-x-6">
              <div className="flex items-center gap-x-4 lg:gap-x-6">
                <div className="text-sm font-medium text-gray-900">
                  {user?.name}
                </div>
                <span className="inline-flex items-center rounded-md bg-primary-50 px-2 py-1 text-xs font-medium text-primary-700 ring-1 ring-inset ring-primary-700/10">
                  {user?.role}
                </span>
              </div>
            </div>
          </div>
        </div>

        <main className="py-10">
          <div className="px-4 sm:px-6 lg:px-8">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}

interface SidebarContentProps {
  navigation: { name: string; href: string; icon: React.ElementType }[]
  location: { pathname: string }
  user: AdminUser | null
  onLogout: () => void
  onClose?: () => void
}

const SidebarContent: React.FC<SidebarContentProps> = ({ 
  navigation, 
  location, 
  onLogout,
  onClose 
}) => (
  <>
    <div className="flex h-16 shrink-0 items-center justify-between">
      <h1 className="text-xl font-bold text-primary-600">
        DentalSchemes
      </h1>
      {onClose && (
        <button onClick={onClose} className="lg:hidden">
          <X className="h-6 w-6 text-gray-500" />
        </button>
      )}
    </div>
    
    <nav className="flex flex-1 flex-col">
      <ul role="list" className="flex flex-1 flex-col gap-y-7">
        <li>
          <ul role="list" className="-mx-2 space-y-1">
            {navigation.map((item) => (
              <li key={item.name}>
                <Link
                  to={item.href}
                  onClick={onClose}
                  className={`
                    group flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6
                    ${location.pathname === item.href
                      ? 'bg-primary-50 text-primary-600'
                      : 'text-gray-700 hover:text-primary-600 hover:bg-gray-50'
                    }
                  `}
                >
                  <item.icon className="h-6 w-6 shrink-0" />
                  {item.name}
                </Link>
              </li>
            ))}
          </ul>
        </li>
        
        <li className="mt-auto">
          <button
            onClick={onLogout}
            className="group -mx-2 flex gap-x-3 rounded-md p-2 text-sm font-semibold leading-6 text-gray-700 hover:text-red-600 hover:bg-red-50 w-full"
          >
            <LogOut className="h-6 w-6 shrink-0" />
            Logout
          </button>
        </li>
      </ul>
    </nav>
  </>
)
