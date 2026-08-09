"use client";

import { createContext, useCallback, useContext, useEffect, useRef, useState, type ReactNode } from "react";
import type { ComponentType } from "react";
import { apiClient } from "../../libs/api";

interface AuthUser {
  id: string;
  username: string;
  email: string;
  first_name?: string;
  last_name?: string;
  user_type?: string;
  provider_status?: string;
}

interface AuthContextValue {
  user: AuthUser | null;
  loading: boolean;
  error: string | null;
  logout: () => Promise<void>;
  refreshAuth: () => Promise<void>;
}

// Create context with default values
const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }): JSX.Element => {
  const [user, setUser] = useState<AuthUser | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const isMounted = useRef(false);

  const performCheck = useCallback(
    async (): Promise<void> => {
      if (typeof window === "undefined") return;

      try {
        setLoading(true);
        setError(null);
        const userInfo = await apiClient.get<AuthUser>("/user/api/v1/auth/me/");
        setUser(userInfo);
      } catch {
        setError(null);
        setUser(null);
      } finally {
        setLoading(false);
      }
    },
    []
  );

  useEffect(() => {
    if (isMounted.current) return;
    isMounted.current = true;

    void performCheck();
  }, [performCheck]);

  const logout = async (): Promise<void> => {
    try {
      setLoading(true);
      setError(null);

      await apiClient.post("/user/logout/");
    } catch (err) {
      console.error("Logout failed:", err);
      const message = err instanceof Error ? err.message : "Logout failed";
      setError(message);
    } finally {
      setUser(null);
      setLoading(false);
    }
  };

  const refreshAuth = async (): Promise<void> => {
    await performCheck();
  };

  const value: AuthContextValue = {
    user,
    loading,
    error,
    logout,
    refreshAuth,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextValue => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};

export const withAuth = <P extends Record<string, unknown>>(WrappedComponent: ComponentType<P>) => {
  const ComponentWithAuth = (props: P) => {
    const { loading, error } = useAuth();

    if (loading) {
      return <div>Loading...</div>;
    }

    if (error) {
      return <div>Error: {error}</div>;
    }

    return <WrappedComponent {...props} />;
  };

  ComponentWithAuth.displayName = `WithAuth(${WrappedComponent.displayName ?? WrappedComponent.name ?? "Component"})`;

  return ComponentWithAuth;
};
