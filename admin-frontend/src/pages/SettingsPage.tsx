import React, { useState, useEffect } from 'react'
import { Save, Shield, Bell, Database, Users, Plus, Trash2, AlertCircle } from 'lucide-react'
import axios from 'axios'
import { useAuthStore } from '../stores/authStore'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

interface Admin {
  id: number
  name: string
  email: string
  role: string
  status: string
  created_at: string
}

export const SettingsPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState('general')
  const { user } = useAuthStore()
  const isSuperAdmin = user?.role === 'super_admin'

  const tabs = [
    { id: 'general', name: 'General', icon: Shield },
    { id: 'notifications', name: 'Notifications', icon: Bell },
    { id: 'database', name: 'Database', icon: Database },
    ...(isSuperAdmin ? [{ id: 'admins', name: 'Admins', icon: Users }] : []),
  ]

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">Settings</h1>

      <div className="mt-6 flex space-x-1 rounded-xl bg-gray-100 p-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex items-center w-full rounded-lg py-2.5 text-sm font-medium leading-5 ${
              activeTab === tab.id
                ? 'bg-white text-primary-700 shadow'
                : 'text-gray-700 hover:bg-white/[0.5] hover:text-gray-900'
            }`}
          >
            <tab.icon className="h-4 w-4 mr-2 ml-2" />
            {tab.name}
          </button>
        ))}
      </div>

      <div className="mt-6 card">
        {activeTab === 'general' && <GeneralSettings />}
        {activeTab === 'notifications' && <NotificationSettings />}
        {activeTab === 'database' && <DatabaseSettings />}
        {activeTab === 'admins' && isSuperAdmin && <AdminManagement />}
      </div>
    </div>
  )
}

const GeneralSettings: React.FC = () => {
  const { user } = useAuthStore()
  const [settings, setSettings] = useState({
    app_name: '',
    support_email: '',
    max_upload_size: '',
    otp_expiry: '',
  })
  const [loading, setLoading] = useState(false)
  const [saved, setSaved] = useState(false)

  useEffect(() => {
    // TODO: Fetch actual settings from backend when API is ready
    // For now, leave fields empty
  }, [])

  const handleSave = async () => {
    setLoading(true)
    try {
      // TODO: Save settings to backend
      await new Promise(resolve => setTimeout(resolve, 500))
      setSaved(true)
      setTimeout(() => setSaved(false), 2000)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h3 className="text-lg font-medium text-gray-900">General Settings</h3>
        <p className="mt-1 text-sm text-gray-500">Manage basic platform configuration.</p>
      </div>

      <div className="grid grid-cols-1 gap-y-6 gap-x-4 sm:grid-cols-6">
        <div className="sm:col-span-3">
          <label htmlFor="app-name" className="block text-sm font-medium text-gray-700">
            Application Name
          </label>
          <input
            type="text"
            id="app-name"
            value={settings.app_name}
            onChange={(e) => setSettings({ ...settings, app_name: e.target.value })}
            placeholder="Enter application name"
            className="input-field mt-1"
          />
        </div>

        <div className="sm:col-span-3">
          <label htmlFor="support-email" className="block text-sm font-medium text-gray-700">
            Support Email
          </label>
          <input
            type="email"
            id="support-email"
            value={settings.support_email}
            onChange={(e) => setSettings({ ...settings, support_email: e.target.value })}
            placeholder="Enter support email"
            className="input-field mt-1"
          />
        </div>

        <div className="sm:col-span-3">
          <label htmlFor="max-upload" className="block text-sm font-medium text-gray-700">
            Max Upload Size (MB)
          </label>
          <input
            type="number"
            id="max-upload"
            value={settings.max_upload_size}
            onChange={(e) => setSettings({ ...settings, max_upload_size: e.target.value })}
            placeholder="Enter max upload size"
            className="input-field mt-1"
          />
        </div>

        <div className="sm:col-span-3">
          <label htmlFor="otp-expiry" className="block text-sm font-medium text-gray-700">
            OTP Expiry (minutes)
          </label>
          <input
            type="number"
            id="otp-expiry"
            value={settings.otp_expiry}
            onChange={(e) => setSettings({ ...settings, otp_expiry: e.target.value })}
            placeholder="Enter OTP expiry time"
            className="input-field mt-1"
          />
        </div>
      </div>

      <div className="flex justify-end">
        <button 
          onClick={handleSave}
          disabled={loading}
          className="btn-primary"
        >
          <Save className="h-4 w-4 mr-2" />
          {saved ? 'Saved!' : loading ? 'Saving...' : 'Save Changes'}
        </button>
      </div>

      {/* Danger Zone */}
      <div className="mt-8 pt-8 border-t border-red-200">
        <h3 className="text-lg font-medium text-red-600 flex items-center">
          <AlertCircle className="h-5 w-5 mr-2" />
          Danger Zone
        </h3>
        <p className="mt-1 text-sm text-gray-500">
          These actions are irreversible. Please proceed with caution.
        </p>

        <div className="mt-4 p-4 border border-red-200 rounded-lg bg-red-50">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="text-sm font-medium text-red-900">Delete My Account</h4>
              <p className="text-sm text-red-700">
                Permanently delete your admin account. {user?.role === 'super_admin' && 'You must create another super admin first if you are the only one.'}
              </p>
            </div>
            <DeleteMyAccountButton />
          </div>
        </div>
      </div>
    </div>
  )
}

const DeleteMyAccountButton: React.FC = () => {
  const { logout } = useAuthStore()
  const [showConfirm, setShowConfirm] = useState(false)
  const [confirmText, setConfirmText] = useState('')
  const [deleting, setDeleting] = useState(false)
  const [error, setError] = useState('')

  const handleDelete = async () => {
    if (confirmText !== 'DELETE') {
      setError('Please type DELETE to confirm')
      return
    }

    setDeleting(true)
    setError('')
    
    try {
      await axios.delete(`${API_URL}/admin/me`)
      alert('Your account has been deleted. You will be logged out.')
      logout()
      window.location.href = '/login'
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete account')
      setDeleting(false)
    }
  }

  return (
    <>
      <button 
        onClick={() => setShowConfirm(true)}
        className="px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 text-sm font-medium"
      >
        Delete Account
      </button>

      {showConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-medium text-red-600 mb-4">Delete Your Account?</h3>
            
            {error && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                {error}
              </div>
            )}

            <p className="text-sm text-gray-600 mb-4">
              This action is <strong>permanent</strong> and cannot be undone. All your data will be permanently removed.
            </p>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Type <code className="bg-gray-100 px-1 py-0.5 rounded">DELETE</code> to confirm:
              </label>
              <input
                type="text"
                value={confirmText}
                onChange={(e) => setConfirmText(e.target.value)}
                className="input-field"
                placeholder="DELETE"
              />
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => {
                  setShowConfirm(false)
                  setConfirmText('')
                  setError('')
                }}
                className="btn-secondary flex-1"
                disabled={deleting}
              >
                Cancel
              </button>
              <button
                onClick={handleDelete}
                disabled={deleting || confirmText !== 'DELETE'}
                className="flex-1 px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 font-medium disabled:opacity-50"
              >
                {deleting ? 'Deleting...' : 'Delete My Account'}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  )
}

const NotificationSettings: React.FC = () => {
  const [settings, setSettings] = useState({
    email_notifications: false,
    sms_notifications: false,
    push_notifications: false,
  })

  return (
    <div className="p-6 space-y-6">
      <div>
        <h3 className="text-lg font-medium text-gray-900">Notification Settings</h3>
        <p className="mt-1 text-sm text-gray-500">Configure notification preferences.</p>
      </div>

      <div className="space-y-4">
        {[
          { key: 'email_notifications', label: 'Email notifications' },
          { key: 'sms_notifications', label: 'SMS notifications' },
          { key: 'push_notifications', label: 'Push notifications' },
        ].map((setting) => (
          <div key={setting.key} className="flex items-center justify-between">
            <span className="text-sm font-medium text-gray-700">{setting.label}</span>
            <label className="relative inline-flex items-center cursor-pointer">
              <input 
                type="checkbox" 
                checked={settings[setting.key as keyof typeof settings]}
                onChange={(e) => setSettings({ ...settings, [setting.key]: e.target.checked })}
                className="sr-only peer" 
              />
              <div className="w-11 h-6 bg-gray-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary-600"></div>
            </label>
          </div>
        ))}
      </div>
    </div>
  )
}

const DatabaseSettings: React.FC = () => {
  const [backingUp, setBackingUp] = useState(false)

  const handleBackup = async () => {
    setBackingUp(true)
    try {
      // TODO: Call backup API
      await new Promise(resolve => setTimeout(resolve, 1000))
      alert('Backup initiated')
    } finally {
      setBackingUp(false)
    }
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h3 className="text-lg font-medium text-gray-900">Database Settings</h3>
        <p className="mt-1 text-sm text-gray-500">Manage database connections and backups.</p>
      </div>

      <div className="space-y-4">
        <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
          <div>
            <h4 className="text-sm font-medium text-gray-900">Database Connection</h4>
            <p className="text-sm text-gray-500">PostgreSQL database server</p>
          </div>
          <span className="px-2 py-1 text-xs font-semibold rounded-full bg-green-100 text-green-800">
            Connected
          </span>
        </div>

        <button 
          onClick={handleBackup}
          disabled={backingUp}
          className="btn-secondary w-full"
        >
          {backingUp ? 'Creating Backup...' : 'Create Backup'}
        </button>
      </div>
    </div>
  )
}

const AdminManagement: React.FC = () => {
  const [admins, setAdmins] = useState<Admin[]>([])
  const [loading, setLoading] = useState(true)
  const [showCreateModal, setShowCreateModal] = useState(false)
  const [error, setError] = useState('')
  const [newAdmin, setNewAdmin] = useState({
    name: '',
    email: '',
    password: '',
    role: 'support_admin',
  })

  useEffect(() => {
    fetchAdmins()
  }, [])

  const fetchAdmins = async () => {
    try {
      const response = await axios.get(`${API_URL}/admin/admins`)
      setAdmins(response.data.admins || [])
    } catch (err) {
      console.error('Failed to fetch admins:', err)
      setError('Failed to load admins')
    } finally {
      setLoading(false)
    }
  }

  const handleCreateAdmin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    try {
      await axios.post(`${API_URL}/admin/admins`, newAdmin)
      setShowCreateModal(false)
      setNewAdmin({ name: '', email: '', password: '', role: 'support_admin' })
      fetchAdmins()
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create admin')
    }
  }

  const handleDeleteAdmin = async (adminId: number) => {
    if (!confirm('Are you sure you want to delete this admin?')) return
    
    try {
      await axios.delete(`${API_URL}/admin/admins/${adminId}`)
      fetchAdmins()
    } catch (err: any) {
      alert(err.response?.data?.detail || 'Failed to delete admin')
    }
  }

  const getRoleColor = (role: string) => {
    switch (role) {
      case 'super_admin': return 'bg-red-100 text-red-800'
      case 'content_admin': return 'bg-blue-100 text-blue-800'
      case 'support_admin': return 'bg-green-100 text-green-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getRoleLabel = (role: string) => {
    switch (role) {
      case 'super_admin': return 'Super Admin'
      case 'content_admin': return 'Content Admin'
      case 'support_admin': return 'Support Admin'
      default: return role
    }
  }

  if (loading) return <div className="p-6">Loading...</div>

  return (
    <div className="p-6 space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h3 className="text-lg font-medium text-gray-900">Admin Management</h3>
          <p className="mt-1 text-sm text-gray-500">Create and manage admin users. Only Super Admins can access this.</p>
        </div>
        <button 
          onClick={() => setShowCreateModal(true)}
          className="btn-primary"
        >
          <Plus className="h-4 w-4 mr-2" />
          Create Admin
        </button>
      </div>

      <div className="space-y-4">
        {admins.length === 0 ? (
          <div className="text-center py-8 text-gray-500">
            No admins found. Create your first admin.
          </div>
        ) : (
          admins.map((admin) => (
            <div key={admin.id} className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
              <div>
                <h4 className="text-sm font-medium text-gray-900">{admin.name}</h4>
                <p className="text-sm text-gray-500">{admin.email}</p>
                <div className="flex gap-2 mt-1">
                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getRoleColor(admin.role)}`}>
                    {getRoleLabel(admin.role)}
                  </span>
                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${
                    admin.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                  }`}>
                    {admin.status}
                  </span>
                </div>
              </div>
              <button 
                onClick={() => handleDeleteAdmin(admin.id)}
                className="text-red-600 hover:text-red-800 p-2"
                title="Delete admin"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
          ))
        )}
      </div>

      {/* Create Admin Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-lg p-6 w-full max-w-md">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Create New Admin</h3>
            
            {error && (
              <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center text-red-700">
                <AlertCircle className="h-4 w-4 mr-2" />
                {error}
              </div>
            )}

            <form onSubmit={handleCreateAdmin} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-gray-700">Name</label>
                <input
                  type="text"
                  required
                  value={newAdmin.name}
                  onChange={(e) => setNewAdmin({ ...newAdmin, name: e.target.value })}
                  className="input-field mt-1"
                  placeholder="Enter admin name"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Email</label>
                <input
                  type="email"
                  required
                  value={newAdmin.email}
                  onChange={(e) => setNewAdmin({ ...newAdmin, email: e.target.value })}
                  className="input-field mt-1"
                  placeholder="Enter admin email"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Password</label>
                <input
                  type="password"
                  required
                  minLength={8}
                  value={newAdmin.password}
                  onChange={(e) => setNewAdmin({ ...newAdmin, password: e.target.value })}
                  className="input-field mt-1"
                  placeholder="Enter password (min 8 chars)"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700">Role</label>
                <select
                  value={newAdmin.role}
                  onChange={(e) => setNewAdmin({ ...newAdmin, role: e.target.value })}
                  className="input-field mt-1"
                >
                  <option value="support_admin">Support Admin - Can view and manage users</option>
                  <option value="content_admin">Content Admin - Can manage schemes and content</option>
                  <option value="super_admin">Super Admin - Full access including admin management</option>
                </select>
              </div>

              <div className="flex gap-3 pt-4">
                <button
                  type="button"
                  onClick={() => setShowCreateModal(false)}
                  className="btn-secondary flex-1"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="btn-primary flex-1"
                >
                  Create Admin
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}
