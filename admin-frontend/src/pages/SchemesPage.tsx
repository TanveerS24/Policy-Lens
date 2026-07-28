import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { 
  Plus, 
  Search, 
  Edit2, 
  Trash2, 
  Eye, 
  X, 
  CheckCircle, 
  ExternalLink,
  FileText,
  Building2,
  AlertTriangle
} from 'lucide-react'
import axios from 'axios'
import { useAuthStore } from '../stores/authStore'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

interface Scheme {
  id: number
  name: string
  code: string
  type: string
  status: string
  ministry?: string
  state?: string
  description: string
  short_description?: string
  coverage_amount?: number
  target_categories?: string[]
  services_covered?: string[]
  income_criteria?: string
  has_original_document?: boolean
}

export const SchemesPage: React.FC = () => {
  const navigate = useNavigate()
  const { token, user } = useAuthStore()
  const queryClient = useQueryClient()

  // Filters & State
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState<'all' | 'active' | 'inactive'>('all')
  const [typeFilter, setTypeFilter] = useState<string>('all')
  
  // Modals State
  const [viewingScheme, setViewingScheme] = useState<Scheme | null>(null)
  const [editingScheme, setEditingScheme] = useState<Scheme | null>(null)
  const [deletingScheme, setDeletingScheme] = useState<Scheme | null>(null)

  // Edit Form State
  const [editFormData, setEditFormData] = useState({
    name: '',
    code: '',
    type: 'state',
    status: 'active',
    coverage_amount: 0,
    ministry: '',
    state: '',
    description: '',
    target_categories: '',
    services_covered: ''
  })

  // Toast Helper
  const triggerToast = (type: 'success' | 'error' | 'warning' | 'info', message: string) => {
    const event = new CustomEvent('toast', { detail: { type, message } })
    document.dispatchEvent(event)
  }

  const canEdit = user?.role === 'super_admin' || user?.role === 'content_admin'

  // Fetch schemes
  const { data: schemes, isLoading } = useQuery({
    queryKey: ['admin-schemes', statusFilter, typeFilter],
    queryFn: async () => {
      const params: Record<string, any> = {}
      if (statusFilter !== 'all') params.status = statusFilter
      if (typeFilter !== 'all') params.type = typeFilter

      const response = await axios.get(`${API_URL}/admin/schemes`, {
        params,
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data.schemes as Scheme[]
    },
    enabled: !!token,
    refetchInterval: 5000, // Live auto-update when new schemes are added anywhere
    refetchIntervalInBackground: true
  })

  // Update Scheme Mutation
  const updateMutation = useMutation({
    mutationFn: async ({ id, payload }: { id: number; payload: any }) => {
      const response = await axios.put(`${API_URL}/admin/schemes/${id}`, payload, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    },
    onSuccess: (data) => {
      triggerToast('success', data.message || 'Scheme updated successfully')
      queryClient.invalidateQueries({ queryKey: ['admin-schemes'] })
      setEditingScheme(null)
    },
    onError: (err: any) => {
      const msg = err.response?.data?.detail || 'Failed to update scheme'
      triggerToast('error', msg)
    }
  })

  // Delete Scheme Mutation
  const deleteMutation = useMutation({
    mutationFn: async (id: number) => {
      const response = await axios.delete(`${API_URL}/admin/schemes/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    },
    onSuccess: (data) => {
      triggerToast('success', data.message || 'Scheme deleted successfully')
      queryClient.invalidateQueries({ queryKey: ['admin-schemes'] })
      setDeletingScheme(null)
    },
    onError: (err: any) => {
      const msg = err.response?.data?.detail || 'Failed to delete scheme'
      triggerToast('error', msg)
    }
  })

  // Open Edit Modal
  const openEditModal = (scheme: Scheme) => {
    setEditingScheme(scheme)
    setEditFormData({
      name: scheme.name || '',
      code: scheme.code || '',
      type: scheme.type || 'state',
      status: scheme.status || 'active',
      coverage_amount: scheme.coverage_amount || 0,
      ministry: scheme.ministry || '',
      state: scheme.state || '',
      description: scheme.description || '',
      target_categories: scheme.target_categories?.join(', ') || '',
      services_covered: scheme.services_covered?.join(', ') || ''
    })
  }

  const toggleEditCategory = (cat: string) => {
    const currentList = editFormData.target_categories.split(',').map(s => s.trim()).filter(Boolean)
    const updated = currentList.includes(cat)
      ? currentList.filter(c => c !== cat)
      : [...currentList, cat]
    setEditFormData({ ...editFormData, target_categories: updated.join(', ') })
  }

  // Handle Edit Submit
  const handleEditSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!editingScheme) return

    const categories = editFormData.target_categories.split(',').map(s => s.trim()).filter(Boolean)
    if (categories.length === 0) {
      triggerToast('warning', 'Target Category is mandatory! Please select at least one category (BPL, Women, Children, Senior Citizens, Disabled).')
      return
    }

    const payload = {
      name: editFormData.name,
      code: editFormData.code,
      type: editFormData.type,
      status: editFormData.status,
      coverage_amount: Number(editFormData.coverage_amount) || 0,
      ministry: editFormData.ministry || undefined,
      state: editFormData.state || undefined,
      description: editFormData.description,
      target_categories: categories,
      services_covered: editFormData.services_covered.split(',').map(s => s.trim()).filter(Boolean)
    }

    updateMutation.mutate({ id: editingScheme.id, payload })
  }

  const filteredSchemes = schemes?.filter((scheme: Scheme) => {
    const q = searchQuery.toLowerCase()
    return scheme.name.toLowerCase().includes(q) || scheme.code.toLowerCase().includes(q)
  })

  return (
    <div className="space-y-6">
      {/* Page Title & Add Button */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <Building2 className="h-7 w-7 text-primary-600" />
            Dental Health Schemes
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Manage public healthcare policies, eligibility parameters, coverage benefits, and documents.
          </p>
        </div>

        <button className="btn-primary flex items-center justify-center shrink-0" onClick={() => navigate('/schemes/add')}>
          <Plus className="h-4 w-4 mr-2" />
          Add New Scheme
        </button>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white p-4 rounded-xl border border-gray-200 shadow-sm flex flex-col md:flex-row items-center justify-between gap-4">
        {/* Search */}
        <div className="relative flex-1 w-full">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search by scheme name or code..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="input-field pl-9 py-2 text-sm w-full"
          />
        </div>

        {/* Filter Dropdowns */}
        <div className="flex flex-wrap items-center gap-3 w-full md:w-auto">
          <div className="flex items-center gap-1.5">
            <span className="text-xs font-semibold text-gray-500">Status:</span>
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value as any)}
              className="px-3 py-1.5 text-xs font-medium border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 bg-white"
            >
              <option value="all">All Status</option>
              <option value="active">Active Only</option>
              <option value="inactive">Inactive Only</option>
            </select>
          </div>

          <div className="flex items-center gap-1.5">
            <span className="text-xs font-semibold text-gray-500">Type:</span>
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="px-3 py-1.5 text-xs font-medium border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 bg-white"
            >
              <option value="all">All Types</option>
              <option value="state">State</option>
              <option value="national">National</option>
              <option value="central">Central</option>
              <option value="ngo">NGO</option>
              <option value="private">Private</option>
            </select>
          </div>
        </div>
      </div>

      {/* Schemes Table */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        {isLoading ? (
          <div className="p-12 text-center text-gray-500">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-primary-600 border-t-transparent mb-3" />
            <p className="text-sm">Loading schemes...</p>
          </div>
        ) : filteredSchemes?.length === 0 ? (
          <div className="p-12 text-center text-gray-500">
            <FileText className="h-12 w-12 text-gray-300 mx-auto mb-3" />
            <h3 className="text-base font-semibold text-gray-800">No Schemes Found</h3>
            <p className="text-sm text-gray-500 mt-1">No dental health schemes match your current search or filter criteria.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-200 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                  <th className="px-6 py-3">Scheme Name</th>
                  <th className="px-6 py-3">Code</th>
                  <th className="px-6 py-3">Type</th>
                  <th className="px-6 py-3">Status</th>
                  <th className="px-6 py-3">Max Coverage</th>
                  <th className="px-6 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 text-sm">
                {filteredSchemes?.map((scheme: Scheme) => (
                  <tr key={scheme.id} className="hover:bg-gray-50/80 transition-colors">
                    <td className="px-6 py-4 font-semibold text-gray-900">
                      <div>
                        <p className="text-gray-900">{scheme.name}</p>
                        {scheme.ministry && <p className="text-xs text-gray-400 font-normal">{scheme.ministry}</p>}
                      </div>
                    </td>
                    <td className="px-6 py-4 font-mono text-xs text-gray-600">{scheme.code}</td>
                    <td className="px-6 py-4 text-gray-600">
                      <span className="capitalize px-2 py-0.5 rounded text-xs font-medium bg-gray-100 border border-gray-200">{scheme.type}</span>
                    </td>
                    <td className="px-6 py-4">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                        scheme.status === 'active' 
                          ? 'bg-emerald-100 text-emerald-800' 
                          : 'bg-gray-100 text-gray-800'
                      }`}>
                        {scheme.status === 'active' ? <CheckCircle className="w-3 h-3 mr-1" /> : null}
                        {scheme.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-gray-700 font-semibold">
                      {scheme.coverage_amount ? `₹${scheme.coverage_amount.toLocaleString()}` : '-'}
                    </td>
                    <td className="px-6 py-4 text-right space-x-2">
                      {/* View Details Button */}
                      <button
                        title="View Details"
                        onClick={() => setViewingScheme(scheme)}
                        className="inline-flex items-center p-1.5 text-gray-500 hover:text-primary-600 hover:bg-gray-100 rounded-lg transition-colors"
                      >
                        <Eye className="h-4 w-4" />
                      </button>

                      {/* Edit Button */}
                      <button
                        title={canEdit ? 'Edit Scheme' : 'Edit Restricted'}
                        onClick={() => {
                          if (canEdit) openEditModal(scheme)
                          else triggerToast('warning', 'Edit permission requires Super Admin or Content Admin role')
                        }}
                        className={`inline-flex items-center p-1.5 rounded-lg transition-colors ${
                          canEdit 
                            ? 'text-primary-600 hover:text-primary-800 hover:bg-primary-50' 
                            : 'text-gray-300 cursor-not-allowed'
                        }`}
                      >
                        <Edit2 className="h-4 w-4" />
                      </button>

                      {/* Delete Button */}
                      <button
                        title={canEdit ? 'Delete Scheme' : 'Delete Restricted'}
                        onClick={() => {
                          if (canEdit) setDeletingScheme(scheme)
                          else triggerToast('warning', 'Delete permission requires Super Admin or Content Admin role')
                        }}
                        className={`inline-flex items-center p-1.5 rounded-lg transition-colors ${
                          canEdit 
                            ? 'text-rose-600 hover:text-rose-800 hover:bg-rose-50' 
                            : 'text-gray-300 cursor-not-allowed'
                        }`}
                      >
                        <Trash2 className="h-4 w-4" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* View Scheme Detail Modal */}
      {viewingScheme && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-gray-900/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-2xl max-h-[85vh] overflow-hidden flex flex-col border border-gray-200">
            <div className="px-6 py-4 bg-gray-50 border-b border-gray-200 flex items-center justify-between shrink-0">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-primary-100 text-primary-700 rounded-lg">
                  <Building2 className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900">{viewingScheme.name}</h3>
                  <p className="text-xs text-gray-500 font-mono">Code: {viewingScheme.code} • Type: {viewingScheme.type}</p>
                </div>
              </div>
              <button onClick={() => setViewingScheme(null)} className="p-1 text-gray-400 hover:text-gray-600 rounded-lg">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 overflow-y-auto space-y-4 text-sm text-gray-700">
              <div>
                <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Description</h4>
                <p className="text-gray-700 whitespace-pre-line leading-relaxed">{viewingScheme.description}</p>
              </div>

              {viewingScheme.income_criteria && (
                <div>
                  <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1">Eligibility Criteria</h4>
                  <p className="text-gray-700 whitespace-pre-line">{viewingScheme.income_criteria}</p>
                </div>
              )}

              <div className="grid grid-cols-2 gap-4 bg-gray-50 p-4 rounded-xl border border-gray-200">
                <div>
                  <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider">Coverage Limit</h4>
                  <p className="font-bold text-gray-900 mt-1">
                    {viewingScheme.coverage_amount ? `₹${viewingScheme.coverage_amount.toLocaleString()}` : 'N/A'}
                  </p>
                </div>
                <div>
                  <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider">Status</h4>
                  <p className="font-bold capitalize text-emerald-600 mt-1">{viewingScheme.status}</p>
                </div>
              </div>

              {viewingScheme.target_categories && viewingScheme.target_categories.length > 0 && (
                <div>
                  <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1.5">Target Categories</h4>
                  <div className="flex flex-wrap gap-1.5">
                    {viewingScheme.target_categories.map((cat, idx) => (
                      <span key={idx} className="bg-primary-50 text-primary-700 text-xs px-2.5 py-1 rounded-md font-medium">
                        {cat}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {viewingScheme.services_covered && viewingScheme.services_covered.length > 0 && (
                <div>
                  <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-1.5">Services Covered</h4>
                  <div className="flex flex-wrap gap-1.5">
                    {viewingScheme.services_covered.map((srv, idx) => (
                      <span key={idx} className="bg-emerald-50 text-emerald-700 text-xs px-2.5 py-1 rounded-md font-medium">
                        {srv}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {viewingScheme.has_original_document && (
                <div className="pt-2">
                  <a
                    href={`${API_URL}/schemes/${viewingScheme.id}/document`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="inline-flex items-center text-xs font-semibold text-primary-600 hover:text-primary-800 bg-white border border-gray-300 px-3 py-2 rounded-lg shadow-sm"
                  >
                    <ExternalLink className="w-4 h-4 mr-1.5" />
                    Download / View Original Scheme PDF Document
                  </a>
                </div>
              )}
            </div>

            <div className="px-6 py-3 bg-gray-50 border-t border-gray-200 text-right">
              <button
                onClick={() => setViewingScheme(null)}
                className="px-4 py-1.5 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-100"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Edit Scheme Modal */}
      {editingScheme && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-gray-900/60 backdrop-blur-sm flex items-center justify-center p-4">
          <form onSubmit={handleEditSubmit} className="bg-white rounded-2xl shadow-xl w-full max-w-3xl max-h-[90vh] overflow-hidden flex flex-col border border-gray-200">
            <div className="px-6 py-4 bg-gray-50 border-b border-gray-200 flex items-center justify-between shrink-0">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-primary-100 text-primary-700 rounded-lg">
                  <Edit2 className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="text-lg font-bold text-gray-900">Edit Scheme Details</h3>
                  <p className="text-xs text-gray-500">ID #{editingScheme.id} • {editingScheme.code}</p>
                </div>
              </div>
              <button type="button" onClick={() => setEditingScheme(null)} className="p-1 text-gray-400 hover:text-gray-600 rounded-lg">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="p-6 overflow-y-auto space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">Scheme Name *</label>
                  <input
                    type="text"
                    required
                    value={editFormData.name}
                    onChange={(e) => setEditFormData({ ...editFormData, name: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">Scheme Code *</label>
                  <input
                    type="text"
                    required
                    value={editFormData.code}
                    onChange={(e) => setEditFormData({ ...editFormData, code: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">Type</label>
                  <select
                    value={editFormData.type}
                    onChange={(e) => setEditFormData({ ...editFormData, type: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="state">State</option>
                    <option value="national">National</option>
                    <option value="central">Central</option>
                    <option value="ngo">NGO</option>
                    <option value="private">Private</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">Status</label>
                  <select
                    value={editFormData.status}
                    onChange={(e) => setEditFormData({ ...editFormData, status: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  >
                    <option value="active">Active</option>
                    <option value="inactive">Inactive</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">Coverage Amount (₹)</label>
                  <input
                    type="number"
                    value={editFormData.coverage_amount}
                    onChange={(e) => setEditFormData({ ...editFormData, coverage_amount: Number(e.target.value) })}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">Ministry / State</label>
                  <input
                    type="text"
                    value={editFormData.ministry}
                    placeholder="e.g. Ministry of Health & Family Welfare"
                    onChange={(e) => setEditFormData({ ...editFormData, ministry: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>

                <div className="md:col-span-2">
                  <label className="block text-xs font-semibold text-gray-700 mb-1">Description *</label>
                  <textarea
                    required
                    rows={3}
                    value={editFormData.description}
                    onChange={(e) => setEditFormData({ ...editFormData, description: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>

                <div className="md:col-span-2">
                  <label className="block text-xs font-semibold text-gray-700 mb-1">
                    Target Category <span className="text-red-500 font-bold">*</span> <span className="text-xs text-red-600 font-normal">(Mandatory — Select or type comma-separated)</span>
                  </label>
                  <div className="flex flex-wrap gap-2 p-2 bg-gray-50 rounded-lg border border-gray-200 mb-2">
                    {['BPL', 'Women', 'Children', 'Senior Citizens', 'Disabled'].map((cat) => {
                      const currentList = editFormData.target_categories.split(',').map(s => s.trim())
                      const isChecked = currentList.includes(cat)
                      return (
                        <label
                          key={cat}
                          className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md cursor-pointer border text-xs font-medium transition-colors ${
                            isChecked
                              ? 'bg-primary-50 border-primary-500 text-primary-700 font-bold'
                              : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-100'
                          }`}
                        >
                          <input
                            type="checkbox"
                            checked={isChecked}
                            onChange={() => toggleEditCategory(cat)}
                            className="rounded text-primary-600 focus:ring-primary-500 h-3.5 w-3.5"
                          />
                          <span>{cat}</span>
                        </label>
                      )
                    })}
                  </div>
                  <input
                    type="text"
                    value={editFormData.target_categories}
                    placeholder="e.g. BPL, Women, Children, Senior Citizens, Disabled"
                    onChange={(e) => setEditFormData({ ...editFormData, target_categories: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                  {editFormData.target_categories.split(',').map(s => s.trim()).filter(Boolean).length === 0 && (
                    <p className="text-xs text-red-500 mt-1 font-semibold">⚠️ Mandatory: Please select at least one category above.</p>
                  )}
                </div>

                <div>
                  <label className="block text-xs font-semibold text-gray-700 mb-1">Services Covered (comma separated)</label>
                  <input
                    type="text"
                    value={editFormData.services_covered}
                    onChange={(e) => setEditFormData({ ...editFormData, services_covered: e.target.value })}
                    className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                  />
                </div>
              </div>
            </div>

            <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex items-center justify-end gap-3 shrink-0">
              <button
                type="button"
                onClick={() => setEditingScheme(null)}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={updateMutation.isPending}
                className="px-5 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 rounded-lg transition-colors disabled:opacity-50"
              >
                {updateMutation.isPending ? 'Saving...' : 'Save Changes'}
              </button>
            </div>
          </form>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {deletingScheme && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-gray-900/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl max-w-md w-full p-6 border border-gray-200 space-y-4">
            <div className="flex items-center gap-3 text-rose-600">
              <AlertTriangle className="w-6 h-6 shrink-0" />
              <h3 className="text-lg font-bold text-gray-900">Delete Scheme</h3>
            </div>
            
            <p className="text-sm text-gray-600">
              Are you sure you want to delete <span className="font-semibold text-gray-900">"{deletingScheme.name}"</span>? This will archive the scheme from public listings.
            </p>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => setDeletingScheme(null)}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="button"
                disabled={deleteMutation.isPending}
                onClick={() => deleteMutation.mutate(deletingScheme.id)}
                className="px-4 py-2 text-sm font-medium text-white bg-rose-600 hover:bg-rose-700 rounded-lg transition-colors disabled:opacity-50"
              >
                {deleteMutation.isPending ? 'Deleting...' : 'Confirm Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
