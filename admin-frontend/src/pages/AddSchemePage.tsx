import React, { useState, useRef, ChangeEvent } from 'react'
import { useNavigate } from 'react-router-dom'
import { useMutation } from '@tanstack/react-query'
import { Upload, FileText, Sparkles, Save, ArrowLeft, RefreshCw } from 'lucide-react'
import axios from 'axios'
import { useAuthStore } from '../stores/authStore'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

interface ExtractedData {
  eligibility_criteria: string
  about_scheme: string
  name: string
  code: string
  type: string
}

interface SchemeFormData {
  name: string
  code: string
  type: string
  ministry: string
  state: string
  eligibility_criteria: string
  about_scheme: string
  target_categories: string[]
  services_covered: string[]
  coverage_amount: number | ''
  min_age: number | ''
  max_age: number | ''
  required_documents: string[]
  website: string
  helpline: string
}

const extractFromPDF = async (file: File, token: string): Promise<ExtractedData> => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await axios.post(`${API_URL}/admin/schemes/extract-from-pdf`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      'Authorization': `Bearer ${token}`
    }
  })
  return response.data
}

const regenerateFromPDF = async (file: File, token: string): Promise<ExtractedData> => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await axios.post(`${API_URL}/admin/schemes/regenerate`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      'Authorization': `Bearer ${token}`
    }
  })
  return response.data
}

const publishScheme = async (data: SchemeFormData, token: string): Promise<{ scheme_id: number; notifications_sent: number }> => {
  const response = await axios.post(`${API_URL}/admin/schemes/publish`, data, {
    headers: {
      'Authorization': `Bearer ${token}`
    }
  })
  return response.data
}

export const AddSchemePage: React.FC = () => {
  const navigate = useNavigate()
  const { token } = useAuthStore()
  const fileInputRef = useRef<HTMLInputElement>(null)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [activeSection, setActiveSection] = useState<'eligibility' | 'about'>('eligibility')
  
  const [formData, setFormData] = useState<SchemeFormData>({
    name: '',
    code: '',
    type: 'national',
    ministry: '',
    state: '',
    eligibility_criteria: '',
    about_scheme: '',
    target_categories: [],
    services_covered: [],
    coverage_amount: '',
    min_age: '',
    max_age: '',
    required_documents: [],
    website: '',
    helpline: ''
  })

  const [error, setError] = useState<string | null>(null)

  const showToast = (type: 'success' | 'error' | 'warning' | 'info', message: string) => {
    document.dispatchEvent(new CustomEvent('toast', { detail: { type, message } }))
  }

  const extractMutation = useMutation<ExtractedData, Error, File>({
    mutationFn: (file: File) => extractFromPDF(file, token || ''),
    onSuccess: (data: ExtractedData) => {
      setError(null)
      setFormData(prev => ({
        ...prev,
        name: data.name,
        code: data.code,
        type: data.type,
        eligibility_criteria: data.eligibility_criteria,
        about_scheme: data.about_scheme
      }))
      showToast('success', 'PDF processed successfully! AI extracted the scheme details.')
    },
    onError: (error: Error) => {
      const msg = error.message || 'Failed to extract data from PDF. Please ensure Ollama is running on localhost:11434'
      setError(msg)
      showToast('error', msg)
    }
  })

  const regenerateMutation = useMutation<ExtractedData, Error, File>({
    mutationFn: (file: File) => regenerateFromPDF(file, token || ''),
    onSuccess: (data: ExtractedData) => {
      setError(null)
      setFormData(prev => ({
        ...prev,
        name: data.name,
        code: data.code,
        type: data.type,
        eligibility_criteria: data.eligibility_criteria,
        about_scheme: data.about_scheme
      }))
      showToast('success', 'Content regenerated successfully!')
    },
    onError: (error: Error) => {
      const msg = error.message || 'Failed to regenerate content. Please ensure Ollama is running on localhost:11434'
      setError(msg)
      showToast('error', msg)
    }
  })

  interface PublishResponse {
    scheme_id: number
    notifications_sent: number
  }

  const publishMutation = useMutation<PublishResponse, Error, SchemeFormData>({
    mutationFn: (data: SchemeFormData) => publishScheme(data, token || ''),
    onSuccess: (data: PublishResponse) => {
      setError(null)
      showToast('success', `Scheme published! ${data.notifications_sent} users notified.`)
      setTimeout(() => navigate('/schemes'), 1500)
    },
    onError: (error: Error) => {
      const msg = error.message || 'Failed to publish scheme'
      setError(msg)
      showToast('error', msg)
    }
  })

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      if (file.type !== 'application/pdf') {
        alert('Please upload a PDF file')
        return
      }
      setUploadedFile(file)
      extractMutation.mutate(file)
    }
  }

  const handleRegenerate = () => {
    if (uploadedFile) {
      regenerateMutation.mutate(uploadedFile)
    }
  }

  const handlePublish = () => {
    if (!formData.name || !formData.code) {
      alert('Please fill in the scheme name and code')
      return
    }
    publishMutation.mutate(formData)
  }

  const handleInputChange = (field: keyof SchemeFormData, value: string | number | string[]) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-4">
          <button 
            onClick={() => navigate('/schemes')}
            className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <ArrowLeft className="h-5 w-5 text-gray-600" />
          </button>
          <h1 className="text-2xl font-semibold text-gray-900">Add New Scheme</h1>
        </div>
      </div>

      {/* Error Display */}
      {error && (
        <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
          <div className="flex items-start gap-3">
            <div className="text-red-500 mt-0.5">⚠️</div>
            <div>
              <h4 className="text-sm font-medium text-red-800">Error</h4>
              <p className="text-sm text-red-600 mt-1">{error}</p>
              <button
                onClick={() => setError(null)}
                className="text-xs text-red-700 underline mt-2 hover:text-red-900"
              >
                Dismiss
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Processing State */}
      {extractMutation.isPending && (
        <div className="card p-8 mb-6">
          <div className="text-center">
            <div className="mx-auto h-16 w-16 bg-blue-100 rounded-full flex items-center justify-center mb-4 animate-pulse">
              <RefreshCw className="h-8 w-8 text-blue-600 animate-spin" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Processing PDF...
            </h3>
            <p className="text-sm text-gray-500 max-w-md mx-auto">
              Extracting text and querying AI for eligibility criteria and scheme details. This may take 30-60 seconds.
            </p>
          </div>
        </div>
      )}

      {/* PDF Upload Section */}
      {!formData.name && !extractMutation.isPending && (
        <div className="card p-8 mb-6">
          <div className="text-center">
            <div className="mx-auto h-16 w-16 bg-blue-100 rounded-full flex items-center justify-center mb-4">
              <Upload className="h-8 w-8 text-blue-600" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Upload Scheme PDF
            </h3>
            <p className="text-sm text-gray-500 mb-6 max-w-md mx-auto">
              Upload a PDF document containing the scheme details. Our AI will extract the eligibility criteria and scheme information.
            </p>
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              className="hidden"
            />
            <button
              onClick={() => fileInputRef.current?.click()}
              disabled={extractMutation.isPending}
              className="btn-primary"
            >
              {extractMutation.isPending ? (
                <>
                  <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                  Processing...
                </>
              ) : (
                <>
                  <FileText className="h-4 w-4 mr-2" />
                  Select PDF File
                </>
              )}
            </button>
          </div>
        </div>
      )}

      {/* Extracted Content Editor */}
      {formData.name && (
        <>
          {/* Basic Info */}
          <div className="card p-6 mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Basic Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Scheme Name *
                </label>
                <input
                  type="text"
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Scheme Code *
                </label>
                <input
                  type="text"
                  value={formData.code}
                  onChange={(e) => handleInputChange('code', e.target.value)}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Type
                </label>
                <select
                  value={formData.type}
                  onChange={(e) => handleInputChange('type', e.target.value)}
                  className="input-field"
                >
                  <option value="national">National</option>
                  <option value="state">State</option>
                  <option value="central">Central</option>
                  <option value="ngo">NGO</option>
                  <option value="private">Private</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Ministry/Department
                </label>
                <input
                  type="text"
                  value={formData.ministry}
                  onChange={(e) => handleInputChange('ministry', e.target.value)}
                  className="input-field"
                  placeholder="e.g., Ministry of Health"
                />
              </div>
            </div>
          </div>

          {/* AI Extracted Content */}
          <div className="card p-6 mb-6">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2">
                <Sparkles className="h-5 w-5 text-purple-600" />
                <h3 className="text-lg font-medium text-gray-900">AI Extracted Content</h3>
              </div>
              <button
                onClick={handleRegenerate}
                disabled={regenerateMutation.isPending}
                className="btn-secondary text-sm"
              >
                {regenerateMutation.isPending ? (
                  <>
                    <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                    Regenerating...
                  </>
                ) : (
                  <>
                    <RefreshCw className="h-4 w-4 mr-2" />
                    Regenerate with AI
                  </>
                )}
              </button>
            </div>

            {/* Section Tabs */}
            <div className="flex gap-4 border-b border-gray-200 mb-4">
              <button
                onClick={() => setActiveSection('eligibility')}
                className={`pb-2 text-sm font-medium transition-colors ${
                  activeSection === 'eligibility'
                    ? 'text-primary-600 border-b-2 border-primary-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Eligibility Criteria
              </button>
              <button
                onClick={() => setActiveSection('about')}
                className={`pb-2 text-sm font-medium transition-colors ${
                  activeSection === 'about'
                    ? 'text-primary-600 border-b-2 border-primary-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                About the Scheme
              </button>
            </div>

            {/* Eligibility Section */}
            {activeSection === 'eligibility' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Eligibility Criteria
                  <span className="text-xs text-gray-500 ml-2">(You can edit this)</span>
                </label>
                <textarea
                  value={formData.eligibility_criteria}
                  onChange={(e) => handleInputChange('eligibility_criteria', e.target.value)}
                  rows={12}
                  className="input-field font-mono text-sm"
                  placeholder="Eligibility criteria will appear here after PDF upload..."
                />
                <p className="mt-2 text-xs text-gray-500">
                  This section focuses on age group, gender, income criteria, category requirements, and other eligibility conditions.
                </p>
              </div>
            )}

            {/* About Section */}
            {activeSection === 'about' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  About the Scheme
                  <span className="text-xs text-gray-500 ml-2">(You can edit this)</span>
                </label>
                <textarea
                  value={formData.about_scheme}
                  onChange={(e) => handleInputChange('about_scheme', e.target.value)}
                  rows={12}
                  className="input-field font-mono text-sm"
                  placeholder="Scheme description will appear here after PDF upload..."
                />
                <p className="mt-2 text-xs text-gray-500">
                  This section describes the purpose, benefits, department/ministry, and target beneficiaries.
                </p>
              </div>
            )}
          </div>

          {/* Additional Details */}
          <div className="card p-6 mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Additional Details</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Coverage Amount (₹)
                </label>
                <input
                  type="number"
                  value={formData.coverage_amount}
                  onChange={(e) => handleInputChange('coverage_amount', e.target.value === '' ? '' : Number(e.target.value))}
                  className="input-field"
                  placeholder="e.g., 50000"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Min Age
                </label>
                <input
                  type="number"
                  value={formData.min_age}
                  onChange={(e) => handleInputChange('min_age', e.target.value === '' ? '' : Number(e.target.value))}
                  className="input-field"
                  placeholder="e.g., 18"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Max Age
                </label>
                <input
                  type="number"
                  value={formData.max_age}
                  onChange={(e) => handleInputChange('max_age', e.target.value === '' ? '' : Number(e.target.value))}
                  className="input-field"
                  placeholder="e.g., 60"
                />
              </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Website
                </label>
                <input
                  type="url"
                  value={formData.website}
                  onChange={(e) => handleInputChange('website', e.target.value)}
                  className="input-field"
                  placeholder="https://..."
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Helpline
                </label>
                <input
                  type="text"
                  value={formData.helpline}
                  onChange={(e) => handleInputChange('helpline', e.target.value)}
                  className="input-field"
                  placeholder="e.g., 1800-xxx-xxxx"
                />
              </div>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="flex items-center justify-end gap-4">
            <button
              onClick={() => navigate('/schemes')}
              className="btn-secondary"
            >
              Cancel
            </button>
            <button
              onClick={handlePublish}
              disabled={publishMutation.isPending || !formData.name || !formData.code}
              className="btn-primary"
            >
              {publishMutation.isPending ? (
                <>
                  <RefreshCw className="h-4 w-4 mr-2 animate-spin" />
                  Publishing...
                </>
              ) : (
                <>
                  <Save className="h-4 w-4 mr-2" />
                  Publish Scheme
                </>
              )}
            </button>
          </div>
        </>
      )}
    </div>
  )
}
