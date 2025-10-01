'use client'

import { useSession, signOut } from 'next-auth/react'
import Link from 'next/link'

interface UserProfileProps {
  isOpen: boolean
  onClose: () => void
}

export default function UserProfile({ isOpen, onClose }: UserProfileProps) {
  const { data: session } = useSession()

  if (!session?.user) return null

  const user = session.user

  return (
    <>
      {/* Overlay */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40"
          onClick={onClose}
        />
      )}

      {/* Profile Dropdown */}
      <div className={`fixed top-16 right-4 w-80 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 z-50 transform transition-all duration-200 ${
        isOpen ? 'translate-y-0 opacity-100' : '-translate-y-2 opacity-0 pointer-events-none'
      }`}>
        <div className="p-6">
          {/* User Info */}
          <div className="flex items-center space-x-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white font-bold text-lg">
              {user.name?.charAt(0).toUpperCase() || 'U'}
            </div>
            <div>
              <h3 className="font-semibold text-gray-900 dark:text-white">{user.name}</h3>
              <p className="text-sm text-gray-500 dark:text-gray-400 capitalize">{user.role}</p>
            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-2 gap-4 mb-6">
            <div className="text-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <div className="text-2xl font-bold text-blue-600">{user.contributions}</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Contributions</div>
            </div>
            <div className="text-center p-3 bg-gray-50 dark:bg-gray-700 rounded-lg">
              <div className="text-2xl font-bold text-green-600">{user.reputation}%</div>
              <div className="text-sm text-gray-600 dark:text-gray-400">Reputation</div>
            </div>
          </div>

          {/* Expertise */}
          {user.expertise && user.expertise.length > 0 && (
            <div className="mb-6">
              <h4 className="text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">Expertise</h4>
              <div className="flex flex-wrap gap-1">
                {user.expertise.map((area, index) => (
                  <span
                    key={index}
                    className="px-2 py-1 text-xs bg-blue-100 dark:bg-blue-900 text-blue-800 dark:text-blue-200 rounded-full"
                  >
                    {area}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* Actions */}
          <div className="space-y-2">
            <Link
              href="/profile"
              className="block w-full px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-md transition-colors"
              onClick={onClose}
            >
              View Profile
            </Link>
            <Link
              href="/my-contributions"
              className="block w-full px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-md transition-colors"
              onClick={onClose}
            >
              My Contributions
            </Link>
            <Link
              href="/settings"
              className="block w-full px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-md transition-colors"
              onClick={onClose}
            >
              Settings
            </Link>
            <button
              onClick={() => signOut({ callbackUrl: '/' })}
              className="block w-full px-4 py-2 text-sm text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-md transition-colors text-left"
            >
              Sign Out
            </button>
          </div>
        </div>
      </div>
    </>
  )
}

