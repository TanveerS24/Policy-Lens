import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation, useQuery } from '@tanstack/react-query'
import { Bell, Send, Calendar, FileText, Users, Clock, CheckCircle, XCircle, AlertCircle, ArrowLeft, RefreshCw } from 'lucide-react'
import axios from 'axios'
import { useAuthStore } from '../stores/authStore'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

interface Scheme {
  id: number
  name: string
  code: string
}

interface Broadcast {
  id: number
  title: string
  message: string
  scheme_id?: number
  scheme_name?: string
  scheduled_at?: string
  sent_at?: string
  status: string
  target_all_users: boolean
  total_users: number
  sent_count: number
  failed_count: number
  created_at: string
  admin_name: string
}

interface BroadcastFormData {
  title: string
  message: string
  scheme_id: number | ''
  scheduled_at: string
  schedule_type: 'immediate' | 'scheduled'
  target_all_users: boolean
}

const NotifyUsersPage: React.FC = () => {
  const navigate = useNavigate()
  const { token } = useAuthStore()
  const [formData, setFormData] = useState<BroadcastFormData>({
    title: '',
    message: '',
    scheme_id: '',
    scheduled_at: '',
    schedule_type: 'immediate',
    target_all_users: true
  })
  const [currentPage, setCurrentPage] = useState(1)
  const [statusFilter, setStatusFilter] = useState('')

  // Fetch schemes for dropdown
  const { data: schemes } = useQuery({
    queryKey: ['schemes'],
    queryFn: async () => {
      try {
        const response = await axios.get(`${API_URL}/schemes`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        return response.data.schemes || []
      } catch (error) {
        console.error('Failed to fetch schemes:', error)
        return []
      }
    },
    enabled: !!token
  })

  // Fetch broadcasts
  const { data: broadcastsData, refetch: refetchBroadcasts } = useQuery({
    queryKey: ['broadcasts', currentPage, statusFilter],
    queryFn: async () => {
      try {
        const params = new URLSearchParams({
          page: currentPage.toString(),
          per_page: '10'
        })
        if (statusFilter) params.append('status', statusFilter)
        
        const response = await axios.get(`${API_URL}/notifications/broadcast?${params}`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        return response.data
      } catch (error) {
        console.error('Failed to fetch broadcasts:', error)
        return { broadcasts: [], total: 0, page: 1, per_page: 10, total_pages: 0 }
      }
    },
    enabled: !!token
  })

  // Create broadcast mutation
  const createBroadcastMutation = useMutation({
    mutationFn: async (data: BroadcastFormData) => {
      const payload = {
        title: data.title,
        message: data.message,
        scheme_id: data.scheme_id ? data.scheme_id : undefined,
        scheduled_at: data.schedule_type === 'scheduled' ? data.scheduled_at : undefined,
        target_all_users: data.target_all_users
      }
      
      const response = await axios.post(`${API_URL}/notifications/broadcast`, payload, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    },
    onSuccess: () => {
      setFormData({
        title: '',
        message: '',
        scheme_id: '',
        scheduled_at: '',
        schedule_type: 'immediate',
        target_all_users: true
      })
      refetchBroadcasts()
      alert('Notification sent successfully!')
    },
    onError: (error: any) => {
      alert(error.response?.data?.detail || 'Failed to send notification')
    }
  })

  // Cancel broadcast mutation
  const cancelBroadcastMutation = useMutation({
    mutationFn: async (broadcastId: number) => {
      const response = await axios.patch(`${API_URL}/notifications/broadcast/${broadcastId}/cancel`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    },
    onSuccess: () => {
      refetchBroadcasts()
      alert('Broadcast cancelled successfully!')
    },
    onError: (error: any) => {
      alert(error.response?.data?.detail || 'Failed to cancel broadcast')
    }
  })

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!formData.title.trim() || !formData.message.trim()) {
      alert('Please fill in both title and message')
      return
    }

    if (formData.schedule_type === 'scheduled' && !formData.scheduled_at) {
      alert('Please select a scheduled time')
      return
    }

    createBroadcastMutation.mutate(formData)
  }

  const handleCancel = (broadcastId: number) => {
    if (window.confirm('Are you sure you want to cancel this broadcast?')) {
      cancelBroadcastMutation.mutate(broadcastId)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'sent':
        return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'scheduled':
        return <Clock className="w-4 h-4 text-blue-500" />
      case 'cancelled':
        return <XCircle className="w-4 h-4 text-red-500" />
      default:
        return <AlertCircle className="w-4 h-4 text-gray-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'sent':
        return 'bg-green-100 text-green-800'
      case 'scheduled':
        return 'bg-blue-100 text-blue-800'
      case 'cancelled':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const getMinDateTime = () => {
    const now = new Date()
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset())
    return now.toISOString().slice(0, 16)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <button
                onClick={() => navigate('/dashboard')}
                className="mr-4 p-2 rounded-lg hover:bg-gray-100 transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <div className="flex items-center">
                <Bell className="w-6 h-6 text-blue-600 mr-3" />
                <div>
                  <h1 className="text-xl font-semibold text-gray-900">Notify Users</h1>
                  <p className="text-sm text-gray-500">Send broadcast notifications to users</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Create Broadcast Form */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold text-gray-900 mb-6">Create New Broadcast</h2>
              
              <form onSubmit={handleSubmit} className="space-y-4">
                {/* Title */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Title *
                  </label>
                  <input
                    type="text"
                    value={formData.title}
                    onChange={(e) => setFormData({ ...formData, title: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    placeholder="Enter notification title"
                    required
                  />
                </div>

                {/* Message */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Message *
                  </label>
                  <textarea
                    value={formData.message}
                    onChange={(e) => setFormData({ ...formData, message: e.target.value })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    rows={4}
                    placeholder="Enter notification message"
                    required
                  />
                </div>

                {/* Scheme Selection */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Attach Scheme (Optional)
                  </label>
                  <select
                    value={formData.scheme_id}
                    onChange={(e) => setFormData({ ...formData, scheme_id: e.target.value ? parseInt(e.target.value) : '' })}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  >
                    <option value="">No scheme attached</option>
                    {schemes?.map((scheme: Scheme) => (
                      <option key={scheme.id} value={scheme.id}>
                        {scheme.name} ({scheme.code})
                      </option>
                    ))}
                  </select>
                </div>

                {/* Scheduling */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Schedule
                  </label>
                  <div className="space-y-2">
                    <label className="flex items-center">
                      <input
                        type="radio"
                        value="immediate"
                        checked={formData.schedule_type === 'immediate'}
                        onChange={(e) => setFormData({ ...formData, schedule_type: 'immediate' })}
                        className="mr-2"
                      />
                      <span className="text-sm">Send Immediately</span>
                    </label>
                    <label className="flex items-center">
                      <input
                        type="radio"
                        value="scheduled"
                        checked={formData.schedule_type === 'scheduled'}
                        onChange={(e) => setFormData({ ...formData, schedule_type: 'scheduled' })}
                        className="mr-2"
                      />
                      <span className="text-sm">Schedule for Later</span>
                    </label>
                  </div>
                  
                  {formData.schedule_type === 'scheduled' && (
                    <input
                      type="datetime-local"
                      value={formData.scheduled_at}
                      onChange={(e) => setFormData({ ...formData, scheduled_at: e.target.value })}
                      min={getMinDateTime()}
                      className="w-full mt-2 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                      required
                    />
                  )}
                </div>

                {/* Targeting */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Target Users
                  </label>
                  <label className="flex items-center">
                    <input
                      type="checkbox"
                      checked={formData.target_all_users}
                      onChange={(e) => setFormData({ ...formData, target_all_users: e.target.checked })}
                      className="mr-2"
                    />
                    <span className="text-sm">Send to all active users</span>
                  </label>
                </div>

                {/* Submit Button */}
                <button
                  type="submit"
                  disabled={createBroadcastMutation.isPending}
                  className="w-full bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 flex items-center justify-center"
                >
                  {createBroadcastMutation.isPending ? (
                    <>
                      <RefreshCw className="w-4 h-4 mr-2 animate-spin" />
                      Sending...
                    </>
                  ) : (
                    <>
                      <Send className="w-4 h-4 mr-2" />
                      Send Notification
                    </>
                  )}
                </button>
              </form>
            </div>
          </div>

          {/* Broadcast History */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow">
              <div className="p-6 border-b border-gray-200">
                <div className="flex items-center justify-between">
                  <h2 className="text-lg font-semibold text-gray-900">Broadcast History</h2>
                  <div className="flex items-center space-x-2">
                    <select
                      value={statusFilter}
                      onChange={(e) => setStatusFilter(e.target.value)}
                      className="px-3 py-1 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                    >
                      <option value="">All Status</option>
                      <option value="sent">Sent</option>
                      <option value="scheduled">Scheduled</option>
                      <option value="cancelled">Cancelled</option>
                    </select>
                    <button
                      onClick={() => refetchBroadcasts()}
                      className="p-2 rounded-lg hover:bg-gray-100 transition-colors"
                    >
                      <RefreshCw className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>

              <div className="p-6">
                {broadcastsData?.broadcasts?.length === 0 ? (
                  <div className="text-center py-8">
                    <Bell className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                    <p className="text-gray-500">No broadcasts found</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {broadcastsData?.broadcasts?.map((broadcast: Broadcast) => (
                      <div key={broadcast.id} className="border border-gray-200 rounded-lg p-4">
                        <div className="flex items-start justify-between">
                          <div className="flex-1">
                            <div className="flex items-center space-x-2 mb-2">
                              {getStatusIcon(broadcast.status)}
                              <h3 className="font-medium text-gray-900">{broadcast.title}</h3>
                              <span className={`px-2 py-1 text-xs rounded-full ${getStatusColor(broadcast.status)}`}>
                                {broadcast.status}
                              </span>
                            </div>
                            
                            <p className="text-gray-600 mb-3">{broadcast.message}</p>
                            
                            <div className="flex items-center space-x-4 text-sm text-gray-500">
                              {broadcast.scheme_name && (
                                <div className="flex items-center">
                                  <FileText className="w-4 h-4 mr-1" />
                                  {broadcast.scheme_name}
                                </div>
                              )}
                              
                              <div className="flex items-center">
                                <Users className="w-4 h-4 mr-1" />
                                {broadcast.sent_count}/{broadcast.total_users} users
                              </div>
                              
                              <div className="flex items-center">
                                <Calendar className="w-4 h-4 mr-1" />
                                {new Date(broadcast.created_at).toLocaleDateString()}
                              </div>
                              
                              <div className="flex items-center">
                                <Clock className="w-4 h-4 mr-1" />
                                {broadcast.admin_name}
                              </div>
                            </div>
                          </div>
                          
                          <div className="ml-4">
                            {broadcast.status === 'scheduled' && (
                              <button
                                onClick={() => handleCancel(broadcast.id)}
                                disabled={cancelBroadcastMutation.isPending}
                                className="px-3 py-1 text-sm bg-red-600 text-white rounded hover:bg-red-700 transition-colors disabled:opacity-50"
                              >
                                Cancel
                              </button>
                            )}
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
                
                {/* Pagination */}
                {broadcastsData && broadcastsData.total_pages > 1 && (
                  <div className="flex items-center justify-between mt-6 pt-6 border-t border-gray-200">
                    <div className="text-sm text-gray-700">
                      Showing {((currentPage - 1) * 10) + 1} to {Math.min(currentPage * 10, broadcastsData.total)} of {broadcastsData.total} broadcasts
                    </div>
                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => setCurrentPage(Math.max(1, currentPage - 1))}
                        disabled={currentPage === 1}
                        className="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50"
                      >
                        Previous
                      </button>
                      <span className="px-3 py-1 text-sm">
                        Page {currentPage} of {broadcastsData.total_pages}
                      </span>
                      <button
                        onClick={() => setCurrentPage(Math.min(broadcastsData.total_pages, currentPage + 1))}
                        disabled={currentPage === broadcastsData.total_pages}
                        className="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50"
                      >
                        Next
                      </button>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export { NotifyUsersPage }
