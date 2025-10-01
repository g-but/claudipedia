import { DefaultSession, DefaultUser } from "next-auth"
import { JWT, DefaultJWT } from "next-auth/jwt"

declare module "next-auth" {
  interface Session {
    user: {
      id: string
      role: string
      expertise: string[]
      contributions: number
      reputation: number
      verified: boolean
    } & DefaultSession["user"]
  }

  interface User extends DefaultUser {
    role: string
    expertise: string[]
    contributions: number
    reputation: number
    verified: boolean
  }
}

declare module "next-auth/jwt" {
  interface JWT extends DefaultJWT {
    role: string
    expertise: string[]
    contributions: number
    reputation: number
    verified: boolean
  }
}

