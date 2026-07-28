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
  ministry?: string
  state?: string
  coverage_amount?: number
  min_age?: number
  max_age?: number
  target_categories?: string[]
  services_covered?: string[]
  required_documents?: string[]
  website?: string
  helpline?: string
  full_document_text?: string
}

interface SchemeFormData {
  name: string
  code: string
  type: string
  ministry: string
  state: string
  eligibility_criteria: string
  about_scheme: string
  full_document_text: string
  target_categories: string[]
  services_covered: string[]
  coverage_amount: number | ''
  min_age: number | ''
  max_age: number | ''
  required_documents: string[]
  website: string
  helpline: string
}

const uploadPDF = async (file: File, token: string, onProgress: (progress: number) => void): Promise<{ file_id: string; filename: string; size: number }> => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await axios.post(`${API_URL}/admin/schemes/upload-pdf`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
      'Authorization': `Bearer ${token}`
    },
    onUploadProgress: (progressEvent) => {
      const percentCompleted = progressEvent.total
        ? Math.round((progressEvent.loaded * 100) / progressEvent.total)
        : 0
      onProgress(percentCompleted)
    }
  })
  return response.data
}

const checkAIHealth = async () => {
  try {
    const res = await axios.get(`${API_URL}/health/ai`, { timeout: 4000 })
    if (res.data?.status !== 'online') {
      throw new Error('AI Service is currently offline. Please ensure Ollama is running.')
    }
  } catch (err: any) {
    const msg = err.response?.data?.detail || 'AI Service is currently offline. Please ensure Ollama is running.'
    throw new Error(msg)
  }
}

const extractFromPDF = async (fileId: string, token: string): Promise<ExtractedData> => {
  await checkAIHealth()
  const formData = new FormData()
  formData.append('file_id', fileId)
  
  const response = await axios.post(`${API_URL}/admin/schemes/extract-from-pdf`, formData, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
      'Authorization': `Bearer ${token}`
    }
  })
  return response.data
}

const regenerateFromPDF = async (file: File, token: string): Promise<ExtractedData> => {
  await checkAIHealth()
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

const publishScheme = async (data: SchemeFormData & { file_id?: string | null }, token: string): Promise<{ scheme_id: number; notifications_sent: number }> => {
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
  const [uploadedFileId, setUploadedFileId] = useState<string | null>(null)
  const [uploadProgress, setUploadProgress] = useState<number>(0)
  const [activeSection, setActiveSection] = useState<'eligibility' | 'about' | 'full_document'>('eligibility')
  
  const [formData, setFormData] = useState<SchemeFormData>({
    name: '',
    code: '',
    type: 'national',
    ministry: '',
    state: '',
    eligibility_criteria: '',
    about_scheme: '',
    full_document_text: '',
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

  const extractMutation = useMutation<ExtractedData, Error, string>({
    mutationFn: (fileId: string) => extractFromPDF(fileId, token || ''),
    onSuccess: (data: ExtractedData) => {
      setError(null)
      setFormData(prev => ({
        ...prev,
        name: data.name || prev.name,
        code: data.code || prev.code,
        type: data.type || prev.type,
        ministry: data.ministry || prev.ministry,
        state: data.state || prev.state,
        eligibility_criteria: data.eligibility_criteria || prev.eligibility_criteria,
        about_scheme: data.about_scheme || prev.about_scheme,
        coverage_amount: data.coverage_amount ?? prev.coverage_amount,
        min_age: data.min_age ?? prev.min_age,
        max_age: data.max_age ?? prev.max_age,
        target_categories: data.target_categories || prev.target_categories,
        services_covered: data.services_covered || prev.services_covered,
        required_documents: data.required_documents || prev.required_documents,
        website: data.website || prev.website,
        helpline: data.helpline || prev.helpline,
        full_document_text: data.full_document_text || prev.full_document_text
      }))
      showToast('success', 'PDF processed successfully! AI extracted all scheme details.')
    },
    onError: (error: any) => {
      const msg = error.response?.data?.detail || error.message || 'Failed to extract data from PDF.'
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
        name: data.name || prev.name,
        code: data.code || prev.code,
        type: data.type || prev.type,
        ministry: data.ministry || prev.ministry,
        state: data.state || prev.state,
        eligibility_criteria: data.eligibility_criteria || prev.eligibility_criteria,
        about_scheme: data.about_scheme || prev.about_scheme,
        coverage_amount: data.coverage_amount ?? prev.coverage_amount,
        min_age: data.min_age ?? prev.min_age,
        max_age: data.max_age ?? prev.max_age,
        target_categories: data.target_categories || prev.target_categories,
        services_covered: data.services_covered || prev.services_covered,
        required_documents: data.required_documents || prev.required_documents,
        website: data.website || prev.website,
        helpline: data.helpline || prev.helpline,
        full_document_text: data.full_document_text || prev.full_document_text
      }))
      showToast('success', 'Content regenerated successfully!')
    },
    onError: (error: any) => {
      const msg = error.response?.data?.detail || error.message || 'Failed to regenerate content.'
      setError(msg)
      showToast('error', msg)
    }
  })

  interface PublishResponse {
    scheme_id: number
    notifications_sent: number
  }

  const publishMutation = useMutation<PublishResponse, Error, SchemeFormData & { file_id?: string | null }>({
    mutationFn: (data: SchemeFormData & { file_id?: string | null }) => publishScheme(data, token || ''),
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

  const uploadMutation = useMutation<{ file_id: string; filename: string; size: number }, Error, File>({
    mutationFn: (file: File) => uploadPDF(file, token || '', setUploadProgress),
    onSuccess: (data) => {
      setUploadedFileId(data.file_id)
      setUploadProgress(100)
      showToast('success', `File "${data.filename}" uploaded successfully! Click "Send to AI" to extract scheme details.`)
    },
    onError: (error: Error) => {
      const msg = error.message || 'Failed to upload PDF'
      showToast('error', msg)
      setUploadProgress(0)
    }
  })

  const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      if (file.type !== 'application/pdf') {
        showToast('error', 'Please upload a PDF file')
        return
      }
      setUploadedFile(file)
      setUploadProgress(0)
      setUploadedFileId(null)
      // Start upload immediately
      uploadMutation.mutate(file)
    }
  }

  const handleSendToAI = () => {
    if (uploadedFileId) {
      extractMutation.mutate(uploadedFileId)
    }
  }

  const handleRegenerate = () => {
    if (uploadedFile) {
      regenerateMutation.mutate(uploadedFile)
    }
  }

  const CATEGORY_OPTIONS = ['BPL', 'Women', 'Children', 'Senior Citizens', 'Disabled']
  const [customCategoryInput, setCustomCategoryInput] = useState('')

  const toggleCategory = (cat: string) => {
    setFormData(prev => {
      const current = prev.target_categories || []
      const updated = current.includes(cat)
        ? current.filter(c => c !== cat)
        : [...current, cat]
      return { ...prev, target_categories: updated }
    })
  }

  const addCustomCategory = () => {
    const trimmed = customCategoryInput.trim()
    if (!trimmed) return
    setFormData(prev => {
      const current = prev.target_categories || []
      if (current.includes(trimmed)) return prev
      return { ...prev, target_categories: [...current, trimmed] }
    })
    setCustomCategoryInput('')
  }

  const removeCategory = (cat: string) => {
    setFormData(prev => ({
      ...prev,
      target_categories: (prev.target_categories || []).filter(c => c !== cat)
    }))
  }

  const handlePublish = () => {
    if (!formData.target_categories || formData.target_categories.length === 0) {
      showToast('error', 'Target category is mandatory! Please select at least one category (BPL, Women, Children, Senior Citizens, Disabled).')
      setError('Target category is mandatory! Please select at least one category (BPL, Women, Children, Senior Citizens, Disabled).')
      return
    }

    const payload = {
      ...formData,
      file_id: uploadedFileId,
      coverage_amount: formData.coverage_amount === '' || formData.coverage_amount === null || formData.coverage_amount === undefined ? null : Number(formData.coverage_amount),
      min_age: formData.min_age === '' || formData.min_age === null || formData.min_age === undefined ? null : Number(formData.min_age),
      max_age: formData.max_age === '' || formData.max_age === null || formData.max_age === undefined ? null : Number(formData.max_age),
    }
    publishMutation.mutate(payload as any)
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

      {/* Upload Progress */}
      {uploadMutation.isPending && (
        <div className="card p-8 mb-6">
          <div className="text-center">
            <div className="mx-auto h-16 w-16 bg-blue-100 rounded-full flex items-center justify-center mb-4 animate-pulse">
              <Upload className="h-8 w-8 text-blue-600" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Uploading PDF...
            </h3>
            <p className="text-sm text-gray-500 max-w-md mx-auto mb-4">
              Uploading file to server. Please wait...
            </p>
            
            <div className="max-w-md mx-auto">
              <div className="flex justify-between text-xs text-gray-500 mb-1">
                <span>Uploading</span>
                <span>{Math.round(uploadProgress)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                <div 
                  className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${uploadProgress}%` }}
                />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* AI Processing State */}
      {extractMutation.isPending && (
        <div className="card p-8 mb-6">
          <div className="text-center">
            <div className="mx-auto h-16 w-16 bg-purple-100 rounded-full flex items-center justify-center mb-4 animate-pulse">
              <Sparkles className="h-8 w-8 text-purple-600 animate-spin" />
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Processing with AI...
            </h3>
            <p className="text-sm text-gray-500 max-w-md mx-auto mb-4">
              Extracting text and querying Ollama AI for 4-5 line summary, eligibility criteria, and scheme parameters. This may take 20-40 seconds.
            </p>
            
            <div className="max-w-md mx-auto">
              <div className="flex justify-between text-xs text-gray-500 mb-1">
                <span>AI Processing</span>
                <span>Extracting...</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2 overflow-hidden">
                <div className="bg-purple-600 h-2 rounded-full animate-pulse" style={{ width: '60%' }} />
              </div>
            </div>
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
              Upload a PDF document containing the scheme details, then send it to AI for extraction.
            </p>
            <input
              ref={fileInputRef}
              type="file"
              accept=".pdf"
              onChange={handleFileChange}
              className="hidden"
            />
            
            {!uploadedFile ? (
              <button
                onClick={() => fileInputRef.current?.click()}
                className="btn-primary"
              >
                <FileText className="h-4 w-4 mr-2" />
                Select PDF File
              </button>
            ) : (
              <div className="space-y-4">
                <div className="flex items-center justify-center gap-2 text-sm text-gray-600 bg-gray-50 p-3 rounded-lg">
                  <FileText className="h-4 w-4" />
                  <span className="font-medium">{uploadedFile.name}</span>
                  <span className="text-gray-400">({(uploadedFile.size / 1024 / 1024).toFixed(2)} MB)</span>
                </div>
                <div className="flex gap-3 justify-center">
                  <button
                    onClick={() => fileInputRef.current?.click()}
                    className="btn-secondary"
                  >
                    Change File
                  </button>
                  <button
                    onClick={handleSendToAI}
                    className="btn-primary bg-purple-600 hover:bg-purple-700"
                  >
                    <Sparkles className="h-4 w-4 mr-2" />
                    Send to AI
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Extracted Content Form */}
      {formData.name && (
        <>
          {/* Basic Info */}
          <div className="card p-6 mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Basic Information</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Scheme Name <span className="text-red-500 font-bold">*</span> <span className="text-xs text-red-600 font-normal">(Required)</span>
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => handleInputChange('name', e.target.value)}
                  className="input-field"
                  placeholder="e.g., National Dental Health Scheme"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Scheme Code <span className="text-red-500 font-bold">*</span> <span className="text-xs text-red-600 font-normal">(Required)</span>
                </label>
                <input
                  type="text"
                  required
                  value={formData.code}
                  onChange={(e) => handleInputChange('code', e.target.value)}
                  className="input-field font-mono"
                  placeholder="e.g., DPM-2026-001"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Type <span className="text-red-500 font-bold">*</span> <span className="text-xs text-red-600 font-normal">(Required)</span>
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
                  placeholder="e.g., Ministry of Health & Family Welfare"
                />
              </div>
            </div>

            {/* Target Category (Mandatory) */}
            <div className="mt-4 pt-4 border-t border-gray-100">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Target Category <span className="text-red-500 font-bold">*</span> <span className="text-xs text-purple-600 font-medium">(AI Auto-detected — Select/edit below or add custom)</span>
              </label>
              <div className="flex flex-wrap gap-2.5 p-3 bg-gray-50 rounded-lg border border-gray-200 mb-3">
                {CATEGORY_OPTIONS.map((cat) => {
                  const isChecked = (formData.target_categories || []).includes(cat)
                  return (
                    <label
                      key={cat}
                      className={`flex items-center gap-2 px-3 py-1.5 rounded-md cursor-pointer border text-sm font-medium transition-colors ${
                        isChecked
                          ? 'bg-purple-50 border-purple-500 text-purple-700 font-semibold'
                          : 'bg-white border-gray-300 text-gray-700 hover:bg-gray-100'
                      }`}
                    >
                      <input
                        type="checkbox"
                        checked={isChecked}
                        onChange={() => toggleCategory(cat)}
                        className="rounded text-purple-600 focus:ring-purple-500"
                      />
                      <span>{cat}</span>
                    </label>
                  )
                })}
              </div>

              {/* Extra / Custom Extracted Category Chips */}
              {(formData.target_categories || []).filter(c => !CATEGORY_OPTIONS.includes(c)).length > 0 && (
                <div className="flex flex-wrap gap-2 mb-3">
                  <span className="text-xs font-semibold text-gray-500 self-center">Additional Categories:</span>
                  {(formData.target_categories || []).filter(c => !CATEGORY_OPTIONS.includes(c)).map((cat) => (
                    <span
                      key={cat}
                      className="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-purple-100 text-purple-800 border border-purple-200"
                    >
                      {cat}
                      <button
                        type="button"
                        onClick={() => removeCategory(cat)}
                        className="hover:text-purple-950 font-bold ml-1"
                      >
                        ×
                      </button>
                    </span>
                  ))}
                </div>
              )}

              {/* Add Custom Category Input */}
              <div className="flex items-center gap-2 max-w-md">
                <input
                  type="text"
                  value={customCategoryInput}
                  onChange={(e) => setCustomCategoryInput(e.target.value)}
                  onKeyDown={(e) => { if (e.key === 'Enter') { e.preventDefault(); addCustomCategory(); } }}
                  placeholder="Add custom target category..."
                  className="flex-1 px-3 py-1.5 text-sm border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                />
                <button
                  type="button"
                  onClick={addCustomCategory}
                  className="px-3 py-1.5 text-xs font-semibold text-purple-700 bg-purple-50 hover:bg-purple-100 border border-purple-200 rounded-lg transition-colors"
                >
                  + Add Category
                </button>
              </div>

              {(!formData.target_categories || formData.target_categories.length === 0) && (
                <p className="text-xs text-red-500 mt-1.5 font-semibold">⚠️ Mandatory: Please select at least one category above.</p>
              )}
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
                Eligibility Criteria *
              </button>
              <button
                onClick={() => setActiveSection('about')}
                className={`pb-2 text-sm font-medium transition-colors ${
                  activeSection === 'about'
                    ? 'text-primary-600 border-b-2 border-primary-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                About the Scheme *
              </button>
              <button
                onClick={() => setActiveSection('full_document')}
                className={`pb-2 text-sm font-medium transition-colors ${
                  activeSection === 'full_document'
                    ? 'text-primary-600 border-b-2 border-primary-600'
                    : 'text-gray-500 hover:text-gray-700'
                }`}
              >
                Full Document
              </button>
            </div>

            {/* Eligibility Section */}
            {activeSection === 'eligibility' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Eligibility Criteria <span className="text-red-500 font-bold">*</span>
                  <span className="text-xs text-gray-500 ml-2">(Auto-extracted bullet points, editable)</span>
                </label>
                <textarea
                  value={formData.eligibility_criteria}
                  onChange={(e) => handleInputChange('eligibility_criteria', e.target.value)}
                  rows={12}
                  className="input-field font-mono text-sm"
                  placeholder="Eligibility criteria bullet points..."
                />
                <p className="mt-2 text-xs text-gray-500">
                  Clearly details age, income limits, target categories, residential criteria, and documentation conditions.
                </p>
              </div>
            )}

            {/* About Section */}
            {activeSection === 'about' && (
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  About the Scheme (Concise 4-5 line summary) <span className="text-red-500 font-bold">*</span>
                  <span className="text-xs text-gray-500 ml-2">(Editable)</span>
                </label>
                <textarea
                  value={formData.about_scheme}
                  onChange={(e) => handleInputChange('about_scheme', e.target.value)}
                  rows={6}
                  className="input-field font-mono text-sm"
                  placeholder="Concise 4-5 line scheme summary..."
                />
                <p className="mt-2 text-xs text-gray-500">
                  A concise 4-5 line description covering purpose, major dental benefits, and target audience.
                </p>
              </div>
            )}

            {/* Full Document Section */}
            {activeSection === 'full_document' && (
              <div>
                {/* Download PDF button if original file exists */}
                {uploadedFile && (
                  <div className="mb-4">
                    <a
                      href={URL.createObjectURL(uploadedFile)}
                      download={uploadedFile.name}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center px-4 py-2 bg-blue-50 text-blue-700 border border-blue-200 rounded-lg text-sm font-semibold hover:bg-blue-100 transition-colors"
                    >
                      <FileText className="h-4 w-4 mr-2 text-blue-600" />
                      Download Original Scheme PDF Document ({uploadedFile.name})
                    </a>
                  </div>
                )}

                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Full Document Text
                  <span className="text-xs text-gray-500 ml-2">(Auto-extracted from PDF, editable)</span>
                </label>
                <textarea
                  value={formData.full_document_text}
                  onChange={(e) => handleInputChange('full_document_text', e.target.value)}
                  rows={14}
                  className="input-field font-mono text-sm"
                  placeholder="Full document text will appear here after PDF processing..."
                />
                <p className="mt-2 text-xs text-gray-500">
                  Complete text extracted from the uploaded PDF for full document viewing.
                </p>
              </div>
            )}
          </div>

          {/* Additional Details */}
          <div className="card p-6 mb-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">Additional Parameters</h3>
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
                  placeholder="e.g., 65"
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
              disabled={publishMutation.isPending}
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
