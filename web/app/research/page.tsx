'use client';

import { useState, useEffect } from 'react';
import { researchAPI, ResearchProfile } from '@/lib/api';

export default function ResearchPage() {
  const [profiles, setProfiles] = useState<ResearchProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newProfile, setNewProfile] = useState({
    name: '',
    description: '',
    domains: [] as string[],
  });

  useEffect(() => {
    loadProfiles();
  }, []);

  const loadProfiles = async () => {
    try {
      setLoading(true);
      const response = await researchAPI.getProfiles();

      if (response.data) {
        setProfiles(response.data);
      } else if (response.error) {
        setError(response.error);
      }
    } catch (err) {
      setError('Failed to load research profiles');
      console.error('Error loading profiles:', err);
    } finally {
      setLoading(false);
    }
  };

  const createProfile = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!newProfile.name.trim() || !newProfile.description.trim()) {
      setError('Name and description are required');
      return;
    }

    try {
      const response = await researchAPI.createProfile({
        user_id: 'current_user', // This should come from auth context
        name: newProfile.name.trim(),
        description: newProfile.description.trim(),
        domains: newProfile.domains,
        contexts: [],
        status: 'active',
        metadata: {},
      });

      if (response.data) {
        setShowCreateForm(false);
        setNewProfile({ name: '', description: '', domains: [] });
        loadProfiles(); // Reload the list
      } else if (response.error) {
        setError(response.error);
      }
    } catch (err) {
      setError('Failed to create research profile');
      console.error('Error creating profile:', err);
    }
  };

  const handleDomainAdd = (domain: string) => {
    if (domain.trim() && !newProfile.domains.includes(domain.trim())) {
      setNewProfile(prev => ({
        ...prev,
        domains: [...prev.domains, domain.trim()]
      }));
    }
  };

  const handleDomainRemove = (domain: string) => {
    setNewProfile(prev => ({
      ...prev,
      domains: prev.domains.filter(d => d !== domain)
    }));
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading research profiles...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Research Profiles</h1>
          <p className="mt-2 text-gray-600">
            Manage your research profiles for truth-seeking and knowledge exploration.
          </p>
        </div>

        {/* Error Display */}
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-md p-4">
            <div className="flex">
              <div className="ml-3">
                <p className="text-sm text-red-800">{error}</p>
              </div>
              <button
                onClick={() => setError(null)}
                className="ml-auto text-red-500 hover:text-red-700"
              >
                ✕
              </button>
            </div>
          </div>
        )}

        {/* Create Profile Button */}
        <div className="mb-6">
          <button
            onClick={() => setShowCreateForm(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium"
          >
            Create Research Profile
          </button>
        </div>

        {/* Create Profile Form */}
        {showCreateForm && (
          <div className="mb-8 bg-white shadow rounded-lg p-6">
            <h2 className="text-xl font-semibold mb-4">Create New Research Profile</h2>
            <form onSubmit={createProfile} className="space-y-4">
              <div>
                <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                  Profile Name *
                </label>
                <input
                  type="text"
                  id="name"
                  value={newProfile.name}
                  onChange={(e) => setNewProfile(prev => ({ ...prev, name: e.target.value }))}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  placeholder="e.g., Quantum Physics Research"
                  required
                />
              </div>

              <div>
                <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                  Description *
                </label>
                <textarea
                  id="description"
                  rows={3}
                  value={newProfile.description}
                  onChange={(e) => setNewProfile(prev => ({ ...prev, description: e.target.value }))}
                  className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Describe your research goals and focus areas..."
                  required
                />
              </div>

              <div>
                <label htmlFor="domains" className="block text-sm font-medium text-gray-700">
                  Research Domains
                </label>
                <div className="mt-1 flex space-x-2">
                  <input
                    type="text"
                    id="domains"
                    className="flex-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500"
                    placeholder="Add a research domain (e.g., quantum-mechanics, machine-learning)"
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') {
                        e.preventDefault();
                        handleDomainAdd(e.currentTarget.value);
                        e.currentTarget.value = '';
                      }
                    }}
                  />
                  <button
                    type="button"
                    onClick={(e) => {
                      const input = e.currentTarget.previousElementSibling as HTMLInputElement;
                      handleDomainAdd(input.value);
                      input.value = '';
                    }}
                    className="px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                  >
                    Add
                  </button>
                </div>

                {newProfile.domains.length > 0 && (
                  <div className="mt-2 flex flex-wrap gap-2">
                    {newProfile.domains.map((domain) => (
                      <span
                        key={domain}
                        className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
                      >
                        {domain}
                        <button
                          type="button"
                          onClick={() => handleDomainRemove(domain)}
                          className="ml-1.5 text-blue-600 hover:text-blue-800"
                        >
                          ✕
                        </button>
                      </span>
                    ))}
                  </div>
                )}
              </div>

              <div className="flex space-x-3">
                <button
                  type="submit"
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-md font-medium"
                >
                  Create Profile
                </button>
                <button
                  type="button"
                  onClick={() => setShowCreateForm(false)}
                  className="bg-gray-300 hover:bg-gray-400 text-gray-700 px-4 py-2 rounded-md font-medium"
                >
                  Cancel
                </button>
              </div>
            </form>
          </div>
        )}

        {/* Profiles List */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h2 className="text-lg font-medium text-gray-900">Your Research Profiles</h2>
          </div>

          {profiles.length === 0 ? (
            <div className="p-6 text-center text-gray-500">
              <p>No research profiles found.</p>
              <p className="mt-2">Create your first profile to start organizing your truth-seeking journey.</p>
            </div>
          ) : (
            <div className="divide-y divide-gray-200">
              {profiles.map((profile) => (
                <div key={profile.id} className="p-6 hover:bg-gray-50">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <h3 className="text-lg font-medium text-gray-900">{profile.name}</h3>
                      <p className="mt-1 text-sm text-gray-600">{profile.description}</p>

                      {profile.domains.length > 0 && (
                        <div className="mt-2 flex flex-wrap gap-1">
                          {profile.domains.map((domain) => (
                            <span
                              key={domain}
                              className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-800"
                            >
                              {domain}
                            </span>
                          ))}
                        </div>
                      )}

                      <div className="mt-2 flex items-center space-x-4 text-sm text-gray-500">
                        <span>Status: {profile.status}</span>
                        <span>Created: {new Date(profile.created_at).toLocaleDateString()}</span>
                        <span>{profile.contexts.length} contexts</span>
                      </div>
                    </div>

                    <div className="flex space-x-2">
                      <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                        View Details
                      </button>
                      <button className="text-blue-600 hover:text-blue-800 text-sm font-medium">
                        Upload Context
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
