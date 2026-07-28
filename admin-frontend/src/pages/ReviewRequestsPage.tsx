import React, { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { 
  FileCheck, 
  Search, 
  Eye, 
  CheckCircle, 
  XCircle, 
  FileText, 
  User as UserIcon, 
  Clock, 
  Sparkles, 
  ShieldAlert, 
  ExternalLink,
  X,
  AlertCircle,
  Building2,
  Check
} from 'lucide-react'
import axios from 'axios'
import { useAuthStore } from '../stores/authStore'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export interface ReviewRequest {
  id: number
  filename: string
  file_size: number
  mime_type: string
  status: string
  publish_status: string
  uploaded_at: string | null
  publish_requested_at: string | null
  user: {
    id: number | null
    name: string | null
    mobile_number: string | null
    email: string | null
  } | null
  summary_generated: boolean
  confidence_score: number | null
  coverage_summary: string | null
  eligibility_criteria: string | null
}

export interface ReviewRequestDetail extends ReviewRequest {
  ai_summary: {
    coverage_summary: string | null
    exclusions: string | null
    waiting_period: string | null
    claims_process: string | null
    renewal_conditions: string | null
    eligibility_criteria: string | null
    coverage_details: Record<string, any>
    exclusions_list: string[]
    confidence_score: number | null
  } | null
  suggested_scheme: {
    name: string
    code: string
    type: string
    description: string
    eligibility_criteria: string
    coverage_amount: number
    target_categories: string[]
    services_covered: string[]
  }
}

export const ReviewRequestsPage: React.FC = () => {
  const { token, user } = useAuthStore()
  const queryClient = useQueryClient()

  // State
  const [searchQuery, setSearchQuery] = useState('')
  const [statusFilter, setStatusFilter] = useState<'all' | 'pending_review' | 'published' | 'rejected'>('all')
  const [selectedRequestId, setSelectedRequestId] = useState<number | null>(null)
  
  // Reject Modal State
  const [rejectingId, setRejectingId] = useState<number | null>(null)
  const [rejectionReason, setRejectionReason] = useState('')

  // Approve Customization Form State
  const [approveFormData, setApproveFormData] = useState({
    scheme_name: '',
    scheme_code: '',
    scheme_type: 'state',
    ministry: '',
    state: '',
    description: '',
    eligibility_criteria: '',
    coverage_amount: 10000,
    target_categories: 'BPL, Women, Children, Senior Citizens, Disabled',
    services_covered: 'Consultation, Cleaning, Extraction'
  })

  // Toast Notification trigger
  const triggerToast = (type: 'success' | 'error' | 'warning' | 'info', message: string) => {
    const event = new CustomEvent('toast', { detail: { type, message } })
    document.dispatchEvent(event)
  }

  const canAction = user?.role === 'super_admin' || user?.role === 'content_admin'

  // Fetch list of requests
  const { data: requestsData, isLoading: isLoadingList } = useQuery({
    queryKey: ['review-requests', statusFilter],
    queryFn: async () => {
      const response = await axios.get(`${API_URL}/admin/review-requests`, {
        params: { status: statusFilter },
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data.review_requests as ReviewRequest[]
    },
    enabled: !!token,
    refetchInterval: 5000,
    refetchIntervalInBackground: true
  })

  // Fetch single request details when modal opens
  const { data: detailData, isLoading: isLoadingDetail } = useQuery({
    queryKey: ['review-request-detail', selectedRequestId],
    queryFn: async () => {
      if (!selectedRequestId) return null
      const response = await axios.get(`${API_URL}/admin/review-requests/${selectedRequestId}`, {
        headers: { Authorization: `Bearer ${token}` }
      })
      const data = response.data as ReviewRequestDetail
      // Pre-fill approve form with suggested scheme data
      setApproveFormData({
        scheme_name: data.suggested_scheme?.name || '',
        scheme_code: data.suggested_scheme?.code || '',
        scheme_type: data.suggested_scheme?.type || 'state',
        ministry: '',
        state: '',
        description: data.suggested_scheme?.description || '',
        eligibility_criteria: data.suggested_scheme?.eligibility_criteria || '',
        coverage_amount: data.suggested_scheme?.coverage_amount || 10000,
        target_categories: data.suggested_scheme?.target_categories?.join(', ') || 'General Citizens',
        services_covered: data.suggested_scheme?.services_covered?.join(', ') || 'Consultation, Cleaning'
      })
      return data
    },
    enabled: !!selectedRequestId && !!token
  })

  // Approve Mutation
  const approveMutation = useMutation({
    mutationFn: async ({ id, payload }: { id: number; payload: any }) => {
      const response = await axios.post(`${API_URL}/admin/review-requests/${id}/approve`, payload, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    },
    onSuccess: (data) => {
      triggerToast('success', data.message || 'Scheme published successfully!')
      queryClient.invalidateQueries({ queryKey: ['review-requests'] })
      setSelectedRequestId(null)
    },
    onError: (err: any) => {
      const errorMsg = err.response?.data?.detail || 'Failed to approve request'
      triggerToast('error', errorMsg)
    }
  })

  // Reject Mutation
  const rejectMutation = useMutation({
    mutationFn: async ({ id, reason }: { id: number; reason: string }) => {
      const response = await axios.post(`${API_URL}/admin/review-requests/${id}/reject`, { rejection_reason: reason }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      return response.data
    },
    onSuccess: (data) => {
      triggerToast('success', data.message || 'Publish request rejected')
      queryClient.invalidateQueries({ queryKey: ['review-requests'] })
      setRejectingId(null)
      setRejectionReason('')
      setSelectedRequestId(null)
    },
    onError: (err: any) => {
      const errorMsg = err.response?.data?.detail || 'Failed to reject request'
      triggerToast('error', errorMsg)
    }
  })

  // Handlers
  const handleApprove = () => {
    if (!selectedRequestId) return
    const payload = {
      scheme_name: approveFormData.scheme_name,
      scheme_code: approveFormData.scheme_code,
      scheme_type: approveFormData.scheme_type,
      ministry: approveFormData.ministry || undefined,
      state: approveFormData.state || undefined,
      description: approveFormData.description,
      eligibility_criteria: approveFormData.eligibility_criteria,
      coverage_amount: Number(approveFormData.coverage_amount) || 0,
      target_categories: approveFormData.target_categories.split(',').map(s => s.trim()).filter(Boolean),
      services_covered: approveFormData.services_covered.split(',').map(s => s.trim()).filter(Boolean),
    }
    approveMutation.mutate({ id: selectedRequestId, payload })
  }

  const handleRejectSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!rejectingId || !rejectionReason.trim()) {
      triggerToast('warning', 'Please enter a rejection reason')
      return
    }
    rejectMutation.mutate({ id: rejectingId, reason: rejectionReason.trim() })
  }

  const filteredRequests = requestsData?.filter(req => {
    const q = searchQuery.toLowerCase()
    const matchName = req.filename.toLowerCase().includes(q)
    const matchUser = (req.user?.name || '').toLowerCase().includes(q) || (req.user?.mobile_number || '').includes(q)
    return matchName || matchUser
  })

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'published':
        return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800"><CheckCircle className="w-3 h-3 mr-1" /> Published</span>
      case 'rejected':
        return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-rose-100 text-rose-800"><XCircle className="w-3 h-3 mr-1" /> Rejected</span>
      case 'pending_review':
      default:
        return <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-800"><Clock className="w-3 h-3 mr-1" /> Pending Review</span>
    }
  }

  const pendingCount = requestsData?.filter(r => r.publish_status === 'pending_review').length || 0
  const publishedCount = requestsData?.filter(r => r.publish_status === 'published').length || 0
  const rejectedCount = requestsData?.filter(r => r.publish_status === 'rejected').length || 0

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <FileCheck className="h-7 w-7 text-primary-600" />
            Document Review Requests
          </h1>
          <p className="mt-1 text-sm text-gray-500">
            Review user-submitted scheme documents, inspect AI summaries & eligibility criteria, and publish them into active public schemes.
          </p>
        </div>
        {!canAction && (
          <div className="bg-amber-50 border border-amber-200 rounded-lg p-3 text-xs text-amber-800 flex items-center gap-2">
            <AlertCircle className="h-4 w-4 shrink-0 text-amber-600" />
            <span>Support Admin View-Only Mode. Approval actions require Super Admin or Content Admin role.</span>
          </div>
        )}
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-gray-500 uppercase tracking-wider">Pending Review</p>
            <p className="text-2xl font-bold text-amber-600 mt-1">{pendingCount}</p>
          </div>
          <div className="p-3 bg-amber-50 rounded-lg text-amber-600">
            <Clock className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-gray-500 uppercase tracking-wider">Approved & Published</p>
            <p className="text-2xl font-bold text-emerald-600 mt-1">{publishedCount}</p>
          </div>
          <div className="p-3 bg-emerald-50 rounded-lg text-emerald-600">
            <CheckCircle className="w-6 h-6" />
          </div>
        </div>

        <div className="bg-white p-5 rounded-xl border border-gray-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-medium text-gray-500 uppercase tracking-wider">Rejected Requests</p>
            <p className="text-2xl font-bold text-rose-600 mt-1">{rejectedCount}</p>
          </div>
          <div className="p-3 bg-rose-50 rounded-lg text-rose-600">
            <XCircle className="w-6 h-6" />
          </div>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-4 bg-white p-4 rounded-xl border border-gray-200 shadow-sm">
        {/* Status Filter Tabs */}
        <div className="flex items-center gap-1 bg-gray-100 p-1 rounded-lg w-full sm:w-auto">
          {(['all', 'pending_review', 'published', 'rejected'] as const).map((tab) => (
            <button
              key={tab}
              onClick={() => setStatusFilter(tab)}
              className={`
                px-3 py-1.5 rounded-md text-xs font-medium capitalize transition-all flex-1 sm:flex-none text-center
                ${statusFilter === tab 
                  ? 'bg-white text-gray-900 shadow-sm font-semibold' 
                  : 'text-gray-600 hover:text-gray-900'
                }
              `}
            >
              {tab.replace('_', ' ')}
            </button>
          ))}
        </div>

        {/* Search Input */}
        <div className="relative w-full sm:w-80">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-gray-400" />
          <input
            type="text"
            placeholder="Search filename or user..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
          />
        </div>
      </div>

      {/* Requests Table */}
      <div className="bg-white rounded-xl border border-gray-200 shadow-sm overflow-hidden">
        {isLoadingList ? (
          <div className="p-12 text-center text-gray-500">
            <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-primary-600 border-t-transparent mb-3" />
            <p className="text-sm">Loading review requests...</p>
          </div>
        ) : filteredRequests?.length === 0 ? (
          <div className="p-12 text-center text-gray-500">
            <FileText className="h-12 w-12 text-gray-300 mx-auto mb-3" />
            <h3 className="text-base font-semibold text-gray-800">No Review Requests Found</h3>
            <p className="text-sm text-gray-500 mt-1">There are no document publish requests matching your selected filters.</p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50 border-b border-gray-200 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                  <th className="px-6 py-3">Document</th>
                  <th className="px-6 py-3">Submitted By</th>
                  <th className="px-6 py-3">Date</th>
                  <th className="px-6 py-3">AI Confidence</th>
                  <th className="px-6 py-3">Publish Status</th>
                  <th className="px-6 py-3 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200 text-sm">
                {filteredRequests?.map((req) => (
                  <tr key={req.id} className="hover:bg-gray-50/80 transition-colors">
                    <td className="px-6 py-4 font-medium text-gray-900">
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-primary-50 text-primary-600 rounded-lg shrink-0">
                          <FileText className="w-5 h-5" />
                        </div>
                        <div>
                          <p className="font-semibold text-gray-900 truncate max-w-xs">{req.filename}</p>
                          <p className="text-xs text-gray-400">{(req.file_size / 1024).toFixed(1)} KB • {req.mime_type}</p>
                        </div>
                      </div>
                    </td>

                    <td className="px-6 py-4 text-gray-700">
                      <div className="flex items-center gap-2">
                        <UserIcon className="w-4 h-4 text-gray-400 shrink-0" />
                        <div>
                          <p className="font-medium text-gray-900">{req.user?.name || 'Anonymous User'}</p>
                          <p className="text-xs text-gray-500">{req.user?.mobile_number || req.user?.email || `User #${req.user?.id}`}</p>
                        </div>
                      </div>
                    </td>

                    <td className="px-6 py-4 text-gray-600 text-xs">
                      {req.publish_requested_at ? new Date(req.publish_requested_at).toLocaleDateString(undefined, { dateStyle: 'medium' }) : 'N/A'}
                    </td>

                    <td className="px-6 py-4">
                      {req.confidence_score !== null ? (
                        <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-semibold ${
                          req.confidence_score >= 80 ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-amber-50 text-amber-700 border border-amber-200'
                        }`}>
                          <Sparkles className="w-3 h-3 mr-1" />
                          {req.confidence_score}% Confidence
                        </span>
                      ) : (
                        <span className="text-xs text-gray-400">Not Scored</span>
                      )}
                    </td>

                    <td className="px-6 py-4">
                      {getStatusBadge(req.publish_status)}
                    </td>

                    <td className="px-6 py-4 text-right">
                      <button
                        onClick={() => setSelectedRequestId(req.id)}
                        className="inline-flex items-center px-3 py-1.5 border border-primary-600 text-primary-600 hover:bg-primary-50 font-medium text-xs rounded-lg transition-colors"
                      >
                        <Eye className="w-4 h-4 mr-1.5" />
                        Review Request
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Detail & Action Modal */}
      {selectedRequestId && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-gray-900/60 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl shadow-xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col border border-gray-200">
            {/* Modal Header */}
            <div className="px-6 py-4 bg-gray-50 border-b border-gray-200 flex items-center justify-between shrink-0">
              <div className="flex items-center gap-3">
                <div className="p-2 bg-primary-100 text-primary-700 rounded-lg">
                  <FileCheck className="w-6 h-6" />
                </div>
                <div>
                  <h2 className="text-lg font-bold text-gray-900">Review Scheme Publish Request</h2>
                  <p className="text-xs text-gray-500">Document #{selectedRequestId} • User Submission Review</p>
                </div>
              </div>
              <button
                onClick={() => setSelectedRequestId(null)}
                className="p-1.5 text-gray-400 hover:text-gray-600 hover:bg-gray-200 rounded-lg transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Content */}
            <div className="p-6 overflow-y-auto flex-1 space-y-6">
              {isLoadingDetail ? (
                <div className="p-12 text-center text-gray-500">
                  <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-primary-600 border-t-transparent mb-3" />
                  <p className="text-sm">Loading document & scheme details...</p>
                </div>
              ) : detailData ? (
                <>
                  {/* Document & User Metadata Card */}
                  <div className="bg-gray-50 p-4 rounded-xl border border-gray-200 grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Uploaded Document Info</h4>
                      <p className="font-semibold text-gray-900">{detailData.filename}</p>
                      <p className="text-xs text-gray-500 mt-0.5">Size: {(detailData.file_size / 1024).toFixed(1)} KB | MIME: {detailData.mime_type}</p>
                      <div className="mt-3">
                        <a
                          href={`${API_URL}/admin/review-requests/${detailData.id}/file`}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="inline-flex items-center text-xs font-semibold text-primary-600 hover:text-primary-800 bg-white border border-gray-300 px-3 py-1.5 rounded-md shadow-sm transition-colors"
                        >
                          <ExternalLink className="w-3.5 h-3.5 mr-1.5" />
                          View / Download Original Document
                        </a>
                      </div>
                    </div>

                    <div>
                      <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Requesting Citizen Info</h4>
                      <p className="font-semibold text-gray-900">{detailData.user?.name || 'Anonymous'}</p>
                      <p className="text-xs text-gray-500 mt-0.5">Mobile: {detailData.user?.mobile_number || 'N/A'}</p>
                      <p className="text-xs text-gray-500">Email: {detailData.user?.email || 'N/A'}</p>
                      <div className="mt-2">
                        {getStatusBadge(detailData.publish_status)}
                      </div>
                    </div>
                  </div>

                  {/* AI Extracted Summary & Eligibility Criteria Section */}
                  {detailData.ai_summary && (
                    <div className="space-y-4">
                      <div className="flex items-center justify-between border-b border-gray-200 pb-2">
                        <h3 className="text-sm font-bold text-gray-900 flex items-center gap-2">
                          <Sparkles className="w-4 h-4 text-amber-500" />
                          AI Summary & Extracted Criteria
                        </h3>
                        <span className="text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                          {detailData.ai_summary.confidence_score}% Confidence
                        </span>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="bg-white p-4 rounded-xl border border-gray-200">
                          <h4 className="text-xs font-bold text-gray-700 uppercase tracking-wider mb-1.5">Coverage Summary</h4>
                          <p className="text-xs text-gray-600 whitespace-pre-line leading-relaxed">{detailData.ai_summary.coverage_summary || 'N/A'}</p>
                        </div>

                        <div className="bg-white p-4 rounded-xl border border-gray-200">
                          <h4 className="text-xs font-bold text-gray-700 uppercase tracking-wider mb-1.5">Eligibility Criteria</h4>
                          <p className="text-xs text-gray-600 whitespace-pre-line leading-relaxed">{detailData.ai_summary.eligibility_criteria || 'N/A'}</p>
                        </div>

                        <div className="bg-white p-4 rounded-xl border border-gray-200">
                          <h4 className="text-xs font-bold text-gray-700 uppercase tracking-wider mb-1.5">Exclusions</h4>
                          <p className="text-xs text-gray-600 whitespace-pre-line leading-relaxed">{detailData.ai_summary.exclusions || 'N/A'}</p>
                        </div>

                        <div className="bg-white p-4 rounded-xl border border-gray-200">
                          <h4 className="text-xs font-bold text-gray-700 uppercase tracking-wider mb-1.5">Claims Process & Renewal</h4>
                          <p className="text-xs text-gray-600 leading-relaxed font-medium">Claims: {detailData.ai_summary.claims_process || 'N/A'}</p>
                          <p className="text-xs text-gray-600 leading-relaxed mt-1">Renewal: {detailData.ai_summary.renewal_conditions || 'N/A'}</p>
                        </div>
                      </div>
                    </div>
                  )}

                  {/* Editable Scheme Metadata Form for Approval */}
                  <div className="border-t border-gray-200 pt-5 space-y-4">
                    <h3 className="text-sm font-bold text-gray-900 flex items-center gap-2">
                      <Building2 className="w-4 h-4 text-primary-600" />
                      Scheme Metadata & Publication Settings
                    </h3>
                    <p className="text-xs text-gray-500">
                      Verify and edit the scheme information that will be published publicly upon approval.
                    </p>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="block text-xs font-semibold text-gray-700 mb-1">Scheme Name *</label>
                        <input
                          type="text"
                          value={approveFormData.scheme_name}
                          onChange={(e) => setApproveFormData({ ...approveFormData, scheme_name: e.target.value })}
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                        />
                      </div>

                      <div>
                        <label className="block text-xs font-semibold text-gray-700 mb-1">Scheme Code *</label>
                        <input
                          type="text"
                          value={approveFormData.scheme_code}
                          onChange={(e) => setApproveFormData({ ...approveFormData, scheme_code: e.target.value })}
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                        />
                      </div>

                      <div>
                        <label className="block text-xs font-semibold text-gray-700 mb-1">Scheme Type</label>
                        <select
                          value={approveFormData.scheme_type}
                          onChange={(e) => setApproveFormData({ ...approveFormData, scheme_type: e.target.value })}
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
                        <label className="block text-xs font-semibold text-gray-700 mb-1">Coverage Amount (₹/$)</label>
                        <input
                          type="number"
                          value={approveFormData.coverage_amount}
                          onChange={(e) => setApproveFormData({ ...approveFormData, coverage_amount: Number(e.target.value) })}
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                        />
                      </div>

                      <div className="md:col-span-2">
                        <label className="block text-xs font-semibold text-gray-700 mb-1">Description</label>
                        <textarea
                          rows={2}
                          value={approveFormData.description}
                          onChange={(e) => setApproveFormData({ ...approveFormData, description: e.target.value })}
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                        />
                      </div>

                      <div className="md:col-span-2">
                        <label className="block text-xs font-semibold text-gray-700 mb-1">Eligibility Criteria</label>
                        <textarea
                          rows={2}
                          value={approveFormData.eligibility_criteria}
                          onChange={(e) => setApproveFormData({ ...approveFormData, eligibility_criteria: e.target.value })}
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                        />
                      </div>

                      <div>
                        <label className="block text-xs font-semibold text-gray-700 mb-1">Target Categories (comma separated)</label>
                        <input
                          type="text"
                          value={approveFormData.target_categories}
                          onChange={(e) => setApproveFormData({ ...approveFormData, target_categories: e.target.value })}
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                        />
                      </div>

                      <div>
                        <label className="block text-xs font-semibold text-gray-700 mb-1">Services Covered (comma separated)</label>
                        <input
                          type="text"
                          value={approveFormData.services_covered}
                          onChange={(e) => setApproveFormData({ ...approveFormData, services_covered: e.target.value })}
                          className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500"
                        />
                      </div>
                    </div>
                  </div>
                </>
              ) : null}
            </div>

            {/* Modal Actions Footer */}
            <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex flex-col sm:flex-row items-center justify-between gap-3 shrink-0">
              <button
                type="button"
                onClick={() => setSelectedRequestId(null)}
                className="w-full sm:w-auto px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>

              {canAction ? (
                <div className="flex items-center gap-3 w-full sm:w-auto">
                  {detailData?.publish_status !== 'rejected' && (
                    <button
                      type="button"
                      onClick={() => setRejectingId(selectedRequestId)}
                      className="flex-1 sm:flex-none inline-flex items-center justify-center px-4 py-2 text-sm font-medium text-rose-700 bg-rose-50 hover:bg-rose-100 border border-rose-200 rounded-lg transition-colors"
                    >
                      <XCircle className="w-4 h-4 mr-1.5" />
                      Reject Request
                    </button>
                  )}

                  {detailData?.publish_status !== 'published' && (
                    <button
                      type="button"
                      onClick={handleApprove}
                      disabled={approveMutation.isPending}
                      className="flex-1 sm:flex-none inline-flex items-center justify-center px-5 py-2 text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg shadow-sm transition-colors disabled:opacity-50"
                    >
                      <Check className="w-4 h-4 mr-1.5" />
                      {approveMutation.isPending ? 'Publishing...' : 'Approve & Publish Scheme'}
                    </button>
                  )}
                </div>
              ) : (
                <div className="text-xs text-amber-700 font-medium">
                  Approval & Rejection restricted to Super Admin and Content Admin.
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Rejection Modal */}
      {rejectingId && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-gray-900/70 backdrop-blur-sm flex items-center justify-center p-4">
          <form onSubmit={handleRejectSubmit} className="bg-white rounded-xl shadow-xl max-w-md w-full p-6 border border-gray-200 space-y-4">
            <div className="flex items-center gap-3 text-rose-600">
              <ShieldAlert className="w-6 h-6 shrink-0" />
              <h3 className="text-lg font-bold text-gray-900">Reject Publish Request</h3>
            </div>
            
            <p className="text-xs text-gray-600">
              Please provide a clear reason for rejecting this document publication request. The user will be notified of this feedback.
            </p>

            <div>
              <label className="block text-xs font-semibold text-gray-700 mb-1">Rejection Reason *</label>
              <textarea
                required
                rows={3}
                value={rejectionReason}
                onChange={(e) => setRejectionReason(e.target.value)}
                placeholder="e.g. Document is blurred or missing official scheme terms and authorization signatures..."
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-rose-500"
              />
            </div>

            <div className="flex items-center justify-end gap-3 pt-2">
              <button
                type="button"
                onClick={() => { setRejectingId(null); setRejectionReason(''); }}
                className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={rejectMutation.isPending}
                className="px-4 py-2 text-sm font-medium text-white bg-rose-600 hover:bg-rose-700 rounded-lg transition-colors disabled:opacity-50"
              >
                {rejectMutation.isPending ? 'Rejecting...' : 'Confirm Rejection'}
              </button>
            </div>
          </form>
        </div>
      )}
    </div>
  )
}
