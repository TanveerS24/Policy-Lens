import React from 'react'
import { useQuery } from '@tanstack/react-query'
import { Users, FileText, Activity, TrendingUp } from 'lucide-react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

interface DashboardStats {
  total_users: number
  new_users_today: number
  total_schemes: number
  active_schemes: number
  total_documents: number
  documents_this_week: number
  total_eligibility_checks: number
  eligibility_checks_this_week: number
}

interface ActivityItem {
  id: number
  action: string
  actor_type: string
  resource_type: string
  created_at: string
}

interface DashboardResponse {
  statistics: DashboardStats
  recent_activity: ActivityItem[]
}

const fetchDashboard = async (): Promise<DashboardResponse> => {
  const response = await axios.get(`${API_URL}/admin/dashboard`)
  return response.data
}

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate()
  const { data, isLoading } = useQuery({
    queryKey: ['dashboard'],
    queryFn: fetchDashboard,
  })

  const stats = data?.statistics
  const recentActivity = data?.recent_activity || []

  const statCards = [
    { 
      name: 'Total Users', 
      value: stats?.total_users || 0, 
      change: `+${stats?.new_users_today || 0} today`,
      icon: Users,
      color: 'bg-blue-500'
    },
    { 
      name: 'Active Schemes', 
      value: stats?.active_schemes || 0, 
      change: `${stats?.total_schemes || 0} total`,
      icon: FileText,
      color: 'bg-green-500'
    },
    { 
      name: 'Eligibility Checks', 
      value: stats?.total_eligibility_checks || 0, 
      change: `+${stats?.eligibility_checks_this_week || 0} this week`,
      icon: Activity,
      color: 'bg-purple-500'
    },
    { 
      name: 'Documents Processed', 
      value: stats?.total_documents || 0, 
      change: `+${stats?.documents_this_week || 0} this week`,
      icon: TrendingUp,
      color: 'bg-orange-500'
    },
  ]

  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
      
      <div className="mt-8 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {statCards.map((stat) => (
          <div key={stat.name} className="card overflow-hidden">
            <div className="p-5">
              <div className="flex items-center">
                <div className="flex-shrink-0">
                  <div className={`${stat.color} rounded-md p-3`}>
                    <stat.icon className="h-6 w-6 text-white" />
                  </div>
                </div>
                <div className="ml-5 w-0 flex-1">
                  <dl>
                    <dt className="text-sm font-medium text-gray-500 truncate">
                      {stat.name}
                    </dt>
                    <dd className="text-2xl font-semibold text-gray-900">
                      {isLoading ? '-' : stat.value}
                    </dd>
                  </dl>
                </div>
              </div>
            </div>
            <div className="bg-gray-50 px-5 py-3">
              <div className="text-sm text-gray-500">
                {stat.change}
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="mt-8 grid grid-cols-1 gap-8 lg:grid-cols-2">
        {/* Recent Activity */}
        <div className="card">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Recent Activity</h3>
          </div>
          <div className="p-6">
            <ul className="space-y-4">
              {isLoading ? (
                <li className="text-sm text-gray-500">Loading...</li>
              ) : recentActivity.length === 0 ? (
                <li className="text-sm text-gray-500">No recent activity</li>
              ) : (
                recentActivity.slice(0, 5).map((activity: ActivityItem) => (
                  <li key={activity.id} className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className="h-8 w-8 rounded-full bg-primary-100 flex items-center justify-center">
                        <Activity className="h-4 w-4 text-primary-600" />
                      </div>
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          {activity.action.replace(/_/g, ' ').replace(/\b\w/g, (l: string) => l.toUpperCase())}
                        </p>
                        <p className="text-xs text-gray-500">
                          {activity.resource_type} by {activity.actor_type}
                        </p>
                      </div>
                    </div>
                    <span className="text-xs text-gray-500">
                      {activity.created_at ? new Date(activity.created_at).toLocaleString() : 'Unknown'}
                    </span>
                  </li>
                ))
              )}
            </ul>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="card">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Quick Actions</h3>
          </div>
          <div className="p-6">
            <div className="grid grid-cols-2 gap-4">
              <button 
                className="btn-primary"
                onClick={() => navigate('/schemes')}
              >
                Add New Scheme
              </button>
              <button 
                className="btn-secondary"
                onClick={() => navigate('/audit-logs')}
              >
                View Audit Logs
              </button>
              <button 
                className="btn-secondary"
                onClick={() => navigate('/users')}
              >
                Export Users
              </button>
              <button 
                className="btn-secondary"
                onClick={() => navigate('/settings')}
              >
                System Settings
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
